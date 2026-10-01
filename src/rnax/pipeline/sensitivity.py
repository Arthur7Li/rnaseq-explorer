from dataclasses import dataclass

import pandas as pd

from rnax.config import AnalysisConfig


@dataclass
class SensitivityRow:
    fdr: float
    lfc: float
    up: int
    down: int
    total_sig: int


@dataclass
class SensitivityResult:
    table: list[SensitivityRow]
    verdict: str
    rationale: str


def run_sensitivity_analysis(results_df: pd.DataFrame, config: AnalysisConfig) -> SensitivityResult:
    """
    Evaluate the robustness of DE results by varying FDR and log2FoldChange thresholds
    without re-running the DESeq2 model.
    """
    default_fdr = config.thresholds.fdr
    default_lfc = config.thresholds.absolute_log2_fold_change
    
    fdr_levels = sorted({0.01, 0.05, 0.10, default_fdr})
    lfc_levels = sorted({0.5, 1.0, 1.5, default_lfc})
    
    table = []
    default_total = 0
    
    for fdr in fdr_levels:
        for lfc in lfc_levels:
            mask = (results_df["padj"] < fdr) & (results_df["log2FoldChange"].abs() >= lfc)
            up = int((mask & (results_df["log2FoldChange"] > 0)).sum())
            down = int((mask & (results_df["log2FoldChange"] < 0)).sum())
            total = up + down
            
            table.append(SensitivityRow(fdr=fdr, lfc=lfc, up=up, down=down, total_sig=total))
            
            if fdr == default_fdr and lfc == default_lfc:
                default_total = total
                
    max_total = max(r.total_sig for r in table)
    min_total = min(r.total_sig for r in table)
    
    if default_total == 0 and max_total == 0:
        verdict = "Stable"
        rationale = "Zero significant genes found across all tested parameter combinations."
    elif default_total < 10 and max_total < 20:
        verdict = "Stable (Low Counts)"
        rationale = "Very few significant genes at default thresholds; shifting counts is uninformative."
    else:
        # Avoid zero division
        if default_total > 0:
            max_diff = max(abs(max_total - default_total), abs(default_total - min_total))
            if (max_diff / default_total) > 0.5:
                verdict = "Sensitive"
                rationale = f"Significant gene count is highly sensitive (>50% shift) to threshold choices. (Default: {default_total}, Max: {max_total}, Min: {min_total})"
            else:
                verdict = "Stable"
                rationale = f"DE scale is robust. Significant gene count varies by less than 50% across threshold grid. (Default: {default_total}, Max: {max_total}, Min: {min_total})"
        else:
            verdict = "Sensitive"
            rationale = f"Default threshold yielded 0 genes, but relaxed thresholds yielded up to {max_total} genes."

    return SensitivityResult(table=table, verdict=verdict, rationale=rationale)
