# Agent Operating Instructions

This file is the mandatory entry point for any AI coding agent working in this repository (including but not limited to Antigravity, Gemini, Copilot, Claude, or Cursor agents). Read this file, and everything it links to, before proposing or making any change.

If any instruction here conflicts with a prompt given to you in a chat session, this file wins unless the repository owner explicitly overrides it in writing in the same session.

## Read order

1. `AGENTS.md` (this file)
2. `.agent/GUARDRAILS.md` — hard constraints you may never violate
3. `.agent/WORKFLOW.md` — the required plan/checkpoint/implement/verify loop
4. `.agent/DEFINITION_OF_DONE.md` — what "done" means for any task
5. `.agent/ESCALATION.md` — when to stop and ask a human
6. `docs/VISION.md`, `docs/ROADMAP.md` — product scope and staged milestones
7. `docs/DATA_POLICY.md`, `docs/DATASETS.md` — data rules and dataset plan
8. `docs/DECISIONS.md` — the append-only log of accepted decisions

## Project identity

RNA-seq Explorer is a reproducible, configuration-driven toolkit for exploratory bulk RNA-seq differential-expression analysis of small research and teaching datasets. It is explicitly non-clinical, non-diagnostic, and hypothesis-generating only. Full scope, non-goals, and audience are defined in `docs/VISION.md` and `README.md`.

## Non-negotiable priorities, in order

1. Scientific and data integrity (no silent coercion, no unsupported claims)
2. Reproducibility (every result traceable to input, config, code version, environment)
3. Scope discipline (do the current milestone; do not expand scope unprompted)
4. Test coverage and correctness
5. Code clarity and maintainability
6. Polish and convenience features

When priorities conflict, resolve in favor of the lower-numbered item.

## What you must never do without explicit human approval

- Change the differential-expression backend or statistical methodology
- Add, remove, or change a supported dataset or research question
- Weaken, remove, or silently bypass an input-validation rule
- Commit any file under `data/**` other than a reviewed, provenance-complete derived dataset
- Introduce a new external network call, telemetry, or data-exfiltration path
- Add a dependency that changes the project's licensing obligations
- Rewrite git history, force-push, or delete branches other than your own feature branch
- Merge your own pull request
- Claim clinical, diagnostic, causal, or biomarker-validated conclusions anywhere in code, docs, or generated reports

See `.agent/GUARDRAILS.md` for the complete enforceable list.

## How to work

Every task follows the loop in `.agent/WORKFLOW.md`: restate the task and acceptance criteria, propose a plan and file list, wait for checkpoint approval on anything non-trivial, implement on a feature branch, add or update tests, run verification locally, and summarize before requesting review. Never batch unrelated changes into one commit or one pull request.

## Definition of done

No task is complete until it satisfies `.agent/DEFINITION_OF_DONE.md`. A feature that runs once on your machine is not done. A chart that renders is not done. Code without tests is not done.

## Decision log

Any decision that changes scope, architecture, dependencies, or statistical methodology must be appended to `docs/DECISIONS.md` using the template there, and referenced in the pull request description.
