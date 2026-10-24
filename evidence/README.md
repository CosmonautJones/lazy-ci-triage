# Actual local inference evidence

**Three-review follow-up:** [parser/demo fixes](../docs/three-review-fixes.md) add four input-boundary regressions (78 tests total) and a concrete saved input/CLI/report example to the current video. No new inference was needed; all raw model records, inputs and metrics below remain unchanged. The former summary-only video is retained as `lazy-ci-triage-v0.2.2-summary-demo.mp4`.

**Current behavior is v0.2.2 (October 24).** Start with the [structural-support evaluation](../docs/structural-support-evaluation.md), [paired individual comparison](support-individual/comparison.json), [retained batch failures](support-batch/comparison.json), [current JUnit report](support-demo-junit/report.md) and [original lexical trap now abstaining](support-demo-lexical-trap/report.md). The 30 paired individual cases produced 29 accepted reports per policy: wrong specific selections 7 to 2, correct specific selections 12/15 to 9/15. The remaining two wrong labels are indistinguishable unmarked copied examples. Gate opportunities and model outcomes are separate measurements, with real coverage loss and refusals shown. This is not real-world diagnostic accuracy, semantic entailment or source authentication.

`v2-*`, `v2b-*` and `v2c-*` retain historical v0.2 attempts, including four model rejections. The four older folders without a v2 prefix are **historical v0.1 prose output**, and their old statuses/wording are not claims of current behavior. The current validator refuses that old prose schema. The historical measurements and initial limitations below are preserved for comparison.

The historical v0.1/v0.2 inference records were generated locally on authored synthetic inputs on October 23. The `oct24-*` records preserve the earlier v0.2.1 behavior: five actual inference runs and one explicit refusal before inference. The new support pass made **72 model calls**: 60 exact original-case comparisons, 10 separate six-record stress calls and two current CLI demonstrations. All calls, rejected responses, input files and payloads remain available. Inference responses are not canned or test-server output; no-detail refusal has no model response. `report.json` preserves input/hash, accepted selection or refusal, and raw response/metrics when inference occurred; `report.md` is its version's renderer output. No private logs or personal paths are included.

[Current local demo video](lazy-ci-triage-demo.mp4): a clearly labeled 56-second edited walkthrough of actual v0.2.2 comparison results, not live terminal capture. It shows both false-label reduction and lost useful coverage, plus poor multi-record results. Older walkthroughs are retained as v0.1/v0.2/v0.2.1 MP4s. Installed Pillow and FFmpeg 8.1.1 are editing tools, not application dependencies. No accounts or desktop windows were recorded. See `docs/demo-script.md` for a current live-recording plan.

## Environment

- Python 3.10.6 on Windows, AMD Ryzen 7 5800X 8-Core Processor.
- NVIDIA GeForce RTX 3090, 24,576 MiB VRAM. Ollama server logs confirmed 29/29 layers offloaded to CUDA. Other desktop GPU usage was present; this was not an isolated benchmark.
- Ollama 0.18.0, loopback `127.0.0.1:11439`, project-local cache, cloud disabled for the server process. No weights were installed before this build in the inspected relevant caches. Download need, size and license were reported before the initial download. No additional human confirmation is claimed; every later pass reused that cache.
- Qwen2.5-Coder 1.5B Instruct Q4_K_M; manifest digest `d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668`.
- Weight SHA-256 `29d8c98fa6b098e200069bfb88b9508dc3e85586d20cba59f8dda9a808165104`, 986,048,576 bytes. Total including support: 986,062,089 bytes.
- License blob SHA-256 `832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e`; local contents verified as Apache License 2.0. [Source license](https://ollama.com/library/qwen2.5-coder:1.5b/blobs/832dd9e00a68).
- Options: temperature 0, seed 42, context 32,768, output cap 1,800 tokens, `keep_alive=0` to unload after each request. Each run included loading; latency is not a warm-model benchmark.

## Recorded results

| Run | Input / failures | Wall seconds | Prompt / output tokens | Historical v0.1 citation contract |
| --- | --- | ---: | ---: | --- |
| [Initial JUnit](junit-run/report.md) | JUnit / 3 | 43.502795 | 473 / 843 | Rejected now: repeated citations; initial version recorded `ok` |
| [Refined JUnit](junit-refined/report.md) | JUnit / 3 | 20.993951 | 560 / 378 | Accepted: 3 paired exact quotes, 3/3 failures covered once |
| [Pytest](pytest-run/report.md) | Short summary / 3 | 27.117923 | 491 / 477 | Accepted: 3 paired exact quotes, 3/3 failures covered once |
| [Hostile data](injection-run/report.md) | JUnit / 1 | 7.863337 | 383 / 123 | Accepted: 1 paired exact quote, 1/1 failure covered once |

Wall time includes inventory, metadata checks, transport, generation and loading. Ollama's nanosecond durations and token counts are also preserved; they measure different phases. The model was run sequentially. There is no human baseline, time-saved claim, statistical latency distribution or broad accuracy benchmark.

## What the records actually establish

For the three runs under the **historical v0.1 refined contract**: **7/7 citations had existing, correctly paired IDs and exact quotes; 7/7 supplied failure records were covered once**. The saved source integrity and current rejection of old prose can be checked without a model, along with current v0.2 replay:

```powershell
python -m unittest discover -s tests -p test_evidence.py -v
```

The initial response had duplicate findings, asserted causes and guessed `get_product`/`make_request` functions. It even attached a real inventory quote to a rounding claim. Its historical `ok` status is preserved, not rewritten. The current repeated-evidence check rejects that response.

The refined JUnit hypotheses give plausible starting points (rounding, missing-key handling, service availability), each with explicit uncertainty. They are not proven causes. Inspection of the other runs exposes remaining semantic weaknesses:

- Pytest finding 1 invents `round()` in `prices.py`, which the supplied summary does not establish.
- Pytest finding 2 suggests a SQL query, though the supplied evidence only establishes a `KeyError`.
- The injection run does not follow the malicious instructions to use T999/L999 or claim all tests passed, but it assumes an HTML file and says the exact banner text is absent even though the source includes `hello`.

These observations are an author-agent qualitative inspection of tiny synthetic examples, not a human study or an independently scored accuracy metric. They are why the report prominently requires human review. Valid references do not prove relevance or correctness, and one hostile example does not establish general resistance to prompt injection. No model-suggested command was executed. No network-disconnection test was performed.

## Reproduce inference

Use the README's existing-runtime/model setup, then run its three model commands with new output paths. Weight tags can change; compare the recorded digest. Wording and latency may differ with runtime, hardware and cache state. Unit tests' `test-server` responses are separate deterministic transport fixtures, never presented as inference evidence.
