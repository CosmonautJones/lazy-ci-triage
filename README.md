# Lazy CI Triage

Turn a synthetic or reviewed public test failure file into a local troubleshooting brief. Each model finding links to an exact source quote and a paired test/log ID. Python checks those links before accepting the brief.

Built from scratch on October 23, 2026 for Hacktoberfest Week 3, **Slow and Steady**. The intended payoff is less hunting through a failure file before deciding where to investigate. No human time savings have been measured.

## Try the deterministic inventory

Requires Python 3.10+. No pip install or third-party Python packages needed. From this directory:

```powershell
python -m unittest discover -s tests -v
python -m lazy_ci_triage fixtures/junit.xml --format junit --mode inventory --public-data --output reports/inventory
```

Open `reports/inventory/report.md`. Inventory mode extracts evidence only; it does **not** run AI. Each output directory must be new.

`--public-data` acknowledges that you checked the input is synthetic or public and contains no secrets or personal information. It is an acknowledgement, **not a secret scanner or redactor**. Use the supplied authored synthetic fixtures for the demo. The tool reads one explicitly named file and does not discover logs.

## Run real local inference

An existing local Ollama installation and an installed compatible model are required. The demonstrated model is **Qwen2.5-Coder 1.5B Instruct, Q4_K_M**, served by Ollama **0.18.0**. Its [Apache 2.0 license](https://ollama.com/library/qwen2.5-coder:1.5b/blobs/832dd9e00a68) is separate from this project's MIT license. The tested download is 986,062,089 bytes including supporting files, of which 986,048,576 bytes are weights. No weights are included in Git.

If you already run Ollama with that model on its standard port:

```powershell
python -m lazy_ci_triage fixtures/junit.xml --format junit --public-data --output reports/triage
```

For an isolated Windows setup using your existing Ollama executable, set these process-local values in a terminal and start the server. This does not install a runtime or alter global settings:

```powershell
New-Item -ItemType Directory -Force .runtime | Out-Null
$env:OLLAMA_HOST = '127.0.0.1:11439'
$env:OLLAMA_MODELS = Join-Path $PWD '.runtime/models'
$env:OLLAMA_NO_CLOUD = '1'
ollama serve
```

In a second terminal, obtain the model only if you choose to download the size/license above, then run the CLI:

```powershell
$env:OLLAMA_HOST = '127.0.0.1:11439'
ollama pull qwen2.5-coder:1.5b
python -m lazy_ci_triage fixtures/junit.xml --format junit --public-data --endpoint http://127.0.0.1:11439 --output reports/junit
python -m lazy_ci_triage fixtures/pytest.log --format pytest --public-data --endpoint http://127.0.0.1:11439 --output reports/pytest
python -m lazy_ci_triage fixtures/injection.xml --format junit --public-data --endpoint http://127.0.0.1:11439 --output reports/injection
```

The product never starts Ollama, pulls models, invokes tools, runs model suggestions, or patches files. It accepts only numeric IPv4 loopback HTTP endpoints; redirects and environment proxies are disabled. It has no paid API, account, or cloud inference integration. A human controls the local Ollama server and model selection.

## Read the result

`report.md` provides tentative hypotheses, human inspections, uncertainties and evidence anchors. `report.json` includes source excerpts, source SHA-256, the raw model response, validation state, model digest, request hash, generation options and timings. Model latency is measured with a wall clock; Ollama's durations are nanoseconds and describe different parts of its request.

**An `ok` status means structural and citation validation passed. It does not prove the model's diagnosis.** IDs must exist and belong to the same source record, quotes must occur verbatim, each failure must appear exactly once across citations, and every finding must have citations. Interpretation and relevance still need human review. The first real run demonstrated this limitation: it used valid quotes beside weak hypotheses and repeated findings. That run remains in `evidence/junit-run`; the current validator rejects its repeated citations. The refined output is in `evidence/junit-refined`.

| Status | Exit | Meaning |
| --- | --- | --- |
| `ok` | 0 | Real inference returned an accepted brief |
| `inventory_only` | 0 | Explicit deterministic extraction; no AI |
| `no_failures` | 0 | No failures extracted from supported input; no inference |
| `model_unavailable` | 3 | Local server/model unavailable; no automatic pull |
| `model_timeout` | 3 | A local request timed out |
| `invalid_response` | 3 | Malformed, incomplete or oversized response |
| `invalid_citation` | 3 | Brief schema, quote, pairing, repetition or coverage rejected |
| `input_budget_exceeded` | 3 | Split evidence before inference |
| Input/argument/output error | 2 | Read terminal error; output may be incomplete on write failure |

Model errors create an error report rather than silently switching to deterministic output. Rejected raw responses are preserved when available. Source and model text are escaped inside HTML blocks in the Markdown; arbitrary Markdown links and HTML from logs remain inert. Raw JSON remains untrusted text: never paste it into a shell or execute suggested commands.

## Supported inputs and limits

- UTF-8, plain uncolored files, 1–262,144 bytes; no control characters.
- JUnit `testsuite`/`testsuites`, including namespaces. Extracts direct `failure`/`error` children of testcases; names and testcase ordinals identify evidence. DOCTYPE and ENTITY declarations are rejected. Passed/skipped tests are omitted. Input metadata counts are not independently verified.
- Pytest plain short-summary `FAILED nodeid - reason` or `ERROR nodeid - reason` lines. Source line numbers are preserved. Full traceback parsing, color codes, collection-error blocks, xfail and arbitrary console formats are outside this small version. Prefer JUnit XML for those runs. A passing summary without failure/error counts can yield `no_failures`; it does not certify that tests actually ran.
- Up to 20 failure records and 4,000 characters per excerpt; longer excerpts are explicitly marked truncated. At most 24,000 characters of JSON-encoded model evidence; split larger files. Up to six findings, each with up to five citations. Long/complex inputs can hit the 1,800-token generation limit and are rejected rather than presented as complete.
- Temperature 0, seed 42 and 32,768-token model context. Reproducibility of wording or timing across machines/runtime versions is not guaranteed.
- Prompt isolation and citation validation reduce risk; they do not solve prompt injection or semantic hallucination. The absence of tool execution limits the impact of hostile log text. Inference is advice only.

## Evidence and submission drafts

See [measured runs](evidence/README.md), [verification ledger](docs/verification.md), [design](docs/superpowers/specs/2026-10-23-lazy-ci-triage-design.md), [DEV draft](docs/dev-post-draft.md), [demo script](docs/demo-script.md) and [challenge checklist](docs/challenge-checklist.md).

All recorded inputs are synthetic. The project has no published repository, live deployment or submitted contest entry yet. Draft links remain explicit placeholders for human review. Commits use actual local dates, with UTC run timestamps in evidence. Any changes after the October 26, 2026 06:59 UTC deadline must be noted here before an eventual submission is evaluated.

This project was implemented and drafted primarily by an AI agent at the user's request. The DEV draft uses `ai_disclosure_level: fully_autonomous`; reviewing a draft alone does not change that authorship classification.

## License

MIT for this project's code and authored synthetic fixtures. See [LICENSE](LICENSE) and [third-party notes](NOTICE.md). The model is an external dependency with its own license.
