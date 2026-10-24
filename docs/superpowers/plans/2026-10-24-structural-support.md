# Structural Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Reduce unsupported tentative families with measured conservative abstention.

**Architecture:** Gate the existing finite family options and validator with identical structural signatures; keep the report schema and source records stable. Evaluate independently frozen synthetic cases against the immutable baseline.

**Tech Stack:** Python standard library, unittest, existing Ollama/Qwen cache, installed video tools.

**Spec:** `docs/superpowers/specs/2026-10-24-structural-support-design.md`

## Global Constraints

- Preserve reviewed f28d2e6 and historical failures; work on quality/structural-support.
- No downloads, installations, publication, spending or contest acceptance.
- No semantic-truth guarantees or human-baseline time-saving claims.
- Synthetic inputs only; no model-authored observations/advice; no command execution.

## Review Focus

- Test identifiers and incidental documentation mentions cannot grant a family.
- Exception messages mentioning other types must not change the outer failure label.
- Conflicting/chained families and absent or unfamiliar syntax must permit abstention.
- Quotes must independently carry the permitted signature, not just a keyword.
- Copied exception-shaped documentation and coverage loss must remain in the measured limitations.

### Task 1: Structural gate and regressions

**Files:** modify brief.py, tests/test_brief.py; create tests/test_structural_support.py and evaluation fixtures. Historical replay updates in tests/test_evidence.py reflect changed policy.

**Interfaces:** `_eligible(text)` feeds prompt and validator; public schema stays unchanged.

- [ ] Add literal positive/negative synthetic tests, including the actual lexical-trap response; run and save RED failures against baseline.
- [ ] Implement anchored signatures, remove pytest identifiers from classification, abstain on conflicts, require quote support.
- [ ] Run full unittest discovery; preserve historical provenance checks under their original policy.

### Task 2: Frozen comparison and actual inference

**Files:** create tools/evaluate_support.py, fixtures/structural-support-heldout.json, evidence/support-*.

**Interfaces:** case IDs/formats/input/expected/category/rationale -> per-case deterministic and real-inference comparison JSON. Baseline loaded from exact Git archive in ignored scratch.

- [ ] Record frozen held-out SHA before reading; do not tune on held-out results.
- [ ] Measure label eligibility, false specific choices, useful coverage and abstentions; preserve failed attempts.
- [ ] Run baseline and candidate real inference with identical cached model/options on paired batches; unload/stop task-owned server.
- [ ] Decide retain/reject based on measured evidence; run regressions/full suite.

### Task 3: Reviewable release

**Files:** update README, quality comparison, verification, demo script, DEV draft and current edited replay; preserve prior versions.

- [ ] Document exact scope, metrics, lost coverage and counterexamples; update demo/draft to current results.
- [ ] Run full tests, artifact integrity checks, compile/whitespace and commit candidate.
- [ ] Fresh independent exact-commit review, fix reproducible material defects with RED/GREEN tests, verify final clean checkout.
- [ ] Produce local safe bundle and precise final handoff; no unsupported delivery claim.
