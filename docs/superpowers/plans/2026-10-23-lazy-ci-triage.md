# Lazy CI Triage Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task-by-task. One independent whole-project review follows implementation.

**Goal:** Produce a local evidence-linked failure brief using a real open-weight model.

**Architecture:** Standard-library parsers create bounded evidence records. Ollama generates structured hypotheses, an independent validator checks every citation, and a renderer writes safe Markdown plus machine-readable provenance.

**Tech Stack:** Python 3.10+, unittest, Ollama 0.18.0; zero package dependencies.

**Spec:** `docs/superpowers/specs/2026-10-23-lazy-ci-triage-design.md`

## Global Constraints
- New isolated Git repository; actual commit times; no public changes.
- Synthetic/public data only, explicit acknowledgement, 256 KiB input and 20 failures maximum.
- No automatic commands, fixes, model pulls, or remote inference in product code.
- Exact quotes and paired T/L IDs required; every failure covered; hypotheses require human review.
- No invented baseline savings; preserve real inference failures as well as successes.

## Review Focus
- Malformed, namespaced, entity-bearing and oversized XML must fail clearly or parse safely.
- Duplicate pytest test names need distinct paired IDs; unrelated logs must not yield invented failures.
- Injection-bearing source excerpts remain inert data and safely rendered text.
- Invalid/incomplete/truncated model output must never be reported as a valid brief.
- Endpoint redirects/proxies and output errors must not leak input or silently succeed.

### Task 1: Input normalization
Files: `fixtures/*`, `tests/test_parsing.py`, `lazy_ci_triage/parsing.py`.
Interface: `parse_input(data: bytes, kind: str) -> Dataset`; immutable Failure records with test_id/log_id/name/location/text and Dataset with input_sha256/failures.
- [ ] Write parser behavior tests, run RED, implement minimal parsers, run full suite GREEN.
- [ ] Commit parser and tests.

### Task 2: Brief contract and rendering
Files: `tests/test_brief.py`, `lazy_ci_triage/brief.py`, `lazy_ci_triage/report.py`.
Interfaces: `build_prompt(dataset) -> dict`, `validate_brief(value, dataset) -> dict`, `render_report(report) -> str`.
- [ ] Write schema/citation/coverage/injection tests, run RED, implement and run GREEN.
- [ ] Commit validated report path.

### Task 3: Local inference and CLI
Files: `tests/test_runtime.py`, `lazy_ci_triage/ollama.py`, `lazy_ci_triage/cli.py`, `lazy_ci_triage/__main__.py`, `pyproject.toml`.
Interfaces: `generate(dataset, model, endpoint, timeout) -> dict`; `main(argv=None) -> int`. CLI writes report.json and report.md to a new directory; statuses/exits documented.
- [ ] Write real loopback HTTP test-server and CLI tests for normal/failure states, run RED, implement and run GREEN.
- [ ] Run actual model on synthetic fixtures, preserve evidence, commit.

### Task 4: Delivery and review
Files: `README.md`, `LICENSE`, `docs/dev-post-draft.md`, `docs/demo-script.md`, `docs/challenge-checklist.md`, `docs/verification.md`.
- [ ] Record model license/digest, hardware/runtime/latency/quality measurements and limitations.
- [ ] Draft official-template post with `fully_autonomous` disclosure and explicit publication placeholders.
- [ ] Independent review, address important findings with RED/GREEN regression tests.
- [ ] Fresh full suite, CLI smoke, commit and return paths/hash/blockers.
