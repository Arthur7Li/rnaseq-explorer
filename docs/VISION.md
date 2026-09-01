# Product Vision

## One-sentence vision

RNA-seq Explorer helps a student or researcher turn validated bulk RNA-seq counts and metadata into a reproducible, reviewable differential-expression report without pretending that exploratory results are clinical conclusions.

## Why this exists

A common downstream RNA-seq task begins with two files: a gene-by-sample count matrix and sample metadata. The technical task is deceptively simple, but trustworthy work requires more than a volcano plot. Users need checks that their inputs match, visibility into sample behavior, appropriate multiple-testing control, documented choices, and an artifact a collaborator can rerun.

The project therefore targets the gap between a one-off notebook and a production platform: a small, opinionated, inspectable workflow that teaches sound practice while remaining useful for real exploratory work.

## User promise

For supported inputs and designs, the tool will:

1. Reject or clearly flag invalid data rather than quietly continuing.
2. Explain each major analysis stage in plain language.
3. Preserve an audit trail: inputs, settings, versions, outputs, and timestamps.
4. Produce figures and tables suitable for review, not unqualified claims.
5. State limitations directly in the final report.

## Primary users and jobs

| User | Job to be done | Success looks like |
|---|---|---|
| Student | Learn how a defensible RNA-seq analysis is structured | Can rerun demo data, explain outputs, and modify a config safely |
| Research assistant | Create a consistent first-pass analysis | Can deliver a report and precise rerun instructions to a supervisor |
| Wet-lab collaborator | Inspect whether an experiment appears coherent | Can see sample QC, group separation, and candidate genes without reading code |
| Bioinformatics reviewer | Audit an exploratory result | Can find data provenance, assumptions, settings, and method limits quickly |
| Hiring manager | Evaluate research-software ability | Sees tests, CI, deliberate scope, clean docs, and responsible claims |

## Non-negotiable constraints

- Inputs are raw integer gene counts, not TPM/FPKM/percentages, for the initial differential-expression path.
- The tool is exploratory and non-clinical.
- No patient-identifiable or restricted data belongs in the repository.
- Every demo dataset needs documented source, license/terms, and a provenance note.
- Every released result report includes method and limitation text.
- An unsupported design must fail with an actionable explanation, not yield a plausible-looking answer.

## Measures of success

- A fresh user completes the demo from a clean environment using documented commands.
- Automated tests cover validation and report-generation critical paths.
- Two independently run demo analyses yield the same key outputs within documented version bounds.
- README gives an honest explanation of scope in under five minutes of reading.
- The author can explain normalization, PCA, log2 fold change, adjusted p-values, and the difference between association and causation.

## Explicit non-goals

This is not a universal genomics platform, a FASTQ-to-results workflow, an AI disease classifier, a clinical test, or a substitute for experimental validation. Feature requests that weaken reproducibility or claims discipline are out of scope.
