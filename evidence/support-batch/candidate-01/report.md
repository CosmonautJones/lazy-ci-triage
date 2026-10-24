# Lazy CI Triage

Status: **invalid_citation** | Mode: **model**

Citation checks are not proof of a diagnosis. Structural eligibility is not semantic entailment.

Model selections can be wrong or irrelevant. Human review is required.

Operational recommendations: refused. No model-suggested commands are executed.

## Observed in supplied file

Python-extracted metadata and decoded/normalized test detail only. Test execution, source authenticity and root cause are not verified.

For JUnit, decoded failure type/message values and element text are joined. Quotes match that normalized record, not raw XML bytes.

Input SHA-256: `289dda78079bd87c4d96b6daf1a58aa3aa5085db5d296c549f24fb4c2df69c9d`

<a id="evidence-L001"></a>

### T001 / L001

<pre>H01 | testcase #1</pre>

Untrusted normalized detail:

<pre>builtins.AssertionError expected total 9, observed 12</pre>

<a id="evidence-L002"></a>

### T002 / L002

<pre>H02 | testcase #2</pre>

Untrusted normalized detail:

<pre>Traceback (most recent call last):
  File &quot;tests/test_limits.py&quot;, line 18, in test_remaining
    assert remaining == 0
AssertionError: assert 2 == 0</pre>

<a id="evidence-L003"></a>

### T003 / L003

<pre>H03 | testcase #3</pre>

Untrusted normalized detail:

<pre>AssertionError assert &#x27;KeyError&#x27; == &#x27;ready&#x27;
def test_label():
    label = &quot;KeyError&quot;
&gt;   assert label == &quot;ready&quot;
E   AssertionError: assert &#x27;KeyError&#x27; == &#x27;ready&#x27;</pre>

<a id="evidence-L004"></a>

### T004 / L004

<pre>H04 | testcase #4</pre>

Untrusted normalized detail:

<pre>FAILED tests/test_records.py::test_sorted - assert [&#x27;pear&#x27;, &#x27;apple&#x27;] == [&#x27;apple&#x27;, &#x27;pear&#x27;]</pre>

<a id="evidence-L005"></a>

### T005 / L005

<pre>H05 | testcase #5</pre>

Untrusted normalized detail:

<pre>FAILED tests/test_flags.py::test_explicit - builtins.AssertionError: enabled flag was false</pre>

<a id="evidence-L006"></a>

### T006 / L006

<pre>H06 | testcase #6</pre>

Untrusted normalized detail:

<pre>builtins.KeyError &#x27;region&#x27;</pre>

## Model hypotheses - unverified selections

No accepted model selections. Inventory mode is deterministic; rejected model responses are not shown as advice.

## Run stopped

<pre>Quote does not occur verbatim in its source.</pre>

## Inference record

<pre>{&#x27;model&#x27;: &#x27;qwen2.5-coder:1.5b&#x27;, &#x27;options&#x27;: {&#x27;temperature&#x27;: 0, &#x27;seed&#x27;: 42, &#x27;num_ctx&#x27;: 32768, &#x27;num_predict&#x27;: 1800}, &#x27;ollama_version&#x27;: &#x27;0.18.0&#x27;, &#x27;model_digest&#x27;: &#x27;d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668&#x27;, &#x27;details&#x27;: {&#x27;parent_model&#x27;: &#x27;&#x27;, &#x27;format&#x27;: &#x27;gguf&#x27;, &#x27;family&#x27;: &#x27;qwen2&#x27;, &#x27;families&#x27;: [&#x27;qwen2&#x27;], &#x27;parameter_size&#x27;: &#x27;1.5B&#x27;, &#x27;quantization_level&#x27;: &#x27;Q4_K_M&#x27;}, &#x27;license_sha256&#x27;: &#x27;832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e&#x27;, &#x27;request_sha256&#x27;: &#x27;2a097b093b21ba6644720f53b3fc2f331a47f61a23da0d1ec6da992a398c9138&#x27;, &#x27;created_at&#x27;: &#x27;2026-10-24T10:04:19.6285101Z&#x27;, &#x27;done_reason&#x27;: &#x27;stop&#x27;, &#x27;total_duration&#x27;: 20128918000, &#x27;load_duration&#x27;: 2933022100, &#x27;prompt_eval_count&#x27;: 1056, &#x27;prompt_eval_duration&#x27;: 92183300, &#x27;eval_count&#x27;: 468, &#x27;eval_duration&#x27;: 2806272400, &#x27;wall_seconds&#x27;: 20.295474}</pre>
