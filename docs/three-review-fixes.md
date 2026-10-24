# Three independent review findings and fixes

Initial frozen candidate: `81e245abe8e6fc7ae37374895538bd55b47fc4f2`; prior reviewed software/evidence baseline `e6def752a09090993bfaca9e5add34e441691df4`. Three fresh agents reviewed code, evidence and entry/media independently before seeing each other's findings. Initial PASS1 was BLOCK, PASS2 PASS, PASS3 BLOCK. Initial reports and reproduction evidence remain outside this checkout under `review-three/`; no unfavorable model output or prior archive was removed.

## Parser boundary repairs

PASS1 reproduced severe backtracking in the pytest summary detector `^=+.*=+$` on small malformed equals-prefix lines. The fix uses explicit prefix/suffix checks with the same minimum delimiter shape. A bounded subprocess regression at the 262,144-byte input limit failed at its three-second deadline before the fix and passes afterward. The child deadline protects the test; it is not a portable performance guarantee.

Inspecting the related delimiter scan exposed another stall: scanning a long whitespace run repeatedly matched/copy-sliced the remaining text at each character. A second subprocess regression with a 200,000-space unsupported node failed at its three-second deadline. The scan now considers each whitespace run once and uses a compiled pattern's position argument, avoiding repeated suffix copies. Existing parameter-delimiter behavior remains covered.

PASS1 also reproduced XML numeric references decoding into disallowed C1/DEL controls after raw-source screening. The parser now screens decoded testcase name/classname and joined failure type/message/body before whitespace stripping. Regression cases cover body, message, type, name and classname, including a control that strip() would otherwise erase. These are input errors, not an impossible quote contract or a new redaction feature.

Four new tests observed RED (first three: twelve failures; added whitespace regression: one deadline failure), then GREEN. Full suite: **78 tests in 10.315 seconds, OK, no skips**, including optional CommonMark integration and all saved-inference replay checks. Compileall and working-diff whitespace checks passed. The previous 74-test log remains `evidence/test-results-pre-three-review.txt`.

## Concrete demo repair

PASS3 found the former video consisted only of overview/result-summary cards. Two cards now show the original `fixtures/lexical-trap.log` failure line, the earlier executed CLI form, and a formatted excerpt of the actual saved report: observed T001/L001, source test/line, exact quote, unclassified selection, fixed uncertainty and operational refusal. The example remains a single supplied failure, not a production diagnosis. The video is visibly labeled edited replay, not live capture; no new inference was run.

The other cards retain false-specific reduction7 to2, correct-specific coverage12/15 to9/15, accepted reports29/30 per policy, weak six-record batches1/5 to2/5, copied-example provenance limits and loading-inclusive timings. No failed experiment is hidden. The previous MP4 is preserved as `evidence/lazy-ci-triage-v0.2.2-summary-demo.mp4`. New MP4: H.2641280x720, silent56.000s,327,748bytes; SHA256 `a7e10f143c6c5d4099b30c3d8247271fe4248cd84509da130965882a28f804d3`. Caption spacing and the article's explicitly synthetic opening were clarified; challenge attribution/link is restored.

## Evidence and final review gate

All frozen cases, original model input files, raw responses, request payloads and evaluation summaries are unchanged. The model prompt, selection schema, family gate and runtime are unchanged. No new download, installation, inference, account action, Library write, public publication or contest acceptance occurred. The parser repair is checked against all saved normal inputs rather than claiming new model quality measurements.

Affected code/media reviewers recheck the repaired exact candidate; the evidence reviewer checks the regenerated source archive and retained measurements. All three final exact-source/artifact signoffs, new archive hashes and clean-checkout proof are supplied in the external handoff after freezing this source. These reviews cannot establish universal correctness, real-world accuracy, eligibility or successful public submission.
