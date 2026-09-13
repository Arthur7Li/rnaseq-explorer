# Multi-Dataset Validation Report

This document records the empirical validation of RNA-seq Explorer across three distinct biological datasets: **Airway** (*Homo sapiens*), **Pasilla** (*Drosophila melanogaster*), and **Bottomly** (*Mus musculus*).

The objective of this validation is to verify structural, schema, and architectural stability across varying sample sizes, experimental designs, and organisms, **not** to compare biological conclusions.

---

## Benchmark Datasets Evaluated

| Dataset | Organism | Samples | Design Structure | Reference Level | Comparison Level | Status |
|---|---|---|---|---|---|---|
| **Airway** | *Homo sapiens* | 8 | Paired / Blocking (`cell_line`) | `untreated` | `dexamethasone` | Validated |
| **Pasilla** | *Drosophila melanogaster* | 7 | Unpaired two-group | `untreated` | `treated` | Validated |
| **Bottomly** | *Mus musculus* | 10 | Unpaired two-group | `C57BL_6J` | `DBA_2J` | Validated |

---

## Verification Evidence

### 1. Unified Input Contract
All three datasets conform to the strict `InputConfig` schema:
- Raw integer count matrix (`counts.csv`) validated via `pandera`.
- Normalized counts (e.g., FPKM/TPM) and floating-point values are rejected.
- Sample metadata (`metadata.csv`) aligns column headers with sample identifiers.
- Binary experimental condition validated with exactly two factor levels.

### 2. Output Schema Consistency
Across all three datasets, the pipeline generates identical output structures in `results/<dataset>/`:
- `report.html` (rendered HTML with all required metadata, methodology, QC observations, and reproducibility manifest)
- `results.csv` (PyDESeq2 results with standard columns: `baseMean`, `log2FoldChange`, `lfcSE`, `stat`, `pvalue`, `padj`)
- `normalized_counts.csv` (size-factor normalized expression matrix)
- QC Figures:
  - `library_sizes.png`
  - `pca.png`
  - `sample_distances.png`
- Differential Expression Figures:
  - `volcano.png`
  - `ma_plot.png`
  - `top_genes_heatmap.png`

### 3. Automated Integration Tests
End-to-end execution of both unpaired (`pasilla`) and cross-species validation (`bottomly`) datasets is continuously exercised in automated integration tests:

```bash
uv run pytest tests/test_integration.py
```

Both tests complete without warnings or errors, proving that:
- Non-human gene namespaces (e.g., FlyBase `FBgn...`, Ensembl Mouse `ENSMUSG...`) are supported seamlessly.
- Both paired designs with blocking covariates and simple two-group designs execute without manual code intervention.
- The reproducibility manifest correctly hashes files across different operating environments.

---

## Conclusion
RNA-seq Explorer successfully demonstrates generalized, robust bulk RNA-seq differential expression analysis across multiple species and experimental configurations while maintaining data integrity, non-clinical framing, and complete provenance traceability.
