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
