---
title: "Lazy CI Triage: let a local model read the red tests first"
published: false
tags: devchallenge, hf26challenge, python, opensource
ai_disclosure_level: fully_autonomous
---

*Draft for human review. Publication links below must be replaced after separate approval. This article was written primarily by an AI agent at the user's request; it has not been published.*

*This is a submission draft for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19).*

## What I Built

A red CI run creates a small chore before the real debugging starts: find the failures, connect each message to a test, and decide what to inspect first.

Lazy CI Triage puts a local model at that starting line. Give it a synthetic or reviewed public JUnit XML file or a plain pytest short summary. It produces a brief with a tentative explanation, a human inspection step, an uncertainty statement and a clickable source excerpt for each failure. Python checks the test IDs, log IDs, exact quotes and failure coverage before showing an accepted result.

The scope is deliberately small: one file in, a Markdown report and JSON evidence record out. No agent tools, automatic fixes or model-suggested commands execute. The maintainer can spend less attention assembling the evidence and more attention deciding whether the model's suggestion makes sense. That is the intended Slow and Steady fit; I have not measured human time saved.

## Demo

**[VIDEO OR DEPLOYED DEMO LINK — pending human review and publication approval]**

The local 56-second video is `evidence/lazy-ci-triage-demo.mp4`, an edited walkthrough of saved real inference results, explicitly labeled rather than presented as live capture. The optional live recording script is `docs/demo-script.md`. The repository includes the original synthetic inputs and actual model responses under `evidence/`, so the demo's claims can be inspected without trusting a screenshot.

On an RTX 3090 with 24 GiB VRAM and an AMD Ryzen 7 5800X, the refined JUnit run took **20.994 seconds wall time**, including local API checks and model loading. Qwen produced three distinct hypotheses, with three accepted citations covering three failures. That is a single synthetic example, not a benchmark or a measured human productivity improvement.

## Code

**[PUBLIC CODE LINK — pending human review and repository publication approval]**

The project and its isolated Git repository were started on October 23, 2026, inside the Week 3 window. The code and synthetic fixtures use the MIT license. The external model has its own Apache 2.0 license; weights are excluded from Git.

## How I Built It

The AI core is Qwen2.5-Coder 1.5B Instruct, quantized Q4_K_M, running locally through Ollama 0.18.0. The demonstration records the exact model digest, generation options, raw response, token counts and wall latency. Python 3.10's standard library handles everything around inference: parsing, bounded local HTTP requests, validation, CLI arguments and reports.

The pipeline is small enough to read in one sitting:

1. Parse failed tests into ordered `T001` test and `L001` log records, with a file hash and source location.
2. Send those records as untrusted JSON data, with a structured output schema and instructions to stay tentative.
3. Check every returned citation against the supplied record. Reject unknown IDs, wrong pairings, invented quotes, repeated evidence or missing failures.
4. Escape source/model text in a Markdown report, alongside the exact evidence a human needs to check.

A useful failure happened in the first actual run. Its quotes and IDs existed, but the model repeated findings and speculated about functions that were never supplied. A rounding hypothesis even carried an unrelated inventory citation. Citation validity did not make the explanation correct.

I kept that response, tightened the prompt and added repeated-evidence checks with regression tests. The refined run produced one tentative finding per failure, with a matching source for each. It is still advice. A model can cite a real line and misinterpret it, and this tool cannot prove semantic relevance automatically.

The other saved runs make that warning concrete: the pytest brief guessed a SQL query behind a `KeyError`, and the hostile-input brief assumed an HTML file. Those details were not established by the logs. Across the three refined-contract runs, seven out of seven citations and failure records pass structural checks. That measures traceability, not diagnostic accuracy. I would review the wording before acting on any suggestion.

The tests cover malformed input, XML entities, duplicate test names, hostile instructions inside logs, response failures and citation rejection. Deterministic transport tests use a clearly labeled local test server; the saved inference examples use the actual model. There is an explicit inventory-only mode for when AI is unavailable, and it never masquerades as a successful AI brief.

## Why Does Open Innovation Matter?

The open-weight model is the part that proposes investigation directions. The surrounding code makes its evidence inspectable and constrains what becomes a report. Once Ollama and the model are installed, this workflow can run without an external inference API, credentials or an internet connection. The demonstrated requests used only loopback; I did not perform a separate network-disconnection experiment.

That gives the builder a concrete choice: inspect the prompt, change the validator, select another locally installed compatible model, and compare the saved responses. No provider API key or per-request inference bill is needed for this path, though electricity and hardware still cost money. The small model is also imperfect, and keeping its first bad response makes that tradeoff visible.

The tool currently accepts only synthetic or reviewed public data. Local inference is useful control over where computation runs; it is not a substitute for reviewing the input or securing the machine.

For this week, laziness means getting an evidence-backed starting point for the task you were going to do anyway. The decision about what to fix stays with the person reading the brief.
