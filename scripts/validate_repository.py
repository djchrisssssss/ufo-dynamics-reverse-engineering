#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import ipaddress
import json
import re
import shutil
import socket
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REGISTRY_STATUSES = {"reachable", "access_restricted", "missing"}
URL_USER_AGENT = "ufo-dynamics-reverse-engineering-validator/1.0"
PRIVATE_HOST_SUFFIXES = (
    ".home",
    ".home.arpa",
    ".internal",
    ".lan",
    ".local",
    ".localhost",
)
BRACKETED_REFERENCE_RE = re.compile(r"\[([A-Za-z0-9_-]+)\]")
TABLE_REFERENCE_RE = re.compile(r"\b(?:src-\d{3}|DIRD_[A-Za-z0-9]+|[a-z]+(?:-[a-z0-9]+)+)\b")
NOTE_ID_RE = re.compile(r"ref-\d{3}[a-z]?")
KEY_JUDGMENT_ID_RE = re.compile(r"KJ-\d+[a-z]?")
NOTE_LIKE_ID_RE = re.compile(r"(?:ref|KJ)-[A-Za-z0-9_-]+")
LATEX_BIB_FIELD_RE = re.compile(r"^\s*([A-Za-z]+)\s*=\s*\{(.*)\},?\s*$")
FULL_TEXT_PATHS = ("docs/en/full-text.md", "docs/zh-TW/full-text.md")
# Tokens of claims withdrawn from the canonical English text; neither language may
# reintroduce them (R5-21).
WITHDRAWN_FULL_TEXT_TOKENS = ("10⁶⁸", "轉導", "最為簡約")
NUMBER_WORDS = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
}
LATEX_BIB_ENTRY_RE = re.compile(
    r"^\s*@(?P<entry_type>[A-Za-z]+)\s*\{\s*(?P<key>[^,\s]+)\s*,",
    re.MULTILINE,
)
LATEX_CITATION_RE = re.compile(
    r"\\(?:no)?cite[A-Za-z*]*\s*(?:\[[^]]*\]\s*)*\{([^}]*)\}",
    re.DOTALL,
)
LATEX_LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
LATEX_REFERENCE_RE = re.compile(
    r"\\(?:auto|page|name|eq|c|C)?ref\{([^}]+)\}"
)
REFERENCE_LIST_ENTRY_RE = re.compile(
    r"^(\d+)(?:\s*[–-]\s*(\d+))?\.\s+\[(PR|GOV|DIRD|BOOK|PRE)\]"
)
REFERENCE_TYPE_LABELS = {
    "peer_reviewed": "PR",
    "government": "GOV",
    "dird": "DIRD",
    "book": "BOOK",
    "preprint": "PRE",
}


def load_json(relative_path: str) -> object:
    return json.loads((ROOT / relative_path).read_text())


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text()


def number_word(value: int) -> str:
    return NUMBER_WORDS.get(value, str(value))


def status_to_category(code: int | None, body_bytes: int | None = None) -> str:
    if code is None:
        return "transient"
    if code == 202 and body_bytes == 0:
        # An empty 202 is a bot challenge, not a delivered document (R5-31).
        return "access_restricted"
    if 200 <= code < 400:
        return "reachable"
    if code in {401, 403}:
        return "access_restricted"
    if code in {404, 410}:
        return "missing"
    if code == 429 or 500 <= code < 600:
        return "transient"
    return "other"


def validate_public_https_url(url: object, *, resolve_host: bool = False) -> str | None:
    if not isinstance(url, str) or not url:
        return "URL must be a non-empty string"
    if any(ord(character) < 32 for character in url):
        return "URL contains control characters"

    try:
        parsed = urllib.parse.urlsplit(url)
        port = parsed.port
    except ValueError as exc:
        return f"URL cannot be parsed: {exc}"

    if parsed.scheme.lower() != "https":
        return "URL must use HTTPS"
    if parsed.username is not None or parsed.password is not None:
        return "URL must not contain credentials"
    if port not in {None, 443}:
        return "URL must use the default HTTPS port"

    hostname = parsed.hostname
    if hostname is None:
        return "URL is missing a hostname"
    hostname = hostname.rstrip(".").lower()
    if not hostname:
        return "URL is missing a hostname"
    if hostname == "localhost" or hostname.endswith(PRIVATE_HOST_SUFFIXES):
        return f"URL hostname {hostname!r} is local or private"

    try:
        literal_address = ipaddress.ip_address(hostname)
    except ValueError:
        try:
            hostname.encode("idna")
        except UnicodeError:
            return f"URL hostname {hostname!r} is invalid"
    else:
        if not literal_address.is_global:
            return f"URL address {literal_address} is not globally routable"

    if not resolve_host:
        return None

    try:
        address_info = socket.getaddrinfo(
            hostname,
            port or 443,
            type=socket.SOCK_STREAM,
        )
    except OSError as exc:
        return f"URL hostname {hostname!r} could not be resolved: {exc}"

    resolved_addresses = {
        item[4][0].split("%", maxsplit=1)[0] for item in address_info if item[4]
    }
    if not resolved_addresses:
        return f"URL hostname {hostname!r} resolved to no addresses"
    for address in sorted(resolved_addresses):
        try:
            parsed_address = ipaddress.ip_address(address)
        except ValueError:
            return f"URL hostname {hostname!r} resolved to invalid address {address!r}"
        if not parsed_address.is_global:
            return (
                f"URL hostname {hostname!r} resolved to non-public address "
                f"{parsed_address}"
            )

    return None


