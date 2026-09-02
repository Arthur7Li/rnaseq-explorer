import tempfile
from pathlib import Path

import pytest
import yaml


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)

@pytest.fixture
def valid_config_dict():
    return {
        "input": {
            "counts": "data/counts.csv",
            "metadata": "data/metadata.csv",
            "gene_id_column": "gene_id"
        },
        "design": {
            "condition_column": "condition",
            "reference_level": "control",
            "comparison_level": "treated"
        },
        "filtering": {
            "minimum_count": 10,
            "minimum_samples": 2
        },
        "thresholds": {
            "fdr": 0.05,
            "absolute_log2_fold_change": 1.0
        },
        "output": {
            "directory": "results/demo",
            "report_title": "Demo Analysis"
        }
    }

@pytest.fixture
def valid_config_file(temp_dir, valid_config_dict):
    import pandas as pd
    counts_path = temp_dir / "counts.csv"
    meta_path = temp_dir / "meta.csv"
    
    pd.DataFrame({
        "gene_id": ["gene1", "gene2"],
        "sample1": [10, 20],
        "sample2": [0, 5]
    }).to_csv(counts_path, index=False)
    
    pd.DataFrame({
        "sample_id": ["sample1", "sample2"],
        "condition": ["treated", "control"]
    }).to_csv(meta_path, index=False)
    
    valid_config_dict["input"]["counts"] = str(counts_path)
    valid_config_dict["input"]["metadata"] = str(meta_path)
    
    config_path = temp_dir / "valid_config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(valid_config_dict, f)
    return config_path
