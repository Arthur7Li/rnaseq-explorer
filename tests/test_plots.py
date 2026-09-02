import pandas as pd
import pytest

from rnax.pipeline.plots import plot_library_sizes, plot_pca, plot_volcano


@pytest.fixture
def sample_counts():
    return pd.DataFrame({
        "sample1": [10, 20, 30],
        "sample2": [15, 25, 35],
    }, index=["gene1", "gene2", "gene3"])


@pytest.fixture
def sample_metadata():
    return pd.DataFrame({
        "sample_id": ["sample1", "sample2"],
        "condition": ["A", "B"],
    }).set_index("sample_id")


@pytest.fixture
def sample_results():
    return pd.DataFrame({
        "log2FoldChange": [1.5, -0.5, -2.0],
        "padj": [0.01, 0.5, 0.0001],
    }, index=["gene1", "gene2", "gene3"])


def test_plot_library_sizes(mocker, sample_counts, sample_metadata):
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    plot_library_sizes(sample_counts, sample_metadata, "condition", "test_lib.png")
    mock_savefig.assert_called_once_with("test_lib.png", dpi=300)


def test_plot_pca(mocker, sample_counts, sample_metadata):
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    plot_pca(sample_counts, sample_metadata, "condition", "test_pca.png")
    mock_savefig.assert_called_once_with("test_pca.png", dpi=300)


def test_plot_volcano(mocker, sample_results):
    mock_savefig = mocker.patch("rnax.pipeline.plots.plt.savefig")
    plot_volcano(sample_results, 0.05, 1.0, "test_volcano.png")
    mock_savefig.assert_called_once_with("test_volcano.png", dpi=300)
