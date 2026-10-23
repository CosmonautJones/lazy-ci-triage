# Lazy CI Triage design

Created 2026-10-23. New standalone project; no inherited project code.

## Intent and authorization
Help a maintainer start investigating failing CI by turning synthetic or reviewed public test output into a short brief, with every hypothesis and proposed inspection tied to a supplied source. The user approved this bounded CLI build and requested implementation without waiting on optional design questions. These choices are the builder's judgment under that approval.

## Approaches
1. Dependency-free Python CLI with local Ollama and Markdown/JSON reports (chosen): reproducible, small, inspectable, no web service to deploy.
2. Web UI: easier browsing but extra dependencies and hosting work beyond scope.
3. Deterministic rules only: useful inventory but insufficient for the requested real AI demonstration. Retain as an explicit `inventory` mode, never disguise it as inference.

## Boundaries
- Python 3.10+, standard library only. Existing Ollama optional for tests, required for inference.
- Accept one UTF-8 JUnit XML or pytest log, maximum 256 KiB, maximum 20 failures, bounded per-failure excerpts. Reject oversized inputs instead of silently dropping failures.
- Require an explicit synthetic/public-data acknowledgement. No recursive discovery, private log collection, credentials, or uploads.
- Normalize failed tests into stable ordered `T001` test IDs and `L001` evidence IDs. Each evidence record includes a source line range (pytest) or testcase ordinal (XML) and the input SHA-256.
- JUnit: reject DOCTYPE/ENTITY declarations and non-UTF-8 input; parse failure/error children, not passed/skipped tests. Pytest: support short summary lines `FAILED nodeid - reason` and `ERROR nodeid - reason`, with those exact source lines as evidence. Do not imply full traceback support.
- Model receives JSON records as untrusted data, clear role separation, no tools, temperature 0, JSON schema with enumerated evidence/test IDs. Validate schema, ID existence, ID pairing, exact quoted substrings, and complete failure coverage independently of inference.
- Model output contains 1–6 findings: hypothesis, human inspection, uncertainty, and 1–5 citations. A citation has test_id, log_id, quote. No uncited summary prose.
- Citation existence and quote matching do not prove a diagnosis. Always label hypotheses and require human review.
- Render untrusted text as escaped HTML in Markdown to prevent active links/HTML or terminal control sequences. No model-provided command execution, shell access, plugins, retries that conceal failures, or automatic fixes.
- Loopback HTTP only, numeric 127.0.0.1, no proxies/redirects. No automatic pull or server start in product code.
- Explicit model-unavailable, timeout, invalid-response, invalid-citation, input-error states. Optional deterministic inventory is selected by user, never an automatic success substitute.

## Parts
`parsing.py`: input validation and normalized evidence. `brief.py`: schema, prompt and citation validation. `ollama.py`: bounded local HTTP inference and metrics. `report.py`: safe Markdown. `cli.py`: user acknowledgement, output state, pre-rendered JSON/Markdown reports in a new directory; explicit output-error exit if file writes fail. `tests/`: standard-library unit/integration tests, plus optional CommonMark renderer integration. `fixtures/`: authored synthetic examples including injection text. `evidence/`: real demo responses and runtime measurements, no private paths or hardware IDs, plus an edited walkthrough video. `docs/`: design, test ledger, rules checklist, draft DEV post and demo script.

## Completion
Deterministic tests pass; fresh independent review; actual local inference on synthetic inputs preserved with model digest, runtime, hardware, wall latency, token counts and citation results. No human time-savings claim. Public repository, video/deployment, DEV publishing and contest entry remain parent-led approval steps.