def fetch_url(url: str, timeout: int) -> tuple[int | None, int | None]:
    """Return (HTTP status, downloaded body bytes); either may be None."""
    safety_error = validate_public_https_url(url, resolve_host=True)
    if safety_error is not None:
        return None, None

    if shutil.which("curl"):
        result = subprocess.run(
            [
                "curl",
                "-L",
                "-s",
                "--proto",
                "=https",
                "--proto-redir",
                "=https",
                "--max-redirs",
                "8",
                "--connect-timeout",
                str(min(timeout, 10)),
                "-o",
                "/dev/null",
                "-w",
                "%{http_code} %{size_download}",
                "--user-agent",
                URL_USER_AGENT,
                "--max-time",
                str(timeout),
                "--",
                url,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        fields = result.stdout.split()
        if not fields or not fields[0].isdigit():
            return None, None
        status = int(fields[0])
        body_bytes: int | None = None
        if len(fields) > 1:
            try:
                body_bytes = int(float(fields[1]))
            except ValueError:
                body_bytes = None
        return (status if status != 0 else None), body_bytes

    request = urllib.request.Request(
        url,
        headers={"User-Agent": URL_USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.getcode(), len(response.read(1))
    except urllib.error.HTTPError as exc:
        return exc.code, None
    except Exception:
        return None, None


def fetch_status(url: str, timeout: int) -> int | None:
    return fetch_url(url, timeout)[0]


def validate_bibliography(errors: list[str]) -> dict[str, int]:
    bibliography = load_json("references/bibliography.json")
    metadata = bibliography["metadata"]
    sources = bibliography["sources"]

    total_sources = len(sources)
    if metadata["total_sources"] != total_sources:
        errors.append(
            f"bibliography metadata total_sources={metadata['total_sources']} != actual {total_sources}"
        )

    category_counts = Counter(source["type"] for source in sources)
    expected_categories = metadata["categories"]
    for key in sorted(set(expected_categories) | set(category_counts)):
        expected = expected_categories.get(key, 0)
        actual = category_counts.get(key, 0)
        if actual != expected:
            errors.append(
                f"bibliography category {key}={expected} != actual {actual}"
            )

    if sum(expected_categories.values()) != total_sources:
        errors.append(
            "bibliography metadata category counts do not sum to total_sources"
        )

    return {
        "total_sources": total_sources,
        "books": category_counts.get("book", 0),
    }


def validate_source_registry(errors: list[str]) -> dict[str, object]:
    registry = load_json("references/source-registry.json")
    metadata = registry["metadata"]
    urls = registry["urls"]

    total_urls = len(urls)
    if metadata["total_urls"] != total_urls:
        errors.append(
            f"source-registry metadata total_urls={metadata['total_urls']} != actual {total_urls}"
        )

    invalid_statuses = sorted(
        {entry["status"] for entry in urls if entry["status"] not in EXPECTED_REGISTRY_STATUSES}
    )
    if invalid_statuses:
        errors.append(
            f"source-registry contains unsupported statuses: {', '.join(invalid_statuses)}"
        )

    url_to_ids: dict[str, list[str]] = {}
    for entry in urls:
        url = entry["url"]
        source_id = entry["source_id"]
        safety_error = validate_public_https_url(url)
        if safety_error is not None:
            errors.append(
                f"source-registry URL for {source_id} is unsafe: {safety_error}"
            )
        url_to_ids.setdefault(url, []).append(source_id)
    duplicate_urls = {
        url: source_ids for url, source_ids in url_to_ids.items() if len(source_ids) > 1
    }
    for url, source_ids in sorted(duplicate_urls.items()):
        errors.append(
            "source-registry contains duplicate url "
            f"{url} for source_ids {', '.join(source_ids)}"
        )

    return {
        "total_urls": total_urls,
        "audit_date": metadata["last_audit"],
        "status_counts": Counter(entry["status"] for entry in urls),
    }


def extract_per_section_references(text: str) -> list[tuple[str, int]]:
    """Return (reference id, line number) pairs cited in a per-section file.

    Bracketed IDs count anywhere. In tables, only the last column of a table whose
    header names a source column (e.g. "Source", "Related Sources") is scanned, so
    prose columns such as "Gap" cannot produce false positives (R5-01).
    """
    references_with_lines: list[tuple[str, int]] = []
    in_table = False
    source_column = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in BRACKETED_REFERENCE_RE.findall(line):
            references_with_lines.append((match, line_number))
        if "|" in line:
            cells = [cell.strip() for cell in line.split("|")[1:-1]]
            if not cells:
                continue
            if not in_table:
                in_table = True
                source_column = "source" in cells[-1].lower()
                continue
            if set(cells[-1]) <= set("-: "):
                continue
            if source_column:
                for match in TABLE_REFERENCE_RE.findall(cells[-1]):
                    references_with_lines.append((match, line_number))
        else:
            in_table = False
    return references_with_lines


def note_map_source_sections(note_map: dict[str, object]) -> dict[str, set[str]]:
    """Map each src ID to the sections of the notes that cite it."""
    sections: dict[str, set[str]] = {}
    for entry in note_map["notes"].values():
        section = entry.get("section")
        if not isinstance(section, str):
            continue
        for source_id in entry.get("src_ids", []):
            sections.setdefault(source_id, set()).add(section)
    return sections


def validate_reference_ids(errors: list[str]) -> None:
    bibliography = load_json("references/bibliography.json")
    registry = load_json("references/source-registry.json")

    bibliography_ids: dict[str, dict[str, object]] = {}
    for source in bibliography["sources"]:
        source_id = source["id"]
        if source_id in bibliography_ids:
            errors.append(f"duplicate bibliography source id: {source_id}")
            continue
        bibliography_ids[source_id] = source

    registry_ids: set[str] = set()
    for entry in registry["urls"]:
        source_id = entry["source_id"]
        registry_ids.add(source_id)
        if source_id.startswith("src-") and source_id not in bibliography_ids:
            errors.append(
                f"source-registry source_id {source_id} is missing from references/bibliography.json"
            )

    known_ids = set(bibliography_ids) | registry_ids
    section_union: dict[str, set[str]] = {
        source_id: set() for source_id in bibliography_ids
    }

    for path in sorted((ROOT / "references/per-section").glob("s*-references.md")):
        section_id = path.name.split("-")[0]
        references_with_lines = extract_per_section_references(path.read_text())

        seen: set[tuple[str, int]] = set()
        for reference_id, line_number in references_with_lines:
            if (reference_id, line_number) in seen:
                continue
            seen.add((reference_id, line_number))

            if reference_id not in known_ids:
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_number} references unknown source id {reference_id}"
                )
                continue

            if reference_id in bibliography_ids:
                section_union[reference_id].add(section_id)
                sections_cited = bibliography_ids[reference_id]["sections_cited"]
                if section_id not in sections_cited:
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line_number} cites {reference_id} but bibliography sections_cited does not include {section_id}"
                    )

    note_map = load_json("references/note-map.json")
    for source_id, sections in note_map_source_sections(note_map).items():
        if source_id in section_union:
            section_union[source_id].update(sections)
    for source_id, source in bibliography_ids.items():
        declared = set(source["sections_cited"])
        expected = section_union[source_id]
        if declared != expected:
            errors.append(
                f"bibliography {source_id} sections_cited={sorted(declared)} != "
                f"per-section listings plus note-map sections {sorted(expected)}"
            )

    for path in sorted((ROOT / "data").rglob("*.csv")):
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = set(reader.fieldnames or [])
            if "source_id" not in fieldnames and "source_ids" not in fieldnames:
                continue

            for line_number, row in enumerate(reader, start=2):
                source_id = (row.get("source_id") or "").strip()
                if source_id and source_id not in known_ids:
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line_number} references unknown source id {source_id}"
                    )

                source_ids = (row.get("source_ids") or "").strip()
                if source_ids:
                    for candidate in [item.strip() for item in re.split(r"[;,]", source_ids)]:
                        if candidate and candidate not in known_ids:
                            errors.append(
                                f"{path.relative_to(ROOT)}:{line_number} references unknown source id {candidate}"
                            )


