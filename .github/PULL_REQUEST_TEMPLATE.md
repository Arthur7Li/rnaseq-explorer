## Summary

What changed and why. Reference the roadmap item / task spec this addresses.

## Milestone

MVP / Good Portfolio / Outstanding — specific `docs/ROADMAP.md` checklist item.

## Changes

- 
- 

## Test evidence

- `uv run pytest` output summary:
- `uv run ruff check .` output summary:
- Manual verification steps performed (if any):

## Definition of Done

Confirm each is true (see `.agent/DEFINITION_OF_DONE.md` for full detail):

- [ ] All acceptance criteria met, no silent scope reduction
- [ ] Tests added/updated, including failure-path tests for new validation rules
- [ ] No normalized values treated as raw counts anywhere in this change
- [ ] No diagnostic/causal/clinical language introduced
- [ ] Any new dependency is pinned with a stated reason
- [ ] Any statistical/design/dataset change is logged in `docs/DECISIONS.md`
- [ ] `.agent/GUARDRAILS.md` reviewed; none violated
- [ ] Docs updated if user-facing behavior changed

## Deviations from plan

Note anything that changed from the original task spec, and why.

## Decision log entries added

Link any new `docs/DECISIONS.md` entries created for this change, or write "None."
