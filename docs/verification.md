# Build and verification ledger

Plan: `docs/superpowers/plans/2026-10-23-lazy-ci-triage.md`

Authorization: supplied delegation requests a bounded design and immediate implementation; optional brainstorming confirmation gates are waived by that explicit instruction.

Ruling: use a new nested repository on branch `build`, rather than a worktree of an existing repository, because challenge requires a brand-new project. No existing checkout read or changed.

Pre-flight: Task 1 Dataset records feed Task 2 prompt/validator and Task 3 runtime. Task 2 validated dictionary feeds Task 3 renderer. Names and IDs remain consistent across interfaces.

Inventory: Python 3.10.6, Git 2.33.1.windows.1, Ollama 0.18.0, RTX 3090 24 GiB. Default Ollama cache empty; relevant Hugging Face language-model cache incomplete. No usable cached model found in the inspected relevant defaults.

Model need reported before download: Qwen2.5-Coder 1.5B Q4_K_M, Apache 2.0, weights 986048576 bytes, support/config 13513 bytes, total 986062089 bytes. Model will be stored in ignored project-local `.runtime`, using existing Ollama and loopback port 11439; no new runtime install or global settings.

Task 1 complete: parser tests first failed with absent implementation, then 11/11 passed. Commit c3d993f. Inputs cover JUnit failure/error/namespaces, duplicate pytest names, malformed/oversized/UTF-16/entity-bearing inputs, truncation and hostile text as data.

Task 2 complete: schema/citation/coverage/render tests failed before implementation, then 18/18 whole suite passed. Commit 4495227. HTML and Markdown source text is inert in HTML blocks.

Task 3 complete: CLI/transport test stubs failed with 17 assertion failures, then 27/27 whole suite passed with loopback permissions. Socket access is restricted by the execution sandbox, so deterministic local HTTP test servers require command escalation here; this is an environment restriction rather than an application fallback. Ordinary Python-only tests run inside the sandbox.

Real inference first attempt: `evidence/junit-run`, 43.502795s, 843 output tokens, weak and duplicated hypotheses. Raw output preserved. Ruling: tighten prompt and reject repeated evidence, rather than hide the flawed run; the validator checks traceability, not semantics, and incorrect diagnoses remain possible.

Refinement RED/GREEN: two tests first failed (repeated citation accepted, schema allowed excess findings); added repeated-evidence rejection and findings bound. Also reproduced/fixed a pytest passing-summary edge case that hid a reported error. Full suite then 30/30 passed. An interrupted HTTP-body characterization test passed with existing malformed-response handling; no transport patch was needed.

Real inference refined JUnit 20.993951s / 378 output tokens; pytest 27.117923s / 477; hostile JUnit 7.863337s / 123. All current-contract runs structurally accepted, 7/7 paired exact citations and full failure coverage. See `evidence/README.md` for remaining semantic errors. No claimed human baseline or accuracy score.

Task 4 in progress: draft README, DEV template with `fully_autonomous`, demo script and rules checklist exist. Independent read-only review requested on commit e2cd005; evidence replay tests and measured-run notes added during review.

Independent review returned four Important issues and one Minor (no Critical). See `independent-review.md`. Final Ruling: malformed chunked HTTP is Important for this tool's explicit failure-state contract, so include it in the same fix pass. Cost if left unfixed: malformed local responses would crash rather than produce an error report.

Review-fix RED: 37 tests ran, 8 assertion failures and 1 uncaught broken-chunk error. Covered active Markdown images from blank lines, omitted parameter IDs, application logs fabricated as tests, unmatched summary counts, invalid Unicode fields/metadata and HTTP chunk framing. A further quote-specific CommonMark check reproduced the same blank-line bug inside the original blockquote wrapper; fixed that wrapper too.

Review-fix GREEN: 38 tests passed in 8.078s, including actual CommonMark integration (already-installed markdown-it-py; optional otherwise), malformed HTTP test servers and CLI Unicode-state check. No second reviewer pass is claimed; all findings have regression coverage. No deferred minors.

Final Ruling: retain the independent review's unverified external/provenance/accuracy areas as explicit limits, supported by builder tool evidence where available; do not portray a synthetic traceability check as human diagnostic accuracy. Cost if ignored: overstated reliability or unsupported submission claims.

Video: generated a local 56-second 1280x720 H.264 silent walkthrough from actual saved inference records, clearly labeled edited replay rather than live capture. 325407 bytes, ffprobe confirmed duration/codec/dimensions. Installed Pillow and FFmpeg 8.1.1 used only to create this artifact, not application dependencies. No system runtime installed.