def validate_note_map(errors: list[str]) -> None:
    note_map = load_json("references/note-map.json")
    bibliography = load_json("references/bibliography.json")
    bibliography_ids = {source["id"] for source in bibliography["sources"]}

    metadata = note_map["metadata"]
    notes = note_map["notes"]
    key_judgments = note_map["key_judgments"]
    auxiliary_sources = note_map["auxiliary_sources"]

    if metadata["total_notes"] != len(notes):
        errors.append(
            "note-map metadata total_notes="
            f"{metadata['total_notes']} != actual {len(notes)}"
        )
    if metadata["total_key_judgments"] != len(key_judgments):
        errors.append(
            "note-map metadata total_key_judgments="
            f"{metadata['total_key_judgments']} != actual {len(key_judgments)}"
        )
    if metadata["total_auxiliary_sources"] != len(auxiliary_sources):
        errors.append(
            "note-map metadata total_auxiliary_sources="
            f"{metadata['total_auxiliary_sources']} != actual {len(auxiliary_sources)}"
        )

    def validate_mapping_entry(
        mapping_id: str,
        entry: dict[str, object],
        *,
        pattern: re.Pattern[str],
        require_section: bool,
    ) -> None:
        if not pattern.fullmatch(mapping_id):
            errors.append(f"note-map contains invalid mapping id: {mapping_id}")

        if require_section:
            section = entry.get("section")
            if not isinstance(section, str) or not re.fullmatch(r"s\d{2}", section):
                errors.append(
                    f"note-map {mapping_id} is missing a valid section id"
                )

        src_ids = entry.get("src_ids")
        auxiliary_ids = entry.get("auxiliary_ids")
        if not isinstance(src_ids, list) or not all(isinstance(item, str) for item in src_ids):
            errors.append(f"note-map {mapping_id} has invalid src_ids")
            src_ids = []
        if not isinstance(auxiliary_ids, list) or not all(
            isinstance(item, str) for item in auxiliary_ids
        ):
            errors.append(f"note-map {mapping_id} has invalid auxiliary_ids")
            auxiliary_ids = []

        if not src_ids and not auxiliary_ids:
            errors.append(f"note-map {mapping_id} has no mapped sources")

        for source_id in src_ids:
            if source_id not in bibliography_ids:
                errors.append(
                    f"note-map {mapping_id} references unknown bibliography source id {source_id}"
                )
        for auxiliary_id in auxiliary_ids:
            if auxiliary_id not in auxiliary_sources:
                errors.append(
                    f"note-map {mapping_id} references unknown auxiliary source id {auxiliary_id}"
                )

    for note_id, entry in notes.items():
        validate_mapping_entry(
            note_id,
            entry,
            pattern=NOTE_ID_RE,
            require_section=True,
        )

    for judgment_id, entry in key_judgments.items():
        validate_mapping_entry(
            judgment_id,
            entry,
            pattern=KEY_JUDGMENT_ID_RE,
            require_section=False,
        )

    mapped_source_ids: set[str] = set()
    for entry in list(notes.values()) + list(key_judgments.values()):
        if isinstance(entry.get("src_ids"), list):
            mapped_source_ids.update(entry["src_ids"])
    further_reading = bibliography.get("metadata", {}).get("further_reading", [])
    if not isinstance(further_reading, list):
        errors.append("bibliography metadata further_reading must be a list of src ids")
        further_reading = []
    for source_id in further_reading:
        if source_id not in bibliography_ids:
            errors.append(
                f"bibliography further_reading lists unknown source id {source_id}"
            )
        elif source_id in mapped_source_ids:
            errors.append(
                f"bibliography further_reading lists {source_id}, which is already mapped by a note"
            )
    unmapped = sorted(bibliography_ids - mapped_source_ids - set(further_reading))
    if unmapped:
        errors.append(
            "bibliography sources not mapped by any note or key judgment "
            "(map them or list them in metadata further_reading): "
            + ", ".join(unmapped)
        )

    note_ids = set(notes)
    judgment_ids = set(key_judgments)
    note_counters: dict[str, Counter] = {}
    judgment_counters: dict[str, Counter] = {}

    for relative_path in FULL_TEXT_PATHS:
        text = read_text(relative_path)
        referenced_note_ids: Counter = Counter()
        referenced_judgment_ids: Counter = Counter()
        noncanonical_ids: set[str] = set()
        for candidate in BRACKETED_REFERENCE_RE.findall(text):
            if NOTE_ID_RE.fullmatch(candidate):
                referenced_note_ids[candidate] += 1
            elif KEY_JUDGMENT_ID_RE.fullmatch(candidate):
                referenced_judgment_ids[candidate] += 1
            elif NOTE_LIKE_ID_RE.fullmatch(candidate):
                noncanonical_ids.add(candidate)
        if noncanonical_ids:
            errors.append(
                f"{relative_path} uses non-canonical note ids: "
                + ", ".join(sorted(noncanonical_ids))
            )

        note_counters[relative_path] = referenced_note_ids
        judgment_counters[relative_path] = referenced_judgment_ids

        missing_notes = sorted(set(referenced_note_ids) - note_ids)
        unused_notes = sorted(note_ids - set(referenced_note_ids))
        missing_judgments = sorted(set(referenced_judgment_ids) - judgment_ids)
        unused_judgments = sorted(judgment_ids - set(referenced_judgment_ids))

        if missing_notes:
            errors.append(
                f"{relative_path} uses note ids missing from note-map: "
                + ", ".join(missing_notes)
            )
        if unused_notes:
            errors.append(
                f"{relative_path} is missing canonical note ids: "
                + ", ".join(unused_notes)
            )
        if missing_judgments:
            errors.append(
                f"{relative_path} uses key judgment ids missing from note-map: "
                + ", ".join(missing_judgments)
            )
        if unused_judgments:
            errors.append(
                f"{relative_path} is missing canonical key judgment ids: "
                + ", ".join(unused_judgments)
            )

    en_notes = note_counters["docs/en/full-text.md"]
    zh_notes = note_counters["docs/zh-TW/full-text.md"]
    if en_notes != zh_notes:
        differences = [
            f"{note_id} (en={en_notes[note_id]}, zh-TW={zh_notes[note_id]})"
            for note_id in sorted(set(en_notes) | set(zh_notes))
            if en_notes[note_id] != zh_notes[note_id]
        ]
        errors.append("bilingual note occurrence mismatch: " + ", ".join(differences))

    en_judgments = judgment_counters["docs/en/full-text.md"]
    zh_judgments = judgment_counters["docs/zh-TW/full-text.md"]
    if en_judgments != zh_judgments:
        differences = [
            f"{judgment_id} (en={en_judgments[judgment_id]}, zh-TW={zh_judgments[judgment_id]})"
            for judgment_id in sorted(set(en_judgments) | set(zh_judgments))
            if en_judgments[judgment_id] != zh_judgments[judgment_id]
        ]
        errors.append(
            "bilingual key judgment occurrence mismatch: " + ", ".join(differences)
        )


