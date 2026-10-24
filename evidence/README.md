# Actual local inference evidence

**Current behavior is v0.2.1 (October 24).** Start with [quality comparison](../docs/quality-comparison.md), [current JUnit report](oct24-junit/report.md), [current lexical counterexample](oct24-lexical-trap/report.md), [explicit no-detail refusal](oct24-no-detail/report.md), and [current measurements](oct24-evaluation.json). Five model reports contain nine paired literal options; one additional input is refused before inference. One accepted family label is still misleading (documentation-only `KeyError` mention). This is traceability in decoded/normalized detail, not raw XML byte matching, semantic entailment or diagnostic accuracy.

`v2-*`, `v2b-*` and `v2c-*` retain historical v0.2 attempts, including four model rejections. The four older folders without a v2 prefix are **historical v0.1 prose output**, and their old statuses/wording are not claims of current behavior. The current validator refuses that old prose schema. The historical measurements and initial limitations below are preserved for comparison.

All records here came from real local model inference on authored synthetic inputs on 2026-10-23. They are not canned responses or test-server output. Files named `report.json` preserve raw response, accepted selection or rejection, input records/hash, model digest, request hash, options and measurements; `report.md` is the renderer's output. No private logs or personal paths are included.

[Current local demo video](lazy-ci-triage-demo.mp4): a clearly labeled edited walkthrough of actual v0.2 saved results, not live terminal capture. The original 56-second v0.1 walkthrough is retained as `lazy-ci-triage-v0.1-demo.mp4`. Installed Pillow and FFmpeg 8.1.1 are editing tools, not application dependencies. No accounts or desktop windows were recorded. See `docs/demo-script.md` for a current live-recording plan.

## Environment

- Python 3.10.6 on Windows, AMD Ryzen 7 5800X 8-Core Processor.
- NVIDIA GeForce RTX 3090, 24,576 MiB VRAM. Ollama server logs confirmed 29/29 layers offloaded to CUDA. Other desktop GPU usage was present; this was not an isolated benchmark.
- Ollama 0.18.0, loopback `127.0.0.1:11439`, project-local cache, cloud disabled for the server process. No weights were installed before this build in the inspected relevant caches. Download need, size and license were reported before the approved download.
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
