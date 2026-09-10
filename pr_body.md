## Summary

This PR executes **Phase 2: Reproducibility Manifest** from the Good Portfolio Version implementation plan.

## Changes
- **`manifest.py`**: Added a new module to calculate file hashes (SHA-256), retrieve the active git commit, detect OS/platform information, and dynamically check the installed versions of key bioinformatics libraries (`pydeseq2`, `pandas`, `scikit-learn`, etc.).
- **`cli.py`**: Intercepts the fully validated `config` at the start of the pipeline and calls `build_manifest()`.
- **`report.py` & `report.html.j2`**: Re-wires the reporting layer to accept the `ReproducibilityManifest` and injects it as a new structured table into the static HTML report.
- **Tests**: Created `test_manifest.py` to ensure `git` subprocesses fail gracefully when absent, and updated `test_report.py` to inject mock manifests.

## Test evidence
- `uv run pytest` runs and passes (31 tests).
- Mypy strictly validates the new `ReproducibilityManifest` typing and its passthrough.

## Definition of Done
- [x] All acceptance criteria met, no silent scope reduction
- [x] Tests added/updated
- [x] `.agent/GUARDRAILS.md` reviewed; none violated