def validate_withdrawn_claims(errors: list[str]) -> None:
    for relative_path in FULL_TEXT_PATHS:
        text = read_text(relative_path)
        for token in WITHDRAWN_FULL_TEXT_TOKENS:
            count = text.count(token)
            if count:
                errors.append(
                    f"{relative_path} contains withdrawn-claim token {token!r} ({count}x)"
                )


def validate_reference_list_inventory(errors: list[str]) -> None:
    bibliography = load_json("references/bibliography.json")
    expected_total = len(bibliography["sources"])
    expected_categories: Counter = Counter()
    for source in bibliography["sources"]:
        source_type = source["type"]
        label = REFERENCE_TYPE_LABELS.get(source_type)
        if label is None:
            errors.append(
                f"cannot inventory bibliography source type {source_type!r}"
            )
            continue
        expected_categories[label] += 1

    for relative_path in FULL_TEXT_PATHS:
        text = read_text(relative_path)
        number_counts: Counter = Counter()
        category_counts: Counter = Counter()

        for line in text.splitlines():
            match = REFERENCE_LIST_ENTRY_RE.match(line)
            if not match:
                continue
            start = int(match.group(1))
            end = int(match.group(2) or start)
            label = match.group(3)
            if end < start:
                errors.append(
                    f"{relative_path} contains descending reference range {start}-{end}"
                )
                continue
            for number in range(start, end + 1):
                number_counts[number] += 1
                category_counts[label] += 1

        expected_numbers = set(range(1, expected_total + 1))
        actual_numbers = set(number_counts)
        missing_numbers = sorted(expected_numbers - actual_numbers)
        unexpected_numbers = sorted(actual_numbers - expected_numbers)
        duplicate_numbers = sorted(
            number for number, count in number_counts.items() if count > 1
        )

        if missing_numbers:
            errors.append(
                f"{relative_path} is missing bibliography numbers: "
                + ", ".join(map(str, missing_numbers))
            )
        if unexpected_numbers:
            errors.append(
                f"{relative_path} contains unexpected bibliography numbers: "
                + ", ".join(map(str, unexpected_numbers))
            )
        if duplicate_numbers:
            errors.append(
                f"{relative_path} contains duplicate bibliography numbers: "
                + ", ".join(map(str, duplicate_numbers))
            )

        for label in sorted(set(expected_categories) | set(category_counts)):
            expected = expected_categories.get(label, 0)
            actual = category_counts.get(label, 0)
            if actual != expected:
                errors.append(
                    f"{relative_path} bibliography category {label}={actual} != expected {expected}"
                )


