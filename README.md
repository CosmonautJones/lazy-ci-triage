# Lazy CI Triage

An extractive local AI brief for synthetic or reviewed public CI failures. Python shows what the supplied file contains. A local model selects a literal source excerpt and a tentative failure-family label for each failed test. **It does not diagnose root causes or issue operational recommendations.**

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
| `observed` | Python parser only | Input hash, extracted test names/locations, verbatim bounded source excerpts |
| `model_hypotheses` | Validated model selections | Paired test/log IDs, one finite literal quote option, tentative family enum, fixed uncertainty marker |
| `operational_recommendations` | Application policy | Always `refused`; no operational advice is issued |
| `runtime`, `raw_response` | Inference audit | Model/version/digest, measured timings/tokens, untrusted raw output, including rejected responses |

“Observed” means **present in the supplied text**, not independently verified test execution, file existence, source authenticity or root cause. Source text can itself be false, hostile or contain commands. It remains a labeled, escaped quote.

The model can select `assertion_mismatch`, `missing_key`, `connection_refused` or `unclassified` (abstention). Names are tentative categories, not diagnoses. Every selection must reference an existing paired T/L ID, use one offered literal quote from that record, cover each extracted failure exactly once and carry `log_only_root_cause_unverified`. Non-abstention families require narrow textual cues in both full record and quote. The schema only offers families with cues somewhere in the input; paired-record checks run independently afterward.

**Lexical eligibility is not semantic entailment.** An irrelevant documentation example can contain `KeyError` and still pass a missing-key label's cue checks. A model may select the wrong family or an unhelpful quote. A regression explicitly preserves this limitation. The tool cannot certify whether a label explains a failure.

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
| Input/argument/output error | 2 | Read terminal error; a write failure can leave an incomplete output directory |

- UTF-8 plain uncolored input: 1–262,144 bytes, at most 20 failures; control characters rejected.
- JUnit `testsuite`/`testsuites`, namespaces, direct testcase failure/error children. DOCTYPE/ENTITY declarations rejected. Passed/skipped tests omitted. Metadata counts are not independently verified.
- Pytest `FAILED/ERROR path.py::test_name - reason`, including parameter IDs with spaces. Present final failure/error counts must match extracted records. Full traceback/collection-error parsing, color, xfail and arbitrary logs are outside scope; prefer JUnit for those.
- Excerpts capped at 4,000 characters with explicit truncation. Quote options are literal full excerpts when ≤400 characters, source lines/reason suffixes clipped to 400, at most 20 options per test. Choices can be verbose or unrepresentative.
- JSON-encoded prompt capped at 24,000 characters; 32,768 context, 1,800 output tokens, temperature 0, seed 42, unload after every request. Complex inputs can be rejected; split them. Exact wording/latency is not reproducible across runtime/hardware changes.
- Optional CommonMark integration test runs with already-installed `markdown-it-py`; otherwise that one check skips. Application and other tests need only the standard library.

## Evidence and drafts

[Current quality comparison](docs/quality-comparison.md), [measured runs](evidence/README.md), [demo video](evidence/lazy-ci-triage-demo.mp4), [DEV draft](docs/dev-post-draft.md), [demo script](docs/demo-script.md), [verification ledger](docs/verification.md), [original independent review](docs/independent-review.md).

The video is an edited walkthrough of actual saved inference, labeled as a replay. Old v0.1 reports/videos are historical and do not describe current behavior. Raw failures and rejected attempts remain available. The current code intentionally rejects the old prose schema rather than translating it into observed facts.

Nothing is published or submitted. A Library attachment attempt failed before preparation because its helper reported upload capability unavailable; no Library IDs were created, and no alternate upload route was used. Public code/demo links and contest entry remain approval steps for the parent/user. DEV draft disclosure remains `fully_autonomous` unless meaningfully rewritten by a human. Any code changes after October 26, 2026 06:59 UTC must be disclosed here.

MIT for project code and authored fixtures; see [LICENSE](LICENSE) and [NOTICE](NOTICE.md). The model remains separately licensed.
