from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from rnax.config import AnalysisConfig


def test_valid_config_parsing(valid_config_file):
    config = AnalysisConfig.from_yaml(valid_config_file)
    assert config.input.gene_id_column == "gene_id"
    assert config.design.condition_column == "condition"
    assert config.design.paired_or_block_column is None
    assert config.output.report_title == "Demo Analysis"


def test_config_with_blocking_covariate(temp_dir, valid_config_dict):
    valid_config_dict["design"]["paired_or_block_column"] = "cell_line"
    config_path = temp_dir / "blocked_config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(valid_config_dict, f)
        
    config = AnalysisConfig.from_yaml(config_path)
    assert config.design.paired_or_block_column == "cell_line"


def test_missing_required_fields(temp_dir, valid_config_dict):
    del valid_config_dict["input"]["counts"]
    config_path = temp_dir / "invalid_config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(valid_config_dict, f)
        
    with pytest.raises(ValidationError) as exc_info:
        AnalysisConfig.from_yaml(config_path)
    assert "counts" in str(exc_info.value)


def test_invalid_fdr_threshold(temp_dir, valid_config_dict):
    valid_config_dict["thresholds"]["fdr"] = 1.5
    config_path = temp_dir / "invalid_config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(valid_config_dict, f)
        
    with pytest.raises(ValidationError):
        AnalysisConfig.from_yaml(config_path)


def test_extra_fields_forbidden(temp_dir, valid_config_dict):
    valid_config_dict["extra_field"] = "not allowed"
    config_path = temp_dir / "invalid_config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(valid_config_dict, f)
        
    with pytest.raises(ValidationError) as exc_info:
        AnalysisConfig.from_yaml(config_path)
    assert "extra_field" in str(exc_info.value)


def test_parse_real_airway_config():
    # Should successfully parse the committed airway.yaml
    repo_root = Path(__file__).parent.parent
    config_path = repo_root / "config" / "airway.yaml"
    
    config = AnalysisConfig.from_yaml(config_path)
    assert config.design.paired_or_block_column == "cell_line"
    assert config.design.condition_column == "treatment"
