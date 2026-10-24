"""Reproduce a version-pinned synthetic comparison; never downloads weights.

This developer evaluation tool runs fixed Git/Python operations, never model text.
It is separate from the application's command-free inference workflow.
"""

import argparse
from dataclasses import asdict
import hashlib
import importlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import zipfile
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "f28d2e6ad7777d782c75dbf47013de0336eb2ee0"
sys.path.insert(0, str(ROOT))
from lazy_ci_triage import __version__
from lazy_ci_triage import brief, ollama, parsing, report


def load_baseline(folder):
    """Extract only the exact reviewed product modules from local Git history."""
    raw = subprocess.run(["git", "archive", "--format=zip", BASELINE, "lazy_ci_triage"], cwd=ROOT,
                         check=True, capture_output=True).stdout
    destination = folder / "baseline-code"
    destination.mkdir()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        archive.extractall(destination)
    package = destination / "lazy_ci_triage"
    spec = importlib.util.spec_from_file_location("baseline_contract", package / "__init__.py",
                                                submodule_search_locations=[str(package)])
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return {name: importlib.import_module("baseline_contract." + name)
            for name in ["brief", "ollama", "parsing", "report"]}


def eligibility(contract, cases):
    rows = []
    for case in cases:
        dataset = contract["parsing"].parse_input(case["input"].encode(), case["format"])
        assert len(dataset.failures) == 1, case["id"]
        payload = contract["brief"].build_prompt(dataset)
        allowed = json.loads(payload["prompt"])["untrusted_evidence"][0]["eligible_families"]
        rows.append({"id": case["id"], "expected": case["expected_family"], "offered": allowed,
                     "hard_limit": case["hard_limit"], "normalized_text": dataset.failures[0].text})
    return rows


def gate_metrics(rows):
    positives = [row for row in rows if row["expected"] != "unclassified"]
    negatives = [row for row in rows if row["expected"] == "unclassified"]
    return {"cases": len(rows), "specific_rubric_cases": len(positives), "abstention_rubric_cases": len(negatives),
            "specific_rubric_family_available": sum(row["expected"] in row["offered"] for row in positives),
            "abstention_cases_allowing_specific": sum(len(row["offered"]) > 1 for row in negatives),
            "cases_allowing_wrong_specific": sum(any(f != row["expected"] and f != "unclassified" for f in row["offered"]) for row in rows),
            "only_abstention_available": sum(row["offered"] == ["unclassified"] for row in rows)}


def combined_input(cases):
    # Retain each independently parsed normalized record exactly as a JUnit body.
    # Original case inputs/formats remain in the frozen fixture and row provenance.
    lines = ["<testsuite>"]
    for case in cases:
        dataset = parsing.parse_input(case["input"].encode(), case["format"])
        text = dataset.failures[0].text
        lines.append('<testcase name="' + case["id"] + '"><failure>' + escape(text) + '</failure></testcase>')
    return ("\n".join(lines) + "\n</testsuite>\n").encode()


