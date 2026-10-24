# Lazy CI Triage

Status: **ok** | Mode: **model**

Citation checks are not proof of a diagnosis. Structural eligibility is not semantic entailment.

Model selections can be wrong or irrelevant. Human review is required.

Operational recommendations: refused. No model-suggested commands are executed.

## Observed in supplied file

Python-extracted metadata and decoded/normalized test detail only. Test execution, source authenticity and root cause are not verified.

For JUnit, decoded failure type/message values and element text are joined. Quotes match that normalized record, not raw XML bytes.

Input SHA-256: `e494c6c187b86dac37806535d0c927af36e8080d97c230f2233a8e410e236a81`

<a id="evidence-L001"></a>

### T001 / L001

<pre>tests/test_AssertionError_badge.py::test_status | line 1</pre>

Untrusted normalized detail:

<pre>FAILED tests/test_AssertionError_badge.py::test_status - RuntimeError: rendering failed</pre>

## Model hypotheses - unverified selections

### T001: Abstained: no specific failure family selected

Model-selected normalized detail quote (literal occurrence checked; support for the label is not proven):

<p><a href="#evidence-L001">T001 / L001</a></p>

<pre>FAILED tests/test_AssertionError_badge.py::test_status - RuntimeError: rendering failed</pre>

Fixed uncertainty: log-only evidence; implementation, environment and root cause remain unverified.

Fixed application-authored review question (not model advice):

<pre>Which additional reviewed source excerpt would help explain this failure?</pre>

## Inference record

<pre>{&#x27;model&#x27;: &#x27;qwen2.5-coder:1.5b&#x27;, &#x27;options&#x27;: {&#x27;temperature&#x27;: 0, &#x27;seed&#x27;: 42, &#x27;num_ctx&#x27;: 32768, &#x27;num_predict&#x27;: 1800}, &#x27;ollama_version&#x27;: &#x27;0.18.0&#x27;, &#x27;model_digest&#x27;: &#x27;d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668&#x27;, &#x27;details&#x27;: {&#x27;parent_model&#x27;: &#x27;&#x27;, &#x27;format&#x27;: &#x27;gguf&#x27;, &#x27;family&#x27;: &#x27;qwen2&#x27;, &#x27;families&#x27;: [&#x27;qwen2&#x27;], &#x27;parameter_size&#x27;: &#x27;1.5B&#x27;, &#x27;quantization_level&#x27;: &#x27;Q4_K_M&#x27;}, &#x27;license_sha256&#x27;: &#x27;832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e&#x27;, &#x27;request_sha256&#x27;: &#x27;12277bb65f178b2db5c2f2bda1a7f34d7085a7d8ab786faf3122d8fd4b56dcce&#x27;, &#x27;created_at&#x27;: &#x27;2026-10-24T10:11:48.6250625Z&#x27;, &#x27;done_reason&#x27;: &#x27;stop&#x27;, &#x27;total_duration&#x27;: 5344555600, &#x27;load_duration&#x27;: 2953577100, &#x27;prompt_eval_count&#x27;: 341, &#x27;prompt_eval_duration&#x27;: 33170600, &#x27;eval_count&#x27;: 70, &#x27;eval_duration&#x27;: 257831000, &#x27;wall_seconds&#x27;: 5.505095}</pre>