Finish disposition: preserve the new standalone `build` branch locally, per the user's explicit no-publishing scope. No remote configured. No merge, repository publication, DEV mutation, contest entry, credentials, new account, global setting, or personal-information sharing performed. Project-local model weights/logs remain ignored in `.runtime`; they are excluded from the safe deliverable.

Final CLI smoke: `python -m lazy_ci_triage fixtures/junit.xml --format junit --mode inventory --public-data --output reports/final-inventory` returned `status=inventory_only mode=inventory failures=3`, exit 0. `python -m compileall -q lazy_ci_triage` and `git diff --check` passed. Saved raw inference JSON stayed unchanged during rendering fixes. A fresh full-suite log is included as `evidence/test-results.txt`.

## v0.2 constrained-format continuation

Parent explicitly authorized local improvement after the semantic snapshot, using only the existing weights. No model download, Library upload, public submission or account action is authorized by this continuation. Automatic tool approval is not treated as additional human authorization. The initial weight download was newly performed after reporting the exact need/size/Apache license; no claim that those weights were originally cached is made.

Ruling: remove free-form model prose rather than claim prompts or lexical checks can establish semantic truth. The model now selects only paired IDs, a finite literal quote option, a tentative family enum and fixed uncertainty. Python alone constructs `observed`; operational recommendations are always refused. Cost: explanations are less nuanced; wrong family choices and unrepresentative or hostile source quotes remain possible.

TDD: replaced contract tests first; RED included accepted historical prose that should now be refused and missing schema-v2 support. After contract/renderer/CLI updates, the whole suite passed 43 tests. Added advice-refusal and quote-length regressions; whitespace quote-length test observed RED then fixed. Family-offer test observed RED, then constrained offered families and added per-record eligibility hints. Full suite then passed 46 tests.

Real inference stage A (`evidence/v2-*`): 5 attempts, 3 accepted, 2 refused. Ambiguous input chose assertion_mismatch without a cue; lexical trap invented a KeyError quote. Stage B (`evidence/v2b-*`): same 3 accepted, 2 refused; ambiguity selected unclassified but paraphrased its quote. All 10 raw records kept.

Ruling: add finite extractive quote options to avoid asking this small model to reproduce arbitrary strings accurately. Literal options are generated from supplied source only, shown in prompt/schema and independently checked against the paired source. Cost: a selected literal option can still be verbose, irrelevant or misleading. No semantic-truth guarantee is claimed.

Independent constrained-format review at c526ec0: fresh GPT-6 Astra high reviewer ran 18 focused tests and replayed stage A; one P2 found (quote slicing could fabricate word boundaries and bypass full-record family eligibility). Single-record regression observed RED. A mixed-record/truncated-option regression also observed RED with the full-source gate removed, then GREEN after restoring it. Quote-option checks and full-source lexical eligibility now both apply. Reviewer did not assess the later quote-option implementation or final real batches; no second independent pass is claimed. No deferred findings.

Real final-format stage C (`evidence/v2c-*`): all 5 reports accepted, 9 paired literal quote options covering 9 extracted failures; 0 operational recommendations. JUnit 12.766146s / 333 output tokens; pytest 11.206768s / 269; hostile 22.807897s / 151; ambiguous 8.096488s / 87; lexical trap 7.406507s / 86. Same digest/options/hardware, no new weights. Each model request unloaded afterward.

Remaining semantic counterexample: the final lexical trap was accepted with a missing_key label although its text says KeyError is only an example and actual cause unknown. This is explicitly unverified model output, outside `observed`. Eight of nine labels agree with an authored example rubric; that is not diagnostic accuracy, root-cause truth or a human study. Hostile quote includes hostile instructions, visibly untrusted and inert. See `docs/quality-comparison.md` and `evidence/v2-evaluation.json`; replay tests cover both acceptance and preserved failures.

The Library attachment failure remains documented: helper reported prepare_uploads unavailable before preparing either existing file; no upload IDs created, no uncertain successful mutation, no bypass or alternate creation route attempted. This revision makes no Library/account call.

Current README, DEV draft and 56-second edited replay video describe v0.2. Original v0.1 raw records and video remain historical. Public code/demo URLs remain placeholders and `fully_autonomous` remains accurate disclosure. The current safe archive excludes ignored model weights, runtime logs, temporary helper files and caches.

Final v0.2 verification: `python -m unittest discover -s tests -v` ran **52 tests in 10.709s, OK**, with no skips in the build environment. Full safe output is `evidence/test-results.txt`; historical v0.1 log retained separately. Compileall, whitespace check and final inventory CLI smoke passed. Current edited replay: H.264 1280x720, 56.000s, 331678 bytes, ffprobe verified and representative card visually inspected. No further model runs are needed for this deliverable.
