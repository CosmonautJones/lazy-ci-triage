# October 24 exact-checkout review follow-up

Starting checkout was clean at `278e67cc1d9926b57ef774f5024298ad40952890`. A fresh independent GPT-6 Astra high reviewer ran the full 52-test suite, replayed all 15 earlier evaluation rows, verified the five final prompt hashes/rendered reports and sampled all seven video cards. The reviewer blocked acceptance on three reproducible P2 defects and one P3 wording issue; this was not described as a final pass.

## Fixes and regression evidence

| Finding | Reproduction | Current behavior |
| --- | --- | --- |
| Parameter ID corrupted by ` - ` inside brackets | `test_x[a - b]` became `test_x[a` | Shared bracket-aware summary splitter preserves balanced IDs; ambiguous/unbalanced syntax is refused with JUnit guidance |
| Short real detail had an impossible quote enum | `<failure>x</failure>` had no valid option | Genuine nonempty options of 1–400 characters are supported consistently |
| Generated notes were treated as source | Empty failure offered `Failure recorded without details.`; long detail offered `[truncated]` | Empty detail stays empty; truncation is a separate flag; application notes are outside quotable detail |
| Historical table looked current | Old prose results labeled “Current citation contract” | Heading explicitly identifies historical v0.1 behavior |

New regression suite first ran RED (59 tests, nine failures). Fixes then passed 59 tests, with additional CLI/replay coverage added afterward. Empty-detail model mode now produces `insufficient_evidence` before any endpoint call; inventory retains the empty observation. A local HTTP fixture explicitly verifies zero requests. The isolated real server logged five generation requests for six current reports, matching the one pre-inference refusal.

“Literal” now explicitly refers to decoded/normalized detail. JUnit entities/attributes are decoded and type/message/body strings are joined; a quote need not be a raw-byte XML slice. Generated annotations remain separate. This clarification avoids promising provenance beyond what the parser records.

## Current real inference

Existing Qwen2.5-Coder 1.5B Q4_K_M weights only, same manifest digest and Ollama 0.18.0. No downloads or installs. `evidence/oct24-*` records five successful model runs and one explicit no-detail refusal. The parameter ID is intact, the one-character quote is accepted with `unclassified`, and the lexical-trap classification is still misleading. No diagnostic-accuracy or semantic-truth claim is made. See `docs/quality-comparison.md` and `evidence/oct24-evaluation.json`.

## Final independent gate

After all code, evidence, draft and demo changes are committed, the independent reviewer rechecks that exact candidate commit. Its final hash and verdict are supplied in the external handoff/review bundle. The repository is then left unchanged and clean; no “pass” is inferred from this preparation note or the earlier blocked review.

## Attachment and publication boundary

Current Library search is read-only and returned no matching artifact IDs. All three current helper sources are byte-identical to the earlier failed prepared-upload invocation; there is no new evidence that its missing capability is fixed. No upload retry, direct-create fallback or alternate route was used. No successful attachment ID means no claimed delivery. Public repository/video/DEV publication, contest acceptance and eligibility decisions remain unperformed. Current deadline and human decisions are recorded in `docs/submission-review.md`.
