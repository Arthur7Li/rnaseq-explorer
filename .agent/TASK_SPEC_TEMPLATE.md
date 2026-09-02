# Task Spec Template

Use this structure at the start of every task, in Step 1 of `.agent/WORKFLOW.md`. Fill in every section; do not skip one because it seems obvious.

```markdown
## Task

One or two sentences describing the goal.

## Milestone

MVP / Good Portfolio / Outstanding — and the specific roadmap checklist item this maps to.

## Acceptance criteria

- Criterion 1 (copied or closely paraphrased from the roadmap/spec, not weakened)
- Criterion 2
- Criterion 3

## Files expected to change

- path/to/file_a.py — what changes and why
- path/to/file_b.py — what changes and why
- tests/test_file_a.py — new/updated tests

## Dependencies and prerequisites

- Any other task that must land first
- Any new library dependency, with justification

## Explicitly out of scope

- Things that might seem related but are deferred to a later milestone

## Risk and unknowns

- Anything uncertain that might require a checkpoint mid-task

## Test plan

- Unit tests: what will be covered
- Integration/smoke tests: what will be covered
- Manual verification steps, if any
```
