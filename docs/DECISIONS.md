# Decision Log

This is an append-only record of decisions that changed scope, architecture, dependencies, statistical methodology, or supported datasets. Never edit or delete a past entry; if a decision is later reversed, add a new entry that supersedes it and links back to the original.

Every entry uses this template:

```markdown
## D-<number>: <short title>

- Date: YYYY-MM-DD
- Status: proposed | accepted | superseded by D-<number>
- Context: why this decision was needed
- Decision: what was decided, stated precisely
- Alternatives considered: brief list with why they were not chosen
- Consequences: what this enables, what it constrains, what follow-up work it creates
```

---

## D-1: Adopt a formal agentic development harness

- Date: 2026-09-01
- Status: accepted
- Context: Implementation work is about to begin with an AI coding agent (Antigravity / Gemini 3.1 Pro High). The project needs enforceable guardrails, a repeatable workflow, and a decision-accountability trail before any application code is written.
- Decision: Add `AGENTS.md`, `.agent/GUARDRAILS.md`, `.agent/WORKFLOW.md`, `.agent/DEFINITION_OF_DONE.md`, `.agent/TASK_SPEC_TEMPLATE.md`, `.agent/ESCALATION.md`, and this decision log as the mandatory operating framework for all future agent-driven changes.
- Alternatives considered: rely on ad hoc chat instructions per session (rejected — not durable or discoverable by the agent); rely on PR review alone without upfront guardrails (rejected — too late to prevent scope drift and unsafe data handling).
- Consequences: All future tasks must follow `.agent/WORKFLOW.md` and satisfy `.agent/DEFINITION_OF_DONE.md`. Any architecture or methodology change must be logged here before or alongside implementation.

## D-2: MVP supports exactly one blocking covariate

- Date: 2026-09-01
- Status: accepted
- Context: The Airway MVP dataset has a paired design (four cell lines, each with an untreated and a dexamethasone-treated sample). The prior roadmap language ("MVP excludes batch covariates") was ambiguous and conflicted with the need to model `cell_line` alongside `treatment`.
- Decision: The MVP officially supports exactly one blocking covariate in addition to the primary two-level treatment factor, expressed for Airway as `expression ~ cell_line + treatment`. This is not general-purpose technical batch correction; arbitrary multiple covariates, interaction terms, and user-authored formulas remain out of scope for the MVP.
- Alternatives considered: model `treatment` alone (rejected — ignores known paired structure and risks confounding cell-line baseline differences with treatment effect); support arbitrary covariate lists immediately (rejected — expands MVP scope prematurely).
- Consequences: Input validation must confirm the blocking column exists, is categorical, has no missing values, and is not perfectly confounded with treatment. `docs/ROADMAP.md` and `config/airway.yaml` should be read together with this entry.

## D-3: Use PyDESeq2 as the MVP differential-expression backend

- Date: 2026-09-01
- Status: accepted
- Context: The project needs a statistically credible engine for bulk RNA-seq differential expression that also integrates cleanly into a Python-first, testable, cross-platform (Windows 11 / macOS Apple Silicon) codebase.
- Decision: Use PyDESeq2, a Python implementation of the DESeq2 method, as the MVP backend. Do not use `rpy2` or a live R dependency for the MVP.
- Alternatives considered: R + DESeq2 invoked via `rpy2` (rejected for MVP — fragile cross-language dependency, harder CI and cross-platform setup); a from-scratch naive statistical test (rejected — not scientifically defensible as the core DE engine); a separate R CLI subprocess (deferred — possible future reference-validation backend, not the MVP default).
- Consequences: Pin the exact PyDESeq2 version in the lockfile. Keep the backend behind a small internal interface so a future R/DESeq2 reference backend remains possible. Add a validation milestone comparing high-level Airway output against a recognized DESeq2/Airway reference workflow before claiming scientific parity.

## D-4: Use uv as the dependency and project manager

- Date: 2026-09-01
- Status: accepted
- Context: The project needs a fast, reproducible, lockfile-based Python project workflow suitable for a solo developer working across Windows 11 and macOS Apple Silicon.
- Decision: Use `uv` with standard PEP 621 metadata in `pyproject.toml` and a committed `uv.lock`.
- Alternatives considered: Poetry (viable but heavier for a new solo project); plain pip/venv (rejected — weaker reproducibility guarantees).
- Consequences: Document `uv sync`, `uv run pytest`, `uv run ruff check .`, and the CLI entry point in the README/quickstart once the package skeleton exists.

## D-5: Use a static HTML report (Jinja2) as the official MVP report format

