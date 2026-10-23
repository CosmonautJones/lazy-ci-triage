"""Loopback-only Ollama transport; never starts servers or downloads weights."""

import hashlib
from http.client import HTTPException
import json
import math
import socket
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from .brief import BriefError, build_prompt, validate_brief

MAX_RESPONSE_BYTES = 1024 * 1024
OPTIONS = {"temperature": 0, "seed": 42, "num_ctx": 32768, "num_predict": 1800}


class InferenceError(RuntimeError):
    def __init__(self, status, message, runtime=None, raw_response=None):
        super().__init__(message)
        self.status = status
        self.runtime = runtime or {}
        self.raw_response = raw_response


def generate(dataset, model, endpoint, timeout):
    endpoint = _endpoint(endpoint)
    if not isinstance(model, str) or not model or len(model) > 200:
        raise InferenceError("invalid_response", "Choose a valid installed local model name.")
    if not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or not 0 < timeout <= 600:
        raise InferenceError("invalid_response", "Timeout must be finite, greater than 0 and at most 600 seconds.")
    prompt = build_prompt(dataset)
    if len(prompt["prompt"]) > 24000:
        raise InferenceError("input_budget_exceeded", "Evidence exceeds the 24000-character model budget; split the input.")
    runtime = {"model": model, "options": OPTIONS.copy()}
    start = time.perf_counter()
    raw = None
    try:
        version = _request(endpoint, "/api/version", None, timeout)
        tags = _request(endpoint, "/api/tags", None, timeout)
        models = tags.get("models")
        if not isinstance(models, list):
            raise InferenceError("invalid_response", "Malformed local model inventory.")
        tag = model if ":" in model else model + ":latest"
        installed = next((entry for entry in models if isinstance(entry, dict) and entry.get("name") == tag), None)
        if installed is None:
            raise InferenceError("model_unavailable", "Requested model is not installed; no download attempted.")
        show = _request(endpoint, "/api/show", {"model": model}, timeout)
        runtime.update({"ollama_version": version.get("version"),
                        "model_digest": installed.get("digest"),
                        "details": show.get("details"),
                        "license_sha256": hashlib.sha256(str(show.get("license", "")).encode()).hexdigest(),
                        "request_sha256": hashlib.sha256(json.dumps(prompt, sort_keys=True).encode()).hexdigest()})
        response = _request(endpoint, "/api/generate", {
            "model": model, **prompt, "stream": False, "keep_alive": 0, "options": OPTIONS,
        }, timeout)
        raw = response.get("response")
        for field in ["created_at", "done_reason", "total_duration", "load_duration", "prompt_eval_count",
                      "prompt_eval_duration", "eval_count", "eval_duration"]:
            if field in response:
                runtime[field] = response[field]
        runtime["wall_seconds"] = round(time.perf_counter() - start, 6)
        if response.get("done") is not True or response.get("done_reason") != "stop" or not isinstance(raw, str):
            raise InferenceError("invalid_response", "Local model response is incomplete or reached its generation limit.")
        try:
            value = json.loads(raw)
        except (ValueError, RecursionError) as exc:
            raise InferenceError("invalid_response", "Local model did not return a JSON brief.") from exc
        try:
            brief = validate_brief(value, dataset)
        except BriefError as exc:
            raise InferenceError("invalid_citation", str(exc)) from exc
        return {"model_hypotheses": brief, "runtime": runtime, "raw_response": raw}
    except InferenceError as exc:
        runtime["wall_seconds"] = round(time.perf_counter() - start, 6)
        exc.runtime = runtime
        exc.raw_response = raw
        raise


def _endpoint(value):
    try:
        parts = urlsplit(value)
        port = parts.port
    except (ValueError, TypeError) as exc:
        raise InferenceError("model_unavailable", "Invalid loopback endpoint.") from exc
    if (parts.scheme != "http" or parts.hostname != "127.0.0.1" or parts.username is not None
            or parts.password is not None or parts.path not in {"", "/"} or parts.query or parts.fragment
            or (port is not None and not 1 <= port <= 65535)):
        raise InferenceError("model_unavailable", "Only http://127.0.0.1:<port> endpoints are allowed.")
    return f"http://127.0.0.1:{port or 80}"


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _request(endpoint, path, body, timeout):
    opener = build_opener(ProxyHandler({}), _NoRedirect())
    data = json.dumps(body).encode() if body is not None else None
    request = Request(endpoint + path, data=data, headers={"Content-Type": "application/json"})
    try:
        with opener.open(request, timeout=timeout) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
    except (TimeoutError, socket.timeout) as exc:
        raise InferenceError("model_timeout", "Local model request timed out; no fallback generated.") from exc
    except HTTPException as exc:
        raise InferenceError("invalid_response", "Local model HTTP response was incomplete or malformed.") from exc
    except (HTTPError, URLError, OSError) as exc:
        status = "model_timeout" if isinstance(getattr(exc, "reason", None), (TimeoutError, socket.timeout)) else "model_unavailable"
        raise InferenceError(status, "Cannot use the local Ollama endpoint; check the server and installed model.") from exc
    if len(raw) > MAX_RESPONSE_BYTES:
        raise InferenceError("invalid_response", "Local model response exceeded 1 MiB.")
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise InferenceError("invalid_response", "Local endpoint returned malformed JSON.") from exc
    if not isinstance(value, dict):
        raise InferenceError("invalid_response", "Local endpoint returned an unexpected JSON type.")
    try:
        json.dumps(value, ensure_ascii=False).encode("utf-8")
    except (UnicodeError, RecursionError) as exc:
        raise InferenceError("invalid_response", "Local endpoint returned invalid Unicode or nesting.") from exc
    if "error" in value:
        raise InferenceError("model_unavailable", "Local model server returned an error.")
    return value
