# Lazy CI Triage

Status: **ok** | Mode: **model**

Citation checks are not proof of a diagnosis. Structural eligibility is not semantic entailment.

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

### T001: Abstained: no specific failure family selected

Model-selected normalized detail quote (literal occurrence checked; support for the label is not proven):

<p><a href="#evidence-L001">T001 / L001</a></p>

<pre>FAILED tests/test_AssertionError_badge.py::test_status - RuntimeError: rendering failed</pre>

Fixed uncertainty: log-only evidence; implementation, environment and root cause remain unverified.

Fixed application-authored review question (not model advice):

<pre>Which additional reviewed source excerpt would help explain this failure?</pre>

### T002: Abstained: no specific failure family selected

Model-selected normalized detail quote (literal occurrence checked; support for the label is not proven):

<p><a href="#evidence-L002">T002 / L002</a></p>

<pre>RuntimeError KeyErrorHandler failed to initialize
RuntimeError: KeyErrorHandler is disabled by configuration</pre>

Fixed uncertainty: log-only evidence; implementation, environment and root cause remain unverified.

Fixed application-authored review question (not model advice):

<pre>Which additional reviewed source excerpt would help explain this failure?</pre>

### T003: Abstained: no specific failure family selected

Model-selected normalized detail quote (literal occurrence checked; support for the label is not proven):

<p><a href="#evidence-L003">T003 / L003</a></p>

<pre>ERROR tests/test_connection_refused_icon.py::test_accessible_label - ValueError: missing aria label</pre>

Fixed uncertainty: log-only evidence; implementation, environment and root cause remain unverified.

Fixed application-authored review question (not model advice):

<pre>Which additional reviewed source excerpt would help explain this failure?</pre>

### T004: Abstained: no specific failure family selected

Model-selected normalized detail quote (literal occurrence checked; support for the label is not proven):

<p><a href="#evidence-L004">T004 / L004</a></p>

<pre>RuntimeError No AssertionError or KeyError was raised.
Validation stopped for an unrelated reason.
The inventory snapshot could not be loaded.</pre>

Fixed uncertainty: log-only evidence; implementation, environment and root cause remain unverified.

Fixed application-authored review question (not model advice):

<pre>Which additional reviewed source excerpt would help explain this failure?</pre>

### T005: Abstained: no specific failure family selected

Model-selected normalized detail quote (literal occurrence checked; support for the label is not proven):

<p><a href="#evidence-L005">T005 / L005</a></p>

<pre>FAILED tests/test_auth_probe.py::test_access - RuntimeError: No ConnectionRefusedError occurred; HTTP response status was 401</pre>

Fixed uncertainty: log-only evidence; implementation, environment and root cause remain unverified.

Fixed application-authored review question (not model advice):

<pre>Which additional reviewed source excerpt would help explain this failure?</pre>

### T006: Abstained: no specific failure family selected

Model-selected normalized detail quote (literal occurrence checked; support for the label is not proven):

<p><a href="#evidence-L006">T006 / L006</a></p>

<pre>Worker stopped before output was written.</pre>

Fixed uncertainty: log-only evidence; implementation, environment and root cause remain unverified.

Fixed application-authored review question (not model advice):

<pre>Which additional reviewed source excerpt would help explain this failure?</pre>

## Inference record

<pre>{&#x27;model&#x27;: &#x27;qwen2.5-coder:1.5b&#x27;, &#x27;options&#x27;: {&#x27;temperature&#x27;: 0, &#x27;seed&#x27;: 42, &#x27;num_ctx&#x27;: 32768, &#x27;num_predict&#x27;: 1800}, &#x27;ollama_version&#x27;: &#x27;0.18.0&#x27;, &#x27;model_digest&#x27;: &#x27;d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668&#x27;, &#x27;details&#x27;: {&#x27;parent_model&#x27;: &#x27;&#x27;, &#x27;format&#x27;: &#x27;gguf&#x27;, &#x27;family&#x27;: &#x27;qwen2&#x27;, &#x27;families&#x27;: [&#x27;qwen2&#x27;], &#x27;parameter_size&#x27;: &#x27;1.5B&#x27;, &#x27;quantization_level&#x27;: &#x27;Q4_K_M&#x27;}, &#x27;license_sha256&#x27;: &#x27;832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e&#x27;, &#x27;request_sha256&#x27;: &#x27;662abe554e25f4e37f95458a272b6891477ee39f401bd7711f9090d76a907b48&#x27;, &#x27;created_at&#x27;: &#x27;2026-10-24T10:06:17.651786Z&#x27;, &#x27;done_reason&#x27;: &#x27;stop&#x27;, &#x27;total_duration&#x27;: 19062840200, &#x27;load_duration&#x27;: 2914954300, &#x27;prompt_eval_count&#x27;: 913, &#x27;prompt_eval_duration&#x27;: 73053900, &#x27;eval_count&#x27;: 448, &#x27;eval_duration&#x27;: 2555720800, &#x27;wall_seconds&#x27;: 19.249646}</pre>
