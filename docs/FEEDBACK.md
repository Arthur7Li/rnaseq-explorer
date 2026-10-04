# External User Feedback

This document serves as the central log and standard procedure for collecting feedback from external beta-testers (specifically users with a background in molecular biology or bioinformatics).

## Standard Feedback Protocol

When soliciting feedback, we ask the tester to perform the following independently:
1. Clone the repository and follow the Quickstart installation.
2. Run the pipeline locally on the provided demo dataset (`uv run rnax analyze --config config/pasilla.yaml`).
3. Open and interpret the generated `results/pasilla/report.html` and accompanying CSVs.
4. File a formalized feedback issue using our predefined template.

## The Feedback Framework

All formal feedback should cover:
- **Setup Experience:** Time required, dependency blockers, OS quirks.
- **Quickstart Followability:** Clarity of the `README.md`, confusing CLI steps.
- **Output Clarity & Usefulness:** Readability of the HTML report, plotting legibility, CSV schema usefulness.
- **Biological / Statistical Concerns:** Validity of claims, missing crucial covariates, edge-case methodology issues.

---

> **TODO:** Share the repository with a biology-aware colleague. Ask them to clone, install, run `config/pasilla.yaml`, review the HTML report, and file feedback using the `External User Feedback` issue template in GitHub.

## Recorded Feedback Sessions

*(No feedback sessions recorded yet.)*