def strip_latex_comments(text: str) -> str:
    stripped_lines: list[str] = []
    for line in text.splitlines(keepends=True):
        comment_index: int | None = None
        for index, character in enumerate(line):
            if character != "%":
                continue
            preceding_backslashes = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == "\\":
                preceding_backslashes += 1
                cursor -= 1
            if preceding_backslashes % 2 == 0:
                comment_index = index
                break
        stripped_lines.append(line if comment_index is None else line[:comment_index] + "\n")
    return "".join(stripped_lines)


def validate_latex_integrity(expected_bib_entries: int, errors: list[str]) -> None:
    bibliography_text = read_text("latex/references.bib")
    main_text = strip_latex_comments(read_text("latex/main.tex"))

    bib_key_lines: dict[str, list[int]] = {}
    for match in LATEX_BIB_ENTRY_RE.finditer(bibliography_text):
        if match.group("entry_type").lower() in {"comment", "preamble", "string"}:
            continue
        key = match.group("key")
        line_number = bibliography_text.count("\n", 0, match.start()) + 1
        bib_key_lines.setdefault(key, []).append(line_number)

    duplicate_bib_keys = {
        key: lines for key, lines in bib_key_lines.items() if len(lines) > 1
    }
    for key, lines in sorted(duplicate_bib_keys.items()):
        errors.append(
            f"latex/references.bib contains duplicate key {key} on lines "
            + ", ".join(map(str, lines))
        )

    bib_keys = set(bib_key_lines)
    if len(bib_keys) != expected_bib_entries:
        errors.append(
            "latex/references.bib unique entry count="
            f"{len(bib_keys)} != bibliography sources {expected_bib_entries}"
        )

    citation_keys: set[str] = set()
    cites_everything = False
    for group in LATEX_CITATION_RE.findall(main_text):
        for key in (item.strip() for item in group.split(",")):
            if key == "*":
                cites_everything = True
            elif key:
                citation_keys.add(key)
    missing_citation_keys = sorted(citation_keys - bib_keys)
    if missing_citation_keys:
        errors.append(
            "latex/main.tex cites keys missing from latex/references.bib: "
            + ", ".join(missing_citation_keys)
        )
    uncited_bib_keys = [] if cites_everything else sorted(bib_keys - citation_keys)
    if uncited_bib_keys:
        # BibTeX prints only cited entries, so uncited keys silently drop out of
        # the compiled bibliography (R5-23).
        errors.append(
            "latex/references.bib keys never cited or \\nocite'd in latex/main.tex: "
            + ", ".join(uncited_bib_keys)
        )

    labels = LATEX_LABEL_RE.findall(main_text)
    duplicate_labels = sorted(
        label for label, count in Counter(labels).items() if count > 1
    )
    if duplicate_labels:
        errors.append(
            "latex/main.tex contains duplicate labels: " + ", ".join(duplicate_labels)
        )

    referenced_labels: set[str] = set()
    for group in LATEX_REFERENCE_RE.findall(main_text):
        referenced_labels.update(
            label.strip() for label in group.split(",") if label.strip()
        )
    missing_labels = sorted(referenced_labels - set(labels))
    if missing_labels:
        errors.append(
            "latex/main.tex references undefined labels: " + ", ".join(missing_labels)
        )


