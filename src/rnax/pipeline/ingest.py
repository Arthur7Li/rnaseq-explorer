
import pandas as pd

from rnax.config import AnalysisConfig
from rnax.validation import validate_counts_schema, validate_metadata_schema


def ingest_data(config: AnalysisConfig) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load and strictly validate counts and metadata according to the configuration.
    
    Args:
        config: The parsed AnalysisConfig.
        
    Returns:
        Tuple of (counts_df, metadata_df).
    """
    try:
        counts_df = pd.read_csv(config.input.counts)
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Failed to read counts file {config.input.counts}: {e}") from e

    try:
        metadata_df = pd.read_csv(config.input.metadata)
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Failed to read metadata file {config.input.metadata}: {e}") from e

    # Validate counts
    counts_df = validate_counts_schema(counts_df, config.input.gene_id_column)
    
    # Extract sample IDs from counts
    sample_ids = [col for col in counts_df.columns if col != config.input.gene_id_column]
    
    # Enforce minimum samples configured
    if len(sample_ids) < config.filtering.minimum_samples:
        raise ValueError(
            f"Count matrix contains {len(sample_ids)} samples, but filtering.minimum_samples "
            f"is set to {config.filtering.minimum_samples}."
        )

    # Validate metadata
    metadata_df = validate_metadata_schema(
        df=metadata_df,
        sample_ids=sample_ids,
        condition_column=config.design.condition_column,
        paired_or_block_column=config.design.paired_or_block_column,
    )
    
    # Set index to gene_id for counts and sample_id for metadata
    counts_df = counts_df.set_index(config.input.gene_id_column)
    metadata_df = metadata_df.set_index("sample_id")
    
    # Align metadata order to match counts column order
    metadata_df = metadata_df.loc[sample_ids]
    
    return counts_df, metadata_df
