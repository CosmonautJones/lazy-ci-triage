# Lazy CI Triage

Status: **invalid_citation** | Mode: **model**

Citation checks are not proof of a diagnosis. Lexical eligibility is not semantic entailment.

Model selections can be wrong or irrelevant. Human review is required.

Operational recommendations: refused. No model-suggested commands are executed.

## Observed in supplied file

Python-extracted metadata and decoded/normalized test detail only. Test execution, source authenticity and root cause are not verified.

For JUnit, decoded failure type/message values and element text are joined. Quotes match that normalized record, not raw XML bytes.

Input SHA-256: `7750afb0891849b13573d84ae443ee746996cab6aa7e80dbf7d61b8a69f2607c`

<a id="evidence-L001"></a>

### T001 / L001

<pre>H13 | testcase #1</pre>

Untrusted normalized detail:

<pre>requests.exceptions.ConnectionError HTTPConnectionPool(host=&#x27;service.invalid&#x27;, port=8123): Max retries exceeded
Traceback (most recent call last):
  File &quot;tests/test_client.py&quot;, line 42, in test_request
    client.get(&quot;http://service.invalid:8123/ping&quot;)
ConnectionRefusedError: [Errno 111] Connection refused

The above exception was the direct cause of the following exception:

requests.exceptions.ConnectionError: HTTPConnectionPool(host=&#x27;service.invalid&#x27;, port=8123): Max retries exceeded with url: /ping (Caused by NewConnectionError(&#x27;Failed to establish a new connection: [Errno 111] Connection refused&#x27;))</pre>

<a id="evidence-L002"></a>

### T002 / L002

<pre>H14 | testcase #2</pre>

Untrusted normalized detail:

<pre>ERROR tests/test_probe.py::test_service - ConnectionRefusedError: [Errno 111] Connection refused</pre>

<a id="evidence-L003"></a>

### T003 / L003

<pre>H15 | testcase #3</pre>

Untrusted normalized detail:

<pre>FAILED tests/test_endpoint.py::test_ready - builtins.ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it</pre>

<a id="evidence-L004"></a>

### T004 / L004

<pre>H16 | testcase #4</pre>

Untrusted normalized detail:

<pre>Review the glossary entry for AssertionError
The guide discusses AssertionError as a vocabulary term.
The page heading is outdated and needs editorial review.</pre>

<a id="evidence-L005"></a>

### T005 / L005

<pre>H17 | testcase #5</pre>

Untrusted normalized detail:

<pre>FAILED docs/test_glossary.py::test_key_entry - documentation note: &quot;KeyError: &#x27;region&#x27;&quot; is an example string; the page title is stale</pre>

<a id="evidence-L006"></a>

### T006 / L006

<pre>H18 | testcase #6</pre>

Untrusted normalized detail:

<pre>ValueError Invalid example text: &quot;ConnectionRefusedError: [Errno 111] Connection refused&quot;
ValueError: the quoted sample must be escaped before rendering.</pre>

## Model hypotheses - unverified selections

No accepted model selections. Inventory mode is deterministic; rejected model responses are not shown as advice.

## Run stopped

<pre>Selected family lacks its required textual cue in the quote; abstain instead.</pre>

## Inference record

<pre>{&#x27;model&#x27;: &#x27;qwen2.5-coder:1.5b&#x27;, &#x27;options&#x27;: {&#x27;temperature&#x27;: 0, &#x27;seed&#x27;: 42, &#x27;num_ctx&#x27;: 32768, &#x27;num_predict&#x27;: 1800}, &#x27;ollama_version&#x27;: &#x27;0.18.0&#x27;, &#x27;model_digest&#x27;: &#x27;d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668&#x27;, &#x27;details&#x27;: {&#x27;parent_model&#x27;: &#x27;&#x27;, &#x27;format&#x27;: &#x27;gguf&#x27;, &#x27;family&#x27;: &#x27;qwen2&#x27;, &#x27;families&#x27;: [&#x27;qwen2&#x27;], &#x27;parameter_size&#x27;: &#x27;1.5B&#x27;, &#x27;quantization_level&#x27;: &#x27;Q4_K_M&#x27;}, &#x27;license_sha256&#x27;: &#x27;832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e&#x27;, &#x27;request_sha256&#x27;: &#x27;f59783c61f128f63865a135f4f13e0f94a2b8190edf1f7ee2b59e01b2d1a1889&#x27;, &#x27;created_at&#x27;: &#x27;2026-10-24T10:05:17.6799026Z&#x27;, &#x27;done_reason&#x27;: &#x27;stop&#x27;, &#x27;total_duration&#x27;: 21195004700, &#x27;load_duration&#x27;: 2869200000, &#x27;prompt_eval_count&#x27;: 1393, &#x27;prompt_eval_duration&#x27;: 104023600, &#x27;eval_count&#x27;: 502, &#x27;eval_duration&#x27;: 3121048600, &#x27;wall_seconds&#x27;: 21.348316}</pre>
