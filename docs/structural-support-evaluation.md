# Structural-support evaluation, October 24

Baseline: independently reviewed `f28d2e6ad7777d782c75dbf47013de0336eb2ee0` (v0.2.1), unchanged in Git. Candidate gate was frozen before opening the independent held-out cases; its `brief.py` SHA-256 is `c088efeed405e44dca61733f7a08bb1e802aa86806c801ff735a4bfb3f839677`. The file is not tuned to held-out outcomes.

The independent author created 30 cases without reading production classification code: 15 actual-family examples, 12 observable abstention examples and three deliberately indistinguishable copied-traceback examples. The latter have byte-identical positive partners and opposing provenance intentions. Neither rules nor a model can infer that missing provenance. Original freeze SHA-256: `ea89c56033b22d24d4a490a1b042ca7af702e80e2b873003c680874f92238f87`. See `fixtures/structural-support-heldout.json` and its [author's rationale](structural-support-heldout-rationale.md). This is a tiny synthetic stress test, not an accuracy estimate for real CI data.

## Method

`tools/evaluate_support.py` obtains the exact baseline modules with local `git archive`; it does not check out another task or fetch anything. For deterministic eligibility it parses each original input in its original format. The primary paired real comparison runs each case separately, with its exact original input/format and no case ID, expected label, category, rationale or hard-limit flag sent. Both versions use the normal product path, identical input bytes and frozen order.

A first six-case pilot joined already-parsed normalized details into synthetic JUnit files, using opaque case IDs as wrapper names. Both policies received identical combined bytes. This exposed cross-record quote errors that confound classification; it is retained as a separate stress test rather than silently replaced by the individual comparison. Batching adds context and changes input packaging. All payloads, original inputs, raw responses, statuses, metrics and rejected attempts are retained. The whole batch is refused if any selection violates the contract; refused proposals are never counted as accepted classifications.

The model/runtime/options are unchanged: cached Qwen2.5-Coder 1.5B Instruct Q4_K_M, manifest `d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668`, Ollama 0.18.0, temperature 0, seed 42, context 32768, output cap 1800, unload after each request. RTX 3090 24 GiB / Ryzen 7 5800X; no hardware isolation or statistical latency benchmark. No downloads or installations.

## Deterministic eligibility, before model inference

| Measure | Baseline | Candidate |
| --- | ---: | ---: |
| Cases allowing any wrong specific family, all 30 | 10 | 3 |
| Observable abstention cases allowing a specific family, of 12 | 5 | 0 |
| Unmarked copied examples allowing a specific family, of 3 | 3 | 3 |
| Correct specific family available, of 15 actual-family examples | 15 | 12 |
| Only abstention offered, all 30 | 7 | 15 |

These are opportunities allowed by the gate, not model choices. The three supported cases lost are H01, H06 and H11: qualified JUnit exception type plus message, no colon or traceback body. The parser joins those metadata fields, and this conservative text gate cannot recover the type boundary. They now abstain despite the authored expected label. This loss is accepted provisionally for fewer unsupported labels, not disguised as a parser failure or a solved classification problem. A future metadata-aware design would require separate testing; this pass does not add one.

## Remaining limits

Anchored syntax narrows the failure channel but cannot establish truth or relevance. Arbitrary supplied content can mimic exception lines, assertion code or expected/got summaries. Real unfamiliar, abbreviated or truncated errors can lose coverage. Chained/conflicting signatures abstain conservatively. Literal quotes may still be verbose or unrepresentative. Root cause, implementation, environment and source authenticity stay unverified; operational advice remains refused.

Historical reports are immutable statements of their version's behavior. The old lexical-trap selection is now rejected by the candidate; old request hashes are checked against five frozen payloads independently reproduced with the exact baseline, rather than silently treating a changed prompt as the old one. Historical normalized source/citation integrity remains tested.

## Six-case stress test: failed reports are part of the result

Ten real model calls completed, five per policy. Baseline accepted one batch (6 selections), refused four; candidate accepted two (12 selections), refused three. Baseline had 5 correct specific selections and 1 wrong specific selection among accepted results. Candidate had 0 correct specific selections, 9 correct abstentions and 3 wrong specific selections, all copied examples. Missing selections due to whole-batch refusal: 24 baseline, 18 candidate. This batch test does **not** establish better useful specific coverage; the candidate's positive batches were refused. Cross-record quote assignment and selecting options without the required support were both observed. Small-model, multi-record reliability remains a material limit, with one failed test per input the more conservative usage. The separate original-case run isolates classification behavior; it does not erase these failures.

## Reproduction

From this Git repository, with Python and Git installed:

```powershell
python tools/evaluate_support.py --output reports/support-gate
```

The comparison requires local Git history containing the pinned baseline commit. A source ZIP alone can run the application and tests, but does not contain that history. It can inspect the saved comparison, requests and raw responses without rerunning the baseline tool.

With the existing local runtime/cache started as in README, add `--inference` and use a fresh output directory. By default this makes 60 sequential model calls (30 per policy), with loads included. `--batch-size 6` reproduces the separate ten-call stress-test packaging. No weights are pulled. Safe committed results live in `evidence/support-individual` and `evidence/support-batch`; developer scratch baseline modules are excluded from the release bundle. The completed individual results and retain decision are recorded below.

## Actual individual-case model results and decision

Sixty paired, sequential real inference calls completed, one original case per input, 30 per version. All attempts are retained; no failed attempt was retried or replaced. The gates and prompts were frozen before reading held-out outcomes.

| Model outcome, all 30 cases per version | Baseline | Candidate |
| --- | ---: | ---: |
| Accepted selections | 29 | 29 |
| Wrong specific selections against authored rubric | 7 | 2 |
| Correct specific selections, of 15 supported cases | 12 | 9 |
| Correct abstentions, of 15 intended-abstention cases | 9 | 13 |
| All accepted abstentions, including coverage loss | 10 | 18 |
| Missing selections due to refused report | 1 | 1 |
| Wrong specific selections on the 3 unknowable copied examples | 2 | 2 |

Wall times across these 60 calls ranged from 4.474 to 12.304 seconds, including loading and metadata/transport. This range describes the recorded calls, not a stable latency guarantee. Every call records the same model digest and options; token counts and per-phase durations remain in JSON.

**Decision: retain the narrower gate as a bounded conservative improvement.** It reduces accepted unsupported specific labels while retaining useful positive selections on these independently authored examples. It also loses useful coverage; this is not a Pareto improvement or a universal classifier. The six-record stress test remains poor, so the result is strongest for a single failed test per input. A later metadata-aware improvement or per-record inference architecture would need a separate design/evaluation, outside this pass.

The three type/message-only cases H01/H06/H11 lose their family at the gate. The model additionally abstains on supported assertion cases H02 and H04 despite eligibility; baseline also abstains on H04. H13, a wrapped refusal, is refused under both policies because the model chooses a quote without the required support. These are distinct losses: gate restrictions, model abstention and validation refusal. None is counted as a correct diagnosis or silently removed.

For a concise semantic inventory, compare each row's expected/selected/status. Observable false labels, coverage misses and hard-limit copies remain separately identifiable by case ID. Source observations are Python output; accepted categories are always model hypotheses with fixed uncertainty. A syntactically valid category can still be wrong, and citation validity proves neither relevance nor claim entailment.

| Error class | Baseline accepted examples | Candidate |
| --- | --- | --- |
| Other-family word inside an assertion | H03 selected missing_key | H03 selects assertion_mismatch |
| Documentation prose or quoted example | H16 assertion, H17 missing key, H18 refused connection | All three abstain |
| Explicit denial of refusal | H23 selected refused connection | Abstains |
| Unmarked copied traceback with missing provenance | H29 missing key, H30 refused connection | Both remain wrong against intended provenance rubric |
| Supported family lost to conservative gate/model | Positive cases missed or refused | H01/H06/H11 gate abstention; H02/H04 model abstention; H13 quote refusal |

Both versions may produce different selections even for identical inputs/options in these recordings. The duplicated hard-limit pairs are evidence that provenance cannot be inferred, not a promise of deterministic model text or a diagnostic scoring shortcut. Seed and temperature settings do not establish cross-run identity.
