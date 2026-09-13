## Summary

This PR implements **Phase 9: README & Community Files** from the Good Portfolio Version implementation plan.

## Changes
- **`README.md`**: Complete rewrite including:
  - CI status badge.
  - Quickstart with fast Pasilla fixture analysis.
  - Multi-dataset benchmark table (Airway, Pasilla, Bottomly) with research questions and configurations.
  - Strict input specification for `counts.csv` and `metadata.csv` with explicit format constraints and examples.
  - Complete output breakdown for all 9 analysis files (HTML report, CSVs, and PNG figures).
  - Statistical methodology overview covering negative binomial GLMs, median-of-ratios normalization, Wald testing, and Benjamini-Hochberg FDR correction.
  - Explicit scientific limitations and academic citations (PyDESeq2, DESeq2, and datasets).
- **Issue Templates**:
  - `.github/ISSUE_TEMPLATE/bug_report.md`: Structured template for bug reporting with environment metadata.
  - `.github/ISSUE_TEMPLATE/feature_request.md`: Structured template for new features with mission and scope checks.
- **`CODE_OF_CONDUCT.md`**: Standard Contributor Covenant v2.1.
- **`docs/WALKTHROUGH.md`**: Self-contained step-by-step tutorial guiding a user through running the Pasilla demo analysis and inspecting generated outputs.
- **`docs/VALIDATION.md`**: Validation report providing multi-dataset schema consistency evidence across Airway, Pasilla, and Bottomly.
- **`CONTRIBUTING.md`**: Updated from the planning phase to reflect current codebase status, referencing the code of conduct, issue templates, and test workflows.

## Test evidence
- `uv run ruff check .` passes with zero issues.
- `uv run mypy src/` passes with zero type errors.
- `uv run pytest` passes.

## Definition of Done
- [x] All acceptance criteria met, no silent scope reduction.
- [x] All required documentation and community files created and linked.
- [x] No code changes (documentation only).
