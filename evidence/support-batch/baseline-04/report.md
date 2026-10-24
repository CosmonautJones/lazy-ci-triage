# Lazy CI Triage

Status: **invalid_citation** | Mode: **model**

Citation checks are not proof of a diagnosis. Lexical eligibility is not semantic entailment.

Model selections can be wrong or irrelevant. Human review is required.

Operational recommendations: refused. No model-suggested commands are executed.

## Observed in supplied file

Python-extracted metadata and decoded/normalized test detail only. Test execution, source authenticity and root cause are not verified.

For JUnit, decoded failure type/message values and element text are joined. Quotes match that normalized record, not raw XML bytes.

Input SHA-256: `1d983b3826a0b651be564c8ea16c21b3a654fc97e6a3a6425d24dd1158c16f35`

<a id="evidence-L001"></a>

### T001 / L001

<pre>H19 | testcase #1</pre>

Untrusted normalized detail:

<pre>FAILED tests/test_AssertionError_badge.py::test_status - RuntimeError: rendering failed</pre>

<a id="evidence-L002"></a>

### T002 / L002

<pre>H20 | testcase #2</pre>

Untrusted normalized detail:

<pre>RuntimeError KeyErrorHandler failed to initialize
RuntimeError: KeyErrorHandler is disabled by configuration</pre>

<a id="evidence-L003"></a>

### T003 / L003

<pre>H21 | testcase #3</pre>

Untrusted normalized detail:

<pre>ERROR tests/test_connection_refused_icon.py::test_accessible_label - ValueError: missing aria label</pre>

<a id="evidence-L004"></a>

### T004 / L004

<pre>H22 | testcase #4</pre>

Untrusted normalized detail:

<pre>RuntimeError No AssertionError or KeyError was raised.
Validation stopped for an unrelated reason.
The inventory snapshot could not be loaded.</pre>

<a id="evidence-L005"></a>

### T005 / L005

<pre>H23 | testcase #5</pre>

Untrusted normalized detail:

<pre>FAILED tests/test_auth_probe.py::test_access - RuntimeError: No ConnectionRefusedError occurred; HTTP response status was 401</pre>

<a id="evidence-L006"></a>

### T006 / L006

<pre>H24 | testcase #6</pre>

Untrusted normalized detail:

<pre>Worker stopped before output was written.</pre>

## Model hypotheses - unverified selections

No accepted model selections. Inventory mode is deterministic; rejected model responses are not shown as advice.

## Run stopped

<pre>Selected family is not eligible for the full source record.</pre>

## Inference record

<pre>{&#x27;model&#x27;: &#x27;qwen2.5-coder:1.5b&#x27;, &#x27;options&#x27;: {&#x27;temperature&#x27;: 0, &#x27;seed&#x27;: 42, &#x27;num_ctx&#x27;: 32768, &#x27;num_predict&#x27;: 1800}, &#x27;ollama_version&#x27;: &#x27;0.18.0&#x27;, &#x27;model_digest&#x27;: &#x27;d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668&#x27;, &#x27;details&#x27;: {&#x27;parent_model&#x27;: &#x27;&#x27;, &#x27;format&#x27;: &#x27;gguf&#x27;, &#x27;family&#x27;: &#x27;qwen2&#x27;, &#x27;families&#x27;: [&#x27;qwen2&#x27;], &#x27;parameter_size&#x27;: &#x27;1.5B&#x27;, &#x27;quantization_level&#x27;: &#x27;Q4_K_M&#x27;}, &#x27;license_sha256&#x27;: &#x27;832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e&#x27;, &#x27;request_sha256&#x27;: &#x27;942c2d3a8361d79a5c2aa6e335e7e00e7c472a63b154cebee2b8b794503de6b5&#x27;, &#x27;created_at&#x27;: &#x27;2026-10-24T10:05:58.3948213Z&#x27;, &#x27;done_reason&#x27;: &#x27;stop&#x27;, &#x27;total_duration&#x27;: 19465494100, &#x27;load_duration&#x27;: 2790093200, &#x27;prompt_eval_count&#x27;: 926, &#x27;prompt_eval_duration&#x27;: 72240600, &#x27;eval_count&#x27;: 452, &#x27;eval_duration&#x27;: 2726707600, &#x27;wall_seconds&#x27;: 19.6189}</pre>
