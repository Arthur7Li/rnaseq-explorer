import shutil
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from rnax.config import AnalysisConfig
from rnax.pipeline.deseq import run_deseq2
from rnax.pipeline.ingest import ingest_data
from rnax.pipeline.report import generate_report


def generate_synthetic_data(num_genes: int, num_samples: int, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    
    conditions = ['control'] * (num_samples // 2) + ['treated'] * (num_samples - num_samples // 2)
    sample_ids = [f"sample_{i+1}" for i in range(num_samples)]
    
    metadata = pd.DataFrame({"sample_id": sample_ids, "condition": conditions})
    metadata.to_csv(out_dir / "metadata.csv", index=False)
    
    np.random.seed(42)
    # n=10, p=0.1
    counts = np.random.negative_binomial(n=10, p=0.1, size=(num_genes, num_samples))
    
    counts_df = pd.DataFrame(counts, columns=sample_ids)
    counts_df.insert(0, "gene_id", [f"gene_{i+1}" for i in range(num_genes)])
    counts_df.to_csv(out_dir / "counts.csv", index=False)
    
    config_content = {
        "input": {
            "counts": str(out_dir / "counts.csv"),
            "metadata": str(out_dir / "metadata.csv"),
            "gene_id_column": "gene_id"
        },
        "design": {
            "condition_column": "condition",
            "reference_level": "control",
            "comparison_level": "treated"
        },
        "filtering": {
            "minimum_count": 10,
            "minimum_samples": num_samples // 2
        },
        "thresholds": {
            "fdr": 0.05,
            "absolute_log2_fold_change": 1.0,
            "top_n_genes": 30
        },
        "output": {
            "directory": str(out_dir / "results"),
            "report_title": f"Benchmark {num_genes} genes",
            "random_seed": 42
        }
    }
    
    config_path = out_dir / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config_content, f)
        
    return config_path

def run_benchmark() -> None:
    scenarios = [
        (1000, 8),
        (5000, 8),
        (10000, 8),
        (20000, 8),
        (50000, 8)
    ]
    
    print("| Genes | Samples | Validation | DESeq2 | Report | Total |")
    print("|-------|---------|------------|--------|--------|-------|")
    
    base_dir = Path("benchmark_tmp")
    if base_dir.exists():
        shutil.rmtree(base_dir)
        
    for num_genes, num_samples in scenarios:
        scenario_dir = base_dir / f"g{num_genes}_s{num_samples}"
        config_path = generate_synthetic_data(num_genes, num_samples, scenario_dir)
        
        config = AnalysisConfig.from_yaml(config_path)
        
        # 1. Validation (Ingest)
        t0 = time.time()
        counts_df, meta_df = ingest_data(config)
        t_val = time.time() - t0
        
        # 2. DESeq2
        t0 = time.time()
        normalized_counts, results, filtering_stats = run_deseq2(counts_df, meta_df, config)
        t_deseq = time.time() - t0
        
        # 3. Report & Plots (combined because generate_report does both now)
        t0 = time.time()
        from rnax.manifest import build_manifest
        manifest = build_manifest(config, config_path)
        generate_report(config, counts_df, meta_df, normalized_counts, results, manifest, filtering_stats, output_dir=Path(config.output.directory))
        t_report = time.time() - t0
        
        t_total = t_val + t_deseq + t_report
        
        print(f"| {num_genes:,} | {num_samples} | {t_val:.2f}s | {t_deseq:.2f}s | {t_report:.2f}s | {t_total:.2f}s |")

    if base_dir.exists():
        shutil.rmtree(base_dir)

if __name__ == "__main__":
    run_benchmark()
