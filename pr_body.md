## Summary

This PR executes **Phase 6: Bottomly Validation Dataset** from the Good Portfolio Version implementation plan.

## Changes
- **`scripts/acquire_bottomly.py`**: Added a pure-Python script that downloads the ReCount dataset (mouse striatum RNA-seq) and subsets it down to 10 samples (5 `C57BL_6J` and 5 `DBA_2J`) to serve as a fast validation fixture. Computes SHA-256 checksums automatically.
- **`data/bottomly/*`**: Created the dataset containing `counts.csv` and `metadata.csv`.
- **`data/bottomly/PROVENANCE.md`**: Wrote provenance documentation tracking the ReCount source, Bottomly et al. citation, and dataset checksums in strict compliance with the data policy.
- **`config/bottomly.yaml`**: Created the analysis configuration file for the Bottomly dataset (strain effect: C57BL/6J vs DBA/2J).
- **`tests/test_integration.py`**: Appended a new integration test (`test_bottomly_integration`) that executes the `rnax analyze` CLI pipeline on the Bottomly dataset to ensure the tool successfully handles mouse gene ID spaces and this specific data format end-to-end.

## Test evidence
- `uv run pytest tests/test_integration.py` runs both Pasilla and Bottomly end-to-end pipelines successfully.
- `uv run pytest` runs and passes all tests without errors.
- `uv run mypy src/` passes cleanly.
- `uv run ruff check .` passes with zero errors.

## Definition of Done
- [x] All acceptance criteria met, no silent scope reduction
- [x] Integration tests for Bottomly dataset added
- [x] `.agent/GUARDRAILS.md` reviewed; explicit human review checkpoint completed for `data/` commits.
