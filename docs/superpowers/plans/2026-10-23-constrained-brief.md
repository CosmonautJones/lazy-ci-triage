# Constrained brief implementation plan

> **For agentic workers:** use inline execution with TDD; fresh independent review after this revision.

Goal: separate deterministic source observations from bounded model hypotheses, eliminate free-form operational advice, preserve honest comparison evidence.
Spec: `docs/superpowers/specs/2026-10-23-constrained-brief-design.md`.
Global constraints: existing weights only; no public uploads/account changes; same small standard-library CLI; no model-suggested command execution.

Review focus: old bad outputs must be rejected; model-authored observations/recommendations must never reach accepted brief; unsupported category cues must reject; abstention remains valid; malicious source text stays verbatim/inert and must not become a verified observation of reality.

- [x] Task 1: write failing schema-v2/actual-bad-output regression tests; replace free-form contract, add lexical cue eligibility and fixed uncertainty; update deterministic transport tests to new shape.
- [x] Task 2: write failing report/CLI tests for separate observations, hypotheses and advice refusal; implement schema-v2 envelope and renderer; keep legacy records historical.
- [x] Task 3: restart existing isolated Ollama with the already-downloaded cache; run real JUnit/pytest/hostile/ambiguous cases, preserve every outcome and evaluate contract/citation checks separately from interpretation.
- [x] Task 4: independent review and necessary fixes; update README, actual-current DEV draft, demo and limitations; fresh whole suite, archive and final commit. Preserve Library upload blocker; no bypass.
