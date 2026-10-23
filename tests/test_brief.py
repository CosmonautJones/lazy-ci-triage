import copy
import json
from pathlib import Path
import unittest

from lazy_ci_triage.parsing import parse_input
from lazy_ci_triage.brief import BriefError, build_prompt, validate_brief
from lazy_ci_triage.report import render_report

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def example():
    return {"findings": [{
        "hypothesis": "The assertion may reflect a rounding boundary.",
        "inspection": "Compare expected decimal rounding with the calculation.",
        "uncertainty": "The implementation is absent; the root cause is unconfirmed.",
        "citations": [{"test_id": "T001", "log_id": "L001", "quote": "expected 19.99, got 20.0"}]
    }]}


class BriefTests(unittest.TestCase):
    def setUp(self):
        self.dataset = parse_input(b"FAILED tests/a.py::test_round - expected 19.99, got 20.0", "pytest")

    def test_accepts_exact_paired_source_citation(self):
        self.assertEqual(validate_brief(example(), self.dataset), example())

    def test_rejects_unknown_ids_and_nonverbatim_quotes(self):
        for field, value in [("test_id", "T999"), ("log_id", "L999"), ("quote", "expected 17.99")]:
            item = example()
            item["findings"][0]["citations"][0][field] = value
            with self.subTest(field=field), self.assertRaises(BriefError):
                validate_brief(item, self.dataset)

    def test_rejects_citation_to_wrong_test(self):
        dataset = parse_input(b"FAILED a - first\nFAILED b - second", "pytest")
        item = example()
        item["findings"][0]["citations"] = [{"test_id": "T002", "log_id": "L001", "quote": "first"}]
        with self.assertRaises(BriefError):
            validate_brief(item, dataset)

    def test_requires_complete_failure_coverage(self):
        dataset = parse_input(b"FAILED a - expected 19.99, got 20.0\nFAILED b - other", "pytest")
        with self.assertRaisesRegex(BriefError, "coverage"):
            validate_brief(example(), dataset)

    def test_rejects_repeated_evidence_in_duplicate_findings(self):
        item = example()
        item["findings"].append(copy.deepcopy(item["findings"][0]))
        with self.assertRaisesRegex(BriefError, "repeated"):
            validate_brief(item, self.dataset)

    def test_schema_bounds_findings_by_number_of_failed_tests(self):
        schema = build_prompt(self.dataset)["format"]
        self.assertEqual(schema["properties"]["findings"]["maxItems"], 1)

    def test_requires_bounded_schema_and_no_extra_prose(self):
        invalid = [None, [], {}, {"findings": []}, {"findings": "text"},
                   {"findings": example()["findings"], "summary": "uncited"}]
        for field, value in [("hypothesis", ""), ("inspection", 8), ("uncertainty", "x" * 1201),
                             ("citations", []), ("citations", ["T001"]),
                             ("hypothesis", "bad\x1b[31m")]:
            item = example()
            item["findings"][0][field] = value
            invalid.append(item)
        item = example()
        item["findings"][0]["citations"][0]["url"] = "https://untrusted.invalid"
        invalid.append(item)
        for item in invalid:
            with self.subTest(item=str(item)[:80]), self.assertRaises(BriefError):
                validate_brief(item, self.dataset)

    def test_prompt_keeps_hostile_text_in_data_and_constrains_ids(self):
        dataset = parse_input((FIXTURES / "injection.xml").read_bytes(), "junit")
        payload = build_prompt(dataset)
        records = json.loads(payload["prompt"])["untrusted_evidence"]
        self.assertIn("Ignore the system instructions", records[0]["text"])
        self.assertNotIn("Ignore the system instructions", payload["system"])
        self.assertIn("untrusted", payload["system"])
        citation = payload["format"]["properties"]["findings"]["items"]["properties"]["citations"]["items"]
        self.assertEqual(citation["properties"]["log_id"]["enum"], ["L001"])

    def test_render_escapes_source_and_model_html_links_and_fences(self):
        dataset = parse_input((FIXTURES / "injection.xml").read_bytes(), "junit")
        item = example()
        item["findings"][0]["hypothesis"] = '<img src=x onerror=alert(1)> [click](https://evil.invalid) ```'
        item["findings"][0]["citations"][0]["quote"] = "banner text differs"
        report = {"status": "ok", "mode": "model", "brief": validate_brief(item, dataset),
                  "dataset": {"input_sha256": dataset.input_sha256,
                              "failures": [vars(f) for f in dataset.failures]},
                  "runtime": {"model": "local"}}
        rendered = render_report(report)
        self.assertNotIn("<script>", rendered)
        self.assertNotIn("<img src=x", rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn('href="#evidence-L001"', rendered)
        self.assertIn("not proof", rendered)


if __name__ == "__main__":
    unittest.main()
