"""Literal regression cases: weakening the gate must re-enable false labels."""

import json
import unittest
from xml.sax.saxutils import escape

from lazy_ci_triage.brief import BriefError, build_prompt, validate_brief
from lazy_ci_triage.parsing import parse_input


def dataset_for(detail, kind="pytest", node="tests/test_demo.py::test_result"):
    if kind == "pytest":
        return parse_input(("FAILED " + node + " - " + detail).encode(), kind)
    return parse_input(("<testsuite><testcase name='demo'><failure>" + escape(detail)
                        + "</failure></testcase></testsuite>").encode(), kind)


def offered(dataset):
    return json.loads(build_prompt(dataset)["prompt"])["untrusted_evidence"][0]["eligible_families"]


class StructuralSupportTests(unittest.TestCase):
    def test_prose_mentions_identifiers_and_quoted_docs_only_offer_abstention(self):
        cases = [
            ("text mentions KeyError as an example; actual cause unknown", "pytest"),
            ("The documentation says ConnectionRefusedError can occur", "junit"),
            ('Guide example: "AssertionError: wrong value"', "pytest"),
            ("No KeyError was raised; fixture result unknown", "pytest"),
            ("see expected value and actual output documentation", "junit"),
            ("> KeyError: 'quoted example'", "junit"),
            ("`ConnectionRefusedError: example`", "pytest"),
        ]
        for text, kind in cases:
            with self.subTest(text=text):
                self.assertEqual(offered(dataset_for(text, kind)), ["unclassified"])
        self.assertEqual(offered(dataset_for("fixture failed", node="tests/KeyError.py::test_assert")), ["unclassified"])

    def test_supported_failure_shapes_retain_their_family(self):
        cases = [
            ("KeyError: 'sku-17'", "pytest", "missing_key"),
            ("builtins.KeyError: 'sku-18'", "pytest", "missing_key"),
            ("Traceback (most recent call last):\n  File \"sample.py\", line 2\n    read()\nKeyError: 'sku-19'", "junit", "missing_key"),
            ("E   AssertionError: mismatch", "junit", "assertion_mismatch"),
            ("assert count == 2", "junit", "assertion_mismatch"),
            ("expected 19.99, got 20.0", "pytest", "assertion_mismatch"),
            ("ConnectionRefusedError: [Errno 111] Connection refused", "pytest", "connection_refused"),
            ("connection refused on loopback", "pytest", "connection_refused"),
        ]
        for text, kind, family in cases:
            with self.subTest(text=text):
                self.assertEqual(offered(dataset_for(text, kind)), [family, "unclassified"])

    def test_message_contents_do_not_override_exception_family(self):
        for detail, family in [("AssertionError: expected KeyError but no exception was raised", "assertion_mismatch"),
                               ("KeyError: 'ConnectionRefusedError assert'", "missing_key"),
                               ("RuntimeError: docs mention KeyError and assert", None)]:
            with self.subTest(detail=detail):
                self.assertEqual(offered(dataset_for(detail)), ([family] if family else []) + ["unclassified"])

    def test_conflicting_failure_signatures_abstain(self):
        dataset = dataset_for("KeyError: 'first'\nDuring handling of the above exception:\nAssertionError: second", "junit")
        self.assertEqual(offered(dataset), ["unclassified"])

    def test_old_false_label_is_rejected_but_literal_abstention_is_valid(self):
        text = "text mentions KeyError as an example; actual cause unknown"
        dataset = dataset_for(text)
        item = {"test_id": "T001", "log_id": "L001", "family": "missing_key", "quote": text,
                "uncertainty": "log_only_root_cause_unverified"}
        with self.assertRaises(BriefError):
            validate_brief({"hypotheses": [item]}, dataset)
        item["family"] = "unclassified"
        self.assertEqual(validate_brief({"hypotheses": [item]}, dataset)["hypotheses"][0]["family"], "unclassified")

    def test_quote_with_only_incidental_keyword_is_not_label_support(self):
        dataset = dataset_for("AssertionError: wrong value\nnotes mention assert", "junit")
        item = {"test_id": "T001", "log_id": "L001", "family": "assertion_mismatch", "quote": "notes mention assert",
                "uncertainty": "log_only_root_cause_unverified"}
        with self.assertRaises(BriefError):
            validate_brief({"hypotheses": [item]}, dataset)

    def test_copied_exception_shaped_example_remains_an_explicit_limit(self):
        # Syntax cannot authenticate input. A copied example is indistinguishable.
        self.assertEqual(offered(dataset_for("KeyError: 'documentation-example'", "junit")),
                         ["missing_key", "unclassified"])


if __name__ == "__main__":
    unittest.main()
