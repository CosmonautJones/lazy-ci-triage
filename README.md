# Lazy CI Triage

An extractive local AI brief for synthetic or reviewed public CI failures. Python shows parsed metadata and decoded/normalized test detail. A local model selects a literal option from that detail and a tentative failure-family label for each failed test. **It does not diagnose root causes or issue operational recommendations.**

Current version: **0.2.2**, prepared locally on October 24, 2026. The independently reviewed v0.2.1 baseline remains in Git at `f28d2e6`. Publication and contest acceptance remain separate human decisions.

New standalone project started October 23, 2026 for Hacktoberfest Week 3, **Slow and Steady**. The intended benefit is a small evidence index to start reviewing failures. No human time savings or diagnostic accuracy have been measured.

## Try it

Python 3.10+, standard library only; no pip install needed:

```powershell
python -m unittest discover -s tests -v
python -m lazy_ci_triage fixtures/junit.xml --format junit --mode inventory --public-data --output reports/inventory
```

Open `reports/inventory/report.md`. Inventory is explicitly deterministic; it does not run AI. Choose a new output directory for every run. `--public-data` acknowledges you reviewed the input for secrets/personal data; it is **not a scanner or redactor**. Use the authored synthetic fixtures for demonstrations.

With an existing Ollama server and installed model on the default port:

```powershell
python -m lazy_ci_triage fixtures/junit.xml --format junit --public-data --output reports/junit
```