- Date: 2026-09-01
- Status: accepted
- Context: The MVP needs one official, reviewable, shareable output artifact for non-technical and technical reviewers alike.
- Decision: Generate a self-contained, browser-openable static HTML report via Jinja2 as the official MVP deliverable, alongside machine-readable CSV/JSON outputs. Markdown may be used for developer/debug output but is not the official report format.
- Alternatives considered: rendered Markdown only (rejected as the primary format — weaker presentation for figures/tables); an interactive web dashboard (rejected for MVP — unnecessary complexity and scope creep).
- Consequences: The report must include provenance references, the design model and contrast, validation summary, QC figures with plain-language observations, DE results, a reproducibility manifest, and explicit limitations.

## D-6: Add top_n_genes config parameter

- Date: 2026-09-10
- Status: accepted
- Context: The top DE genes heatmap requires a configurable parameter for how many genes to display.
- Decision: Add `top_n_genes` as a new optional field in `ThresholdsConfig` with a default of 30.
- Alternatives considered: Hardcoding 30 (rejected — reduces user flexibility for different datasets).
- Consequences: Allows the top genes heatmap to be generated dynamically based on user preference while maintaining a sensible default.


## D-7: Add dataset_limitations config field

- Date: 2026-09-13
- Status: accepted
- Context: Different biological datasets possess unique scientific constraints, experimental caveats, and biological limitations (e.g. cell-line generalization, mouse strain mapping bias, or sample size limits) that must be communicated alongside generic tool limitations.
- Decision: Add `dataset_limitations: list[str] = Field(default_factory=list)` to `AnalysisConfig`. Render these dynamically as a dedicated section in the HTML report when provided.
- Alternatives considered: hardcoding dataset caveats in the Jinja2 template (rejected — violates separation of concerns and breaks generality for custom user datasets); omitting dataset-specific caveats (rejected — violates scientific integrity and transparency principles).
- Consequences: Each dataset configuration YAML can declare tailored scientific limitations that appear directly in the output report, keeping the core codebase generic while ensuring strict biological integrity.

## D-8: Adopt Wong (2011) colorblind-safe palette as standard plot color scheme

