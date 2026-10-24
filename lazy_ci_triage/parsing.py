"""Bounded parsers for synthetic/public JUnit and pytest summaries."""

from dataclasses import dataclass
import hashlib
import re
import xml.etree.ElementTree as ET

MAX_BYTES = 256 * 1024
MAX_FAILURES = 20
MAX_EXCERPT = 4000
CONTROL_CHARACTERS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")
PYTEST_REASON_SEPARATOR = re.compile(r"\s+-\s+")


class InputError(ValueError):
    """Input cannot be safely or meaningfully parsed."""


@dataclass(frozen=True)
class Failure:
    test_id: str
    log_id: str
    name: str
    location: str
    text: str
    truncated: bool = False


@dataclass(frozen=True)
class Dataset:
    input_sha256: str
    failures: tuple[Failure, ...]


def parse_input(data: bytes, kind: str) -> Dataset:
    if kind not in {"junit", "pytest"}:
        raise InputError("Choose junit or pytest input format.")
    if not data or len(data) > MAX_BYTES:
        raise InputError("Input must contain 1 to 262144 bytes.")
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise InputError("Input must be UTF-8 text.") from exc
    if CONTROL_CHARACTERS.search(text):
        raise InputError("Control characters are not supported; use plain uncolored logs.")
    records = _junit(text) if kind == "junit" else _pytest(text)
    if len(records) > MAX_FAILURES:
        raise InputError("At most 20 failed test records are supported; split the input.")
    failures = []
    for index, (name, location, excerpt) in enumerate(records, 1):
        if len(name) > 500:
            raise InputError("Test name exceeds 500 characters.")
        truncated = len(excerpt) > MAX_EXCERPT
        if truncated:
            excerpt = excerpt[:MAX_EXCERPT]
        failures.append(Failure(f"T{index:03}", f"L{index:03}", name,
                                location, excerpt, truncated))
    return Dataset(hashlib.sha256(data).hexdigest(), tuple(failures))


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _junit(text: str) -> list[tuple[str, str, str]]:
    if re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", text, re.IGNORECASE):
        raise InputError("XML declarations of entities or doctypes are forbidden.")
    try:
        root = ET.fromstring(text)
    except (ET.ParseError, ValueError) as exc:
        raise InputError("Malformed JUnit XML.") from exc
    if _local_name(root.tag) not in {"testsuite", "testsuites"}:
        raise InputError("JUnit root must be testsuite or testsuites.")
    records = []
    ordinal = 0
    for case in root.iter():
        if _local_name(case.tag) != "testcase":
            continue
        ordinal += 1
        bad = [child for child in case if _local_name(child.tag) in {"failure", "error"}]
        if not bad:
            continue
        name = case.get("name", "unnamed")
        if case.get("classname"):
            name = case.get("classname") + "::" + name
        parts = []
        for child in bad:
            parts.append(" ".join(filter(None, [child.get("type"), child.get("message")]))
                         + "\n" + "".join(child.itertext()))
        excerpt = "\n".join(parts)
        # XML character references are decoded after the raw-source check.
        # Check before strip() can erase a decoded C1 control such as U+0085.
        if CONTROL_CHARACTERS.search(name) or CONTROL_CHARACTERS.search(excerpt):
            raise InputError("Control characters are not supported in decoded JUnit fields.")
        records.append((name, f"testcase #{ordinal}", excerpt.strip()))
    return records


def _pytest(text: str) -> list[tuple[str, str, str]]:
    records = []
    for line_number, line in enumerate(text.splitlines(), 1):
        parts = pytest_summary_parts(line)
        if parts:
            records.append((parts[0], f"line {line_number}", line))
    # Equivalent delimiter shape without overlapping regex repetitions on
    # adversarial '=' prefixes that do not end in '='.
    summaries = [line for line in text.splitlines()
                 if len(line) >= 2 and line.startswith("=") and line.endswith("=")]
    counts = [sum(int(count) for count in re.findall(r"\b(\d+) (?:failed|errors?)\b", line))
              for line in summaries if re.search(r"\b\d+ (?:passed|failed|errors?|skipped)\b", line)]
    if counts and counts[-1] != len(records):
        raise InputError("Pytest summary count does not match extracted failure records; use JUnit XML.")
    if not records:
        if (not any(re.search(r"\b\d+ passed\b", line) for line in summaries)
                or any(re.search(r"\b[1-9]\d* (?:failed|errors?)\b", line) for line in summaries)):
            raise InputError("No supported pytest summary found; use plain short-summary output or JUnit XML.")
    return records


def pytest_summary_parts(line: str) -> tuple[str, str] | None:
    """Split a supported summary outside parameter brackets, or reject ambiguity."""
    match = re.match(r"^(?:FAILED|ERROR)\s+(.+)$", line)
    if not match or not re.search(r"\.py::", match.group(1)):
        return None
    body = match.group(1)
    depth = 0
    node, reason = body.rstrip(), ""
    for index, char in enumerate(body):
        if char == "[":
            depth += 1
        elif char == "]":
            if depth == 0:
                raise InputError("Ambiguous pytest parameter brackets; use JUnit XML.")
            depth -= 1
        elif char.isspace() and depth == 0 and (index == 0 or not body[index - 1].isspace()):
            # Scan each whitespace run once and avoid copying the remaining
            # body at every potential delimiter position.
            separator = PYTEST_REASON_SEPARATOR.match(body, index)
            if separator:
                node = body[:index].rstrip()
                reason = body[separator.end():]
                break
    if depth:
        raise InputError("Ambiguous pytest parameter brackets; use JUnit XML.")
    if not re.fullmatch(r".+\.py::.+", node):
        return None
    return node, reason
