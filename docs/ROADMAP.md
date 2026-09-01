# Target Plan and Quality Gates

This plan defines the release levels. Do not advance a level because features exist; advance only when that level's acceptance criteria are demonstrated on a clean environment and documented.

## Delivery model

| Level | Purpose | Estimated focused effort | Outcome |
|---|---|---:|---|
| MVP | Prove one trustworthy vertical slice | 10–18 hours | Demo analysis runs end-to-end |
| Good portfolio version | Demonstrate reliable research software | 35–55 hours total | Reusable, tested, documented repository |
| Outstanding version | Demonstrate mature engineering and scientific judgment | 60–80 hours total | Shareable tool with strong reproducibility and extension path |

Time estimates assume focused work and AI-assisted implementation, but include time for you to understand, test, debug, and explain every decision. AI output is not evidence of completion.

## MVP: one complete vertical slice

### Goal

Take one small, permitted bulk RNA-seq demo dataset with two conditions from input files to a static report. Establish the contract before adding features.

### Required capabilities

- `counts.csv` and `metadata.csv` input contract documented with example files
- CLI command that validates inputs and exits non-zero with useful errors
- Validation for matching sample IDs, duplicates, missing condition labels, negative/non-integer counts, and insufficient replicates
- Config file containing condition column, reference group, comparison group, output path, and fixed random seed where applicable
- Basic QC: library-size plot and PCA or a clearly documented equivalent
- One documented differential-expression backend producing gene ID, base mean, log2 fold change, p-value, and adjusted p-value
- Volcano plot and CSV results table
- Static HTML or Markdown report that records input names, config, method, key outputs, and limitations
- README quickstart that works from a clean clone

### MVP acceptance checklist

- [ ] A user can run one documented command on demo data.
- [ ] Invalid sample IDs produce a readable error, not a misleading report.
- [ ] The report names the comparison direction unambiguously.
- [ ] Results include adjusted p-values and do not call exploratory hits validated biomarkers.
- [ ] The demo is reproducible in a newly created environment.
- [ ] At least 8 automated tests pass locally.
- [ ] You can explain each figure and each output-column meaning without AI assistance.

### MVP deliberately excludes

Pathway enrichment, batch covariates, Docker, a web UI, raw-read processing, multiple contrasts, and model selection. Record ideas as issues; do not expand scope.

## Good portfolio version: reliable and reviewable

### Goal

Turn the vertical slice into a clean, reusable portfolio project that demonstrates thoughtful data engineering, statistical boundaries, reproducibility, and software craftsmanship.

### Required capabilities

- All MVP requirements maintained
- Typed, modular source structure separating CLI, validation, analysis, plotting, report generation, and I/O
- Formal input schema and a complete example config
- Optional batch covariate in the supported design, with validation and clear report wording
- Low-count filtering rules documented and logged
- Sample-distance heatmap or hierarchical clustering alongside PCA
- MA plot and top-gene heatmap
- FDR threshold and fold-change threshold configurable, with defaults and caveats documented
- Dataset provenance document: source, accession/identifier, retrieval date, terms/license, preprocessing status, and sample mapping
- Reproducibility manifest recording package versions, Python/R version, platform, config hash, input hashes, and command
- Unit tests for validation, configuration, output schema, and at least one deterministic integration test
- GitHub Actions CI running linting, tests, and a demo smoke test on pushes/pull requests
- Dependency lockfile or pinned environment; no secret or large raw data committed
- Clear issue templates, contribution guidance, code of conduct or contributor expectations, and license selection
- A 2–3 minute demo asset or concise walkthrough in docs

### Good-version acceptance checklist

- [ ] CI is green from a fresh clone and runs without private credentials.
- [ ] A malformed count file, malformed metadata file, and bad config each fail safely with tested messages.
- [ ] A reviewer can trace every report number to an input file, configuration setting, and code version.
- [ ] The report distinguishes QC observations from biological conclusions.
- [ ] Two demo datasets or two planned contrasts run successfully, including one expected-warning case.
- [ ] Code coverage is measured; critical validation/reporting paths are covered.
- [ ] README includes install, quickstart, input specification, outputs, methodology, limitations, and citation/data attribution.
- [ ] You can defend the scope choice: count-matrix analysis rather than raw FASTQ processing.

## Outstanding version: reproducible research tool

### Goal

Make the project strong enough that a research-minded reviewer sees a credible foundation for continued open-source development—not merely an attractive demo.

### Required capabilities

- All Good portfolio requirements maintained
- Containerized execution using Docker or equivalent, plus a documented non-container route
- Workflow orchestration through a lightweight, documented system such as Snakemake or a rigorously tested internal runner
- Multiple planned contrasts and explicit design-matrix validation
- Optional gene annotation layer and pathway/enrichment module that clearly separates database-derived annotations from statistical results
- Report sections for data provenance, QC, model specification, results, parameter sensitivity, limitations, and rerun instructions
- Parameter-sensitivity comparison for at least one reasonable filtering/threshold setting; report whether high-level conclusions are stable
- Golden-file or snapshot testing for report outputs, with stable deterministic fixtures
- Performance benchmark on several synthetic input sizes and documented resource expectations
- Release process: semantic versioning, changelog, release notes, archived example output, and `CITATION.cff`
- Security/data-handling review: no restricted data, no sensitive data in logs, dependency scanning, and secret scan in CI
- Accessibility and usability review of plots and report, including colorblind-safe palette and readable labels
- External feedback from at least one biology-aware user, recorded as issues or a short feedback note with resulting changes

### Outstanding acceptance checklist

- [ ] A clean container run recreates the documented demo report.
- [ ] Reproducibility metadata is sufficient for a reviewer to identify exact inputs, environment, config, and release.
- [ ] Workflow failure points have helpful messages and tested recovery guidance.
- [ ] Benchmark and quality results are visible in the repository rather than claimed only in prose.
- [ ] At least one external user has followed the quickstart and supplied feedback.
- [ ] A tagged release can be installed/run using release documentation.
- [ ] Every claim in the README stays within exploratory, non-clinical scope.

## Build sequence

1. Select demo dataset and write `docs/DATA_POLICY.md` before building analysis code.
2. Freeze the MVP input/output contract.
3. Implement validation tests first.
4. Implement the vertical slice on demo data.
5. Generate the report and verify every value manually against intermediate outputs.
6. Add CI and fresh-environment reproduction test.
7. Perform a structured code, methods, and README audit.
8. Only then add Good-version features; revisit scope after every milestone.

## Continuous verification questions

At every pull request or milestone, answer:

- Does this change preserve the raw-count and two-condition assumptions, or document an intentional extension?
- Can an invalid input create a plausible-looking result? If yes, add validation or stop.
- Is the output traceable to a versioned input and config?
- Are we separating result generation from biological/clinical interpretation?
- Does a fresh clone still run the demo?
- Is every generated line of code understood, tested, and maintainable by the author?

## Definition of done

A feature is done only when implementation, tests, error behavior, documentation, and report representation are complete. A chart is not done merely because it renders; it must have a title, labeled axes, sensible scaling, deterministic test coverage or fixture verification, and an explanation of what it can and cannot imply.
