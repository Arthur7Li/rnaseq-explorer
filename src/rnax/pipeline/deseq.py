
import logging
from dataclasses import dataclass

import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

from rnax.config import AnalysisConfig

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from rnax.config import ContrastSpec

logger = logging.getLogger(__name__)


@dataclass
class FilteringResult:
    filtered_counts: pd.DataFrame
    genes_before: int
    genes_after: int
    min_count: int
    min_samples: int


def filter_low_counts(
    counts: pd.DataFrame, 
    min_count: int, 
    min_samples: int
) -> FilteringResult:
    """
    Filter out genes that do not have at least `min_count` counts
    in at least `min_samples`.
    
    Args:
        counts: Unfiltered raw count matrix (genes x samples).
        min_count: Minimum number of reads a gene must have in a sample.
        min_samples: Minimum number of samples that must meet the min_count.
        
    Returns:
        FilteringResult containing filtered count matrix and filtering stats.
    """
    genes_before = counts.shape[0]
    keep = (counts >= min_count).sum(axis=1) >= min_samples
    filtered_counts = counts[keep]
    genes_after = filtered_counts.shape[0]

    logger.info(
        f"Filtering: {genes_before} genes → {genes_after} genes "
        f"(kept genes with >= {min_count} counts in >= {min_samples} samples)"
    )

    return FilteringResult(
        filtered_counts=filtered_counts,
        genes_before=genes_before,
        genes_after=genes_after,
        min_count=min_count,
        min_samples=min_samples,
    )


def run_deseq2(
    counts_df: pd.DataFrame,
    metadata_df: pd.DataFrame,
    config: AnalysisConfig,
    contrast_spec: "ContrastSpec | None" = None
) -> tuple[pd.DataFrame, pd.DataFrame, FilteringResult]:
    """
    Run PyDESeq2 differential expression pipeline.
    
    Args:
        counts_df: Validated raw counts (genes x samples).
        metadata_df: Validated metadata.
        config: Analysis configuration.
        contrast_spec: Optional specific contrast to run. If None, falls back to config.design.
        
    Returns:
        Tuple of (normalized_counts_df, deseq_results_df, filtering_result).
    """
    from rnax.config import ContrastSpec
    
    cond_col = contrast_spec.condition_column if contrast_spec else config.design.condition_column
    comp_level = contrast_spec.comparison_level if contrast_spec else config.design.comparison_level
    ref_level = contrast_spec.reference_level if contrast_spec else config.design.reference_level

    # 1. Filter low count genes
    filtering_result = filter_low_counts(
        counts_df,
        config.filtering.minimum_count,
        config.filtering.minimum_samples,
    )
    filtered_counts = filtering_result.filtered_counts
    
    # 2. Setup the design formula
    design_formula = f"~ {cond_col}"
    if config.design.paired_or_block_column:
        # Block factor should ideally be first in formula to control for variance
        design_formula = f"~ {config.design.paired_or_block_column} + {cond_col}"

    # PyDESeq2 expects counts transposed as (samples x genes)
    counts_t = filtered_counts.T

    # 3. Initialize DeseqDataSet
    dds = DeseqDataSet(
        counts=counts_t,
        metadata=metadata_df,
        design=design_formula,
        refit_cooks=True,
        n_cpus=1,  # Single-threaded by default to ensure reproducibility/stability
    )
    
    # Run the DESeq2 pipeline
    dds.deseq2()
    
    # 4. Extract Results
    # In PyDESeq2, contrast is passed as [factor, numerator, denominator]
    contrast = [cond_col, comp_level, ref_level]
    
    stat_res = DeseqStats(
        dds,
        contrast=contrast,
        n_cpus=1
    )
    
    stat_res.summary()
    results_df = stat_res.results_df
    
    # Extract normalized counts (samples x genes) and transpose back to (genes x samples)
    normalized_counts = dds.layers["normed_counts"].T
    # The columns are sample IDs, index is gene IDs
    normalized_counts = pd.DataFrame(
        normalized_counts, 
        index=filtered_counts.index, 
        columns=filtered_counts.columns
    )
    
    return normalized_counts, results_df, filtering_result
