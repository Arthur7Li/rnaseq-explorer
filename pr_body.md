## Summary

This PR completes **Phase 8: Enhanced Report Content** from the implementation plan.

## Changes
- **`src/rnax/config.py`**: Added a new `dataset_limitations: list[str]` field to `AnalysisConfig`.
- **`config/*.yaml`**: Updated dataset configuration files (`airway`, `bottomly`, and example configs) with dataset-specific scientific caveats and limitations.
- **`src/rnax/templates/report.html.j2`**: Performed a major template redesign to properly contextualize the pipeline outputs. Added new sections in the following order:
  1. **Data Provenance**: Explicitly displays inputs and cryptographic SHA-256 hashes side-by-side with metadata.
  2. **QC Observations**: Restructured QC descriptions to emphasize observation rather than causation.
  3. **Methodology**: Detailed explanation of the underlying PyDESeq2 Negative Binomial GLM, median-of-ratios normalization, Wald test, and FDR correction. Included proper academic citations (Love et al. 2014).
  4. **Dataset-Specific Limitations**: Dynamically rendered bulleted list of limitations defined within the YAML config.
  5. **General Limitations**: Expanded to outline common bulk RNA-seq pitfalls, including count-based assumptions, sample size issues, and lack of causal inference.
  6. **How to Reproduce**: Integrated a direct, copy-pasteable CLI command and an inline reproducibility manifest dump.
- **`tests/test_report.py`**: Added assertions validating that all new template sections render successfully and test that the dataset limitations block disappears gracefully when empty.

## Test evidence
- `uv run pytest` (39 tests) all pass successfully, including the new unit tests.
- `uv run ruff check .` passes perfectly.
- `uv run mypy src/` reports zero type errors.

## Definition of Done
- [x] All acceptance criteria met, no silent scope reduction.
- [x] Template restructuring complete with updated scientific phrasing.
- [x] Tests fully updated and passing.
