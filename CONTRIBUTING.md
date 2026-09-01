# Contributing

## Current status

RNA-seq Explorer is in the planning stage. Before opening a large pull request, open an issue describing the proposed use case, supported input contract, statistical assumptions, tests, and documentation impact.

## Principles

- Preserve exploratory, non-clinical framing.
- Do not commit patient-identifiable, restricted, or unclear-license data.
- Add or update tests for behavior changes.
- Keep production workflow code out of exploratory notebooks.
- Document changes to inputs, outputs, defaults, and statistical assumptions.
- Prefer explicit errors to silent data transformations.

## Pull-request checklist

- [ ] Tests pass locally.
- [ ] New behavior has tests, including failure behavior where relevant.
- [ ] Documentation and example configuration are updated.
- [ ] No credentials, tokens, or sensitive data are present.
- [ ] Claims remain hypothesis-generating and non-clinical.
- [ ] The author can explain and maintain the proposed implementation.
