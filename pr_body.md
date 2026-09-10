## Summary

This PR executes **Phase 3: New Visualizations** from the Good Portfolio Version implementation plan.

## Changes
- **`plots.py`**:
  - Implemented `plot_sample_distances()`: Computes pairwise Euclidean distances on log1p-normalized counts, plotted as a clustered heatmap with condition/block annotations using `seaborn.clustermap`.
  - Implemented `plot_ma()`: Plots log2FoldChange against log10(baseMean), highlighting significant genes with the same color palette as the volcano plot.
  - Implemented `plot_top_genes_heatmap()`: Selects the top `n_top` genes by ascending `padj`, computes z-scores per gene across samples using `scipy.stats.zscore`, and generates a clustered heatmap (rows clustered, columns ordered by condition).
- **`config.py`**: Added `top_n_genes` (default: 30) to `ThresholdsConfig`.
- **`report.py` & `report.html.j2`**: Wired the new plots into the pipeline and embedded them in the HTML report with interpretive captions.
- **`docs/DECISIONS.md`**: Added decision `D-6` for the new `top_n_genes` config parameter.
- **Tests**: Added tests for all three new plot functions and updated `test_report.py` mocks.

## Test evidence
- `uv run pytest` runs and passes (36 tests).
- `uv run mypy src/` strictly validates the new plotting code.
- `uv run ruff check .` is clean.

## Definition of Done
- [x] All acceptance criteria met, no silent scope reduction
- [x] Tests added/updated
- [x] `.agent/GUARDRAILS.md` reviewed; none violated
