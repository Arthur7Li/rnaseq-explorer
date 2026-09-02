import pandas as pd
import pytest

from rnax.config import AnalysisConfig
from rnax.pipeline.deseq import filter_low_counts, run_deseq2


@pytest.fixture
def sample_counts():
    return pd.DataFrame({
        "gene1": [10, 15, 20, 25],
        "gene2": [0, 0, 1, 0],
        "gene3": [5, 5, 5, 5],
        "gene4": [100, 200, 150, 100],
    }, index=["sample1", "sample2", "sample3", "sample4"]).T


@pytest.fixture
def sample_metadata():
    return pd.DataFrame({
        "sample_id": ["sample1", "sample2", "sample3", "sample4"],
        "condition": ["A", "A", "B", "B"],
        "batch": ["1", "2", "1", "2"],
    }).set_index("sample_id")


@pytest.fixture
def mock_config():
    config = AnalysisConfig.model_construct()
    config.filtering = type("obj", (object,), {"minimum_count": 5, "minimum_samples": 2})()
    config.design = type("obj", (object,), {
        "condition_column": "condition",
        "paired_or_block_column": "batch",
        "reference_level": "A",
        "comparison_level": "B"
    })()
    return config


def test_filter_low_counts(sample_counts):
    # min_count=5, min_samples=2
    filtered = filter_low_counts(sample_counts, min_count=5, min_samples=2)
    # gene1: all >=5 -> keep
    # gene2: max is 1 -> drop
    # gene3: all 5 -> keep
    # gene4: all >=5 -> keep
    assert "gene2" not in filtered.index
    assert "gene1" in filtered.index
    assert "gene3" in filtered.index
    assert "gene4" in filtered.index
    assert filtered.shape == (3, 4)


def test_run_deseq2_mocked(mocker, sample_counts, sample_metadata, mock_config):
    # Mock PyDESeq2 to avoid slow computations during unit testing
    mock_dds = mocker.patch("rnax.pipeline.deseq.DeseqDataSet")
    mock_dds_instance = mock_dds.return_value
    # mock normed_counts property/layer (drop gene2 which gets filtered)
    filtered_counts = sample_counts.drop("gene2")
    mock_dds_instance.layers = {"normed_counts": filtered_counts.T.values}
    
    mock_ds = mocker.patch("rnax.pipeline.deseq.DeseqStats", autospec=True)
    mock_ds_instance = mock_ds.return_value
    mock_ds_instance.results_df = pd.DataFrame({
        "log2FoldChange": [1.0, -1.0, 0.5],
        "padj": [0.01, 0.05, 0.99]
    }, index=["gene1", "gene3", "gene4"])
    
    norm_counts, results = run_deseq2(sample_counts, sample_metadata, mock_config)
    
    # Assert DeseqDataSet was initialized with correct params
    mock_dds.assert_called_once()
    _, kwargs = mock_dds.call_args
    assert "batch" in kwargs["design_factors"]
    assert "condition" in kwargs["design_factors"]
    # assert the count matrix passed was transposed
    assert kwargs["counts"].shape == (4, 3) # samples x filtered genes
    
    mock_dds_instance.deseq2.assert_called_once()
    
    # Assert DeseqStats called with correct contrast
    mock_ds.assert_called_once()
    _, ds_kwargs = mock_ds.call_args
    assert ds_kwargs["contrast"] == ["condition", "B", "A"]
    
    mock_ds_instance.summary.assert_called_once()
    
    # Check outputs
    assert norm_counts.shape == (3, 4)
    assert list(norm_counts.columns) == ["sample1", "sample2", "sample3", "sample4"]
    assert results.shape == (3, 2)
