from pathlib import Path

import pandas as pd
from jinja2 import Environment, FileSystemLoader

from rnax.config import AnalysisConfig
from rnax.pipeline.plots import plot_library_sizes, plot_pca, plot_volcano


def generate_report(
    config: AnalysisConfig,
    raw_counts: pd.DataFrame,
    metadata: pd.DataFrame,
    norm_counts: pd.DataFrame,
    results_df: pd.DataFrame
):
    """
    Generate plots, export CSVs, and render the static HTML report.
    """
    out_dir = Path(config.output.directory)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Export CSVs
    results_path = out_dir / "results.csv"
    results_df.to_csv(results_path)
    
    norm_counts_path = out_dir / "normalized_counts.csv"
    norm_counts.to_csv(norm_counts_path)
    
    # Generate Plots
    plot_library_sizes(
        raw_counts, 
        metadata, 
        config.design.condition_column, 
        str(out_dir / "library_sizes.png")
    )
    
    plot_pca(
        norm_counts, 
        metadata, 
        config.design.condition_column, 
        str(out_dir / "pca.png")
    )
    
    plot_volcano(
        results_df, 
        config.thresholds.fdr, 
        config.thresholds.absolute_log2_fold_change, 
        str(out_dir / "volcano.png")
    )
    
    # Calculate sig stats
    fdr_thresh = config.thresholds.fdr
    lfc_thresh = config.thresholds.absolute_log2_fold_change
    
    sig_mask = (results_df["padj"] < fdr_thresh) & (results_df["log2FoldChange"].abs() >= lfc_thresh)
    sig_up = (sig_mask & (results_df["log2FoldChange"] > 0)).sum()
    sig_down = (sig_mask & (results_df["log2FoldChange"] < 0)).sum()
    total_genes = results_df.shape[0]
    
    # Render HTML
    template_dir = Path(__file__).parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)), autoescape=True)
    template = env.get_template("report.html.j2")
    
    html_content = template.render(
        config=config,
        total_genes=total_genes,
        sig_up=sig_up,
        sig_down=sig_down
    )
    
    report_path = out_dir / "report.html"
    with open(report_path, "w") as f:
        f.write(html_content)
