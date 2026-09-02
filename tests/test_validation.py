import pandas as pd
import pytest
from pandera.errors import SchemaError

from rnax.validation import validate_counts_schema, validate_metadata_schema


@pytest.fixture
def valid_counts():
    return pd.DataFrame({
        "gene_id": ["gene1", "gene2", "gene3"],
        "sample1": [10, 20, 0],
        "sample2": [0, 5, 100],
    })


@pytest.fixture
def valid_metadata():
    return pd.DataFrame({
        "sample_id": ["sample1", "sample2"],
        "condition": ["treated", "control"],
        "batch": ["A", "B"],
    })


def test_valid_counts(valid_counts):
    validated = validate_counts_schema(valid_counts, "gene_id")
    assert validated.shape == (3, 3)


def test_counts_missing_gene_id(valid_counts):
    with pytest.raises(ValueError, match="not found"):
        validate_counts_schema(valid_counts, "wrong_gene_id_col")


def test_counts_negative_values(valid_counts):
    bad_counts = valid_counts.copy()
    bad_counts.loc[0, "sample1"] = -5
    
    with pytest.raises(SchemaError, match="non-negative"):
        validate_counts_schema(bad_counts, "gene_id")


def test_counts_float_values(valid_counts):
    bad_counts = valid_counts.copy()
    bad_counts["sample1"] = bad_counts["sample1"].astype(float)
    bad_counts.loc[0, "sample1"] = 5.5
    
    with pytest.raises(SchemaError):
        # Pandera might fail coercion or fail the integer check
        validate_counts_schema(bad_counts, "gene_id")


def test_counts_duplicate_genes(valid_counts):
    bad_counts = valid_counts.copy()
    bad_counts.loc[0, "gene_id"] = "gene2"
    
    with pytest.raises(SchemaError):
        validate_counts_schema(bad_counts, "gene_id")


def test_valid_metadata(valid_metadata):
    validated = validate_metadata_schema(
        valid_metadata, 
        ["sample1", "sample2"], 
        "condition", 
        "batch"
    )
    assert validated.shape == (2, 3)


def test_metadata_missing_sample_id():
    df = pd.DataFrame({"condition": ["treated"]})
    with pytest.raises(ValueError, match="Metadata must contain"):
        validate_metadata_schema(df, ["sample1"], "condition")


def test_metadata_mismatched_samples(valid_metadata):
    with pytest.raises(SchemaError, match="exactly match"):
        # Missing sample2
        validate_metadata_schema(valid_metadata, ["sample1"], "condition")
        
    with pytest.raises(SchemaError, match="exactly match"):
        # Extra sample3
        validate_metadata_schema(valid_metadata, ["sample1", "sample2", "sample3"], "condition")


def test_metadata_missing_condition(valid_metadata):
    bad_meta = valid_metadata.drop(columns=["condition"])
    with pytest.raises(SchemaError):
        validate_metadata_schema(bad_meta, ["sample1", "sample2"], "condition")


def test_metadata_missing_block_column(valid_metadata):
    bad_meta = valid_metadata.drop(columns=["batch"])
    with pytest.raises(SchemaError):
        validate_metadata_schema(bad_meta, ["sample1", "sample2"], "condition", "batch")


def test_metadata_nan_condition(valid_metadata):
    bad_meta = valid_metadata.copy()
    bad_meta.loc[0, "condition"] = None
    with pytest.raises(SchemaError):
        validate_metadata_schema(bad_meta, ["sample1", "sample2"], "condition")
