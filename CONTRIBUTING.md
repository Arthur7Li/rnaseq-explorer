# Contributing to RNA-seq Explorer

Thank you for your interest in contributing to RNA-seq Explorer! We welcome contributions that align with our mission of providing reproducible, transparent, and configuration-driven bulk RNA-seq exploratory analysis for research and education.

## Community Standards

All contributors and participants are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before participating in our issues, discussions, or pull requests.

## Issues and Feature Requests

Before opening a pull request, please search existing issues or open a new one to discuss your proposed changes:
- **Bug Reports**: Use our [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md) and include minimal reproducible configs and logs.
- **Feature Requests**: Use our [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md) and ensure your suggestion aligns with the project's non-clinical, hypothesis-generating scope.

## Principles

1. **Exploratory & Non-Clinical Framing**: Never introduce clinical, diagnostic, or causal claims into code, documentation, or generated outputs.
2. **Data Integrity & Provenance**: Never commit raw sequencing data (FASTQ/BAM) or patient-identifiable datasets. Any new test fixtures must include complete `PROVENANCE.md` logs and SHA-256 hashes.
3. **Reproducibility**: All statistical workflows must be deterministically configurable with pinned random seeds and logged environment manifests.
4. **No Silent Coercion**: Reject malformed inputs with explicit, informative errors rather than silently coercing types.
5. **Rigorous Testing**: Every feature must include automated unit and/or integration tests maintaining high test coverage.

## Development Workflow

1. Clone the repository and install dependencies with `uv`:
   ```bash
   git clone https://github.com/Arthur7Li/rnaseq-explorer.git
   cd rnaseq-explorer
   uv sync --dev
   ```

2. Create a feature branch:
   ```bash
   git checkout -b feat/your-feature-name
   ```

3. Run linting, type-checking, and tests:
   ```bash
   uv run ruff check .
   uv run mypy src/
   uv run pytest --cov=rnax --cov-report=term-missing
   ```

4. If using AI coding agents (Antigravity, Cursor, Copilot, etc.), adhere strictly to the operational guardrails in `AGENTS.md` and `.agent/GUARDRAILS.md`.

## Pull Request Checklist

Before submitting your pull request:
- [ ] All tests pass locally (`uv run pytest`).
- [ ] Code is formatted and lint-clean (`uv run ruff check .`).
- [ ] Type annotations pass static analysis (`uv run mypy src/`).
- [ ] New functionality includes corresponding unit and/or integration tests.
- [ ] Documentation and example configs (`config/analysis.example.yaml`) are updated.
- [ ] No private, proprietary, or clinical data files are committed.
- [ ] Scientific claims remain hypothesis-generating and non-clinical.
