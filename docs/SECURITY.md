# Security Policy

## Strict Offline & Privacy Guarantees
RNA-seq Explorer operates strictly on the host machine. The core analysis pipeline makes **zero network requests** at runtime. 
- There is no telemetry.
- There are no analytics.
- Your count matrices and sample metadata never leave your local environment.

*Note:* Optional gene set annotation acquisition scripts (`scripts/acquire_annotations.py`) make targeted HTTP requests to Ensembl or NCBI, but the PyDESeq2 differential expression engine itself remains fully isolated.

## Dependency Auditing
Our CI pipeline runs automated security scanning on every pull request to `main`:
1. **Secret Scanning:** We utilize `trufflehog` to ensure API keys, credentials, or `.env` files are never accidentally committed to the repository.
2. **Dependency Auditing:** We utilize `pip-audit` to cross-reference our Python dependency tree against the PyPI vulnerability database. Known CVEs in transient dependencies will cause the CI pipeline to block merging.

## Reporting a Vulnerability

If you discover a security vulnerability within the repository, please **do not** open a public issue. Instead, email the repository owner directly.

Please include:
- A description of the vulnerability.
- Steps to reproduce it.
- Possible mitigation strategies if known.

We aim to respond to all vulnerability reports within 48 hours.
