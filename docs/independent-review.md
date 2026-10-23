# Independent review and disposition

2026-10-23. A fresh read-only reviewer (GPT-6 Astra, high reasoning) reviewed the whole new project at commit `e2cd005`, including source, tests, design, README and saved real-inference records. It did not change files or run GPU inference. It ran 23 existing parser, brief and evidence-replay tests successfully; socket-dependent full-suite evidence was supplied by the implementer.

Verdict before fixes: changes requested; no critical issues, four important findings and one minor. The following is a faithful finding summary with the implemented disposition. Full regression RED/GREEN results were observed in this build session; no second reviewer pass is claimed.

| Finding | Original severity | Reproduction | Disposition |
| --- | --- | --- | --- |
| Blank lines let untrusted Markdown escape `p` blocks | Important | Multiline hypothesis/test name activated remote Markdown images under CommonMark | Fixed using escaped `pre` blocks at the start of HTML blocks for every untrusted field, including citation quotes. Actual CommonMark regression failed before fix, passed after. |
| Parameterized pytest IDs containing spaces were omitted | Important | Two failed tests yielded only one parsed record | Fixed node ID parsing; parameter text retained. Regression failed before fix, passed after. |
| Application `ERROR`/`FAILED` lines fabricated tests | Important | `ERROR database - connection lost` parsed as a pytest test | Require recognizable Python `.py::test` node IDs; unrelated log levels are rejected. Regression failed before fix, passed after. Added final failure-count consistency check to reject partial extraction. |
| Lone Unicode surrogate passed validation and crashed Markdown output | Important | Escaped `\ud800` in model text created `ok` JSON before UTF-8 encoding failed | Reject invalid Unicode in brief fields and local API metadata; pre-render/encode outputs before creating directory; catch encoding errors. Validator and runtime regressions failed before fix; CLI regression confirms an error report and exit 3. |
| Broken chunk framing escaped HTTP error handling | Minor | Real local test server sent an unfinished chunk | Regraded Important because clear inference-failure states are a required behavior; catch HTTP protocol exceptions. Real malformed-chunk regression raised before fix and returns `invalid_response` after fix. |

Final fix-pass verification: **38 tests passed**, including CommonMark rendering, CLI malformed Unicode and actual loopback HTTP framing tests. No failed tests, skips or deferred review findings in the demonstrated environment. On machines without optional `markdown-it-py`, one CommonMark integration test skips; runtime requires only Python standard library.

## Review scope rulings

- External contest terms, licensing and publication compliance: reviewer did not independently browse. Builder verified official challenge/rules/disclosure and model license separately; parent remains responsible for final eligibility and publication review.
- Inference, hardware and download provenance: reviewer checked saved consistency only. Actual tool-run evidence, model digest and hardware details are recorded in `evidence/README.md`; no independent inference reproduction is claimed.
- Model accuracy and injection resistance: tiny synthetic examples do not establish either. Remaining semantic mistakes are explicit in `evidence/README.md` and the DEV draft. Cost if this limit is ignored: a human could act on an unsupported hypothesis despite correct citations.
- Full HTTP suite: reviewer did not rerun it. Builder's fresh whole-suite run covers those boundaries; no claim that the reviewer ran all 38 tests.

Deferred minors: none. Remaining product limits are documented scope boundaries, not hidden review findings.