def parse_bibtex_entries(text: str) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    matches = list(LATEX_BIB_ENTRY_RE.finditer(text))
    for index, match in enumerate(matches):
        if match.group("entry_type").lower() in {"comment", "preamble", "string"}:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        fields: dict[str, str] = {}
        for line in text[match.end():end].splitlines():
            field_match = LATEX_BIB_FIELD_RE.match(line)
            if field_match:
                fields[field_match.group(1).lower()] = field_match.group(2)
        entries[match.group("key")] = fields
    return entries


def normalize_title(title: str) -> str:
    title = re.sub(r"^DIRD #\d+:\s*", "", title)
    for latex, plain in (("\\varepsilon", "epsilon"), ("\\epsilon", "epsilon"), ("\\mu", "mu")):
        title = title.replace(latex, plain)
    title = title.replace("ε", "epsilon").replace("μ", "mu")
    title = re.sub(r"\\[A-Za-z]+|\\.", "", title)
    return re.sub(r"[\W_]+", "", title.lower())


def validate_bibtex_metadata(errors: list[str]) -> None:
    """Cross-check references.bib against bibliography.json (R5-24)."""
    sources = load_json("references/bibliography.json")["sources"]
    entries = parse_bibtex_entries(read_text("latex/references.bib"))
    by_doi: dict[str, str] = {}
    by_title: dict[str, list[str]] = {}
    for key, fields in entries.items():
        if fields.get("doi"):
            by_doi[fields["doi"].lower()] = key
        by_title.setdefault(normalize_title(fields.get("title", "")), []).append(key)

    matched_keys: set[str] = set()
    for source in sources:
        source_id = source["id"]
        doi = (source.get("doi") or "").lower()
        key = by_doi.get(doi) if doi else None
        if key is None:
            candidates = by_title.get(normalize_title(source.get("title", "")), [])
            key = candidates[0] if len(candidates) == 1 else None
        if key is None:
            errors.append(
                f"bibliography {source_id} has no matching latex/references.bib entry (by DOI or title)"
            )
            continue
        if key in matched_keys:
            errors.append(f"latex/references.bib entry {key} matches more than one bibliography source")
        matched_keys.add(key)
        fields = entries[key]
        bib_doi = (fields.get("doi") or "").lower()
        if bib_doi != doi:
            errors.append(
                f"bibliography {source_id} doi={doi or None} != references.bib {key} doi={bib_doi or None}"
            )
        if normalize_title(fields.get("title", "")) != normalize_title(source.get("title", "")):
            errors.append(f"bibliography {source_id} title differs from references.bib {key}")
        if str(source.get("date", ""))[:4] != fields.get("year", ""):
            errors.append(
                f"bibliography {source_id} year={str(source.get('date', ''))[:4]} != references.bib {key} year={fields.get('year')}"
            )
    for key in sorted(set(entries) - matched_keys):
        errors.append(f"latex/references.bib entry {key} matches no bibliography source")


def validate_statistics(errors: list[str]) -> dict[str, int]:
    schema = load_json("data/schemas/statistics-schema.json")
    try:
        jsonschema.Draft202012Validator.check_schema(schema)
    except jsonschema.exceptions.SchemaError as exc:
        errors.append(f"statistics schema is invalid: {exc.message}")
        return {
            "total_points": 0,
            "verified_points": 0,
            "low_unverified_points": 0,
            "withdrawn_points": 0,
            "confidence_by_section": {},
        }
    validator = jsonschema.Draft202012Validator(
        schema,
        format_checker=jsonschema.FormatChecker(),
    )

    total_points = 0
    verified_points = 0
    low_unverified_points = 0
    withdrawn_points = 0
    confidence_by_section: dict[str, Counter] = {}
    seen_ids: dict[str, str] = {}
    for path in sorted((ROOT / "data/statistics").glob("*.json")):
        data = json.loads(path.read_text())
        validation_errors = sorted(
            validator.iter_errors(data), key=lambda err: list(err.absolute_path)
        )
        for err in validation_errors:
            location = "/".join(str(part) for part in err.absolute_path) or "<root>"
            errors.append(f"{path.name} schema error at {location}: {err.message}")

        if validation_errors:
            continue

        stats = data["statistics"]
        filename_section = path.stem.split("-")[0]
        if data["section"] != filename_section:
            errors.append(
                f"{path.name} declares section {data['section']} but filename implies {filename_section}"
            )

        for stat in stats:
            stat_id = stat["id"]
            if stat_id in seen_ids:
                errors.append(
                    f"duplicate statistic id {stat_id} in {path.name} and {seen_ids[stat_id]}"
                )
            else:
                seen_ids[stat_id] = path.name
            if not stat_id.startswith(f"{data['section']}-"):
                errors.append(
                    f"{path.name} statistic id {stat_id} does not match section {data['section']}"
                )

        total_points += len(stats)
        verified_points += sum(1 for stat in stats if stat["verified"])
        low_unverified_points += sum(
            1 for stat in stats if not stat["verified"] and stat["confidence"] == "low"
        )
        withdrawn_points += sum(1 for stat in stats if stat["value"] == "not defined")
        confidence_by_section[filename_section] = Counter(
            stat["confidence"] for stat in stats
        )

    unverified_points = total_points - verified_points
    if low_unverified_points + withdrawn_points != unverified_points:
        errors.append(
            "unverified statistics must each be a low-confidence estimate or a "
            f"withdrawn 'not defined' record: {unverified_points} unverified != "
            f"{low_unverified_points} low-confidence + {withdrawn_points} withdrawn"
        )

    return {
        "total_points": total_points,
        "verified_points": verified_points,
        "low_unverified_points": low_unverified_points,
        "withdrawn_points": withdrawn_points,
        "confidence_by_section": confidence_by_section,
    }


