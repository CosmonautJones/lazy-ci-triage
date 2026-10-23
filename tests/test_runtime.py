from contextlib import contextmanager, redirect_stderr, redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest

from lazy_ci_triage.cli import main
from lazy_ci_triage.ollama import InferenceError, generate
from lazy_ci_triage.parsing import parse_input
from test_brief import example

ROOT = Path(__file__).resolve().parents[1]
DATASET = parse_input(b"FAILED tests/a.py::test_round - expected 19.99, got 20.0", "pytest")


@contextmanager
def local_server(scenario="ok"):
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            self.answer()

        def do_POST(self):
            self.answer()

        def answer(self):
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))) or b"{}")
            requests.append((self.path, body))
            if scenario == "redirect":
                self.send_response(302)
                self.send_header("Location", "http://example.invalid/private")
                self.end_headers()
                return
            if self.path == "/api/version":
                value = {"version": "test-server"}
            elif self.path == "/api/tags":
                value = {"models": [{"name": "fixture:latest", "digest": "sha256:synthetic-test-digest"}]}
            elif self.path == "/api/show":
                value = {"license": "Apache License, Version 2.0", "details": {"parameter_size": "1.5B", "quantization_level": "Q4_K_M"}}
                if scenario == "metadata_unicode":
                    value["details"]["parameter_size"] = "\ud800"
            elif self.path == "/api/generate":
                if scenario == "timeout":
                    time.sleep(0.15)
                brief = example()
                if scenario == "malformed_unicode":
                    brief["findings"][0]["hypothesis"] = "Could fail.\ud800"
                if scenario == "broken_chunk":
                    self.send_response(200)
                    self.send_header("Transfer-Encoding", "chunked")
                    self.end_headers()
                    self.wfile.write(b"10\r\npartial\r\n")
                    self.close_connection = True
                    return
                if scenario == "bad_citation":
                    brief["findings"][0]["citations"][0]["log_id"] = "L999"
                value = {"model": "fixture:latest", "done": scenario != "incomplete", "done_reason": "stop",
                         "response": json.dumps(brief), "total_duration": 100000000,
                         "eval_count": 80, "prompt_eval_count": 300, "eval_duration": 50000000}
                if scenario == "bad_json":
                    value["response"] = "not JSON"
                if scenario == "length":
                    value["done_reason"] = "length"
                if scenario == "oversized":
                    value["response"] = "x" * (1024 * 1024)
            else:
                value = {"error": "unknown path"}
            encoded = json.dumps(value).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            try:
                self.wfile.write(encoded[:10] if scenario == "broken_body" and self.path == "/api/generate" else encoded)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}", requests
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


class RuntimeTests(unittest.TestCase):
    def test_real_http_transport_returns_validated_brief_and_metrics(self):
        with local_server() as (endpoint, requests):
            result = generate(DATASET, "fixture:latest", endpoint, 2)
        self.assertEqual(result["brief"], example())
        self.assertEqual(result["runtime"]["model_digest"], "sha256:synthetic-test-digest")
        self.assertEqual(result["runtime"]["eval_count"], 80)
        self.assertGreater(result["runtime"]["wall_seconds"], 0)
        payload = [body for path, body in requests if path == "/api/generate"][0]
        self.assertFalse(payload["stream"])
        self.assertEqual(payload["options"]["temperature"], 0)
        self.assertEqual(payload["keep_alive"], 0)

    def test_rejects_remote_credentials_paths_and_non_http_endpoints(self):
        for endpoint in ["https://127.0.0.1:3", "http://localhost:5", "http://example.com", "http://user@127.0.0.1", "http://127.0.0.1/api", "http://127.0.0.1?key=x"]:
            with self.subTest(endpoint=endpoint), self.assertRaises(InferenceError):
                generate(DATASET, "fixture:latest", endpoint, 1)

    def test_reports_model_failure_states_without_fallback(self):
        cases = [("bad_citation", "invalid_citation"), ("bad_json", "invalid_response"),
                 ("incomplete", "invalid_response"), ("length", "invalid_response"),
                 ("oversized", "invalid_response"), ("redirect", "model_unavailable"),
                 ("timeout", "model_timeout")]
        cases.append(("broken_body", "invalid_response"))
        cases.extend([("malformed_unicode", "invalid_citation"),
                      ("metadata_unicode", "invalid_response"), ("broken_chunk", "invalid_response")])
        for scenario, expected in cases:
            with self.subTest(scenario=scenario), local_server(scenario) as (endpoint, _):
                with self.assertRaises(InferenceError) as caught:
                    generate(DATASET, "fixture:latest", endpoint, 0.04 if scenario == "timeout" else 2)
                self.assertEqual(caught.exception.status, expected)

    def test_missing_model_never_calls_generate(self):
        with local_server() as (endpoint, requests), self.assertRaises(InferenceError) as caught:
            generate(DATASET, "not-installed:latest", endpoint, 2)
        self.assertEqual(caught.exception.status, "model_unavailable")
        self.assertNotIn("/api/generate", [path for path, _ in requests])


