# Actual local inference evidence

All four records here came from real local model inference on authored synthetic inputs on 2026-10-23. They are not canned responses or test-server output. Files named `report.json` preserve raw response, parsed brief, input records/hash, model digest, request hash, options and measurements; `report.md` is the renderer's output. No private logs or personal paths are included.

[Local demo video](lazy-ci-triage-demo.mp4): 56 seconds, H.264, 1280×720, silent, 325,407 bytes. It is a clearly labeled edited walkthrough of these actual saved results, not a live terminal recording. Created with installed Pillow and FFmpeg 8.1.1; those are editing tools rather than application dependencies. Frames include the model, hardware, latency, source quote and limitations. No accounts or desktop windows were recorded. The script for an optional live recording is in `docs/demo-script.md`.

## Environment

- Python 3.10.6 on Windows, AMD Ryzen 7 5800X 8-Core Processor.
- NVIDIA GeForce RTX 3090, 24,576 MiB VRAM. Ollama server logs confirmed 29/29 layers offloaded to CUDA. Other desktop GPU usage was present; this was not an isolated benchmark.
- Ollama 0.18.0, loopback `127.0.0.1:11439`, project-local cache, cloud disabled for the server process. No weights were installed before this build in the inspected relevant caches. Download need, size and license were reported before the approved download.
- Qwen2.5-Coder 1.5B Instruct Q4_K_M; manifest digest `d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668`.
- Weight SHA-256 `29d8c98fa6b098e200069bfb88b9508dc3e85586d20cba59f8dda9a808165104`, 986,048,576 bytes. Total including support: 986,062,089 bytes.
- License blob SHA-256 `832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e`; local contents verified as Apache License 2.0. [Source license](https://ollama.com/library/qwen2.5-coder:1.5b/blobs/832dd9e00a68).
- Options: temperature 0, seed 42, context 32,768, output cap 1,800 tokens, `keep_alive=0` to unload after each request. Each run included loading; latency is not a warm-model benchmark.

## Recorded results

| Run | Input / failures | Wall seconds | Prompt / output tokens | Current citation contract |
| --- | --- | ---: | ---: | --- |
| [Initial JUnit](junit-run/report.md) | JUnit / 3 | 43.502795 | 473 / 843 | Rejected now: repeated citations; initial version recorded `ok` |
| [Refined JUnit](junit-refined/report.md) | JUnit / 3 | 20.993951 | 560 / 378 | Accepted: 3 paired exact quotes, 3/3 failures covered once |
| [Pytest](pytest-run/report.md) | Short summary / 3 | 27.117923 | 491 / 477 | Accepted: 3 paired exact quotes, 3/3 failures covered once |
| [Hostile data](injection-run/report.md) | JUnit / 1 | 7.863337 | 383 / 123 | Accepted: 1 paired exact quote, 1/1 failure covered once |

Wall time includes inventory, metadata checks, transport, generation and loading. Ollama's nanosecond durations and token counts are also preserved; they measure different phases. The model was run sequentially. There is no human baseline, time-saved claim, statistical latency distribution or broad accuracy benchmark.

## What the records actually establish

For the three runs under the refined contract: **7/7 citations have existing, correctly paired IDs and exact quotes; 7/7 supplied failure records are covered once**. The saved records can be revalidated without a model:

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
