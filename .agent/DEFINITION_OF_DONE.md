# Definition of Done

A task is not complete until every applicable item below is true. "It runs on my machine once" is not done. "The chart renders" is not done. Check every box honestly; do not mark something done that you have not verified.

## Correctness

- [ ] The implementation satisfies every acceptance criterion stated in the task spec, with no silent scope reduction.
- [ ] Edge cases are handled: empty input, single sample, mismatched IDs, duplicate IDs, missing values, non-integer/negative counts, and unsupported design.
- [ ] All new or changed behavior is covered by automated tests, including at least one failure-path test per new validation rule.
- [ ] `uv run pytest` passes locally with no skipped tests unless explicitly justified in the PR description.

## Reproducibility

- [ ] Any new dependency is pinned in the lockfile with a stated reason.
- [ ] Any non-deterministic step uses a fixed, documented seed.
- [ ] The feature runs successfully from a clean environment using only documented commands.
- [ ] Generated outputs (reports, figures, tables) record input identifiers, configuration, code version, and library versions.

## Scientific and data integrity

- [ ] No normalized value (TPM/FPKM/RPKM/CPM/log-transformed/precomputed fold change) is treated as a raw count.
- [ ] No result, figure, or report uses diagnostic, causal, or clinical language.
- [ ] Any change to statistical methodology or supported design has a corresponding `docs/DECISIONS.md` entry and explicit approval.
- [ ] Any change under `data/**` has a complete, checked `PROVENANCE.md`.

## Code quality

- [ ] `uv run ruff check .` passes with no new warnings introduced.
- [ ] Public functions have type hints and docstrings describing inputs, outputs, and failure modes.
- [ ] No dead code, commented-out blocks, or leftover debug prints.
- [ ] Error messages are specific and actionable, not generic exceptions.

## Process

- [ ] Changes are on a feature branch, not committed directly to `main`.
- [ ] The commit/PR is scoped to one task; unrelated changes are not bundled in.
- [ ] The PR description explains what changed, why, and how it was verified.
- [ ] `.agent/GUARDRAILS.md` has been checked and none were violated.
- [ ] Any deviation from the original plan is called out explicitly, not buried in the diff.

## Documentation

- [ ] README/docs are updated if user-facing behavior changed.
- [ ] The roadmap checklist item (if any) is marked complete only after a human confirms the above.
