## Summary

This PR executes **Phase 4: Filtering Transparency & Threshold Documentation** from the Good Portfolio Version implementation plan.

## Changes
- **`deseq.py`**:
  - Defined `FilteringResult` dataclass (`filtered_counts`, `genes_before`, `genes_after`, `min_count`, `min_samples`).
  - Added logging in `filter_low_counts` with exact gene retention and rule numbers.
  - Updated `run_deseq2` to return `(normalized_counts, results_df, filtering_result)`.
- **`report.py` & `report.html.j2`**:
  - Passed `FilteringResult` into `generate_report` and the Jinja2 template.
  - Added "Pre-filtering Summary" subsection under Quality Control detailing genes before, genes after, genes removed, and the exact threshold rule applied.
  - Added threshold caveat notice emphasizing that FDR and fold-change thresholds are conventional cutoffs, not biological truths, and that results require independent validation.
- **`cli.py`**: Updated differential expression execution to unpack `filtering` and pass it to `generate_report`.
- **`README.md`**: Added "Filtering Defaults & Customization" documentation explaining default rules and YAML configuration.
- **Tests**: Updated `test_deseq.py`, `test_cli.py`, and `test_report.py` to assert filtering metrics and check logging messages.

## Test evidence
- `uv run pytest` runs and passes (36 tests).
- `uv run mypy src/` passes cleanly.
- `uv run ruff check .` passes with zero errors.

## Definition of Done
- [x] All acceptance criteria met, no silent scope reduction
- [x] Tests added/updated
- [x] `.agent/GUARDRAILS.md` reviewed; none violated
