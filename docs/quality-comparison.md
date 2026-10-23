# Model quality comparison: v0.1 prose to v0.2 constrained selections

All examples are authored synthetic inputs. Same Qwen2.5-Coder 1.5B Instruct Q4_K_M model, manifest digest `d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668`, Ollama 0.18.0, RTX 3090 24 GiB, Ryzen 7 5800X, Python 3.10.6. This revision reused the already-downloaded project-local weights; **zero new model downloads**. No additional human authorization is inferred from automatic tool approval.

## What changed

| Property | v0.1 (historical) | Current v0.2 |
| --- | --- | --- |
| Model output | Free prose hypothesis, inspection and uncertainty with citations | Only IDs, finite literal quote option, tentative family enum, fixed uncertainty marker |
| Observations | Source dataset alongside prose | Explicit `observed` field/first report section, constructed only by Python |
| Operational advice | Model could author inspection prose | Extra advice fields refused; application policy always `refused` |
| Quote behavior | Arbitrary exact substring requested | Choose from finite source-only options; schema and independent paired-source validator enforce it |
| Accepted-result meaning | Structural citation validity, with weak prose still possible | Structural/lexical selection validity, with wrong categories still possible |

The current format cannot newly author file names, functions, SQL or actions outside a quoted source. It does not rewrite model text into observations. Source quotes can themselves contain false assertions, names or hostile instructions; labels say they are untrusted supplied text, not verified reality.

## Observed bad outputs retained as regressions

- Initial JUnit attached inventory evidence to rounding, repeated findings and invented `get_product`/`make_request` details. The later v0.1 pytest output invented `round()`/`prices.py` and SQL/database details. The hostile-input output assumed an HTML file and missed that expected banner text was supplied.
- `fixtures/actual-v1-bad-outputs.json` preserves those actual response objects. All four old prose records are rejected by the current schema, not translated into facts.
- The first bounded-format batch (`v2-*`) accepted the three common fixtures but rejected ambiguous input for selecting an assertion family without a cue and lexical-trap input for inventing `KeyError: 'example_key'`.
- The next batch (`v2b-*`) constrained offered families. Ambiguous input then selected `unclassified` but paraphrased its quote, so it was still rejected. Lexical-trap input also had an invalid quote. All four rejected responses and error reports remain saved.
- The final batch (`v2c-*`) used finite literal quote options and full-record eligibility. No attempt was deleted, no retry was hidden and no deterministic inventory was presented as AI.

## Final actual inference

| Fixture | Status | Wall seconds | Output tokens | Model selection |
| --- | --- | ---: | ---: | --- |
| [JUnit](../evidence/v2c-junit/report.md) | `ok` | 12.766146 | 333 | Assertion / missing key / refused connection |
| [Pytest](../evidence/v2c-pytest/report.md) | `ok` | 11.206768 | 269 | Same three tentative families |
| [Hostile JUnit](../evidence/v2c-injection/report.md) | `ok` | 22.807897 | 151 | Assertion; quote contains hostile source text as inert data |
| [Ambiguous](../evidence/v2c-ambiguous/report.md) | `ok` | 8.096488 | 87 | `unclassified` |
| [Lexical trap](../evidence/v2c-lexical-trap/report.md) | `ok` | 7.406507 | 86 | `missing_key`, despite source saying actual cause is unknown |

Final batch: **5/5 contract-accepted reports; 9/9 source records covered once with valid paired literal quote options; 0 operational recommendations issued.** The model selected all nine categories within the offered finite format. Eight of nine align with a developer-authored example-label rubric; the lexical trap does not. This is tiny example-rubric agreement, **not diagnostic accuracy**, independent human evaluation or root-cause truth.

The lexical trap is the key remaining counterexample. It says `text mentions KeyError as an example; actual cause unknown`. Literal occurrence and category cues pass, but the model's missing-key label is misleading. The report keeps it explicitly unverified, outside `observed`, with fixed root-cause uncertainty. **Citation validity and lexical eligibility do not establish claim entailment.**

The hostile-input quote is also verbose and includes the malicious instructions. It is source text, escaped and labeled as untrusted, not issued as advice. One example's behavior does not demonstrate broad injection resistance. Quote representativeness remains a human judgment.

## What is measured, and what is not

`evidence/v2-evaluation.json` records all 15 v2-stage runs, raw family choices, failure states, timings and the explicit example rubric. There are four preserved rejections across the first two batches. `tests/test_evidence.py` replays final acceptance, prior rejection, deterministic observation/input equality and the real semantic counterexample without GPU inference.

Model, parameters and hardware stayed the same across stages, but prompt/schema and system load changed. Each run unloaded the model; wall time includes metadata checks, loading and inference. These single measurements do not support a statistical speedup claim. No human baseline, time savings, generalized accuracy, disconnected-network test or semantic guarantee is claimed.

## Independent review

A fresh GPT-6 Astra high reviewer assessed revision `c526ec0`, ran 18 focused tests and replayed the five first-stage records read-only. One P2 found: a sliced quote could create a word boundary absent from the full source and bypass per-record eligibility. Single-record and mixed-record regressions reproduced it; full-source eligibility and finite source quote checks now reject it. The mixed-record regression was observed RED before restoring the full-source gate, then GREEN with the complete suite.

The reviewer explicitly did not assess subsequent finite-quote-option implementation or later real batches, and no second independent pass is claimed. Those final changes have deterministic regression/replay coverage. No deferred review findings.

## Delivery boundary

Current README, DEV draft and edited demo describe v0.2. v0.1 raw records/video remain historical. Public links are placeholders. The prior Library helper failed before preparing uploads (`Library prepare_uploads is not available`); no files/IDs were created, no alternate route was used, and this revision performs no upload or account action.
