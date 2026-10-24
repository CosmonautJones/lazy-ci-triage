"""Integrity of saved real runs; these tests never masquerade as inference."""

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import unittest

from lazy_ci_triage.brief import BriefError, build_prompt, validate_brief
from lazy_ci_triage.parsing import parse_input
from lazy_ci_triage.report import render_report

ROOT = Path(__file__).resolve().parents[1]
DIGEST = "d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668"


class SupportEvidenceTests(unittest.TestCase):
    def test_frozen_cases_keep_their_hash_and_indistinguishable_pairs(self):
        raw = (ROOT / "fixtures/structural-support-heldout.json").read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), "ea89c56033b22d24d4a490a1b042ca7af702e80e2b873003c680874f92238f87")
        cases = {case["id"]: case for case in json.loads(raw)}
        for positive, copy in [("H02", "H28"), ("H07", "H29"), ("H12", "H30")]:
            self.assertEqual(cases[positive]["input"], cases[copy]["input"])
            self.assertNotEqual(cases[positive]["expected_family"], cases[copy]["expected_family"])

    def test_all_individual_inputs_are_exact_and_current_responses_replay(self):
        cases = json.loads((ROOT / "fixtures/structural-support-heldout.json").read_text())
        for index, case in enumerate(cases, 1):
            for variant in ["baseline", "candidate"]:
                with self.subTest(case=case["id"], variant=variant):
                    folder = ROOT / "evidence/support-individual" / f"{variant}-{index:02}"
                    data = (folder / ("input.xml" if case["format"] == "junit" else "input.log")).read_bytes()
                    self.assertEqual(data, case["input"].encode())
                    dataset = parse_input(data, case["format"])
                    record = json.loads((folder / "report.json").read_text())
                    self.assertEqual(record["observed"], json.loads(json.dumps(asdict(dataset))))
                    payload = json.loads((folder / "request.json").read_text())
                    self.assertEqual(hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest(), record["runtime"]["request_sha256"])
                    self.assertEqual(record["runtime"]["model_digest"], DIGEST)
                    self.assertEqual(record["runtime"]["ollama_version"], "0.18.0")
                    self.assertGreater(record["runtime"]["eval_count"], 0)
                    self.assertEqual(record["operational_recommendations"]["status"], "refused")
                    raw = json.loads(record["raw_response"])
                    if record["status"] == "ok":
                        self.assertEqual(raw, record["model_hypotheses"])
                        self.assertEqual(len(raw["hypotheses"]), 1)
                        self.assertEqual(raw["hypotheses"][0]["test_id"], "T001")
                        self.assertEqual(raw["hypotheses"][0]["log_id"], "L001")
                        self.assertIn(raw["hypotheses"][0]["quote"], dataset.failures[0].text)
                    else:
                        self.assertEqual(record["status"], "invalid_citation")
                        self.assertIsNone(record["model_hypotheses"])
                    if variant == "candidate":
                        self.assertEqual(payload, build_prompt(dataset))
                        if record["status"] == "ok":
                            self.assertEqual(validate_brief(raw, dataset), record["model_hypotheses"])
                        else:
                            with self.assertRaises(BriefError):
                                validate_brief(raw, dataset)
                        self.assertEqual((folder / "report.md").read_text(encoding="utf-8"), render_report(record))

    def test_comparison_counts_include_refusals_and_coverage_loss(self):
        comparison = json.loads((ROOT / "evidence/support-individual/comparison.json").read_text())
        self.assertEqual(len(comparison["runs"]), 60)
        for variant, false, correct, abstained in [("baseline", 7, 12, 10), ("candidate", 2, 9, 18)]:
            measured = comparison["model"][variant]
            self.assertEqual(measured["metrics"]["false_specific"], false)
            self.assertEqual(measured["metrics"]["correct_specific"], correct)
            self.assertEqual(measured["metrics"]["all_abstentions"], abstained)
            self.assertEqual(measured["metrics"]["accepted_selections"], 29)
            self.assertEqual(measured["metrics"]["missing_due_to_refused_report"], 1)
            # Compare summary rows to the actual accepted report, never raw rejected proposals.
            for index, row in enumerate(measured["rows"], 1):
                record = json.loads((ROOT / "evidence/support-individual" / f"{variant}-{index:02}" / "report.json").read_text())
                selected = record["model_hypotheses"]["hypotheses"][0]["family"] if record["model_hypotheses"] else None
                self.assertEqual(row["selected"], selected)
                self.assertEqual(row["status"], record["status"])

    def test_failed_batch_stress_reports_are_retained_and_still_refused(self):
        comparison = json.loads((ROOT / "evidence/support-batch/comparison.json").read_text())
        self.assertEqual(len(comparison["runs"]), 10)
        for variant, accepted in [("baseline", 6), ("candidate", 12)]:
            self.assertEqual(comparison["model"][variant]["metrics"]["accepted_selections"], accepted)
        for run in comparison["runs"]:
            folder = ROOT / "evidence/support-batch" / run["run"]
            record = json.loads((folder / "report.json").read_text())
            self.assertEqual(record["status"], run["status"])
            self.assertEqual(record["runtime"]["model_digest"], DIGEST)
            if run["run"].startswith("candidate"):
                dataset = parse_input((folder / "input.xml").read_bytes(), "junit")
                if record["status"] != "ok":
                    self.assertIsNone(record["model_hypotheses"])
                    with self.assertRaises(BriefError):
                        validate_brief(json.loads(record["raw_response"]), dataset)
                else:
                    self.assertEqual(validate_brief(json.loads(record["raw_response"]), dataset), record["model_hypotheses"])

    def test_current_cli_demo_preserves_junit_and_abstains_on_original_trap(self):
        for run, fixture, kind, families in [
            ("junit", "junit.xml", "junit", ["assertion_mismatch", "missing_key", "connection_refused"]),
            ("lexical-trap", "lexical-trap.log", "pytest", ["unclassified"]),
        ]:
            folder = ROOT / "evidence" / ("support-demo-" + run)
            record = json.loads((folder / "report.json").read_text())
            dataset = parse_input((ROOT / "fixtures" / fixture).read_bytes(), kind)
            self.assertEqual(record["status"], "ok")
            self.assertEqual(record["app_version"], "0.2.2")
            self.assertEqual(record["observed"], json.loads(json.dumps(asdict(dataset))))
            self.assertEqual([s["family"] for s in record["model_hypotheses"]["hypotheses"]], families)
            self.assertEqual(validate_brief(json.loads(record["raw_response"]), dataset), record["model_hypotheses"])
            self.assertEqual((folder / "report.md").read_text(encoding="utf-8"), render_report(record))


if __name__ == "__main__":
    unittest.main()