- Date: 2026-09-29
- Status: accepted
- Context: Scientific figures must be accessible to readers with color-vision deficiencies (CVD). The initial volcano and MA plots used red and blue (#e41a1c, #377eb8), which can be ambiguous under protanopia or deuteranopia and lacked secondary encoding channels.
- Decision: Adopt the Wong (2011) colorblind-safe palette (`#D55E00` vermillion for upregulated, `#0072B2` blue for downregulated, `#999999` gray for non-significant) across all pipeline plots. Implement point-shape differentiation (triangles vs inverted triangles vs circles) as a secondary encoding channel. Use minimum 12pt axis labels and 14pt titles via `matplotlib.rc_context`. Provide descriptive `alt` text for all HTML report images.
- Alternatives considered: Using default matplotlib/seaborn palettes (rejected — not guaranteed colorblind-safe); Viridis/Cividis continuous colormaps for discrete categories (rejected — harder to interpret for binary significance states).
- Consequences: All visualization outputs adhere to accessibility guidelines without compromising visual clarity. HTML reports are screen-reader accessible.

## D-9: Support multiple planned contrasts via optional `contrasts` config field

- Date: 2026-09-29
- Status: accepted
- Context: Researchers often need to compare multiple groups (e.g. A vs B, A vs C) within a single dataset. Running separate configuration files and pipelines is tedious and breaks the cohesiveness of the report. The design matrix also requires validation to ensure the model is computationally feasible and biologically sound.
- Decision: Add an optional `contrasts` list to `AnalysisConfig`. When provided, the CLI loops over the contrasts, running `DeseqStats` for each and outputting distinct subdirectories and an `index.html`. Add rigorous design matrix validation to check for confounding variables and minimum replicate counts. The single-contrast `design` block remains the fallback for backward compatibility.
- Alternatives considered: Using interaction terms (rejected — too complex for a standard automated pipeline); requiring users to write custom Python scripts (rejected — reduces reproducibility and accessibility).
- Consequences: The tool can now naturally support complex multi-group experimental designs while keeping the configuration simple. Backward compatibility is strictly maintained.

### D-10: Optional Gene Annotation and Pathway Enrichment Module
**Date:** 2026-09-30
**Context:** Biological interpretation of DE results requires gene symbols and pathway over-representation analysis (ORA). However, external network calls during analysis break reproducibility and air-gapped usability.
**Decision:** We implemented an optional annotation/enrichment module that relies entirely on locally bundled CSVs (for annotations) and local GMT files (for enrichment) via `gseapy`. All network retrieval logic is confined to an offline setup script (`scripts/fetch_annotations.py`).
**Consequences:** The analysis remains strictly reproducible without runtime network dependencies. Enrichment results are heavily caveated as exploratory. The project bundle size increases slightly to accommodate small annotation CSVs.

### D-11: Parameter Sensitivity Analysis Module
**Date:** 2026-09-30
**Context:** Users often struggle with arbitrary threshold selection (e.g., FDR=0.05 vs 0.1) and whether their core conclusions hold under alternate criteria.
**Decision:** We implemented a post-hoc parameter sensitivity analysis module that evaluates a matrix of FDR and Absolute log2FoldChange thresholds on the primary pipeline results. It outputs a summary matrix and a Stability Verdict ("Stable" or "Sensitive") based on whether the number of significant genes fluctuates dramatically.
**Consequences:** The analysis offers immediate visual confidence in the findings without recalculating the expensive PyDESeq2 generalized linear model. The module sits fully outside the core statistical pathway, acting purely as an interpretive aid in the HTML report.

## [D-12] Snakemake Workflow Orchestration (Phase 5)
**Date:** 2026-10-01
**Context:** Power users need a way to run the RNA-seq analysis pipeline in a step-by-step manner with failure recovery, DAG orchestration, and intermediate file tracking.
**Decision:** We introduced Snakemake as an optional dependency (`rnax[workflow]`). We created a `workflow/Snakefile` that leverages the existing PyDESeq2 pipeline functions (`ingest_data`, `run_deseq2`, `generate_plots`, etc.) using Snakemake's native Python `run:` directive.
**Rationale:** 
- Instead of relying on a monolithic CLI command, decomposing the pipeline into explicit rules (`validate`, `deseq2`, `plots`, `sensitivity`, `annotate`, `report`) allows step-wise resumption and avoids completely re-running the DESeq2 model if plotting or reporting fails.
- We opted to serialize intermediate pandas DataFrames as pickles (`.pkl`) rather than Parquet to avoid introducing a mandatory dependency on `pyarrow` or `fastparquet` for workflow users. 
- We refactored `report.py` to decouple plotting logic from HTML rendering, facilitating independent rules in Snakemake without disrupting the existing `rnax analyze` CLI behavior.
**Consequences:** The CLI retains its simple one-shot `rnax analyze` execution flow, while advanced execution scenarios are fully supported by `snakemake -s workflow/Snakefile --config rnax_config=...`.

## [D-13] Containerize with Docker (Phase 6)
**Date:** 2026-10-03
**Context:** Need to ensure reproducibility of the execution environment across different operating systems.
**Decision:** We containerized the RNA-seq Explorer via a `python:3.12-slim` multi-stage build `Dockerfile` and provided a `docker-compose.yml` file. We used `uv` in the builder stage for fast dependency resolution.
**Rationale:** A multi-stage build minimizes the final image size and attack surface. Keeping the native execution path supported means developers or users without Docker can still run the tool easily via `uv run`. 
**Consequences:** Users can choose to run `rnax` via `uv run` natively, or `docker compose run` via Docker, yielding identical analysis results.

## [D-14] Golden-File / Snapshot Testing (Phase 7)
**Date:** 2026-10-03
**Context:** Need a fast, reliable way to prevent unintended regressions in the structure and schemas of our pipeline outputs without hardcoding fragile assertions.
**Decision:** We adopted `pytest-snapshot` for golden-file testing of pipeline artifacts (specifically `results.csv` schema, `normalized_counts.csv` shape, and `report.html` section headings).
**Rationale:** Standard assertions for large text files or data schemas become verbose and difficult to maintain. By utilizing a fixed random seed within our `AnalysisConfig` during testing, we ensure that PyDESeq2 produces entirely deterministic outputs. Snapshot testing allows us to trivially capture these outputs and bump them easily (`--snapshot-update`) when intentional changes are made.
**Consequences:** Developers must run `pytest --snapshot-update` when making intentional changes that alter pipeline output schemas or report structure, and verify the resulting file diffs in version control.

## [D-15] GEO Case Study Selection (Phase 12)
**Date:** 2026-10-03
**Context:** The "Outstanding" portfolio milestone mandates incorporating a curated, real-world case study from the NCBI Gene Expression Omnibus (GEO) to demonstrate public data hygiene and responsible interpretation.
**Decision:** We selected **GSE324987** (Zebrafish neurexin double mutants).
**Rationale:** This dataset perfectly meets all 8 selection criteria and triggers zero rejection criteria. It provides pristine, raw integer count tables in the supplementary files, preventing us from needing to perform costly FASTQ alignments. It has exactly 3 replicates per biological group, explicitly clear metadata matching column names, and a stable PMID (42362769). Most importantly, as an animal-model study using whole-brain tissue, it naturally invites discussion of meaningful scientific caveats (e.g., bulk tissue masking cell-type specific signals) without ever risking prohibited clinical or diagnostic language.
**Considered but Rejected:**
- GSE188391 (Mouse Melanoma): Rejected due to mismatch between the sample IDs in the provided counts table and the GEO metadata.
- GSE319384 (Human Pancreatic Cancer PANC-1): Rejected because the study remains unpublished (missing PMID) despite having a clean counts matrix.
