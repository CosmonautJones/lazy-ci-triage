# Constrained brief revision

Parent approved this local quality revision after the v0.1 semantic snapshot. No new model weights, public upload, publishing or account actions are permitted.

The original free-text brief could cite real evidence while inventing functions, files, databases or commands. Prompt reminders did not prevent that. Replace prose generation with a deliberately narrower extractive format.

## Chosen bounded design

- CLI report schema version 2 has separate `observed` and `model_hypotheses` fields. `observed` is constructed only from the deterministic parser's dataclasses and input hash. It reports what the supplied text contains, not whether tests actually ran or logs are true.
- The model returns only a `hypotheses` array, exactly one item per extracted failed test. An item contains paired `test_id`/`log_id`, an exact source `quote`, a `family` enum and a fixed `uncertainty` enum. It cannot author observation fields, file/function names, explanations or operational recommendations.
- Families: `assertion_mismatch`, `missing_key`, `connection_refused`, `unclassified`. The last is the explicit abstention option. Each non-abstention family requires a narrow textual cue in the exact quoted source; this is a lexical eligibility check, not semantic entailment or proof of root cause. Misleading or hostile logs can contain those same cues.
- `uncertainty` must equal `log_only_root_cause_unverified`. The renderer supplies a fixed explanation for every model selection. It never treats model-selected family as an observed fact.
- The renderer shows deterministic observed records first, then **Model hypotheses — unverified selections**, with fixed tentative family descriptions, an exact quote link, fixed human review questions and explicit uncertainty. No operational advice is issued. Generic review questions are application-authored, not model recommendations.
- Unknown fields, including `observed`, `inspection`, `recommendations` and the old free-text schema, fail closed. Invalid model payloads remain available only as explicitly untrusted raw JSON for audit, never displayed as accepted advice in Markdown.
- Keep v0.1 real outputs and claims unchanged as historical records. Add regression fixtures using those actual outputs. Save new actual inference and evaluation records under v2 names, compare scope/traceability/unsupported prose honestly, and update the demo/draft to current behavior.

## Tradeoff

Removing all free-form model prose prevents that channel from inventing names and operational actions. It also removes nuanced explanations. Model choice of family or quote can still be irrelevant, misleading or wrong; lexical checks do not establish claim entailment. The useful narrow task is selecting one representative exact quote and a tentative broad failure family for each test, beside source facts a human can inspect. No diagnosis, fix or human time saving is established.
