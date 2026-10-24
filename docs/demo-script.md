# Current v0.2.1 demo script — October 24

The local `evidence/lazy-ci-triage-demo.mp4` is a 56-second silent edited walkthrough of actual October 24 results, labeled as a replay rather than live terminal capture. The old v0.1/v0.2 videos are historical. This is an optional 90-second live-terminal plan, plus actual inference wait.

Use only synthetic fixtures. Capture relative paths in a clean terminal; exclude other windows, accounts, usernames, hardware IDs and hostnames. Start the existing Ollama runtime/cache as described in README; no download is needed on the build machine.

**0–15s:** “A real citation can still sit beside a bad explanation. This small tool now separates what a log says from what a local model selects.” Show the synthetic JUnit failure file.

**15–25s:**

```powershell
python -m unittest discover -s tests -v
```

**25–50s, plus measured wait:**

```powershell
python -m lazy_ci_triage fixtures/junit.xml --format junit --public-data --endpoint http://127.0.0.1:11439 --output reports/video-v2-junit
```

“This runs Qwen2.5-Coder 1.5B locally. Python builds `observed`; JUnit detail is decoded and normalized, not raw XML bytes. The model can only select IDs, a literal option from that detail, a family enum and fixed uncertainty.” Open the report. Show **Observed in supplied file** first, then **Model hypotheses — unverified selections**. Point out that generic review questions are application-authored and operational recommendations are refused. Show model digest and measured latency in JSON. Label any time cut; do not promise identical timings.

**50–65s:** Show `evidence/oct24-parameter-delimiter/report.md` and the intact `test_label[a - b]` name, followed by `evidence/oct24-short-detail/report.md`. “Real short detail can be quoted. A failure with no detail is refused before any model request; it is still visible in inventory.” Show the explicit `oct24-no-detail` report. No generated placeholder is presented as evidence.

**65–80s:** Open `evidence/oct24-lexical-trap/report.md`. “Here is a remaining weakness: KeyError occurs only as a documentation example, yet the model chose a missing-key label. Literal matching cannot prove semantic support. That label stays unverified and separate from observations.” Mention that hostile quoted instructions remain inert data and no command executor exists.

**80–90s:** “This bounded local experiment uses open weights without a provider API key. The current batch has nine traceable normalized-detail selections across five model runs, plus one pre-inference refusal. Those are not nine proven diagnoses. No human time-savings claim.”

Keep public code/video URLs as placeholders until approved. `fully_autonomous` remains the accurate DEV disclosure unless the human meaningfully rewrites the article. This revision performs no Library upload, public publication or account action.
