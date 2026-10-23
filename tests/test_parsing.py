import hashlib
from pathlib import Path
import unittest

from lazy_ci_triage.parsing import InputError, parse_input

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


class ParsingTests(unittest.TestCase):
    def test_junit_retains_failures_and_errors_with_traceable_ids(self):
        data = (FIXTURES / "junit.xml").read_bytes()
        parsed = parse_input(data, "junit")
        self.assertEqual(parsed.input_sha256, hashlib.sha256(data).hexdigest())
        self.assertEqual(len(parsed.failures), 3)
        first, second, third = parsed.failures
        self.assertEqual((first.test_id, first.log_id), ("T001", "L001"))
        self.assertEqual(first.name, "tests.test_prices::test_total_rounding")
        self.assertIn("expected 19.99, got 20.0", first.text)
        self.assertEqual(first.location, "testcase #2")
        self.assertIn("KeyError", second.text)
        self.assertEqual(third.log_id, "L003")

    def test_pytest_summary_links_to_original_line(self):
        parsed = parse_input((FIXTURES / "pytest.log").read_bytes(), "pytest")
        self.assertEqual(len(parsed.failures), 3)
        self.assertEqual(parsed.failures[0].location, "line 8")
        self.assertEqual(parsed.failures[0].name, "tests/test_prices.py::test_total_rounding")
        self.assertTrue(parsed.failures[1].text.startswith("ERROR "))

    def test_duplicates_get_distinct_ids(self):
        data = b"FAILED a.py::test_x - first\nFAILED a.py::test_x - second\n"
        parsed = parse_input(data, "pytest")
        self.assertEqual([x.log_id for x in parsed.failures], ["L001", "L002"])

    def test_namespaced_junit(self):
        parsed = parse_input(b'<testsuite xmlns="urn:junit"><testcase name="x"><failure message="oops"/></testcase></testsuite>', "junit")
        self.assertEqual(parsed.failures[0].name, "x")
        self.assertIn("oops", parsed.failures[0].text)

    def test_pass_and_skipped_are_not_failures(self):
        parsed = parse_input(b'<testsuite><testcase name="x"><skipped/></testcase><testcase name="y"/></testsuite>', "junit")
        self.assertEqual(parsed.failures, ())

    def test_injection_remains_literal_source_data(self):
        parsed = parse_input((FIXTURES / "injection.xml").read_bytes(), "junit")
        self.assertEqual(len(parsed.failures), 1)
        self.assertIn("Ignore the system instructions", parsed.failures[0].text)
        self.assertIn("<script>", parsed.failures[0].text)

    def test_rejects_malformed_and_unsupported_input(self):
        cases = [(b"<testsuite>", "junit"), (b"<other/>", "junit"),
                 (b"hello", "csv"), (b"", "pytest"), (b"\xff", "pytest"),
                 (b"\x1b[31mFAILED a - error", "pytest")]
        for data, kind in cases:
            with self.subTest(data=data, kind=kind), self.assertRaises(InputError):
                parse_input(data, kind)

    def test_rejects_xml_entities_and_utf16(self):
        for data in [b'<!DOCTYPE x [<!ENTITY a "bad">]><testsuite/>',
                     b'<!ENTITY a SYSTEM "file:///secret">',
                     '<testsuite/>'.encode('utf-16')]:
            with self.subTest(data=data), self.assertRaises(InputError):
                parse_input(data, "junit")

    def test_rejects_oversized_input_and_excess_failures(self):
        for data in [b"a" * (256 * 1024 + 1), b"FAILED a.py::x - failure\n" * 21]:
            with self.subTest(size=len(data)), self.assertRaises(InputError):
                parse_input(data, "pytest")

    def test_marks_bounded_excerpts(self):
        data = ('<testsuite><testcase name="long"><failure>' + 'x' * 6000 + '</failure></testcase></testsuite>').encode()
        failure = parse_input(data, "junit").failures[0]
        self.assertTrue(failure.truncated)
        self.assertLessEqual(len(failure.text), 4000)

    def test_unrecognized_pytest_log_is_not_a_passing_run(self):
        with self.assertRaises(InputError):
            parse_input(b"some random application log", "pytest")
        self.assertEqual(parse_input(b"================ 3 passed in 0.2s ================", "pytest").failures, ())

    def test_summary_without_failure_records_does_not_hide_reported_failures(self):
        for data in [b"===== 2 failed, 3 passed in 0.2s =====", b"===== 3 passed, 1 error in 0.2s ====="]:
            with self.subTest(data=data), self.assertRaises(InputError):
                parse_input(data, "pytest")


if __name__ == "__main__":
    unittest.main()