The demonstrated setup uses Qwen2.5-Coder 1.5B Instruct Q4_K_M through Ollama 0.18.0. Its [Apache 2.0 model license](https://ollama.com/library/qwen2.5-coder:1.5b/blobs/832dd9e00a68) is separate from this project's MIT license. The initial build newly downloaded 986,062,089 bytes including support files, after reporting the need, exact size and license. Weights are excluded from Git; this revision reused those cached weights and downloaded nothing.

To reuse the isolated cache on the build machine, start the already-installed runtime in a terminal:

```powershell
$env:OLLAMA_HOST = '127.0.0.1:11439'
$env:OLLAMA_MODELS = Join-Path $PWD '.runtime/models'
$env:OLLAMA_NO_CLOUD = '1'
ollama serve
```

In another terminal:

```powershell
python -m lazy_ci_triage fixtures/junit.xml --format junit --public-data --endpoint http://127.0.0.1:11439 --output reports/junit
python -m lazy_ci_triage fixtures/pytest.log --format pytest --public-data --endpoint http://127.0.0.1:11439 --output reports/pytest
python -m lazy_ci_triage fixtures/injection.xml --format junit --public-data --endpoint http://127.0.0.1:11439 --output reports/hostile
python -m lazy_ci_triage fixtures/ambiguous.log --format pytest --public-data --endpoint http://127.0.0.1:11439 --output reports/ambiguous
```

On another machine, install your own compatible local runtime/model only if you choose to accept its size and license. The application never starts a server, pulls weights or calls a paid API. Only `http://127.0.0.1:<port>` is allowed; proxies/redirects are disabled. No tools, shell commands, automatic fixes, account linking or cloud inference integration exist in the application.

## What the report means

Schema version 2 separates these fields:

| Field | Origin | Meaning |
| --- | --- | --- |
| `observed` | Python parser only | Input hash, parsed test names/locations, bounded decoded/normalized detail |
| `model_hypotheses` | Validated model selections | Paired test/log IDs, one finite literal quote option, tentative family enum, fixed uncertainty marker |
| `operational_recommendations` | Application policy | Always `refused`; no operational advice is issued |
| `runtime`, `raw_response` | Inference audit | Model/version/digest, measured timings/tokens, untrusted raw output, including rejected responses |

“Observed” means **parsed from the supplied file**, not independently verified test execution, file existence, source authenticity or root cause. JUnit XML entities/attributes are decoded, and failure type/message values and element text are joined into a normalized record; a selected quote matches that record and may not occur byte-for-byte in raw XML. Pytest detail preserves its summary line. Generated “no detail” and truncation notes remain outside quotable detail. Supplied text can itself be false, hostile or contain commands; it remains labeled and escaped.

The model can select `assertion_mismatch`, `missing_key`, `connection_refused` or `unclassified` (abstention). Names are tentative categories, not diagnoses. Every selection must reference an existing paired T/L ID, use one offered literal quote from that record, cover each extracted failure exactly once and carry `log_only_root_cause_unverified`. Specific families require an anchored failure signature in both full record and selected quote. The schema offers the union of eligible families across records; the validator independently enforces each paired record's eligibility. A model can still choose an ineligible family or another record's option, in which case the whole report is refused.

**Structural eligibility is not semantic entailment.** The gate strips pytest test identifiers and recognizes exception-shaped lines (including qualified Python names and pytest `E` prefixes), assertion statements/expected-got summaries and direct refused-connection reasons. A recognized exception's message does not separately grant other families. Missing, unfamiliar or conflicting signatures allow only abstention. An ordinary prose-only `KeyError` mention no longer grants a missing-key label; an unmarked copied `KeyError: 'example'` line still can. The tool cannot authenticate the source or certify whether a label explains a failure.

The frozen 30-case [structural-support evaluation](docs/structural-support-evaluation.md) measures the tradeoff against v0.2.1. Wrong specific-family opportunities fell from 10 to 3 cases, while the expected specific family remained available for 12/15 supported cases, down from 15/15. All three remaining false opportunities are deliberately indistinguishable copied tracebacks. Type/message-only JUnit metadata without recognized text syntax loses coverage. These gate counts are not real-model classification accuracy; actual selections, refusals and coverage are reported separately in the evaluation.

Model-authored observations, explanations, file/function fields, free-form recommendations and confirmation claims are refused. That closes the old prose channel that invented `round()`, SQL queries and an HTML file. It does not make source quotes or category selections true. Fixed tentative descriptions and generic human review questions come from application code and are labeled accordingly; they are not model recommendations.

Markdown shows observations first and unverified selections separately. Blank-line-safe escaped `pre` blocks keep hostile HTML/Markdown inert. Raw JSON remains untrusted audit data; never execute text from it. Rejected model responses are not rendered as accepted advice.

## States and limits

| Status | Exit | Meaning |
| --- | --- | --- |
| `ok` | 0 | Constrained selection contract passed; no semantic-truth guarantee |
| `inventory_only` | 0 | Explicit deterministic extraction, no AI |
| `no_failures` | 0 | No supported failures extracted; no inference and no independent test-success verification |
| `model_unavailable`, `model_timeout` | 3 | Local server/model/request problem; no automatic pull or fallback |
| `invalid_response` | 3 | Malformed, incomplete, oversized or invalid-Unicode response |
| `invalid_citation` | 3 | Schema/quote/pairing/coverage/family/uncertainty contract refused |
| `input_budget_exceeded` | 3 | Split input before inference |
| `insufficient_evidence` | 3 | At least one failure has no nonempty detail; no model endpoint is contacted |
| Input/argument/output error | 2 | Read terminal error; a write failure can leave an incomplete output directory |

- UTF-8 plain uncolored input: 1–262,144 bytes, at most 20 failures; control characters rejected.
- JUnit `testsuite`/`testsuites`, namespaces, direct testcase failure/error children. DOCTYPE/ENTITY declarations rejected. Passed/skipped tests omitted. Metadata counts are not independently verified.
- Pytest `FAILED/ERROR path.py::test_name - reason`, including balanced parameter brackets containing spaces or ` - `. Ambiguous/unbalanced brackets are rejected with guidance to use JUnit. Present final failure/error counts must match extracted records. Full traceback/collection-error parsing, color, xfail and arbitrary logs are outside scope; prefer JUnit for those.
- Detail is capped at 4,000 characters with truncation flagged separately. Quote options are literal full normalized records when ≤400 characters, detail lines/reason suffixes clipped to 400, at most 20 options per test. Genuine short detail (1–3 characters) is supported; a failure with no detail is still available in inventory mode but cannot produce a model brief. Choices can be verbose or unrepresentative.
- JSON-encoded prompt capped at 24,000 characters; 32,768 context, 1,800 output tokens, temperature 0, seed 42, unload after every request. Complex inputs can be rejected; split them. Exact wording/latency is not reproducible across runtime/hardware changes.
- Optional CommonMark integration test runs with already-installed `markdown-it-py`; otherwise that one check skips. Application and other tests need only the standard library.

## Evidence and drafts

[Current quality comparison](docs/quality-comparison.md), [measured runs](evidence/README.md), [demo video](evidence/lazy-ci-triage-demo.mp4), [final DEV article](docs/dev-entry.md), [evidence appendix](docs/evidence-appendix.md), [demo script](docs/demo-script.md), [verification ledger](docs/verification.md), [original independent review](docs/independent-review.md).

The video is an edited walkthrough of actual saved inference, labeled as a replay. Older v0.1/v0.2/v0.2.1 reports/videos are historical; `oct24-*` records preserve v0.2.1 behavior. The new structural-support comparison identifies candidate and baseline separately. Raw failures and rejected attempts remain available. The current code rejects the old prose schema and the old prose-only lexical-trap label rather than translating them into observed facts. Copied exception-shaped examples remain a limit.

The code, edited demo and evidence are prepared for approved public release. DEV post and contest visibility require separate verification; publication is not proof of contest acceptance. See [publication provenance](PUBLICATION.md). DEV draft disclosure remains `fully_autonomous` unless meaningfully rewritten by a human. Any code changes after October 26, 2026 06:59 UTC must be disclosed here. See the [precise remaining submission checklist and attachment status](docs/submission-review.md).

MIT for project code and authored fixtures; see [LICENSE](LICENSE) and [NOTICE](NOTICE.md). The model remains separately licensed.
