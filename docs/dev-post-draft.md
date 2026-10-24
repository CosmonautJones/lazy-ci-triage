---
title: "Lazy CI Triage: a small local experiment in reading failing tests"
published: false
tags: devchallenge, hf26challenge, python, opensource
ai_disclosure_level: fully_autonomous
---

*Unpublished review draft, written primarily by an AI agent. Public links and publication still require human approval.*

*Prepared for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19).*

## What I Built

An early version of Lazy CI Triage linked a synthetic inventory failure record to a rounding explanation. The citation existed. The explanation was wrong.

That failure shaped this small project for **Slow and Steady**: automate a little of the evidence-gathering chore before debugging, while keeping guesses visibly separate from the supplied log.

The Python CLI reads synthetic or reviewed public JUnit XML or pytest summaries. Python extracts test metadata and normalized failure detail. A local open-weight model selects a literal quote and a tentative category: assertion mismatch, missing key, refused connection, or unclassified.

The report shows parsed observations first and unverified model selections afterward. It refuses operational recommendations and never executes model-suggested commands. The cautious use case is **one failed test per input**. This is an experimental evidence index, not a production diagnosis tool. No human time savings have been measured.

## Demo

**[DEMO VIDEO LINK — insert approved public URL]**

The 56-second video shows a supplied failure line, the earlier CLI command and its actual saved report excerpt, followed by the comparison results and failures. It is clearly labeled as an edited replay, not live capture.

Inference used Qwen2.5-Coder 1.5B Instruct Q4_K_M through Ollama 0.18.0, on an RTX 3090 with 24 GiB VRAM and a Ryzen 7 5800X. The paired individual runs took 4.474–12.304 seconds each, including loading. Those timings describe these recordings, not a speed guarantee.

## Code

**[PUBLIC CODE LINK — insert approved repository URL]**

The standalone project and local Git repository began October 23, 2026. Code and authored synthetic fixtures use MIT; the external Qwen model uses Apache 2.0. Weights are excluded from Git. The application uses Python's standard library.

From the repository, the tests run without model weights:

```powershell
python -m unittest discover -s tests -v
```

The build environment passed 78 tests, including the optional CommonMark check and regressions for malformed-input stalls and decoded XML controls. Saved fixtures, request payloads, raw model responses, rejected attempts and measurements are included. Re-running inference requires an existing compatible local model; setup and exact digest are documented in the README.

## How I Built It

The useful change was to give the model a smaller job. Free-form explanations invented functions and database details. The current format permits only paired test/log IDs, a finite literal quote, a tentative family and fixed uncertainty. Python validates those selections; the model cannot write the observed section.

Quotes match decoded, normalized detail. For JUnit, XML type/message/body values are joined; this is not raw-byte XML quotation. Source authenticity and root cause remain unverified.

Word matching was also too permissive: a documentation mention of `KeyError` could grant a missing-key label. The revised gate requires recognizable failure syntax in both the record and quote, ignores pytest identifiers, and abstains when support is missing or conflicting.

A separate agent froze 30 synthetic cases before the candidate saw them. Real inference on each original case compared the reviewed baseline with the narrower gate:

| Outcome | Baseline | Revised |
| --- | ---: | ---: |
| Wrong specific labels against the authored rubric | 7 | 2 |
| Correct specific labels, of 15 supported cases | 12 | 9 |
| Accepted reports, of 30 | 29 | 29 |

Fewer wrong labels came with less useful coverage. Some JUnit type/message-only records now abstain. Both versions refused one wrapped-connection example because the selected quote lacked support.

Batching was worse: only 1/5 baseline and 2/5 revised six-record stress reports passed validation. Cross-record quote errors remain saved. The two remaining wrong individual labels come from unmarked copied tracebacks. Those inputs are identical to positive examples; no syntax check can recover the missing provenance. Citation validity does not prove that a claim follows from its evidence.

## Why Does Open Innovation Matter?

Open weights let this be a local experiment whose prompt, schema, validator and raw results can be inspected together. After runtime and model setup, inference uses a loopback endpoint without a provider API key. A disconnected-network test was not performed.

This pass reused cached weights; the initial build downloaded about 986 MB after reporting the size and license. Hardware and electricity still cost money. A rule-based classifier could cover part of this narrow task; AI is not claimed to be uniquely necessary.

The result is deliberately modest: a small source-linked starting point, with abstentions and failed experiments beside it. The maintainer still decides what the failure means.
