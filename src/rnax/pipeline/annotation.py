import logging
from pathlib import Path

import gseapy as gp
import pandas as pd

logger = logging.getLogger(__name__)

def load_gene_annotations(gene_ids: list[str], organism: str, annotation_dir: Path) -> pd.DataFrame:
    """
    Load gene symbols and descriptions from a local bundled CSV in data/annotations/.
    """
    supported = ["human", "mouse", "drosophila"]
    if organism not in supported:
        logger.warning(f"Unsupported organism '{organism}' for annotation. Falling back to empty annotations.")
        return pd.DataFrame()
        
    csv_path = annotation_dir / f"{organism}_genes.csv"
    if not csv_path.exists():
        logger.warning(f"Annotation file {csv_path} not found. Run scripts/fetch_annotations.py. Falling back to empty annotations.")
        return pd.DataFrame()
        
    try:
        df = pd.read_csv(csv_path)
    except (OSError, ValueError) as e:
        logger.error(f"Error reading annotation file {csv_path}: {e}")
        return pd.DataFrame()
        
    if "gene_id" not in df.columns:
        logger.error(f"Annotation file {csv_path} is missing 'gene_id' column.")
        return pd.DataFrame()
        
    subset = df[df["gene_id"].isin(gene_ids)].copy()
    subset.set_index("gene_id", inplace=True)
    return subset


def run_enrichment(results_df: pd.DataFrame, gene_sets_path: Path | str, organism: str, fdr_thresh: float) -> pd.DataFrame | None:
    """
    Extract significant gene IDs (by padj < threshold) and run ORA using gseapy.enrich.
    Returns enrichment results or None if insufficient genes or unsupported organism.
    """
    supported = ["human", "mouse", "drosophila"]
    if organism not in supported:
        logger.warning(f"Organism '{organism}' not supported for enrichment.")
        return None

    if "gene_symbol" not in results_df.columns:
        logger.warning("Enrichment requires 'gene_symbol' column in results_df. Skipping enrichment.")
        return None
        
    sig_df = results_df[results_df["padj"] < fdr_thresh]
    gene_list = sig_df["gene_symbol"].dropna().astype(str).tolist()
    
    if len(gene_list) < 5:
        logger.warning(f"Only {len(gene_list)} significant genes found (FDR < {fdr_thresh}). Enrichment requires at least 5. Skipping.")
        return None
        
    try:
        # Ensure no network calls by checking if gene_sets_path is an existing file
        gs_path_str = str(gene_sets_path)
        if not Path(gs_path_str).exists():
            logger.warning(f"Gene sets file '{gs_path_str}' not found locally. To prevent runtime network calls, enrichment is skipped. Please provide a local GMT file.")
            return None
            
        enr = gp.enrich(
            gene_list=gene_list,
            gene_sets=gs_path_str,
            background=None,
            outdir=None,
            no_plot=True
        )
        if enr.results.empty:
            return None
            
        return enr.results
    except Exception as e:  # noqa: BLE001
        logger.error(f"Enrichment analysis failed: {e}")
        return None
