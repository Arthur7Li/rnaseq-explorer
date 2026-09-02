from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class InputConfig(BaseModel):
    counts: Path
    metadata: Path
    gene_id_column: str


class DesignConfig(BaseModel):
    condition_column: str
    reference_level: str
    comparison_level: str
    paired_or_block_column: str | None = None


class FilteringConfig(BaseModel):
    minimum_count: int = 10
    minimum_samples: int = 2


class ThresholdsConfig(BaseModel):
    fdr: float = Field(default=0.05, ge=0.0, le=1.0)
    absolute_log2_fold_change: float = Field(default=1.0, ge=0.0)


class OutputConfig(BaseModel):
    directory: Path
    report_title: str
    random_seed: int = 42


class AnalysisConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    input: InputConfig
    design: DesignConfig
    filtering: FilteringConfig = Field(default_factory=FilteringConfig)
    thresholds: ThresholdsConfig = Field(default_factory=ThresholdsConfig)
    output: OutputConfig

    @classmethod
    def from_yaml(cls, yaml_path: Path | str) -> "AnalysisConfig":
        import yaml
        
        path = Path(yaml_path)
        if not path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {path}")
            
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            
        if not isinstance(data, dict):
            raise TypeError("Configuration must be a YAML dictionary")
            
        return cls.model_validate(data)
