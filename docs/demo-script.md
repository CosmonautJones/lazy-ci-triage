# Local demo script (about 90 seconds, plus actual inference wait)

Use only this repository's synthetic fixtures. A 56-second silent edited walkthrough of the saved real results already exists at `evidence/lazy-ci-triage-demo.mp4`, labeled as an edited replay rather than live terminal capture. This script is an optional live-terminal recording plan. Record a clean terminal with relative paths; do not capture other windows, accounts, hardware IDs or hostnames.

Before recording, use the README's isolated Ollama setup and installed model. The demo endpoint is `http://127.0.0.1:11439`. Choose new output directories. Show actual waiting time, or label any cut with the measured wall time from the saved report.

**0–15s — state the chore.** “This is Lazy CI Triage. It reads test failures and drafts where a human could investigate. These are authored synthetic logs.” Show `fixtures/junit.xml` and its assertion, missing-key and refused-connection failures.

**15–25s — prove the deterministic guardrails.**

```powershell
python -m unittest discover -s tests -v
```

**25–50s, plus wait — run the actual model.**

```powershell
python -m lazy_ci_triage fixtures/junit.xml --format junit --public-data --endpoint http://127.0.0.1:11439 --output reports/video-junit
```

Say: “Qwen2.5-Coder 1.5B is running locally through Ollama. This is inference, not a canned response.” Open `reports/video-junit/report.md` and follow a citation to its source excerpt. Inspect the JSON runtime section for model digest, wall seconds and tokens. Do not promise an identical response on every run.

**50–65s — show a real limitation.** Open `evidence/junit-run/report.md` and point out the initial duplicate findings and unrelated citation. “These references existed, but the reasoning was weak. The current contract rejects repeated citations. It still cannot prove that a diagnosis is right.” Then show the refined report.

**65–80s — show hostile data and failure handling.** Show `fixtures/injection.xml`; explain that instructions inside source logs are untrusted text and that the program has no command executor. Use the saved real `evidence/injection-run/report.md` to show the actual outcome, including rejection if that is what happened. Do not execute anything the model writes.

**80–90s — explain the open choice.** “The weights and local runtime make the inference path inspectable and replaceable without a paid API. This is an evidence-linked starting point, not an automatic fix. No human time savings have been measured.”

The eventual video/deployed demo URL and public code URL belong in the DEV draft only after approval. Keep `fully_autonomous` disclosure unless the human meaningfully rewrites the article. Publishing or approving this script alone is not a change of authorship.
