from pathlib import Path

import pandas as pd

from rnax.config import AnalysisConfig, DesignConfig, InputConfig, OutputConfig, ThresholdsConfig
from rnax.pipeline.sensitivity import run_sensitivity_analysis


def test_sensitivity_stable() -> None:
    # stable output, hits don't change much
    df = pd.DataFrame({
        "padj": [0.001, 0.001, 0.001, 0.001, 0.001, 0.99, 0.99],
        "log2FoldChange": [2.0, 2.0, -2.0, -2.0, 2.0, 0.1, -0.1]
    })
    
    config = AnalysisConfig(
        input=InputConfig(counts=Path("mock"), metadata=Path("mock"), gene_id_column="id"),
        design=DesignConfig(condition_column="cond", reference_level="A", comparison_level="B"),
        output=OutputConfig(directory=Path("mock"), report_title="title"),
        thresholds=ThresholdsConfig(fdr=0.05, absolute_log2_fold_change=1.0)
    )
    
    res = run_sensitivity_analysis(df, config)
    assert "Stable" in res.verdict
    assert len(res.table) >= 9
    

def test_sensitivity_sensitive() -> None:
    # sensitive output, changing FDR from 0.01 to 0.1 reveals many more genes
    # need >= 20 total to bypass "Low Counts" check
    padjs = [0.005] * 2 + [0.02] * 5 + [0.03] * 5 + [0.04] * 5 + [0.06] * 5 + [0.08] * 5
    lfcs = [1.5] * len(padjs)
    
    df = pd.DataFrame({
        "padj": padjs,
        "log2FoldChange": lfcs
    })
    
    config = AnalysisConfig(
        input=InputConfig(counts=Path("mock"), metadata=Path("mock"), gene_id_column="id"),
        design=DesignConfig(condition_column="cond", reference_level="A", comparison_level="B"),
        output=OutputConfig(directory=Path("mock"), report_title="title"),
        thresholds=ThresholdsConfig(fdr=0.01, absolute_log2_fold_change=1.0)
    )
    
    res = run_sensitivity_analysis(df, config)
    assert res.verdict == "Sensitive"
    
    
def test_sensitivity_zero_hits() -> None:
    # no significant genes
    df = pd.DataFrame({
        "padj": [0.5, 0.9, 0.8],
        "log2FoldChange": [0.1, -0.1, 0.2]
    })
    
    config = AnalysisConfig(
        input=InputConfig(counts=Path("mock"), metadata=Path("mock"), gene_id_column="id"),
        design=DesignConfig(condition_column="cond", reference_level="A", comparison_level="B"),
        output=OutputConfig(directory=Path("mock"), report_title="title"),
        thresholds=ThresholdsConfig()
    )
    
    res = run_sensitivity_analysis(df, config)
    assert res.verdict == "Stable"
    assert "Zero significant genes" in res.rationale


def test_sensitivity_low_counts() -> None:
    # low counts, small absolute change
    df = pd.DataFrame({
        "padj": [0.01, 0.02],
        "log2FoldChange": [2.0, -2.0]
    })
    
    config = AnalysisConfig(
        input=InputConfig(counts=Path("mock"), metadata=Path("mock"), gene_id_column="id"),
        design=DesignConfig(condition_column="cond", reference_level="A", comparison_level="B"),
        output=OutputConfig(directory=Path("mock"), report_title="title"),
        thresholds=ThresholdsConfig(fdr=0.01, absolute_log2_fold_change=1.0)
    )
    
    res = run_sensitivity_analysis(df, config)
    assert "Stable (Low Counts)" in res.verdict
