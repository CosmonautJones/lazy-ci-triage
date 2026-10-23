# Lazy CI Triage

Status: **invalid_citation** | Mode: **model**

Citation checks are not proof of a diagnosis. Lexical eligibility is not semantic entailment.

Model selections can be wrong or irrelevant. Human review is required.

Operational recommendations: refused. No model-suggested commands are executed.

## Observed in supplied file

Python-extracted metadata and verbatim source text only. Test execution, source authenticity and root cause are not verified.

Input SHA-256: `5c65c9b3ecb1008c992e69b6ceb3b04a2f544dc413869923dd29996d576cd06c`

<a id="evidence-L001"></a>

### T001 / L001

<pre>tests/test_worker.py::test_completion | line 2</pre>

Untrusted source excerpt:

<pre>FAILED tests/test_worker.py::test_completion - worker returned status 7; no implementation or environment details supplied</pre>

## Model hypotheses - unverified selections

No accepted model selections. Inventory mode is deterministic; rejected model responses are not shown as advice.

## Run stopped

<pre>Selected family lacks its required textual cue in the quote; abstain instead.</pre>

## Inference record

<pre>{&#x27;model&#x27;: &#x27;qwen2.5-coder:1.5b&#x27;, &#x27;options&#x27;: {&#x27;temperature&#x27;: 0, &#x27;seed&#x27;: 42, &#x27;num_ctx&#x27;: 32768, &#x27;num_predict&#x27;: 1800}, &#x27;ollama_version&#x27;: &#x27;0.18.0&#x27;, &#x27;model_digest&#x27;: &#x27;d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668&#x27;, &#x27;details&#x27;: {&#x27;parent_model&#x27;: &#x27;&#x27;, &#x27;format&#x27;: &#x27;gguf&#x27;, &#x27;family&#x27;: &#x27;qwen2&#x27;, &#x27;families&#x27;: [&#x27;qwen2&#x27;], &#x27;parameter_size&#x27;: &#x27;1.5B&#x27;, &#x27;quantization_level&#x27;: &#x27;Q4_K_M&#x27;}, &#x27;license_sha256&#x27;: &#x27;832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e&#x27;, &#x27;request_sha256&#x27;: &#x27;c1f5f464003aca51a9af462970087aa4931b9b1451ad0881ce955cc376220116&#x27;, &#x27;created_at&#x27;: &#x27;2026-10-23T12:17:27.3976879Z&#x27;, &#x27;done_reason&#x27;: &#x27;stop&#x27;, &#x27;total_duration&#x27;: 5742903600, &#x27;load_duration&#x27;: 2571227700, &#x27;prompt_eval_count&#x27;: 281, &#x27;prompt_eval_duration&#x27;: 30815900, &#x27;eval_count&#x27;: 89, &#x27;eval_duration&#x27;: 296020800, &#x27;wall_seconds&#x27;: 5.932614}</pre>
