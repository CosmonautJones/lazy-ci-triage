"""Command line interface."""

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from . import __version__
from .ollama import InferenceError, generate
from .parsing import InputError, MAX_BYTES, parse_input
from .report import render_report


def main(argv=None):
    parser = argparse.ArgumentParser(description="Draft evidence-linked CI hypotheses from synthetic/public test output.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--format", choices=["junit", "pytest"], required=True)
    parser.add_argument("--output", type=Path, required=True, help="New directory; existing paths are never overwritten")
    parser.add_argument("--mode", choices=["model", "inventory"], default="model")
    parser.add_argument("--model", default="qwen2.5-coder:1.5b")
    parser.add_argument("--endpoint", default="http://127.0.0.1:11434")
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--public-data", action="store_true", help="Acknowledge input is synthetic or reviewed public data without secrets/personal data")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)
    if not args.public_data:
        print("Input rejected: --public-data acknowledgement is required. Use synthetic or reviewed public data only.", file=sys.stderr)
        return 2
    if args.output.exists() or args.output.is_symlink():
        print("Output rejected: choose a new directory.", file=sys.stderr)
        return 2
    try:
        with args.input.open("rb") as source:
            dataset = parse_input(source.read(MAX_BYTES + 1), args.format)
    except (OSError, InputError) as exc:
        # Avoid echoing input paths or malformed source text to the terminal.
        message = str(exc) if isinstance(exc, InputError) else "Input file could not be read."
        print("Input rejected: " + message, file=sys.stderr)
        return 2
    report = {"app_version": __version__, "created_at_utc": datetime.now(timezone.utc).isoformat(),
              "mode": args.mode, "status": "inventory_only", "dataset": asdict(dataset),
              "brief": None, "runtime": {}, "raw_response": None}
    code = 0
    if not dataset.failures:
        report["status"] = "no_failures"
    elif args.mode == "model":
        try:
            report.update(generate(dataset, args.model, args.endpoint, args.timeout))
            report["status"] = "ok"
        except InferenceError as exc:
            report.update(status=exc.status, error=str(exc), runtime=exc.runtime, raw_response=exc.raw_response)
            code = 3
    try:
        args.output.mkdir(parents=True, exist_ok=False)
        (args.output / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        (args.output / "report.md").write_text(render_report(report), encoding="utf-8")
    except OSError:
        print("Output failed: reports could not be written completely. Inspect the selected directory.", file=sys.stderr)
        return 2
    print(f"status={report['status']} mode={args.mode} failures={len(dataset.failures)}")
    return code