def build_doc_expectations(
    bibliography_summary: dict[str, int],
    registry_summary: dict[str, object],
    stats_summary: dict[str, object],
) -> dict[str, list[str]]:
    total_sources = bibliography_summary["total_sources"]
    total_books = bibliography_summary["books"]
    total_urls = registry_summary["total_urls"]
    total_points = stats_summary["total_points"]
    verified_points = stats_summary["verified_points"]
    low_unverified_points = stats_summary["low_unverified_points"]
    verified_percentage = f"{(verified_points / total_points) * 100:.1f}%"
    books_percentage = f"{(total_books / total_sources) * 100:.1f}%"
    s02_counts = stats_summary["confidence_by_section"].get("s02", Counter())
    s02_total = sum(s02_counts.values())
    nif_reference = "59. [GOV] Lawrence Livermore National Laboratory. \"Achieving Fusion Ignition.\" 2025."

    return {
        "README.md": [
            f"Master bibliography ({total_sources} sources)",
            f"{verified_points} of {total_points} quantitative records are marked as source-cross-checked in repository metadata",
            f"│   ├── bibliography.json            # {total_sources} sources",
            f"│   ├── references.bib               # {total_sources} BibTeX entries",
            f"Cross-referencing {total_sources} sources / 交叉比對 {total_sources} 筆來源",
            f"{total_points} 筆定量紀錄中，有 {verified_points} 筆在 repo metadata 中標記為已完成來源交叉檢查",
        ],
        "CLAUDE.md": [
            f"Master bibliography ({total_sources} sources)",
            f"BibTeX bibliography ({total_sources} entries)",
        ],
        "docs/en/full-text.md": [
            f"{verified_points} of the {total_points} quantitative records cited in this assessment are marked as source-cross-checked in repository metadata",
            f"Source provenance and reliability tier for all {total_sources} bibliography entries",
            f"Organizing and cross-referencing {total_sources} bibliography sources across peer-reviewed articles, government documents, DIRDs, and books.",
            f"URL verification status for all {total_urls} tracked web sources",
            nif_reference,
        ],
        "docs/zh-TW/full-text.md": [
            f"本評估引用的 {total_points} 筆定量紀錄中，有 {verified_points} 筆在 repo metadata 中標記為已完成來源交叉檢查",
            f"全部 {total_sources} 筆參考書目之來源出處及可靠性層級",
            f"組織並交叉比對 {total_sources} 筆參考書目來源",
            f"全部 {total_urls} 個追蹤 URL 之驗證狀態",
            nif_reference,
        ],
        "docs/en/verification-report.md": [
            f"| Total bibliography sources | {total_sources} |",
            f"| Records marked source-cross-checked in metadata | {verified_points}/{total_points} ({verified_percentage}) |",
            f"| Tracked URLs in source registry | {total_urls} |",
            f"| Books / Monographs | {total_books} | {books_percentage} |",
            "\n".join(
                [
                    f"### Section 2: Observable Characteristics ({s02_total} data points)",
                    "",
                    "| Confidence | Count |",
                    "|-----------|-------|",
                    f"| High | {s02_counts.get('high', 0)} |",
                    f"| Moderate | {s02_counts.get('moderate', 0)} |",
                    f"| Low | {s02_counts.get('low', 0)} |",
                ]
            ),
        ],
        "docs/zh-TW/verification-report.md": [
            f"| 參考文獻總數 | {total_sources} |",
            f"| metadata 標記為已完成來源交叉檢查之紀錄 | {verified_points}/{total_points} ({verified_percentage}) |",
            f"| 來源註冊中的追蹤 URL | {total_urls} |",
            f"| 學術專書 | {total_books} | {books_percentage} |",
            f"高度信心：{s02_counts.get('high', 0)} 個、中度信心：{s02_counts.get('moderate', 0)} 個、低度信心：{s02_counts.get('low', 0)} 個",
        ],
        ".zenodo.json": [
            f"{verified_points} of {total_points} quantitative records are marked as source-cross-checked in repository metadata",
            f"{number_word(low_unverified_points)} model-dependent estimates are retained as low-confidence analysis",
            f"cross-references {total_sources} bibliography sources",
        ],
        "latex/main.tex": [
            f"synthesis and cross-referencing of {total_sources} bibliography sources",
        ],
    }


