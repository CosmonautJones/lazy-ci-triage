# Held-out synthetic evaluation rationale

Frozen authored set for Lazy CI Triage classification robustness. This set was created independently without reading current or planned production classification code, project files, inference output, or implementation candidates. Only applicable ancestor workspace instructions were inspected. No inference or project installation was performed.

## Scope and schema

`cases.json` is a UTF-8 JSON array of 30 cases. Every case has `id`, `format` (`junit` or `pytest`), `input`, `expected_family`, `category`, `rationale`, and boolean `hard_limit`. Inputs, names, paths, messages, values, and the reserved domain are synthetic.

The supported observations are JUnit failure/error type, message, and body (type and message normalized together before the body), or a pytest short-summary reason. Pytest cases contain only supported FAILED/ERROR summary lines; they do not assume traceback text survives outside that summary. JUnit uses ordinary XML elements, escaped attributes, and CDATA bodies.

## Balance and coverage

- 15 cases have a supported actual family: five assertion_mismatch, five missing_key, and five connection_refused.
- 15 cases have an intended unclassified label: 12 observable negatives and three indistinguishable copied examples.
- Formats: 18 JUnit cases and 12 pytest cases.
- Three hard_limit cases are explicitly marked; the other 27 are resolvable from the intended supported evidence.

Positive coverage includes qualified exception names, empty fields, exception-form messages, multiline terminal tracebacks, assertion source statements and rendered comparisons, incidental other-family strings inside actual failures, non-string dictionary keys, platform message variation, and a wrapped refusal cause. These examples stay inside the supplied formats.

Observable negative coverage includes prose mentions, explicitly quoted documentation snippets, exception-name substrings in identifiers and paths, explicit denial of named failures, absent or ambiguous evidence, an unsupported related lookup exception, and a distinct network timeout.

## Hard limits and scoring

H28/H02, H29/H07, and H30/H12 are exact full-input pairs with opposing intended provenance labels. The former in each pair was authored as an unmarked copied documentation example and requires unclassified by intent; the latter was authored as an actual failure. Their supported observable inputs are byte-for-byte identical. No deterministic classifier restricted to those inputs can satisfy both labels. A language model cannot recover the missing provenance either.

Score the 27 non-hard-limit cases as the actionable robustness comparison. Report the three hard-limit outcomes separately, preserving their intended labels and explaining the information limit. Do not count the hard-limit rows as evidence that a classifier should guess the invisible provenance. Across all 30 rows, a deterministic input-only classifier has a ceiling of 27 correct because of the three contradictory pairs.

Run classification with each case's input and format only. Do not feed id, expected_family, category, rationale, or hard_limit to the classifier. Compare the resulting family to expected_family after the run. Keep actual-family recall separate from false-positive rates on observable unclassified cases; aggregate accuracy can hide accidental prose or identifier matches.

## Freeze discipline

This set was authored before access to the implementation candidate and is frozen for the first held-out comparison. Do not tune implementation against individual hidden cases before that initial comparison. Preserve the original files and hashes; record evaluation results in a separate file. Any later label correction or expansion should be a separately versioned artifact with an explanation rather than a silent edit.

