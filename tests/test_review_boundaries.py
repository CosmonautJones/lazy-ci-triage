"""Independent-review regressions for deterministic input boundaries."""

from pathlib import Path
import subprocess
import sys
import unittest

from lazy_ci_triage.parsing import InputError, parse_input

ROOT = Path(__file__).resolve().parents[1]


class ReviewBoundaryTests(unittest.TestCase):
    def test_long_whitespace_without_reason_delimiter_finishes_in_bounded_child(self):
        script = ("from lazy_ci_triage.parsing import InputError, parse_input\n"
                  "try:\n    parse_input(b'FAILED a.py::test ' + b' ' * 200000 + b'x', 'pytest')\n"
                  "except InputError:\n    pass\n"
                  "else:\n    raise AssertionError('Oversized test identifier accepted')\n")
        try:
            result = subprocess.run([sys.executable, "-B", "-c", script], cwd=ROOT,
                                    capture_output=True, text=True, timeout=3)
        except subprocess.TimeoutExpired:
            self.fail("Pytest delimiter search exceeded the bounded three-second child deadline")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_malformed_summary_at_size_limit_finishes_in_bounded_child(self):
        # Reintroducing overlapping separator repetitions stalls this child.
        script = ("from lazy_ci_triage.parsing import InputError, parse_input\n"
                  "try:\n    parse_input(b'=' * 262143 + b'x', 'pytest')\n"
                  "except InputError:\n    pass\n"
                  "else:\n    raise AssertionError('Malformed summary accepted')\n")
        try:
            result = subprocess.run([sys.executable, "-B", "-c", script], cwd=ROOT,
                                    capture_output=True, text=True, timeout=3)
        except subprocess.TimeoutExpired:
            self.fail("Malformed pytest separator exceeded the bounded three-second child deadline")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_decoded_controls_in_junit_details_are_input_errors(self):
        for char in ["&#127;", "&#x85;", "&#x9f;"]:
            for detail in [f"<failure>{char}</failure>",
                           f'<error type="KeyError" message="{char}"/>',
                           f'<failure type="{char}">detail</failure>']:
                data = ('<testsuite><testcase name="demo">' + detail + '</testcase></testsuite>').encode()
                with self.subTest(detail=detail), self.assertRaises(InputError):
                    parse_input(data, "junit")

    def test_decoded_controls_in_junit_metadata_are_input_errors(self):
        for attributes in ['name="&#127;"', 'name="demo" classname="&#x85;"']:
            data = ('<testsuite><testcase ' + attributes + '><failure>detail</failure></testcase></testsuite>').encode()
            with self.subTest(attributes=attributes), self.assertRaises(InputError):
                parse_input(data, "junit")


if __name__ == "__main__":
    unittest.main()