class CliTests(unittest.TestCase):
    def invoke(self, args):
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            return main(args)

    def test_requires_public_data_acknowledgement(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "result"
            code = self.invoke([str(ROOT / "fixtures/junit.xml"), "--format", "junit", "--output", str(output), "--mode", "inventory"])
            self.assertEqual(code, 2)
            self.assertFalse(output.exists())

    def test_inventory_is_explicitly_labeled_and_writes_traceable_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "result"
            code = self.invoke([str(ROOT / "fixtures/junit.xml"), "--format", "junit", "--output", str(output), "--mode", "inventory", "--public-data"])
            report = json.loads((output / "report.json").read_text())
            self.assertEqual(code, 0)
            self.assertEqual(report["mode"], "inventory")
            self.assertEqual(report["status"], "inventory_only")
            self.assertIsNone(report["brief"])
            self.assertEqual(len(report["dataset"]["failures"]), 3)
            self.assertIn("inventory_only", (output / "report.md").read_text(encoding="utf-8"))

    def test_model_error_report_preserves_rejected_response(self):
        with tempfile.TemporaryDirectory() as temp, local_server("bad_citation") as (endpoint, _):
            source = Path(temp) / "source.log"
            source.write_text("FAILED a.py::test_round - expected 19.99, got 20.0")
            output = Path(temp) / "result"
            code = self.invoke([str(source), "--format", "pytest", "--output", str(output), "--model", "fixture:latest", "--endpoint", endpoint, "--public-data"])
            report = json.loads((output / "report.json").read_text())
            self.assertEqual(code, 3)
            self.assertEqual(report["status"], "invalid_citation")
            self.assertIsNone(report["brief"])
            self.assertIn("L999", report["raw_response"])

    def test_no_failures_skips_unavailable_model(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "pass.xml"
            source.write_text('<testsuite><testcase name="x"/></testsuite>')
            output = Path(temp) / "result"
            code = self.invoke([str(source), "--format", "junit", "--output", str(output), "--public-data"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads((output / "report.json").read_text())["status"], "no_failures")

    def test_invalid_unicode_never_creates_an_ok_report(self):
        with tempfile.TemporaryDirectory() as temp, local_server("malformed_unicode") as (endpoint, _):
            source = Path(temp) / "source.log"
            source.write_text("FAILED a.py::test_round - expected 19.99, got 20.0")
            output = Path(temp) / "result"
            code = self.invoke([str(source), "--format", "pytest", "--output", str(output), "--model", "fixture:latest", "--endpoint", endpoint, "--public-data"])
            report = json.loads((output / "report.json").read_text())
            self.assertEqual(code, 3)
            self.assertEqual(report["status"], "invalid_citation")
            self.assertIsNone(report["brief"])
            self.assertTrue((output / "report.md").exists())

    def test_does_not_overwrite_existing_output_or_read_missing_file(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "existing"
            target.mkdir()
            sentinel = target / "keep.txt"
            sentinel.write_text("keep")
            code = self.invoke([str(ROOT / "fixtures/junit.xml"), "--format", "junit", "--output", str(target), "--mode", "inventory", "--public-data"])
            self.assertEqual(code, 2)
            self.assertEqual(sentinel.read_text(), "keep")
            self.assertEqual(self.invoke([str(Path(temp) / "missing"), "--format", "junit", "--output", str(Path(temp) / "result"), "--public-data"]), 2)


if __name__ == "__main__":
    unittest.main()
