"""Keep deterministic source observations apart from unverified model choices."""

from html import escape

from .brief import FAMILY_COPY


def _plain(value):
    return escape(str(value), quote=True)


def render_report(report):
    if report.get("schema_version") != 2:
        raise ValueError("Only schema-version-2 reports can be rendered by this version.")
    observed = report["observed"]
    lines = ["# Lazy CI Triage", "", f"Status: **{report['status']}** | Mode: **{report['mode']}**", "",
             "Citation checks are not proof of a diagnosis. Structural eligibility is not semantic entailment.", "",
             "Model selections can be wrong or irrelevant. Human review is required.", "",
             "Operational recommendations: refused. No model-suggested commands are executed.", "",
             "## Observed in supplied file", "",
             "Python-extracted metadata and decoded/normalized test detail only. Test execution, source authenticity and root cause are not verified.", "",
             "For JUnit, decoded failure type/message values and element text are joined. Quotes match that normalized record, not raw XML bytes.", "",
             f"Input SHA-256: `{observed['input_sha256']}`", ""]
    if not observed["failures"]:
        lines.extend(["No failures extracted from the supported input. This does not verify test success.", ""])
    for source in observed["failures"]:
        lines.extend([f'<a id="evidence-{source["log_id"]}"></a>', "", f'### {source["test_id"]} / {source["log_id"]}', "",
                      "<pre>" + _plain(source["name"]) + " | " + _plain(source["location"]) + "</pre>", "",
                      "Untrusted normalized detail:", "", "<pre>" + _plain(source["text"]) + "</pre>", ""])
        if not source["text"]:
            lines.extend(["Application note: no failure detail text was supplied. This note is not quotable evidence.", ""])
        if source["truncated"]:
            lines.extend(["Excerpt truncated; consult the original input.", ""])
    lines.extend(["## Model hypotheses - unverified selections", ""])
    if report.get("model_hypotheses"):
        for selection in report["model_hypotheses"]["hypotheses"]:
            label, question = FAMILY_COPY[selection["family"]]
            lines.extend([f'### {selection["test_id"]}: {label}', "",
                          "Model-selected normalized detail quote (literal occurrence checked; support for the label is not proven):", "",
                          f'<p><a href="#evidence-{selection["log_id"]}">{selection["test_id"]} / {selection["log_id"]}</a></p>', "",
                          "<pre>" + _plain(selection["quote"]) + "</pre>", "",
                          "Fixed uncertainty: log-only evidence; implementation, environment and root cause remain unverified.", "",
                          "Fixed application-authored review question (not model advice):", "",
                          "<pre>" + _plain(question) + "</pre>", ""])
    else:
        lines.extend(["No accepted model selections. Inventory mode is deterministic; rejected model responses are not shown as advice.", ""])
    if report.get("error"):
        lines.extend(["## Run stopped", "", "<pre>" + _plain(report["error"]) + "</pre>", ""])
    if report.get("runtime"):
        lines.extend(["## Inference record", "", "<pre>" + _plain(report["runtime"]) + "</pre>", ""])
    return "\n".join(lines)
