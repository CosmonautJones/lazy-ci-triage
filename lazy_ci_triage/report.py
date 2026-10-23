"""Safe, human-readable Markdown reports."""

from html import escape


def _plain(value):
    # HTML blocks keep Markdown syntax in untrusted strings inert, too.
    return escape(str(value), quote=True)


def render_report(report):
    dataset = report["dataset"]
    lines = ["# Lazy CI Triage", "", f"Status: **{report['status']}** · Mode: **{report['mode']}**", "",
             "Hypotheses require human review. Citation checks are not proof of a diagnosis.", "",
             "No suggested commands are executed. Source excerpts are untrusted data.", "",
             f"Input SHA-256: `{dataset['input_sha256']}`", ""]
    if report.get("error"):
        lines.extend(["## Run stopped", "", "<p>" + _plain(report["error"]) + "</p>", ""])
    runtime = report.get("runtime", {})
    if runtime:
        lines.extend(["## Inference record", "", "<pre>" + _plain(runtime) + "</pre>", ""])
    if report.get("brief"):
        lines.extend(["## Troubleshooting hypotheses", ""])
        for index, finding in enumerate(report["brief"]["findings"], 1):
            lines.extend([f"### {index}. Hypothesis", "", "<p>" + _plain(finding["hypothesis"]) + "</p>", "",
                          "**Inspect:**", "", "<p>" + _plain(finding["inspection"]) + "</p>", "",
                          "**Uncertainty:**", "", "<p>" + _plain(finding["uncertainty"]) + "</p>", ""])
            for cite in finding["citations"]:
                lines.extend([f'<p><a href="#evidence-{cite["log_id"]}">{cite["test_id"]} / {cite["log_id"]}</a></p>',
                              "", "<blockquote><pre>" + _plain(cite["quote"]) + "</pre></blockquote>", ""])
    lines.extend(["## Source evidence", ""])
    if not dataset["failures"]:
        lines.extend(["No failures extracted. This is not an independent verification of test success.", ""])
    for source in dataset["failures"]:
        lines.extend([f'<a id="evidence-{source["log_id"]}"></a>', "",
                      f'### {source["test_id"]} / {source["log_id"]}', "",
                      "<p>" + _plain(source["name"]) + " · " + _plain(source["location"]) + "</p>", "",
                      "<pre>" + _plain(source["text"]) + "</pre>", ""])
        if source["truncated"]:
            lines.extend(["Excerpt truncated to the input budget; consult the original input.", ""])
    return "\n".join(lines)
