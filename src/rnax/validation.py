
import pandas as pd
import pandera as pa


def validate_counts_schema(df: pd.DataFrame, gene_id_column: str) -> pd.DataFrame:
    """
    Validate the count matrix.
    
    Args:
        df: The pandas DataFrame representing the counts.
        gene_id_column: The column name for gene identifiers.
        
    Returns:
        The validated DataFrame.
        
    Raises:
        SchemaError: If the dataframe fails validation.
        ValueError: If gene_id_column is missing.
    """
    if gene_id_column not in df.columns:
        raise ValueError(f"Required gene ID column '{gene_id_column}' not found in counts data.")

    # All columns except gene_id_column should be non-negative integers
    sample_cols = [col for col in df.columns if col != gene_id_column]
    
    columns_schema = {
        gene_id_column: pa.Column(str, unique=True, coerce=True),
    }
    
    for col in sample_cols:
        # non-negative integer check
        columns_schema[col] = pa.Column(
            int,
            checks=pa.Check.ge(0, error="Counts must be non-negative integers"),
            coerce=False,
            nullable=False,
        )

    schema = pa.DataFrameSchema(
        columns=columns_schema,
        strict=True,
        coerce=False
    )
    
    return schema.validate(df)


def validate_metadata_schema(
    df: pd.DataFrame, 
    sample_ids: list[str], 
    condition_column: str,
    paired_or_block_column: str | None = None
) -> pd.DataFrame:
    """
    Validate the metadata matrix.
    
    Args:
        df: The pandas DataFrame representing the metadata.
        sample_ids: The list of sample IDs (columns from the count matrix) that must be present.
        condition_column: The column defining the experimental condition.
        paired_or_block_column: The optional blocking covariate column.
        
    Returns:
        The validated DataFrame.
    """
    if "sample_id" not in df.columns:
        raise ValueError("Metadata must contain a 'sample_id' column.")
        
    columns_schema = {
        "sample_id": pa.Column(
            str, 
            checks=[
                pa.Check(
                    lambda s: set(s) == set(sample_ids),
                    error="Metadata sample IDs must exactly match the count matrix sample columns."
                )
            ],
            unique=True,
            coerce=True
        ),
        condition_column: pa.Column(str, nullable=False, coerce=True),
    }

    if paired_or_block_column:
        columns_schema[paired_or_block_column] = pa.Column(
            str, 
            nullable=False, 
            coerce=True,
            # Implicitly validating that it has no missing values and acts categorically
        )

    schema = pa.DataFrameSchema(
        columns=columns_schema,
        strict=False, # Allow extra metadata columns
        coerce=True
    )
    
    return schema.validate(df)
