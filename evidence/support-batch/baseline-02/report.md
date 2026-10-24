# Lazy CI Triage

Status: **invalid_citation** | Mode: **model**

Citation checks are not proof of a diagnosis. Lexical eligibility is not semantic entailment.

Model selections can be wrong or irrelevant. Human review is required.

Operational recommendations: refused. No model-suggested commands are executed.

## Observed in supplied file

Python-extracted metadata and decoded/normalized test detail only. Test execution, source authenticity and root cause are not verified.

For JUnit, decoded failure type/message values and element text are joined. Quotes match that normalized record, not raw XML bytes.

Input SHA-256: `d3ec89b537d7a60ed51ba5d42dadcdbb5669a590dd3b82bc69a466e65fd6432a`

<a id="evidence-L001"></a>

### T001 / L001

<pre>H07 | testcase #1</pre>

Untrusted normalized detail:

<pre>Traceback (most recent call last):
  File &quot;tests/test_payload.py&quot;, line 24, in test_lookup
    return payload[&quot;AssertionError&quot;]
builtins.KeyError: &#x27;AssertionError&#x27;</pre>

<a id="evidence-L002"></a>

### T002 / L002

<pre>H08 | testcase #2</pre>

Untrusted normalized detail:

<pre>KeyError: 17
Mapping lookup failed.</pre>

<a id="evidence-L003"></a>

### T003 / L003

<pre>H09 | testcase #3</pre>

Untrusted normalized detail:

<pre>FAILED tests/test_routes.py::test_zone - KeyError: &#x27;routing.zone&#x27;</pre>

<a id="evidence-L004"></a>

### T004 / L004

<pre>H10 | testcase #4</pre>

Untrusted normalized detail:

<pre>ERROR tests/test_cache.py::test_partition - builtins.KeyError: (&#x27;west&#x27;, 3)</pre>

<a id="evidence-L005"></a>

### T005 / L005

<pre>H11 | testcase #5</pre>

Untrusted normalized detail:

<pre>builtins.ConnectionRefusedError [Errno 111] Connection refused</pre>

<a id="evidence-L006"></a>

### T006 / L006

<pre>H12 | testcase #6</pre>

Untrusted normalized detail:

<pre>Traceback (most recent call last):
  File &quot;tests/test_socket.py&quot;, line 31, in test_connect
    sock.connect(address)
ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it</pre>

## Model hypotheses - unverified selections

No accepted model selections. Inventory mode is deterministic; rejected model responses are not shown as advice.

## Run stopped

<pre>Quote does not occur verbatim in its source.</pre>

## Inference record

<pre>{&#x27;model&#x27;: &#x27;qwen2.5-coder:1.5b&#x27;, &#x27;options&#x27;: {&#x27;temperature&#x27;: 0, &#x27;seed&#x27;: 42, &#x27;num_ctx&#x27;: 32768, &#x27;num_predict&#x27;: 1800}, &#x27;ollama_version&#x27;: &#x27;0.18.0&#x27;, &#x27;model_digest&#x27;: &#x27;d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668&#x27;, &#x27;details&#x27;: {&#x27;parent_model&#x27;: &#x27;&#x27;, &#x27;format&#x27;: &#x27;gguf&#x27;, &#x27;family&#x27;: &#x27;qwen2&#x27;, &#x27;families&#x27;: [&#x27;qwen2&#x27;], &#x27;parameter_size&#x27;: &#x27;1.5B&#x27;, &#x27;quantization_level&#x27;: &#x27;Q4_K_M&#x27;}, &#x27;license_sha256&#x27;: &#x27;832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e&#x27;, &#x27;request_sha256&#x27;: &#x27;f0aaeb6e2e709e36e6c57d0a3cfff6cf22bbd7e5d5ae0331efbc5c905eecb677&#x27;, &#x27;created_at&#x27;: &#x27;2026-10-24T10:04:38.5568733Z&#x27;, &#x27;done_reason&#x27;: &#x27;stop&#x27;, &#x27;total_duration&#x27;: 18784787700, &#x27;load_duration&#x27;: 2765422100, &#x27;prompt_eval_count&#x27;: 1107, &#x27;prompt_eval_duration&#x27;: 91498900, &#x27;eval_count&#x27;: 458, &#x27;eval_duration&#x27;: 2688483200, &#x27;wall_seconds&#x27;: 18.923455}</pre>
