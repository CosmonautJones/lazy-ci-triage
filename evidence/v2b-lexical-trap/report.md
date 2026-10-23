# Lazy CI Triage

Status: **invalid_citation** | Mode: **model**

Citation checks are not proof of a diagnosis. Lexical eligibility is not semantic entailment.

Model selections can be wrong or irrelevant. Human review is required.

Operational recommendations: refused. No model-suggested commands are executed.

## Observed in supplied file

Python-extracted metadata and verbatim source text only. Test execution, source authenticity and root cause are not verified.

Input SHA-256: `f1dfd38f335572ede9ad0838ab01aa6ca1231ba617780c818e4080b9a4cf8f98`

<a id="evidence-L001"></a>

### T001 / L001

<pre>tests/test_docs.py::test_error_example | line 2</pre>

Untrusted source excerpt:

<pre>FAILED tests/test_docs.py::test_error_example - text mentions KeyError as an example; actual cause unknown</pre>

## Model hypotheses - unverified selections

No accepted model selections. Inventory mode is deterministic; rejected model responses are not shown as advice.

## Run stopped

<pre>Quote does not occur verbatim in its source.</pre>

## Inference record

<pre>{&#x27;model&#x27;: &#x27;qwen2.5-coder:1.5b&#x27;, &#x27;options&#x27;: {&#x27;temperature&#x27;: 0, &#x27;seed&#x27;: 42, &#x27;num_ctx&#x27;: 32768, &#x27;num_predict&#x27;: 1800}, &#x27;ollama_version&#x27;: &#x27;0.18.0&#x27;, &#x27;model_digest&#x27;: &#x27;d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668&#x27;, &#x27;details&#x27;: {&#x27;parent_model&#x27;: &#x27;&#x27;, &#x27;format&#x27;: &#x27;gguf&#x27;, &#x27;family&#x27;: &#x27;qwen2&#x27;, &#x27;families&#x27;: [&#x27;qwen2&#x27;], &#x27;parameter_size&#x27;: &#x27;1.5B&#x27;, &#x27;quantization_level&#x27;: &#x27;Q4_K_M&#x27;}, &#x27;license_sha256&#x27;: &#x27;832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e&#x27;, &#x27;request_sha256&#x27;: &#x27;9c3e0d7ddf4ff4474dce65935a04dd2dba7bca71254db6fc4ad6acc10f723ab6&#x27;, &#x27;created_at&#x27;: &#x27;2026-10-23T12:20:40.9047366Z&#x27;, &#x27;done_reason&#x27;: &#x27;stop&#x27;, &#x27;total_duration&#x27;: 6343011700, &#x27;load_duration&#x27;: 2918289300, &#x27;prompt_eval_count&#x27;: 314, &#x27;prompt_eval_duration&#x27;: 33312700, &#x27;eval_count&#x27;: 86, &#x27;eval_duration&#x27;: 285730000, &#x27;wall_seconds&#x27;: 6.53505}</pre>
