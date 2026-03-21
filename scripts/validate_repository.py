#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REGISTRY_STATUSES = {"reachable", "access_restricted", "missing"}
BRACKETED_REFERENCE_RE = re.compile(r"\[([A-Za-z0-9_-]+)\]")
TABLE_REFERENCE_RE = re.compile(r"\b(?:src-\d{3}|DIRD_[A-Za-z0-9]+|[a-z]+(?:-[a-z0-9]+)+)\b")


def load_json(relative_path: str) -> object:
    return json.loads((ROOT / relative_path).read_text())


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text()


def status_to_category(code: int | None) -> str:
    if code in {200, 202}:
        return "reachable"
    if code == 403:
        return "access_restricted"
    if code == 404:
        return "missing"
    return "other"


def fetch_status(url: str, timeout: int) -> int | None:
    if shutil.which("curl"):
        result = subprocess.run(
            [
                "curl",
                "-L",
                "-s",
                "-o",
                "/dev/null",
                "-w",
                "%{http_code}",
                "--max-time",
                str(timeout),
                url,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        code = result.stdout.strip()
        return int(code) if code.isdigit() else None

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ufo-dynamics-reverse-engineering-validator/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.getcode()
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception:
        return None


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
    for key, expected in expected_categories.items():
        actual = category_counts.get(key, 0)
        if actual != expected:
            errors.append(
                f"bibliography category {key}={expected} != actual {actual}"
            )

    return {
        "total_sources": total_sources,
        "books": category_counts.get("book", 0),
    }


def validate_source_registry(errors: list[str]) -> dict[str, int]:
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

    return {"total_urls": total_urls}


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
        if source_id in registry_ids:
            errors.append(f"duplicate source-registry source_id: {source_id}")
        registry_ids.add(source_id)
        if source_id.startswith("src-") and source_id not in bibliography_ids:
            errors.append(
                f"source-registry source_id {source_id} is missing from references/bibliography.json"
            )

    known_ids = set(bibliography_ids) | registry_ids

    for path in sorted((ROOT / "references/per-section").glob("s*-references.md")):
        section_id = path.name.split("-")[0]
        text = path.read_text()
        references_with_lines: list[tuple[str, int]] = []

        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in BRACKETED_REFERENCE_RE.findall(line):
                references_with_lines.append((match, line_number))
            if "|" in line:
                cells = [cell.strip() for cell in line.split("|")[1:-1]]
                if not cells:
                    continue
                for match in TABLE_REFERENCE_RE.findall(cells[-1]):
                    references_with_lines.append((match, line_number))

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
                sections_cited = bibliography_ids[reference_id]["sections_cited"]
                if section_id not in sections_cited:
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line_number} cites {reference_id} but bibliography sections_cited does not include {section_id}"
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


def validate_statistics(errors: list[str]) -> dict[str, int]:
    schema = load_json("data/schemas/statistics-schema.json")
    validator_cls = getattr(jsonschema, "Draft202012Validator", jsonschema.Draft7Validator)
    validator = validator_cls(schema)

    total_points = 0
    verified_points = 0
    confidence_by_section: dict[str, Counter] = {}
    for path in sorted((ROOT / "data/statistics").glob("*.json")):
        data = json.loads(path.read_text())
        validation_errors = sorted(
            validator.iter_errors(data), key=lambda err: list(err.absolute_path)
        )
        for err in validation_errors:
            location = "/".join(str(part) for part in err.absolute_path) or "<root>"
            errors.append(f"{path.name} schema error at {location}: {err.message}")

        stats = data["statistics"]
        total_points += len(stats)
        verified_points += sum(1 for stat in stats if stat["verified"])
        confidence_by_section[path.stem.split("-")[0]] = Counter(
            stat["confidence"] for stat in stats
        )

    return {
        "total_points": total_points,
        "verified_points": verified_points,
        "confidence_by_section": confidence_by_section,
    }


def validate_docs(
    bibliography_summary: dict[str, int],
    registry_summary: dict[str, int],
    stats_summary: dict[str, int],
    errors: list[str],
) -> None:
    total_sources = bibliography_summary["total_sources"]
    total_books = bibliography_summary["books"]
    total_urls = registry_summary["total_urls"]
    total_points = stats_summary["total_points"]
    verified_points = stats_summary["verified_points"]
    disputed_points = total_points - verified_points
    verified_percentage = f"{(verified_points / total_points) * 100:.1f}%"
    books_percentage = f"{(total_books / total_sources) * 100:.1f}%"
    s02_counts = stats_summary["confidence_by_section"]["s02"]
    s02_total = sum(s02_counts.values())

    expectations = {
        "README.md": [
            f"Master bibliography ({total_sources} sources)",
            f"{verified_points} of {total_points} quantitative data points are independently cross-checked",
            f"│   ├── bibliography.json            # {total_sources} sources",
            f"│   ├── references.bib               # {total_sources} BibTeX entries",
            f"Cross-referencing {total_sources} sources / 交叉比對 {total_sources} 筆來源",
            f"{total_points} 個定量資料點中有 {verified_points} 個已對照引用來源完成交叉檢查；另有 {disputed_points} 個具爭議之估計值以低信心分析保留。",
        ],
        "CLAUDE.md": [
            f"Master bibliography ({total_sources} sources)",
            f"BibTeX bibliography ({total_sources} entries)",
        ],
        "docs/en/full-text.md": [
            f"{verified_points} of the {total_points} quantitative data points cited in this assessment are independently cross-checked",
            f"Source provenance and reliability tier for all {total_sources} bibliography entries",
            f"Organizing and cross-referencing {total_sources} bibliography sources across peer-reviewed articles, government documents, DIRDs, and books.",
            "59. [GOV] Lawrence Livermore National Laboratory. \"NIF Sets New Records for Energy Yield and Target Gain.\" 2025.",
        ],
        "docs/zh-TW/full-text.md": [
            f"本評估引用的 {total_points} 個定量資料點中，有 {verified_points} 個已對照其引用來源完成獨立交叉檢查",
            f"全部 {total_sources} 筆參考書目之來源出處及可靠性層級",
            f"組織並交叉比對 {total_sources} 筆參考書目來源",
            "59. [GOV] Lawrence Livermore National Laboratory. \"NIF Sets New Records for Energy Yield and Target Gain.\" 2025.",
        ],
        "report-en.md": [
            f"{verified_points} of the {total_points} quantitative data points cited in this assessment are independently cross-checked",
            f"Source provenance and reliability tier for all {total_sources} bibliography entries",
            f"Organizing and cross-referencing {total_sources} bibliography sources across peer-reviewed articles, government documents, DIRDs, and books.",
            "59. [GOV] Lawrence Livermore National Laboratory. \"NIF Sets New Records for Energy Yield and Target Gain.\" 2025.",
        ],
        "report-zh-TW.md": [
            f"本評估引用的 {total_points} 個定量資料點中，有 {verified_points} 個已對照其引用來源完成獨立交叉檢查",
            f"全部 {total_sources} 筆參考書目之來源出處及可靠性層級",
            f"組織並交叉比對 {total_sources} 筆參考書目來源",
            "59. [GOV] Lawrence Livermore National Laboratory. \"NIF Sets New Records for Energy Yield and Target Gain.\" 2025.",
        ],
        "docs/en/verification-report.md": [
            f"| Total bibliography sources | {total_sources} |",
            f"| Data points independently cross-checked | {verified_points}/{total_points} ({verified_percentage}) |",
            f"| Tracked URLs in source registry | {total_urls} |",
            f"| Books / Monographs | {total_books} | {books_percentage} | Tier 2 (academic) |",
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
            f"| 已獨立交叉檢查之資料點 | {verified_points}/{total_points} ({verified_percentage}) |",
            f"| 來源註冊中的追蹤 URL | {total_urls} |",
            f"| 學術專書 | {total_books} | {books_percentage} | 第二層（學術） |",
            f"高度信心：{s02_counts.get('high', 0)} 個、中度信心：{s02_counts.get('moderate', 0)} 個、低度信心：{s02_counts.get('low', 0)} 個",
        ],
        ".zenodo.json": [
            f"{verified_points} of {total_points} quantitative data points are independently cross-checked",
            "contested estimates are retained as low-confidence analysis",
        ],
        "latex/main.tex": [
            f"synthesis and cross-referencing of {total_sources} bibliography sources",
        ],
    }

    for relative_path, snippets in expectations.items():
        text = read_text(relative_path)
        for snippet in snippets:
            if snippet not in text:
                errors.append(f"{relative_path} is missing expected snippet: {snippet}")


def check_urls(timeout: int, enforce_registry_status: bool, errors: list[str]) -> Counter:
    registry = load_json("references/source-registry.json")
    summary = Counter()

    for entry in registry["urls"]:
        code = fetch_status(entry["url"], timeout)
        category = status_to_category(code)
        summary[str(code) if code is not None else "ERR"] += 1
        print(f"{code or 'ERR'}\t{category}\t{entry['source_id']}\t{entry['url']}")
        if enforce_registry_status and category != entry["status"]:
            errors.append(
                "live URL status mismatch for "
                f"{entry['source_id']}: registry={entry['status']} live={category} "
                f"(http={code or 'ERR'})"
            )

    return summary


def validate_live_url_docs(summary: Counter, total_urls: int, errors: list[str]) -> None:
    registry = load_json("references/source-registry.json")
    audit_date = registry["metadata"]["last_audit"]
    reachable = summary.get("200", 0) + summary.get("202", 0)
    restricted_or_missing = summary.get("403", 0) + summary.get("404", 0)

    expectations = {
        "docs/en/verification-report.md": [
            f"| HTTP 200/202 during {audit_date} automated spot check | {reachable}/{total_urls} |",
            f"| HTTP 403/404 during {audit_date} automated spot check | {restricted_or_missing}/{total_urls} |",
            f"*Last updated: {audit_date}*",
        ],
        "docs/zh-TW/verification-report.md": [
            f"| {audit_date} 自動 HTTP 抽查之 200/202 回應 | {reachable}/{total_urls} |",
            f"| {audit_date} 自動 HTTP 抽查之 403/404 回應 | {restricted_or_missing}/{total_urls} |",
            f"*最後更新：{audit_date}*",
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

    errors: list[str] = []
    bibliography_summary = validate_bibliography(errors)
    registry_summary = validate_source_registry(errors)
    validate_reference_ids(errors)
    stats_summary = validate_statistics(errors)
    validate_docs(bibliography_summary, registry_summary, stats_summary, errors)

    if args.check_urls:
        summary = check_urls(args.url_timeout, args.enforce_url_status, errors)
        validate_live_url_docs(summary, registry_summary["total_urls"], errors)
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
                "independently_cross_checked_points": stats_summary["verified_points"],
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
