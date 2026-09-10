## Summary

This PR implements **Phase 7: CI Smoke Test** from the Good Portfolio Version implementation plan.

## Changes
- **`.github/workflows/ci.yml`**: Added a `smoke-test` job running after the `test` job.
  - Automatically executes `uv run rnax analyze --config config/pasilla.yaml` on CI runners using the committed Pasilla test fixture dataset (no network download required).
  - Asserts that all expected output files are generated:
    - `results/pasilla/report.html`
    - `results/pasilla/results.csv`
    - `results/pasilla/normalized_counts.csv`
    - `results/pasilla/library_sizes.png`
    - `results/pasilla/pca.png`
    - `results/pasilla/volcano.png`
    - `results/pasilla/sample_distances.png`
    - `results/pasilla/ma_plot.png`
    - `results/pasilla/top_genes_heatmap.png`
  - Validates that the generated HTML report contains the mandatory exploratory `LIMITATION NOTICE`.

## Test evidence
- Smoke test commands executed and validated locally.
- `uv run ruff check .` passes with zero issues.
- `uv run mypy src/` passes with zero issues.
- `uv run pytest` passes.

## Definition of Done
- [x] All acceptance criteria met, no silent scope reduction
- [x] CI smoke test added and validated
- [x] `.agent/GUARDRAILS.md` adhered to (no data additions, no unauthorized network calls)
