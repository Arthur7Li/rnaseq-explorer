## Summary

This PR executes **Phase 5: Pasilla Test Fixture Dataset** from the Good Portfolio Version implementation plan.

## Changes
- **`scripts/acquire_pasilla.py`**: Added a pure-Python script that downloads the Bioconductor pasilla package release tarball (v1.40.0), extracts the count and metadata files into memory, formats them into a clean CSV format, and writes them to the `data/pasilla` directory. It computes and logs the SHA-256 checksums of the extracted datasets.
- **`data/pasilla/*`**: Created the standard Pasilla fixture dataset containing `counts.csv` and `metadata.csv`.
- **`data/pasilla/PROVENANCE.md`**: Wrote full provenance documentation detailing the data source, mapping rules, dataset version, and checksums in strict compliance with the data policy.
- **`config/pasilla.yaml`**: Created the analysis configuration file for the pasilla dataset (unpaired experimental design: knockdown vs. control).
- **`tests/test_integration.py`**: Introduced a comprehensive end-to-end integration test that uses `typer.testing.CliRunner` to execute the full pipeline (`rnax analyze`) on the Pasilla dataset, validating the CLI exit code, the generation of output CSVs, PNG plots, and the full HTML report.

## Test evidence
- `uv run pytest tests/test_integration.py` executes successfully. The end-to-end pipeline completes in ~11 seconds.
- `uv run pytest` runs and passes all 37 tests.
- `uv run mypy src/` passes cleanly.
- `uv run ruff check .` passes with zero errors.

## Definition of Done
- [x] All acceptance criteria met, no silent scope reduction
- [x] Tests added/updated (Integration tests introduced!)
- [x] `.agent/GUARDRAILS.md` reviewed; explicit human review checkpoint completed for `data/` commits.
