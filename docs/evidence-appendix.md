# Lazy CI Triage evidence appendix

This supports the article about version 0.2.2, source commit `5a7727956c5432c7fc3229d577c73c1403c58420`. The article describes retained project evidence, not independently witnessed execution or proven human benefit. No new model inference was run for this editorial review.

## Claims and original sources

Project-relative paths below refer to the reviewed source ZIP/checkout. The `analysis/` folder belongs to the [downloadable evidence supplement](https://github.com/CosmonautJones/lazy-ci-triage/releases/download/v0.2.2/lazy-ci-triage-evidence-v0.2.2.zip). The original [ten-agent article review record](https://github.com/CosmonautJones/lazy-ci-triage/blob/main/docs/reviewed-ten-agent-record.md) describes the prepublication candidate, not a new review of publication edits.

| Claim | Original source | Important limit |
| --- | --- | --- |
| Inventory quote did not support precision explanation | First finding in `evidence/junit-run/report.json`; `fixtures/junit.xml` | Supplied logs do not establish the true price-failure cause. |
| Saved demo input and abstention | `fixtures/lexical-trap.log`; `evidence/support-demo-lexical-trap/report.json` and `.md` | Python already restricts this example to abstention. Video is an edited replay. |
| Individual counts and refusals | Fixture `fixtures/structural-support-heldout.json`; all 60 input/request/report sets and `comparison.json` in `evidence/support-individual/` | One recorded pass over authored synthetic cases, not representative CI accuracy. |
| Three indistinguishable copies | Complete input pairs H02/H28, H07/H29, H12/H30 in fixture and saved inputs | Opposing intended provenance cannot be inferred from identical bytes. |
| Coverage loss and refused quote | H01 and H13 input/reports under `evidence/support-individual/{baseline,candidate}-NN/` | H01 loses a supported label; H13 is missing due to refusal, not a correct abstention. |
| Poor six-record batches | All10 reports and `comparison.json` in `evidence/support-batch/` | Revised accepted batches contain zero correct specifics. More accepted reports do not imply better classification. |
| Retrospective rules comparison | Both `analysis/support_*_ablation.py` scripts, full result JSON/Markdown in `analysis/` | Shared parser/gate/validator, already-seen cases, no full runtime/CLI comparison. |
|78 recorded passing tests; no execution of suggestions | `evidence/test-results.txt`; production parser/brief/CLI/renderer/transport | Historical tests and bounded implementation checks, not accuracy or security certification. |

## Denominators and retained failures

There are 15 supported positives, 12 observable intended abstentions and 3 copied-input cases. All 30 remain in the records.

| Outcome | Earlier model | Revised model | Offline deterministic rule |
| --- | ---: | ---: | ---: |
| Correct specific labels / 15 supported |12|9|12|
| Specific-label disagreements with all 30 rubric labels |7|2|3|
| Disagreements excluding copies / 27 |5|0|0|
| Correct intended abstentions / 15 |9|13|12|
| Abstentions on supported positives / 15 |1|5|3|
| Missing due to refusal / 30 |1|1|0|

Each model workflow accepted29/ 30 reports. The rule extension's 30 selections pass the current validator. That checks IDs, source quotes and syntax, not semantic truth or usefulness. Separate six-record stress acceptance is 1/5 earlier and 2/5 revised reports; never pool those batch calls with the 60 individual calls.

The recorded individual range is 4.474132-12.303920 seconds, including loading and metadata/generation, not full parsing/rendering time. Saved runtime fields identify Qwen2.5-Coder 1.5B Instruct Q4_K_M, Ollama 0.18.0 and digest `d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668`. Hardware is recorded build context. Human time savings, repeated-run reliability, disconnected operation and a closed-API comparison were not measured.

## Reproduce without new weights

- The source ZIP can run inventory mode, product tests and saved-record checks without weights. Optional CommonMark integration ran in the recorded build environment.
- Baseline-policy replay in `tools/evaluate_support.py` needs Git history containing `f28d2e6ad7777d782c75dbf47013de0336eb2ee0`; ZIP-only distribution lacks that history.
- Both supplementary scripts require the exact 5a772795 checkout and pinned fixture/gate hashes. Clone the repository as `lazy-ci-triage` and check out `5a7727956c5432c7fc3229d577c73c1403c58420` for this exact software snapshot. Keep the extracted `lazy-ci-triage-evidence` folder beside it. From the supplement's `analysis/` folder, choose fresh outputs:

```powershell
python -B support_gate_ablation.py --repo ../../lazy-ci-triage --output ../new-gate-results
python -B support_contract_ablation.py --repo ../../lazy-ci-triage --output ../new-contract-results
```

The saved result files are unchanged. The family script's pinned Git HEAD was updated for the email-only history rewrite; its selection logic and input hashes are unchanged. The historical result JSON retains the original private-review commit identifier, mapped in `PUBLICATION.md`. New inference additionally needs an existing compatible local runtime/cache; inspect saved responses without rerunning it. Hashes pin retained contents, not historical chronology or absence of unrecorded attempts.

## Identities and remaining review gate

- Original reviewed source ZIP SHA-256: `c7bd9a05e320e32529fb7f4fc248ab754453db486e594bdd33f470b12d0982c9`.
- 56-second demo SHA-256: `a7e10f143c6c5d4099b30c3d8247271fe4248cd84509da130965882a28f804d3`.
- 30-case fixture SHA-256: `ea89c56033b22d24d4a490a1b042ca7af702e80e2b873003c680874f92238f87`.
- Contract-results SHA-256: `951e4d9716833b5f84bd29911326d26f4b56fcd53f12fb448ca574fe94651eaa`.

The article retains `fully_autonomous` disclosure. Publication changes are limited to public links, review-copy wording, email-privacy commit references and this reproduction layout. See [publication provenance](https://github.com/CosmonautJones/lazy-ci-triage/blob/main/PUBLICATION.md). Public post/contest visibility must be checked separately; no acceptance or prize is implied. Deadline: October 26, 2026, 06:59 UTC / 01:59 Chicago CDT. [Official requirements](https://dev.to/page/hacktoberfest-week3-2026-10-19-contest-rules).
