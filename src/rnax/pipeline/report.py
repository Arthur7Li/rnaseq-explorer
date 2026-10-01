from pathlib import Path
from typing import TYPE_CHECKING, Any

import pandas as pd
from jinja2 import Environment, FileSystemLoader

from rnax.config import AnalysisConfig

if TYPE_CHECKING:
    from rnax.config import ContrastSpec
from rnax.manifest import ReproducibilityManifest
from rnax.pipeline.deseq import FilteringResult
from rnax.pipeline.plots import (
    plot_library_sizes,
    plot_ma,
    plot_pca,
    plot_sample_distances,
    plot_top_genes_heatmap,
    plot_volcano,
)


def generate_report(
    config: AnalysisConfig,
    raw_counts: pd.DataFrame,
    metadata: pd.DataFrame,
    norm_counts: pd.DataFrame,
    results_df: pd.DataFrame,
    manifest: ReproducibilityManifest,
    filtering: FilteringResult,
    contrast_spec: "ContrastSpec | None" = None,
    output_dir: Path | None = None,
    annot_df: "pd.DataFrame | None" = None,
    enrich_df: "pd.DataFrame | None" = None,
    sensitivity_res: "Any | None" = None,
) -> None:
    """
    Generate plots, export CSVs, and render the static HTML report.
    """

    out_dir = output_dir if output_dir is not None else Path(config.output.directory)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    cond_col = contrast_spec.condition_column if contrast_spec else config.design.condition_column
    
    # Export CSVs
    results_path = out_dir / "results.csv"
    results_df.to_csv(results_path)
    
    if annot_df is not None and not annot_df.empty:
        # Join annotations
        annotated_results = results_df.join(annot_df, how="left")
        annot_path = out_dir / "annotated_results.csv"
        annotated_results.to_csv(annot_path)
        
    if enrich_df is not None and not enrich_df.empty:
        enrich_path = out_dir / "enrichment_results.csv"
        enrich_df.to_csv(enrich_path)
    
    norm_counts_path = out_dir / "normalized_counts.csv"
    norm_counts.to_csv(norm_counts_path)
    
    # Generate Plots
    alt_library_sizes = plot_library_sizes(
        raw_counts, 
        metadata, 
        cond_col, 
        str(out_dir / "library_sizes.png")
    )
    
    alt_pca = plot_pca(
        norm_counts, 
        metadata, 
        cond_col, 
        str(out_dir / "pca.png")
    )
    
    alt_volcano = plot_volcano(
        results_df, 
        config.thresholds.fdr, 
        config.thresholds.absolute_log2_fold_change, 
        str(out_dir / "volcano.png")
    )
    
    alt_sample_distances = plot_sample_distances(
        norm_counts, 
        metadata, 
        cond_col, 
        config.design.paired_or_block_column, 
        str(out_dir / "sample_distances.png")
    )
    
    alt_ma = plot_ma(
        results_df, 
        config.thresholds.fdr, 
        config.thresholds.absolute_log2_fold_change, 
        str(out_dir / "ma_plot.png")
    )
    
    alt_top_genes_heatmap = plot_top_genes_heatmap(
        norm_counts, 
        results_df, 
        metadata, 
        cond_col, 
        config.design.paired_or_block_column, 
        config.thresholds.top_n_genes, 
        str(out_dir / "top_genes_heatmap.png")
    )
    
    plot_alts = {
        "library_sizes": alt_library_sizes or "Library Sizes per Sample",
        "pca": alt_pca or "PCA of Normalized Counts",
        "volcano": alt_volcano or "Volcano Plot",
        "sample_distances": alt_sample_distances or "Sample Distance Matrix",
        "ma": alt_ma or "MA Plot",
        "top_genes_heatmap": alt_top_genes_heatmap or "Top DE Genes Heatmap",
    }
    
    # Calculate sig stats
    fdr_thresh = config.thresholds.fdr
    lfc_thresh = config.thresholds.absolute_log2_fold_change
    
    sig_mask = (results_df["padj"] < fdr_thresh) & (results_df["log2FoldChange"].abs() >= lfc_thresh)
    sig_up = (sig_mask & (results_df["log2FoldChange"] > 0)).sum()
    sig_down = (sig_mask & (results_df["log2FoldChange"] < 0)).sum()
    total_genes = results_df.shape[0]
    
    # Get top genes for report table (with annotations if available)
    disp_df = results_df.copy()
    if annot_df is not None and not annot_df.empty:
        disp_df = disp_df.join(annot_df, how="left")
    
    top_genes_df = disp_df[sig_mask].sort_values("padj").head(50)
    top_genes_records = top_genes_df.reset_index().to_dict(orient="records")
    
    enrichment_records = []
    if enrich_df is not None and not enrich_df.empty:
        enrich_disp = enrich_df[enrich_df["Adjusted P-value"] < config.annotation.enrichment_fdr] if "Adjusted P-value" in enrich_df.columns else enrich_df
        enrichment_records = enrich_disp.head(20).to_dict(orient="records")
    
    # Render HTML
    template_dir = Path(__file__).parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)), autoescape=True)
    template = env.get_template("report.html.j2")
    
    html_content = template.render(
        config=config,
        contrast_spec=contrast_spec,
        total_genes=total_genes,
        sig_up=sig_up,
        sig_down=sig_down,
        manifest=manifest,
        filtering=filtering,
        plot_alts=plot_alts,
        top_genes=top_genes_records,
        enrichment=enrichment_records,
        sensitivity=sensitivity_res,
    )
    
    report_path = out_dir / "report.html"
    with open(report_path, "w") as f:
        f.write(html_content)
