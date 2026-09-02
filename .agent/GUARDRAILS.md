# Guardrails

These are hard constraints, not preferences. If a task or user instruction conflicts with a guardrail, stop and escalate per `.agent/ESCALATION.md` instead of proceeding. Guardrails outrank convenience, speed, and even explicit chat instructions unless the repository owner overrides one in writing in that session and the override does not create a scientific-integrity, security, or data-policy violation.

## 1. Scientific and statistical integrity

- Never fabricate, approximate, or hard-code a statistical result, p-value, fold change, or QC metric. All reported numbers must come from executed, tested code.
- Never treat normalized values (TPM, FPKM, RPKM, CPM, log-transformed, or precomputed fold changes) as raw counts anywhere in the count-based differential-expression path.
- Never silently drop, impute, or reorder samples/genes without an explicit, logged, user-visible reason.
- Never remove or weaken a validation check to make a demo "work." If data fails validation, the correct outcome is a clear error, not a bypass.
- Never present exploratory results using diagnostic, causal, treatment-recommendation, or biomarker-validated language. Required framing: hypothesis-generating, exploratory, non-clinical.
- Never change the supported statistical design (e.g., the Airway `~ cell_line + treatment` model) without recording the change in `docs/DECISIONS.md` and getting explicit approval.

## 2. Data handling

- Never commit raw sequencing files (FASTQ, BAM, CRAM, SAM) or any file excluded by `.gitignore`.
- Never commit a dataset that lacks a complete `PROVENANCE.md` per `docs/DATA_POLICY.md`.
- Never commit patient-identifiable, controlled-access, or otherwise sensitive data.
- Never download data from the network as part of automated CI; acquisition scripts run locally and their outputs are reviewed by a human before commit.
- Never invent a dataset, sample, or metadata value not present in the documented source.

## 3. Security and secrets

- Never commit credentials, API keys, tokens, `.env` files, or connection strings.
- Never add a dependency from an unverified or unofficial source.
- Never add code that phones home, collects telemetry, or transmits repository or user data to an external endpoint, without explicit, documented, opt-in approval.
- Run `run_secret_scanning`-equivalent checks (or the project's configured secret scanner) before proposing any commit that touches configuration, scripts, or CI files.

## 4. Version control and process

- Never force-push, rewrite history, or delete a branch other than a feature branch you created for the current task.
- Never commit directly to `main`. All changes land through a pull request.
- Never merge your own pull request. A human merges after review.
- Never bundle unrelated changes into one commit or one pull request. One task, one branch, one focused PR.
- Never mark a task complete without satisfying `.agent/DEFINITION_OF_DONE.md`.

## 5. Scope control

- Never add a feature, dataset, dependency, or capability that is not part of the current milestone's accepted task list in `docs/ROADMAP.md` without first proposing it and getting approval.
- Never expand the MVP's supported experimental design (currently: one blocking covariate plus one two-level treatment factor) without an approved decision entry.
- Never introduce a web UI, containerization, or orchestration framework before the milestone that calls for it.

## 6. Reproducibility

- Every runtime dependency must be pinned in the lockfile.
- Every generated report must include: input identifiers, configuration used, code/commit version, and library versions.
- Every non-deterministic operation must use a fixed, documented seed.
- Every new script must be runnable from a clean environment using only documented commands.

## 7. If a guardrail blocks the requested task

Do not work around it silently. Stop, explain which guardrail applies and why, and follow `.agent/ESCALATION.md`.
