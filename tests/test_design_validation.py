import pandas as pd
import pytest

from rnax.config import AnalysisConfig, ContrastSpec


@pytest.fixture
def mock_config():
    config = AnalysisConfig.model_construct()
    config.design = type("obj", (object,), {
        "condition_column": "condition",
        "paired_or_block_column": None,
        "reference_level": "A",
        "comparison_level": "B"
    })()
    config.contrasts = None
    return config


def test_validate_design_matrix_success(mock_config):
    metadata = pd.DataFrame({
        "condition": ["A", "A", "A", "B", "B", "B"]
    })
    warnings = mock_config.validate_design_matrix(metadata)
    assert len(warnings) == 0


def test_validate_design_matrix_missing_condition_column(mock_config):
    metadata = pd.DataFrame({
        "wrong_column": ["A", "A", "A", "B", "B", "B"]
    })
    with pytest.raises(ValueError, match="Condition column 'condition' not found"):
        mock_config.validate_design_matrix(metadata)


def test_validate_design_matrix_missing_level(mock_config):
    metadata = pd.DataFrame({
        "condition": ["A", "A", "A", "C", "C", "C"]
    })
    with pytest.raises(ValueError, match="Comparison level 'B' not found"):
        mock_config.validate_design_matrix(metadata)


def test_validate_design_matrix_low_sample_size_warning(mock_config):
    metadata = pd.DataFrame({
        "condition": ["A", "A", "B", "B", "B"]
    })
    warnings = mock_config.validate_design_matrix(metadata)
    assert len(warnings) == 1
    assert "has < 3 replicates" in warnings[0]


def test_validate_design_matrix_perfect_confounding(mock_config):
    mock_config.design.paired_or_block_column = "block"
    # Block 1 only has A, Block 2 only has B
    metadata = pd.DataFrame({
        "condition": ["A", "A", "A", "B", "B", "B"],
        "block": ["b1", "b1", "b1", "b2", "b2", "b2"]
    })
    with pytest.raises(ValueError, match="Perfect confounding detected"):
        mock_config.validate_design_matrix(metadata)


def test_validate_design_matrix_multiple_contrasts():
    config = AnalysisConfig.model_construct()
    config.design = type("obj", (object,), {
        "condition_column": "condition",
        "paired_or_block_column": None,
        "reference_level": "A",
        "comparison_level": "B"
    })()
    config.contrasts = [
        ContrastSpec(name="AvsB", condition_column="condition", reference_level="A", comparison_level="B"),
        ContrastSpec(name="CvsA", condition_column="condition", reference_level="A", comparison_level="C")
    ]
    
    metadata = pd.DataFrame({
        "condition": ["A", "A", "A", "B", "B", "B", "C", "C", "C"]
    })
    
    warnings = config.validate_design_matrix(metadata)
    assert len(warnings) == 0


def test_validate_design_matrix_multiple_contrasts_error():
    config = AnalysisConfig.model_construct()
    config.design = type("obj", (object,), {
        "condition_column": "condition",
        "paired_or_block_column": None,
        "reference_level": "A",
        "comparison_level": "B"
    })()
    config.contrasts = [
        ContrastSpec(name="AvsB", condition_column="condition", reference_level="A", comparison_level="B"),
        ContrastSpec(name="CvsA", condition_column="condition", reference_level="A", comparison_level="C")
    ]
    
    metadata = pd.DataFrame({
        "condition": ["A", "A", "A", "B", "B", "B"]
    })
    
    with pytest.raises(ValueError, match="Comparison level 'C' not found"):
        config.validate_design_matrix(metadata)
