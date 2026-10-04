import json
import re
from pathlib import Path
from typing import Any

import pandas as pd
import pytest
from typer.testing import CliRunner

from rnax.cli import app


@pytest.fixture(scope="module")
def setup_pasilla_fixed_seed(tmp_path_factory: Any) -> Any:
    """
    Sets up a temporary directory with the pasilla configuration
    with a fixed random seed to ensure deterministic outputs.
    """
    temp_dir = tmp_path_factory.mktemp("pasilla_snapshot")
    out_dir = temp_dir / "results"
    config_path = temp_dir / "pasilla_snapshot.yaml"
    
    import yaml
    config_content = {
        "input": {
            "counts": "data/pasilla/counts.csv",
            "metadata": "data/pasilla/metadata.csv",
            "gene_id_column": "gene_id"
        },
        "design": {
            "condition_column": "condition",
            "reference_level": "untreated",
            "comparison_level": "treated"
        },
        "filtering": {
            "minimum_count": 10,
            "minimum_samples": 2
        },
        "thresholds": {
            "fdr": 0.05,
            "absolute_log2_fold_change": 1.0,
            "top_n_genes": 30
        },
        "output": {
            "directory": str(out_dir),
            "report_title": "Snapshot Test Report",
            "random_seed": 42
        }
    }
    
    with open(config_path, "w") as f:
        yaml.dump(config_content, f)
        
    return config_path, out_dir


@pytest.fixture(scope="module")
def run_pasilla_snapshot_pipeline(setup_pasilla_fixed_seed: Any) -> Any:
    """
    Runs the pipeline once per test module to avoid redundant slow DESeq2 runs.
    """
    if not Path("data/pasilla/counts.csv").exists():
        pytest.skip("Pasilla test data not found. Run scripts/acquire_pasilla.py first.")
        
    config_path, out_dir = setup_pasilla_fixed_seed
    
    runner = CliRunner()
    result = runner.invoke(app, ["analyze", "--config", str(config_path)])
    
    assert result.exit_code == 0
    return out_dir


@pytest.mark.slow
def test_snapshot_results_schema(snapshot: Any, run_pasilla_snapshot_pipeline: Any) -> None:
    """Verifies that the shape and dtypes of results.csv remain perfectly stable."""
    out_dir = run_pasilla_snapshot_pipeline
    
    results_df = pd.read_csv(out_dir / "results.csv", index_col=0)
    
    schema = {
        "shape": list(results_df.shape),
        "index_name": results_df.index.name,
        "columns": {col: str(dtype) for col, dtype in results_df.dtypes.items()}
    }
    
    snapshot.assert_match(json.dumps(schema, indent=2), "pasilla_results_schema.json")


@pytest.mark.slow
def test_snapshot_normalized_counts_shape(snapshot: Any, run_pasilla_snapshot_pipeline: Any) -> None:
    """Verifies the shape of the normalized counts matrix."""
    out_dir = run_pasilla_snapshot_pipeline
    
    norm_df = pd.read_csv(out_dir / "normalized_counts.csv", index_col=0)
    
    shape_info = f"Rows: {norm_df.shape[0]}, Cols: {norm_df.shape[1]}"
    snapshot.assert_match(shape_info, "pasilla_norm_counts_shape.txt")


@pytest.mark.slow
def test_snapshot_report_structure(snapshot: Any, run_pasilla_snapshot_pipeline: Any) -> None:
    """Verifies that the HTML report contains the required sections by extracting all headings."""
    out_dir = run_pasilla_snapshot_pipeline
    
    html = (out_dir / "report.html").read_text()
    
    headings = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', html)
    clean_headings = [re.sub(r'<[^>]+>', '', h).strip() for h in headings]
    headings_text = "\n".join(clean_headings)
    snapshot.assert_match(headings_text, "pasilla_report_sections.txt")
