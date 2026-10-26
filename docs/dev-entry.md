---
title: "Lazy CI Triage and the limits of a correct citation"
published: true
tags: devchallenge, hf26challenge, python, opensource
ai_disclosure_level: fully_autonomous
---

*Written primarily by AI agents under my direction.*

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19).*

## What I Built

The first version of Lazy CI Triage cited an inventory error while explaining a price-rounding failure. Both came from a synthetic test file. The inventory quote was real, but it did not support the explanation.

That became the constraint for this project: keep the supplied evidence separate from what the model thinks it means.

Lazy CI Triage is a small experimental Python CLI. It reads JUnit XML or supported pytest short summaries and makes an index of failed tests. Python extracts the test metadata and failure detail. A local open-weight model selects a literal quote and a tentative category: assertion mismatch, missing key, refused connection, or `unclassified`, meaning no specific label.

The intended user is someone inspecting one failed test, or building a similar tool and checking its boundaries. The hoped-for payoff is less manual gathering before debugging. **We have not measured human time savings or shown that the model adds value over simple rules.** One failed test per input is the cautious use case; batches remain unreliable.

## Demo

**[56-second demo video](https://github.com/CosmonautJones/lazy-ci-triage/releases/download/v0.2.2/lazy-ci-triage-demo.mp4)**

Here is the synthetic failure line shown in the saved demo:

```text
FAILED tests/test_docs.py::test_error_example - text mentions KeyError as an example; actual cause unknown
```

The saved report keeps the two kinds of output distinct:

| Report part | Actual saved result |
| --- | --- |
| Python observation | `tests/test_docs.py::test_error_example`, line 2, `T001 / L001` |
| Model selection | `unclassified` |
| Selected quote | The complete failure line above, checked against that same record |
| Uncertainty | Root cause unverified; operational recommendations refused |

The category rules already require abstention on this example. It shows how the report presents a boundary, rather than demonstrating extra intelligence from the model.

The 56-second video is an edited replay of saved input, the earlier CLI command, report excerpts and comparison results. It is not live capture. The later rules-only analysis below is in the separate evidence appendix.

You can reproduce the parsed observations without weights or a running model:

```powershell
python -m lazy_ci_triage fixtures/lexical-trap.log --format pytest --public-data --mode inventory --output reports/article-inventory
```

Use a new output directory. Inventory mode reproduces the observations, not the historical model response. `--public-data` acknowledges that you reviewed the input; it does not scan for or redact secrets or personal data. Use synthetic or reviewed public inputs only.

## Code

**[Lazy CI Triage source code](https://github.com/CosmonautJones/lazy-ci-triage)**

The standalone project and local repository began October 23, 2026. The reviewed software is version 0.2.2, published at commit `5a772795` after replacing private Git author emails. Its files match the reviewed software tree. Project code and authored synthetic fixtures use MIT. The external Qwen weights use Apache 2.0 and are excluded from Git. The application uses Python's standard library.

The saved build log records 78 passing tests, including the optional CommonMark check in that environment. Tests run without model weights:

```powershell
python -m unittest discover -s tests -v
```

The source includes fixtures, requests, raw responses and refused attempts. The README documents supported formats, limits, runtime setup and the exact model digest.

## How I Built It

The model gets finite choices for paired test/log IDs, source quotes, a category and a fixed uncertainty marker. Python validates the selections and writes the observed section itself. For each record, the validator permits only abstention when recognizable failure signatures are absent or conflicting. A specific category must have matching syntax in both the record and selected quote. An invalid selection can cause the whole report to be refused.

For JUnit, quotes match decoded, normalized type/message/body detail, not raw XML bytes. Hostile instructions can remain in quoted source data; the tool escapes their markup and never executes them. It refuses operational recommendations. These checks establish traceability and structural eligibility, not source authenticity, root cause or semantic truth.

One recorded pass compared earlier and revised workflows on 30 authored synthetic cases prepared by a separate AI agent. There were 15 supported cases, 12 observable intended abstentions, and three copied-traceback cases. Each copied case has the exact same input as a positive example but a different intended provenance label. That missing context cannot be recovered from the bytes.

Each workflow made 30 real model calls. These are results against the authored rubric, not a real-world accuracy estimate:

| Outcome | Earlier workflow | Revised workflow |
| --- | ---: | ---: |
| Correct specific labels, of 15 supported cases | 12 | 9 |
| Specific labels disagreeing with the rubric, across all 30 | 7 | 2 |
| Those disagreements excluding the three copied cases, of 27 | 5 | 0 |
| Reports passing validation, of 30 | 29 | 29 |

Fewer rubric disagreements came with fewer correct specific labels. For example, a JUnit failure with type `builtins.AssertionError` and message `expected total 9, observed 12` received an assertion-mismatch label before the change and abstained afterward. Both workflows also refused one wrapped-connection case after selecting a quote without the required support.

The separate six-record stress test was poor: only 1/5 earlier and 2/5 revised reports passed validation. The accepted revised batches contained no correct specific labels. Those failures remain saved.

We then checked whether a model was needed for this narrow selection task. A retrospective rule reused the current parser and category gate across all 30 already-seen cases. It selected the sole permitted specific category or abstained. An extension chose the first eligible same-record quote, added the required IDs and uncertainty, and called the unchanged validator. All 30 deterministic selections validated.

On the same 15 supported cases, the rule selected 12 correct specific labels; the revised model selected 9. Neither made a wrong specific selection on the 27 cases excluding the copied examples. On the three copies, the rule disagreed with all three intended abstention labels and the model with two.

This check shares the existing implementation and seen cases. It is neither a new held-out benchmark nor an equivalent end-to-end runtime test. It does not establish that rules are generally superior, but it leaves model-added usefulness unproved here. Repeated-run reliability and human debugging benefit were not measured.

The **[evidence appendix](https://github.com/CosmonautJones/lazy-ci-triage/blob/main/docs/evidence-appendix.md)** contains the separate rule scripts, all 30 selections and reproduction requirements. It is additional to the original source ZIP. Replaying the earlier workflow requires Git history containing the pinned baseline; the ZIP alone does not include that history.

For this write-up, I asked ten separate AI reviewer agents, our review council, to challenge the implementation, evidence and prose through separate first reviews and a shared claims ledger. Their scoped decisions and caveats belong in the accompanying review record. These are project reviews, not an outside expert panel or independent empirical validation.

## Why Does Open Innovation Matter?

Open weights let us run this model on our own machine. The project also makes its prompt, validator and retained results available for inspection. Inference uses a loopback endpoint without a provider API key. A disconnected-network test and a measured closed-API comparison were not performed.

The recorded runs used Qwen2.5-Coder 1.5B Instruct Q4_K_M through Ollama 0.18.0, on an RTX 3090 with 24 GiB VRAM and a Ryzen 7 5800X. The 60 individual comparison calls took 4.474-12.304 seconds each, including loading. That is a recorded call range, not a full-CLI speed guarantee.

The initial build downloaded about 986 MB after reporting the size and license. Later work reused those weights. Hardware and electricity still cost money.

What I can share is a working evidence index and an inspectable local-model experiment, including the cases where the model did less than the rules. If you are building something similar, the inventory command and saved results give you a starting point for deciding how much work to hand to the model.
