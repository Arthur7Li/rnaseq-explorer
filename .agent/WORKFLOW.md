# Required Agent Workflow

Every task, regardless of size, follows this loop. Do not skip steps to move faster. Skipping steps is the primary cause of scope drift, broken reproducibility, and unreviewable pull requests.

## Step 0 — Orient

Read `AGENTS.md`, `.agent/GUARDRAILS.md`, the relevant section of `docs/ROADMAP.md`, and any file the task explicitly references. State, in your own words, which milestone (MVP / Good Portfolio / Outstanding) this task belongs to.

## Step 1 — Restate the task

Before writing any code, restate:

- The goal, in one or two sentences
- The exact acceptance criteria (copy them from the roadmap/task spec; do not paraphrase away specifics)
- Files you expect to create or modify
- Tests you expect to add or update
- Anything explicitly out of scope for this task

Use `.agent/TASK_SPEC_TEMPLATE.md` as the structure.

## Step 2 — Checkpoint (required for anything non-trivial)

A change is non-trivial if it does any of the following: adds a dependency, changes a public function signature, changes validation behavior, changes statistical methodology, touches `data/**`, touches CI, or spans more than roughly 150 changed lines.

For non-trivial changes, stop after Step 1 and present the plan for human approval before writing implementation code. For trivial changes (typo fixes, docstrings, comments, adding a single obvious test), you may proceed directly to Step 3.

## Step 3 — Branch

Create a feature branch named `type/short-description`, for example `feat/count-matrix-validation` or `fix/pca-nan-handling`. Never work directly on `main`.

## Step 4 — Implement

- Write the smallest correct implementation that satisfies the acceptance criteria.
- Write tests alongside or before the implementation, not after everything else is "working."
- Add docstrings/comments only where they clarify non-obvious reasoning; do not narrate obvious code.
- Prefer explicit errors over silent fallbacks.
- If you discover the task is larger or riskier than expected, stop and return to Step 2 rather than expanding scope silently.

## Step 5 — Verify locally

Run, and report the output of:

```bash
uv run pytest
uv run ruff check .
uv run mypy src/ # once type checking is configured
```

All tests must pass. Do not report success without having actually executed the commands. If a test is flaky or skipped, say so explicitly and explain why.

## Step 6 — Self-review against Definition of Done

Walk through `.agent/DEFINITION_OF_DONE.md` line by line before proposing the pull request. Do not proceed if any item is unmet; either finish it or explicitly flag it as a follow-up task with a reason.

## Step 7 — Summarize and request review

Open a pull request (or present the diff, if the tool cannot open one) containing:

- What changed and why, referencing the task/roadmap item
- Files changed, grouped logically
- Test results
- Any deviations from the original plan, and why
- Any new entries added to `docs/DECISIONS.md`
- Explicit confirmation that `.agent/GUARDRAILS.md` was not violated

Do not merge. A human reviews and merges.

## Step 8 — Wait

After requesting review, wait for feedback before starting the next task. Do not chain unrelated work into the same branch while waiting.
