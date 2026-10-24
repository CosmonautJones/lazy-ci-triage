# Current v0.2.2 demo script — October 24

`evidence/lazy-ci-triage-demo.mp4` is a 56-second silent edited replay of saved actual inference/comparison results. It now displays the literal line from `fixtures/lexical-trap.log`, the earlier executed CLI form and a formatted excerpt of `evidence/support-demo-lexical-trap/report.md`/JSON: observed T001/L001 from summary line 2, the exact quoted line, `unclassified`, fixed uncertainty and operational refusal. It is labeled as a replay, not live terminal capture; pause these cards to read. Historical videos remain separately named, including the prior summary-only v0.2.2 video. Below is an optional 90-second live plan, plus actual inference wait; never present an edited time cut as live latency.

Use authored synthetic inputs, relative paths and a clean terminal. Exclude unrelated windows, accounts, usernames, hardware IDs and hostnames. Start only the existing local runtime/cache as described in README; no model download is needed on the build machine.

**0–15s:** “A real citation can still sit beside a wrong category. Python keeps parsed observations separate from the local model's tentative choices.” Show `fixtures/junit.xml` and explain that its XML attributes/body are decoded and normalized, not raw-byte excerpts.

**15–30s:** Run the reproducible suite:

```powershell
python -m unittest discover -s tests -v
```

“These tests cover input parsing, ID/quote validation, malformed local responses and saved real-model evidence. They do not establish diagnostic accuracy.”

**30–50s, plus measured wait:**

```powershell
python -m lazy_ci_triage fixtures/junit.xml --format junit --public-data --endpoint http://127.0.0.1:11439 --output reports/video-support-junit
python -m lazy_ci_triage fixtures/lexical-trap.log --format pytest --public-data --endpoint http://127.0.0.1:11439 --output reports/video-support-trap
```

“Same cached Qwen2.5-Coder 1.5B, no paid API. The current saved JUnit run took 15.357 seconds and the original prose-only trap 4.939 seconds, loading included. Timings can change. The trap now selects unclassified; the older wrong label stays saved and is rejected by the current validator.” Show observations first, then hypotheses. The model cannot author observations or recommendations; generic review questions are application-authored.

**50–70s:** Open `docs/structural-support-evaluation.md`. “An independent agent froze 30 synthetic cases before the candidate saw them. Wrong specific labels fell from 7 to 2 in individual real inference, but correct specific labels fell from 12/15 to 9/15. Both accepted 29/30. This is a conservative tradeoff, not general accuracy.” Show the explicit type/message-only coverage losses, model abstentions and wrapped-refusal rejection.

**70–85s:** Show the indistinguishable H07/H29 input pair and the separate six-record stress results. “A copied traceback can be identical to a real error. Syntax cannot recover that missing provenance. Multi-record quote pairing also remains weak: 1/5 baseline and 2/5 candidate stress reports accepted. One failed test per input is cautious usage.” Keep refused outputs and hard-limit cases visible.

**85–90s:** “Everything is local and reviewable: source, synthetic fixtures, prompts, raw responses, failures and measurements. No model-suggested command execution, human time-savings claim or universal reliability promise.”

Public code/demo links remain placeholders pending separate approval. The primarily agent-authored DEV draft retains `fully_autonomous` disclosure unless meaningfully rewritten by a human. No public upload, account change or contest acceptance occurs in this preparation.
