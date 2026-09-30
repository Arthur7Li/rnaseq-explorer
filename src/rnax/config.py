from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    import pandas as pd


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
    top_n_genes: int = Field(default=30, ge=1)


class OutputConfig(BaseModel):
    directory: Path
    report_title: str
    random_seed: int = 42


class ContrastSpec(BaseModel):
    name: str
    condition_column: str
    reference_level: str
    comparison_level: str


class AnalysisConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    input: InputConfig
    design: DesignConfig
    filtering: FilteringConfig = Field(default_factory=FilteringConfig)
    thresholds: ThresholdsConfig = Field(default_factory=ThresholdsConfig)
    dataset_limitations: list[str] = Field(default_factory=list)
    output: OutputConfig
    contrasts: list[ContrastSpec] | None = None

    def validate_design_matrix(self, metadata_df: "pd.DataFrame") -> list[str]:
        import pandas as pd
        
        warnings = []
        
        contrasts_to_check = self.contrasts
        if not contrasts_to_check:
            contrasts_to_check = [
                ContrastSpec(
                    name=f"{self.design.comparison_level}_vs_{self.design.reference_level}",
                    condition_column=self.design.condition_column,
                    reference_level=self.design.reference_level,
                    comparison_level=self.design.comparison_level
                )
            ]
            
        block_col = self.design.paired_or_block_column
        if block_col and block_col not in metadata_df.columns:
            raise ValueError(f"Block column '{block_col}' not found in metadata.")
            
        for contrast in contrasts_to_check:
            cond_col = contrast.condition_column
            if cond_col not in metadata_df.columns:
                raise ValueError(f"Condition column '{cond_col}' not found in metadata for contrast '{contrast.name}'.")
            
            ref_level = contrast.reference_level
            comp_level = contrast.comparison_level
            
            if ref_level not in metadata_df[cond_col].values:
                raise ValueError(f"Reference level '{ref_level}' not found in condition column '{cond_col}'.")
                
            if comp_level not in metadata_df[cond_col].values:
                raise ValueError(f"Comparison level '{comp_level}' not found in condition column '{cond_col}'.")
                
            if block_col:
                subset = metadata_df[metadata_df[cond_col].isin([ref_level, comp_level])]
                crosstab = pd.crosstab(subset[cond_col], subset[block_col])
                # If every block only has samples from one condition, it's confounded.
                if (crosstab > 0).sum(axis=0).eq(1).all():
                    raise ValueError(f"Perfect confounding detected between '{cond_col}' and '{block_col}' for contrast '{contrast.name}'.")
                    
            ref_count = (metadata_df[cond_col] == ref_level).sum()
            comp_count = (metadata_df[cond_col] == comp_level).sum()
            
            if ref_count < 3:
                warnings.append(f"Contrast '{contrast.name}': Reference group '{ref_level}' has < 3 replicates (n={ref_count}).")
            if comp_count < 3:
                warnings.append(f"Contrast '{contrast.name}': Comparison group '{comp_level}' has < 3 replicates (n={comp_count}).")
                
        return warnings

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
