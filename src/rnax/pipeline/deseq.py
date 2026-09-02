
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

from rnax.config import AnalysisConfig


def filter_low_counts(
    counts: pd.DataFrame, 
    min_count: int, 
    min_samples: int
) -> pd.DataFrame:
    """
    Filter out genes that do not have at least `min_count` counts
    in at least `min_samples`.
    
    Args:
        counts: Unfiltered raw count matrix (genes x samples).
        min_count: Minimum number of reads a gene must have in a sample.
        min_samples: Minimum number of samples that must meet the min_count.
        
    Returns:
        Filtered count matrix.
    """
    keep = (counts >= min_count).sum(axis=1) >= min_samples
    return counts[keep]


def run_deseq2(
    counts_df: pd.DataFrame,
    metadata_df: pd.DataFrame,
    config: AnalysisConfig
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Run PyDESeq2 differential expression pipeline.
    
    Args:
        counts_df: Validated raw counts (genes x samples).
        metadata_df: Validated metadata.
        config: Analysis configuration.
        
    Returns:
        Tuple of (normalized_counts_df, deseq_results_df).
    """
    # 1. Filter low count genes
    filtered_counts = filter_low_counts(
        counts_df,
        config.filtering.minimum_count,
        config.filtering.minimum_samples,
    )
    
    # 2. Setup the design formula
    design_factors = [config.design.condition_column]
    if config.design.paired_or_block_column:
        # In formulaic, you put block first so it controls variance before condition
        # But for pydeseq2 string formula, just join with +
        design_factors.append(config.design.paired_or_block_column)

    # PyDESeq2 expects counts transposed as (samples x genes)
    counts_t = filtered_counts.T

    # 3. Initialize DeseqDataSet
    dds = DeseqDataSet(
        counts=counts_t,
        metadata=metadata_df,
        design_factors=design_factors, # Note: PyDESeq2 <= 0.4.1 uses design_factors list.
                                       # Wait, if we use formulaic via formula string?
                                       # Actually, PyDESeq2's DeseqDataSet signature handles
                                       # design_factors as a single string formula or list.
                                       # Let's just use formula string if supported, or list of strings.
                                       # The standard argument in newer pydeseq2 is `design_factors`.
                                       # Passing it as a list of column names builds `~ col1 + col2`.
                                       # Let's pass the list of column names.
        refit_cooks=True,
        n_cpus=1,  # Single-threaded by default to ensure reproducibility/stability
    )
    
    # Run the DESeq2 pipeline
    dds.deseq2()
    
    # 4. Extract Results
    # In PyDESeq2, contrast is passed as [factor, numerator, denominator]
    contrast = [
        config.design.condition_column,
        config.design.comparison_level,
        config.design.reference_level
    ]
    
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
    
    return normalized_counts, results_df