def infer(contract, cases, folder, model, endpoint, version):
    kind = cases[0]["format"] if len(cases) == 1 else "junit"
    data = cases[0]["input"].encode() if len(cases) == 1 else combined_input(cases)
    folder.mkdir()
    (folder / ("input.xml" if kind == "junit" else "input.log")).write_bytes(data)
    dataset = contract["parsing"].parse_input(data, kind)
    payload = contract["brief"].build_prompt(dataset)
    (folder / "request.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    output = {"app_version": version, "schema_version": 2, "mode": "model", "status": "ok",
              "observed": asdict(dataset), "operational_recommendations": {"status": "refused"}}
    try:
        output.update(contract["ollama"].generate(dataset, model, endpoint, 180))
    except contract["ollama"].InferenceError as exc:
        output.update(status=exc.status, error=str(exc), runtime=exc.runtime,
                      raw_response=exc.raw_response, model_hypotheses=None)
    (folder / "report.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    (folder / "report.md").write_text(contract["report"].render_report(output), encoding="utf-8")
    return output


def model_rows(cases, output):
    accepted = output.get("model_hypotheses")
    selections = {item["test_id"]: item for item in accepted["hypotheses"]} if accepted else {}
    rows = []
    for index, case in enumerate(cases, 1):
        selection = selections.get(f"T{index:03}")
        rows.append({"id": case["id"], "expected": case["expected_family"], "hard_limit": case["hard_limit"],
                     "status": output["status"], "selected": selection["family"] if selection else None})
    return rows


def model_metrics(rows):
    return {"cases": len(rows), "accepted_selections": sum(r["selected"] is not None for r in rows),
            "false_specific": sum(r["selected"] not in {None, "unclassified", r["expected"]} for r in rows),
            "correct_specific": sum(r["selected"] == r["expected"] and r["expected"] != "unclassified" for r in rows),
            "correct_abstention": sum(r["selected"] == r["expected"] == "unclassified" for r in rows),
            "all_abstentions": sum(r["selected"] == "unclassified" for r in rows),
            "missing_due_to_refused_report": sum(r["selected"] is None for r in rows),
            "hard_limit_false_specific": sum(r["hard_limit"] and r["selected"] not in {None, "unclassified", r["expected"]} for r in rows)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=ROOT / "fixtures/structural-support-heldout.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--inference", action="store_true")
    parser.add_argument("--batch-size", type=int, choices=[1, 6], default=1,
                        help="One uses exact original cases; six is a separate cross-record stress test.")
    parser.add_argument("--model", default="qwen2.5-coder:1.5b")
    parser.add_argument("--endpoint", default="http://127.0.0.1:11439")
    args = parser.parse_args()
    args.output.mkdir()  # Refuse overwriting evidence or replaying an uncertain attempt.
    baseline = load_baseline(args.output)
    current = {"brief": brief, "ollama": ollama, "parsing": parsing, "report": report}
    cases_bytes = args.cases.read_bytes()
    cases = json.loads(cases_bytes)
    result = {"scope": "Authored synthetic rubric, not diagnostic accuracy; includes identical inputs with unknowable differing provenance labels.",
              "baseline_commit": BASELINE, "candidate_version": __version__,
              "batch_size": args.batch_size,
              "cases_sha256": hashlib.sha256(cases_bytes).hexdigest(),
              "candidate_brief_sha256": hashlib.sha256((ROOT / "lazy_ci_triage/brief.py").read_bytes()).hexdigest(),
              "baseline_brief_sha256": hashlib.sha256((args.output / "baseline-code/lazy_ci_triage/brief.py").read_bytes()).hexdigest(),
              "gate": {}, "model": {}, "runs": []}
    for variant, contract in [("baseline", baseline), ("candidate", current)]:
        rows = eligibility(contract, cases)
        result["gate"][variant] = {"metrics": gate_metrics(rows), "rows": rows}
    (args.output / "comparison.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.inference:
        all_rows = {"baseline": [], "candidate": []}
        # Frozen order; paired policies receive identical input bytes and format.
        for offset in range(0, len(cases), args.batch_size):
            batch = cases[offset:offset + args.batch_size]
            for variant, contract, version in [("baseline", baseline, "0.2.1"), ("candidate", current, __version__)]:
                run = f"{variant}-{offset // args.batch_size + 1:02}"
                output = infer(contract, batch, args.output / run, args.model, args.endpoint, version)
                all_rows[variant].extend(model_rows(batch, output))
                result["runs"].append({"run": run, "ids": [c["id"] for c in batch], "status": output["status"],
                                       "wall_seconds": output.get("runtime", {}).get("wall_seconds"),
                                       "eval_count": output.get("runtime", {}).get("eval_count")})
                result["model"][variant] = {"metrics": model_metrics(all_rows[variant]), "rows": all_rows[variant]}
                (args.output / "comparison.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
                print(run, output["status"], output.get("runtime", {}).get("wall_seconds"), flush=True)
    print(json.dumps({k: {v: r["metrics"] for v, r in result[k].items()} for k in ["gate", "model"]}, indent=2))


if __name__ == "__main__":
    main()
