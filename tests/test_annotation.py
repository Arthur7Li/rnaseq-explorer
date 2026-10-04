from typing import Any

import pandas as pd

from rnax.pipeline.annotation import load_gene_annotations, run_enrichment


def test_load_gene_annotations_success(tmp_path: Any) -> None:
    # create a mock annotation csv
    df = pd.DataFrame([
        {"gene_id": "G1", "gene_symbol": "Gene1", "description": "Desc1"},
        {"gene_id": "G2", "gene_symbol": "Gene2", "description": "Desc2"},
    ])
    df.to_csv(tmp_path / "human_genes.csv", index=False)
    
    annot = load_gene_annotations(["G1", "G3"], "human", tmp_path)
    
    assert not annot.empty
    assert "G1" in annot.index
    assert "G3" not in annot.index
    assert annot.loc["G1", "gene_symbol"] == "Gene1"
    

def test_load_gene_annotations_missing_or_unknown(tmp_path: Any, caplog: Any) -> None:
    # Unknown organism
    annot = load_gene_annotations(["G1"], "alien", tmp_path)
    assert annot.empty
    assert "Unsupported organism" in caplog.text
    
    caplog.clear()
    
    # Missing file
    annot = load_gene_annotations(["G1"], "mouse", tmp_path)
    assert annot.empty
    assert "not found" in caplog.text


def test_run_enrichment_insufficient_genes(caplog: Any) -> None:
    df = pd.DataFrame({
        "gene_symbol": ["G1", "G2"],
        "padj": [0.01, 0.04]
    })
    res = run_enrichment(df, "mock.gmt", "human", 0.05)
    assert res is None
    assert "requires at least 5" in caplog.text


def test_run_enrichment_missing_symbol(caplog: Any) -> None:
    df = pd.DataFrame({
        "padj": [0.01, 0.04, 0.01, 0.01, 0.01]
    })
    res = run_enrichment(df, "mock.gmt", "human", 0.05)
    assert res is None
    assert "requires 'gene_symbol' column" in caplog.text


def test_run_enrichment_mocked(mocker: Any, tmp_path: Any) -> None:
    # Create a dummy GMT file so it passes the local file check
    gmt_file = tmp_path / "mock.gmt"
    gmt_file.write_text("TERM\t\tG1\tG2\n")
    
    df = pd.DataFrame({
        "gene_symbol": ["G1", "G2", "G3", "G4", "G5"],
        "padj": [0.01, 0.01, 0.01, 0.01, 0.01]
    })
    
    mock_enrich = mocker.patch("rnax.pipeline.annotation.gp.enrich")
    mock_enr = mocker.Mock()
    mock_enr.results = pd.DataFrame({
        "Term": ["TERM1"],
        "Overlap": ["2/5"],
        "P-value": [0.001],
        "Adjusted P-value": [0.01],
        "Genes": ["G1;G2"]
    })
    mock_enrich.return_value = mock_enr
    
    res = run_enrichment(df, gmt_file, "human", 0.05)
    
    assert res is not None
    assert len(res) == 1
    assert res.iloc[0]["Term"] == "TERM1"
    
    mock_enrich.assert_called_once()
    _, kwargs = mock_enrich.call_args
    assert set(kwargs["gene_list"]) == {"G1", "G2", "G3", "G4", "G5"}
    assert kwargs["gene_sets"] == str(gmt_file)
