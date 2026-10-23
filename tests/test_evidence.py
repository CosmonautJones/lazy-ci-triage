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
    def test_saved_real_runs_match_inputs_and_current_citation_contract(self):
        for run, fixture, kind in [("junit-refined", "junit.xml", "junit"),
                                   ("pytest-run", "pytest.log", "pytest"),
                                   ("injection-run", "injection.xml", "junit")]:
            with self.subTest(run=run):
                report = json.loads((ROOT / "evidence" / run / "report.json").read_text())
                dataset = parse_input((ROOT / "fixtures" / fixture).read_bytes(), kind)
                self.assertEqual(report["dataset"], json.loads(json.dumps(asdict(dataset))))
                self.assertEqual(report["status"], "ok")
                self.assertEqual(json.loads(report["raw_response"]), report["brief"])
                self.assertEqual(validate_brief(report["brief"], dataset), report["brief"])
                self.assertEqual(report["runtime"]["model_digest"], "d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668")
                self.assertGreater(report["runtime"]["eval_count"], 0)

    def test_historical_first_attempt_is_rejected_by_current_contract(self):
        report = json.loads((ROOT / "evidence/junit-run/report.json").read_text())
        dataset = parse_input((ROOT / "fixtures/junit.xml").read_bytes(), "junit")
        with self.assertRaisesRegex(BriefError, "repeated"):
            validate_brief(json.loads(report["raw_response"]), dataset)


if __name__ == "__main__":
    unittest.main()
