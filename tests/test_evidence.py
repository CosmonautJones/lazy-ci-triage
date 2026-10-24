"""Replay saved REAL inference records without running a model.

These are integrity checks on committed demo artifacts, not inference mocks.
"""

from dataclasses import asdict
import json
from pathlib import Path
import unittest

from lazy_ci_triage.brief import BriefError, validate_brief
from lazy_ci_triage.parsing import parse_input

ROOT = Path(__file__).resolve().parents[1]


class EvidenceReplayTests(unittest.TestCase):
    def assert_historical_literal_citations(self, selection, dataset):
        """Provenance replay, not retroactive acceptance under a changed policy."""
        by_id = {failure.log_id: failure for failure in dataset.failures}
        self.assertEqual(len(selection["hypotheses"]), len(dataset.failures))
        self.assertEqual({item["test_id"] for item in selection["hypotheses"]}, {f.test_id for f in dataset.failures})
        for item in selection["hypotheses"]:
            self.assertEqual(by_id[item["log_id"]].test_id, item["test_id"])
            self.assertIn(item["quote"], by_id[item["log_id"]].text)
            self.assertEqual(item["uncertainty"], "log_only_root_cause_unverified")

    def test_oct24_historical_records_match_input_and_frozen_baseline_prompt(self):
        import hashlib
        frozen = json.loads((ROOT / "evidence/oct24-baseline-prompts.json").read_text())
        cases = [("junit", "junit.xml", "junit"), ("pytest", "pytest.log", "pytest"),
                 ("lexical-trap", "lexical-trap.log", "pytest"),
                 ("parameter-delimiter", "parameter-delimiter.log", "pytest"),
                 ("short-detail", "short-detail.xml", "junit")]
        for run, fixture, kind in cases:
            with self.subTest(run=run):
                folder = ROOT / "evidence" / ("oct24-" + run)
                report = json.loads((folder / "report.json").read_text())
                dataset = parse_input((ROOT / "fixtures" / fixture).read_bytes(), kind)
                self.assertEqual(report["observed"], json.loads(json.dumps(asdict(dataset))))
                self.assertEqual(report["app_version"], "0.2.1")
                self.assertEqual(report["status"], "ok")
                self.assertEqual(json.loads(report["raw_response"]), report["model_hypotheses"])
                self.assert_historical_literal_citations(report["model_hypotheses"], dataset)
                prompt_hash = hashlib.sha256(json.dumps(frozen["requests"][run], sort_keys=True).encode()).hexdigest()
                self.assertEqual(report["runtime"]["request_sha256"], prompt_hash)
        parameter = json.loads((ROOT / "evidence/oct24-parameter-delimiter/report.json").read_text())
        self.assertEqual(parameter["observed"]["failures"][0]["name"], "tests/test_parameters.py::test_label[a - b]")
        short = json.loads((ROOT / "evidence/oct24-short-detail/report.json").read_text())
        self.assertEqual(short["model_hypotheses"]["hypotheses"][0]["quote"], "x")

    def test_oct24_no_detail_record_is_an_explicit_pre_inference_refusal(self):
        report = json.loads((ROOT / "evidence/oct24-no-detail/report.json").read_text())
        self.assertEqual(report["status"], "insufficient_evidence")
        self.assertEqual(report["observed"]["failures"][0]["text"], "")
        self.assertEqual(report["runtime"], {})
        self.assertIsNone(report["raw_response"])
        self.assertIsNone(report["model_hypotheses"])

    def test_final_v2_real_runs_keep_observations_and_model_selections_separate(self):
        cases = [("v2c-junit", "junit.xml", "junit"), ("v2c-pytest", "pytest.log", "pytest"),
                 ("v2c-injection", "injection.xml", "junit"), ("v2c-ambiguous", "ambiguous.log", "pytest"),
                 ("v2c-lexical-trap", "lexical-trap.log", "pytest")]
        count = 0
        for run, fixture, kind in cases:
            with self.subTest(run=run):
                report = json.loads((ROOT / "evidence" / run / "report.json").read_text())
                dataset = parse_input((ROOT / "fixtures" / fixture).read_bytes(), kind)
                self.assertEqual(report["observed"], json.loads(json.dumps(asdict(dataset))))
                self.assertEqual(report["schema_version"], 2)
                self.assertEqual(report["status"], "ok")
                self.assertEqual(report["operational_recommendations"]["status"], "refused")
                selection = json.loads(report["raw_response"])
                self.assertEqual(selection, report["model_hypotheses"])
                self.assert_historical_literal_citations(selection, dataset)
                count += len(selection["hypotheses"])
        self.assertEqual(count, 9)

    def test_preserved_v2_model_failures_are_still_refused(self):
        for run in ["v2-ambiguous", "v2-lexical-trap", "v2b-ambiguous", "v2b-lexical-trap"]:
            with self.subTest(run=run):
                report = json.loads((ROOT / "evidence" / run / "report.json").read_text())
                fixture = "ambiguous.log" if run.endswith("ambiguous") else "lexical-trap.log"
                dataset = parse_input((ROOT / "fixtures" / fixture).read_bytes(), "pytest")
                self.assertEqual(report["status"], "invalid_citation")
                self.assertIsNone(report["model_hypotheses"])
                with self.assertRaises(BriefError):
                    validate_brief(json.loads(report["raw_response"]), dataset)

    def test_historical_false_lexical_trap_is_rejected_by_current_policy(self):
        dataset = parse_input((ROOT / "fixtures/lexical-trap.log").read_bytes(), "pytest")
        for run in ["v2c-lexical-trap", "oct24-lexical-trap"]:
            report = json.loads((ROOT / "evidence" / run / "report.json").read_text())
            self.assertEqual(report["model_hypotheses"]["hypotheses"][0]["family"], "missing_key")
            self.assertIn("actual cause unknown", report["observed"]["failures"][0]["text"])
            with self.assertRaises(BriefError):
                validate_brief(report["model_hypotheses"], dataset)

    def test_historical_real_runs_match_inputs_but_old_prose_schema_is_rejected(self):
        for run, fixture, kind in [("junit-refined", "junit.xml", "junit"),
                                   ("pytest-run", "pytest.log", "pytest"),
                                   ("injection-run", "injection.xml", "junit")]:
            with self.subTest(run=run):
                report = json.loads((ROOT / "evidence" / run / "report.json").read_text())
                dataset = parse_input((ROOT / "fixtures" / fixture).read_bytes(), kind)
                self.assertEqual(report["dataset"], json.loads(json.dumps(asdict(dataset))))
                self.assertEqual(report["status"], "ok")
                self.assertEqual(json.loads(report["raw_response"]), report["brief"])
                with self.assertRaises(BriefError):
                    validate_brief(report["brief"], dataset)
                self.assertEqual(report["runtime"]["model_digest"], "d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668")
                self.assertGreater(report["runtime"]["eval_count"], 0)

    def test_historical_first_attempt_is_rejected_by_current_contract(self):
        report = json.loads((ROOT / "evidence/junit-run/report.json").read_text())
        dataset = parse_input((ROOT / "fixtures/junit.xml").read_bytes(), "junit")
        with self.assertRaises(BriefError):
            validate_brief(json.loads(report["raw_response"]), dataset)


if __name__ == "__main__":
    unittest.main()
