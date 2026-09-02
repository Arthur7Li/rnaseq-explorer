# Escalation Protocol

Stop and ask a human whenever any of the following is true. Do not guess, do not silently pick the "safer-sounding" option, and do not proceed with a partial workaround.

## Always escalate when

- A guardrail in `.agent/GUARDRAILS.md` appears to block the requested task.
- The task requires choosing or changing the differential-expression backend, statistical model, or supported experimental design.
- The task requires adding a new dataset, or changing which dataset is official for a given phase.
- You discover the current documentation is ambiguous or self-contradictory (for example, an old scope statement conflicts with a newer one).
- A dependency you need is unmaintained, has a restrictive/unclear license, or has known security advisories.
- You cannot verify a claim (statistical, biological, or about a library's behavior) from documentation or executed code.
- The task, as written, would require weakening a validation rule or silently handling malformed data.
- You are not confident the tests you wrote actually exercise the failure mode they claim to test.
- A previously approved decision in `docs/DECISIONS.md` would need to be reversed or contradicted.
- The requested change would touch more files or take meaningfully longer than the task spec implied.

## How to escalate

1. Stop implementation work immediately; do not commit a partial or speculative fix.
2. State clearly: what you were asked to do, what specifically is blocking or ambiguous, and which guardrail/doc it relates to.
3. Present 2-3 concrete options with trade-offs. Do not present zero options ("it's unclear, what should I do") or a single option disguised as neutral.
4. Recommend one option and say why, but do not act on it until approved.
5. Wait for an explicit answer before resuming.

## What escalation is not

Escalation is not a way to avoid effort on straightforward tasks. If the task spec and existing docs already answer the question, proceed — do not escalate merely to double-check settled decisions. Re-reading `AGENTS.md`, `.agent/GUARDRAILS.md`, and the relevant `docs/*.md` file is expected before deciding something is genuinely ambiguous.
