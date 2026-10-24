---
title: "Lazy CI Triage: a real citation can still support a bad explanation"
published: false
tags: devchallenge, hf26challenge, python, opensource
ai_disclosure_level: fully_autonomous
---

*Unpublished draft for human review. Written primarily by an AI agent at the user's request. Replace the public-link placeholders only after separate approval.*

*A submission draft for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19).*

## What I Built

A citation can be real and still sit beside a bad explanation. The first local CI brief in this project did exactly that: it linked a real inventory error to a rounding hypothesis. Another run suggested a SQL query where the supplied log established only a `KeyError`.

Lazy CI Triage started as a small way to reduce the chore before debugging: read a failure file, identify the tests and collect the lines worth inspecting. Its current version keeps that job small. Python extracts observed metadata and verbatim source excerpts. A local model selects an exact excerpt and a tentative broad failure family for each failed test. The report puts those two sources of information in separate sections.

"Observed" means the file was parsed into metadata and normalized detail. For JUnit, XML values are decoded and failure type/message/text are joined; a quote matches that normalized record, not necessarily raw XML bytes. It does not prove tests ran, a named file exists or the text is truthful. "Model hypothesis" means an unverified category selection. The tool issues no operational recommendations and runs no suggested commands.

That is the Slow and Steady idea: get a bounded evidence index for the task you were going to do anyway. The maintainer still decides what the failure means. No human time savings have been measured.

## Demo

**[VIDEO OR DEPLOYED DEMO LINK — pending review and publication approval]**

The local video, `evidence/lazy-ci-triage-demo.mp4`, is an edited walkthrough of saved actual inference results, explicitly labeled as a replay rather than live terminal capture. Original synthetic inputs, raw responses, rejected attempts and measured timings are included with the code. The current comparison is in `docs/quality-comparison.md`.

The model is Qwen2.5-Coder 1.5B Instruct Q4_K_M, served by Ollama 0.18.0 on an RTX 3090 with 24 GiB VRAM and an AMD Ryzen 7 5800X. Every run records the model digest, options, input hash, wall time and token counts. These are tiny synthetic examples, not a latency benchmark or productivity study.

The useful screen to pause on is the boundary between the two report sections. A missing-key example contains the parsed test name and error detail first; the model's “possible missing-key failure” label comes afterward, with uncertainty and a link back to the quoted detail. Neither the label nor the generic review question becomes an observed fact.

## Code

**[PUBLIC CODE LINK — pending repository publication approval]**

This standalone project and its Git repository began on October 23, 2026, within the Week 3 window. Project code and authored synthetic fixtures use MIT. The external Qwen model uses Apache 2.0; weights are excluded from Git. The current Python CLI has no third-party runtime dependencies.

## How I Built It

The useful change was to ask the model to do less.

The initial format allowed a hypothesis, an inspection step, uncertainty text and citations. Python verified paired IDs and exact quotes, but that did not stop invented functions or explanations. A prompt asking the model to stay tentative helped some outputs and failed on others. Correct references were never a substitute for checking what the sentences claimed.

The revised format has no free-form explanation or recommendation field. The model chooses only:

- paired test and log IDs;
- one literal quote from finite options derived from that record;
- a tentative family: assertion mismatch, missing key, refused connection, or unclassified;
- a fixed uncertainty marker saying root cause is unverified.

Python independently validates those choices. It supplies the observed section directly from parsed input. Unknown fields, model-authored observations, invented quotes, duplicate coverage and operational advice are rejected. The report uses fixed tentative descriptions and application-authored review questions, with their origin stated.

A fresh review found a more mundane provenance bug: the parser had inserted “no details” and truncation markers into quotable text. Those generated notes now stay outside evidence. Real one-character detail is supported; a failure with no detail produces an explicit `insufficient_evidence` report before any model request. Pytest parameter IDs containing ` - ` are preserved, while ambiguous bracket syntax is refused with guidance to use JUnit. The saved observations need the same scrutiny as the AI output.

The family checks are deliberately modest. `KeyError` must appear as a textual cue for a missing-key label, for example. That is lexical eligibility, not semantic entailment. A documentation example can mention `KeyError` while the actual cause remains unknown. A test preserves that counterexample rather than claiming the validator can decide truth.

Real inference exposed another small-model weakness: even when it selected “unclassified,” it sometimes paraphrased the requested quote. Those attempts were rejected and preserved. The final extractive format offers literal quote choices to constrain that failure channel. It still cannot guarantee that the selected quote is representative or that a selected category is useful.

In the final five-fixture run, all nine source records had valid paired quote selections. An ambiguous status-code message yielded “unclassified.” But a deliberate trap still yielded a misleading missing-key label: its text mentioned `KeyError` only as an example and said the actual cause was unknown. The label passed the lexical checks. It remained an unverified model selection, not an observed fact. That is a useful boundary to show in a demo, rather than hide behind a passing validation count.

The CLI reads one explicitly named synthetic/public file, calls only a numeric loopback endpoint and writes Markdown plus JSON. Hostile source text is escaped, and rejected raw output stays in audit JSON rather than appearing as accepted advice. No agent tools, auto-fixes, runtime installation or model pull happen inside the application.

## Why Does Open Innovation Matter?

The open-weight model makes the selection step a local, inspectable experiment. The prompt, schema and validator can be changed together, and the raw results can be compared. Once the existing runtime and weights are installed, inference needs no provider API key or external inference service. The recorded requests used loopback; a separate network-disconnection experiment was not performed.

This revision reused the same cached weights. The initial build had downloaded about 986 MB after reporting the exact need, size and Apache license first. Hardware and electricity still cost money, so “local” does not mean costless.

The tradeoff is visible in the repository: the tighter format prevents newly authored prose from inventing files or telling someone to restart an imagined database. It also gives up nuanced explanations. A rule-based classifier could cover parts of this narrow task; the project tests a real model's excerpt/category selections rather than claiming AI is uniquely necessary.

For me, the useful result is a smaller, more honest starting point. The model gets a bounded role. The human gets the source beside it, including the cases where the tool refused a result.