def validate_docs(
    bibliography_summary: dict[str, int],
    registry_summary: dict[str, object],
    stats_summary: dict[str, object],
    errors: list[str],
) -> None:
    if bibliography_summary["total_sources"] == 0 or stats_summary["total_points"] == 0:
        errors.append(
            "cannot validate derived documentation counts without valid bibliography and statistics data"
        )
        return

    expectations = build_doc_expectations(
        bibliography_summary, registry_summary, stats_summary
    )
    for relative_path, snippets in expectations.items():
        text = read_text(relative_path)
        for snippet in snippets:
            if snippet not in text:
                errors.append(f"{relative_path} is missing expected snippet: {snippet}")


def check_urls(timeout: int, enforce_registry_status: bool, errors: list[str]) -> Counter:
    registry = load_json("references/source-registry.json")
    summary = Counter()

    for entry in registry["urls"]:
        code, body_bytes = fetch_url(entry["url"], timeout)
        category = status_to_category(code, body_bytes)
        summary[str(code) if code is not None else "ERR"] += 1
        print(f"{code or 'ERR'}\t{category}\t{entry['source_id']}\t{entry['url']}")
        if enforce_registry_status and category != entry["status"]:
            errors.append(
                "live URL status mismatch for "
                f"{entry['source_id']}: registry={entry['status']} live={category} "
                f"(http={code or 'ERR'})"
            )

    return summary


def validate_persisted_url_docs(
    registry_summary: dict[str, object], errors: list[str]
) -> None:
    total_urls = registry_summary["total_urls"]
    audit_date = registry_summary["audit_date"]
    status_counts = registry_summary["status_counts"]
    if not isinstance(status_counts, Counter):
        errors.append("source-registry status summary is unavailable")
        return

    reachable = status_counts.get("reachable", 0)
    restricted_or_missing = (
        status_counts.get("access_restricted", 0) + status_counts.get("missing", 0)
    )

    expectations = {
        "docs/en/verification-report.md": [
            f"| Reachable (HTTP 2xx/3xx with content) during {audit_date} automated spot check | {reachable}/{total_urls} |",
            f"| Restricted or missing (HTTP 401/403/404/410 or empty 202) during {audit_date} automated spot check | {restricted_or_missing}/{total_urls} |",
        ],
        "docs/zh-TW/verification-report.md": [
            f"| {audit_date} 自動 HTTP 抽查之可存取回應（HTTP 2xx/3xx 且有內容） | {reachable}/{total_urls} |",
            f"| {audit_date} 自動 HTTP 抽查之受限或遺失回應（HTTP 401/403/404/410 或空白 202） | {restricted_or_missing}/{total_urls} |",
        ],
    }

    for relative_path, snippets in expectations.items():
        text = read_text(relative_path)
        for snippet in snippets:
            if snippet not in text:
                errors.append(f"{relative_path} is missing expected snippet: {snippet}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check-urls",
        action="store_true",
        help="Run live HTTP spot checks for the tracked URL registry.",
    )
    parser.add_argument(
        "--url-timeout",
        type=int,
        default=20,
        help="Timeout in seconds for each URL spot check.",
    )
    parser.add_argument(
        "--enforce-url-status",
        action="store_true",
        help="Fail if live URL status categories do not match references/source-registry.json.",
    )
    args = parser.parse_args()

    if args.enforce_url_status and not args.check_urls:
        parser.error("--enforce-url-status requires --check-urls")
    if args.url_timeout <= 0:
        parser.error("--url-timeout must be greater than zero")

    errors: list[str] = []
    bibliography_summary = validate_bibliography(errors)
    registry_summary = validate_source_registry(errors)
    validate_reference_ids(errors)
    validate_note_map(errors)
    validate_withdrawn_claims(errors)
    validate_reference_list_inventory(errors)
    validate_latex_integrity(bibliography_summary["total_sources"], errors)
    validate_bibtex_metadata(errors)
    stats_summary = validate_statistics(errors)
    validate_docs(bibliography_summary, registry_summary, stats_summary, errors)
    validate_persisted_url_docs(registry_summary, errors)

    if args.check_urls:
        summary = check_urls(args.url_timeout, args.enforce_url_status, errors)
    else:
        summary = None

    if errors:
        print("validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("local consistency checks passed")
    print(
        json.dumps(
            {
                "bibliography_sources": bibliography_summary["total_sources"],
                "tracked_urls": registry_summary["total_urls"],
                "quantitative_data_points": stats_summary["total_points"],
                "source_cross_checked_points": stats_summary["verified_points"],
            },
            indent=2,
        )
    )

    if summary is not None:
        print("url spot-check summary:")
        print(json.dumps(summary, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
