from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import socket
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPOSITORY_ROOT / "scripts" / "validate_repository.py"
MODULE_SPEC = importlib.util.spec_from_file_location("validate_repository", MODULE_PATH)
assert MODULE_SPEC is not None and MODULE_SPEC.loader is not None
validator = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(validator)


def statistic(section: str, statistic_id: str) -> dict[str, object]:
    return {
        "id": statistic_id,
        "metric": "Test metric",
        "value": 1,
        "unit": "m",
        "date": "2026-01-01",
        "source": "Test source",
        "confidence": "high",
        "verification_status": "verified",
        "verified": True,
        "verification_note": "Test verification",
    }


def statistics_document(
    section: str, statistics: list[dict[str, object]]
) -> dict[str, object]:
    return {
        "section": section,
        "title": "Test section",
        "last_updated": "2026-01-01",
        "statistics": statistics,
    }


class StatisticsValidationTests(unittest.TestCase):
    def run_statistics_validation(
        self, filename: str, document: dict[str, object]
    ) -> tuple[list[str], dict[str, int]]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            schema_path = root / "data" / "schemas" / "statistics-schema.json"
            statistics_path = root / "data" / "statistics" / filename
            schema_path.parent.mkdir(parents=True)
            statistics_path.parent.mkdir(parents=True)
            schema_path.write_text(
                (REPOSITORY_ROOT / "data" / "schemas" / "statistics-schema.json").read_text()
            )
            statistics_path.write_text(json.dumps(document))

            errors: list[str] = []
            with mock.patch.object(validator, "ROOT", root):
                summary = validator.validate_statistics(errors)
        return errors, summary

    def test_format_checker_rejects_invalid_dates_and_uri(self) -> None:
        document = statistics_document("s02", [statistic("s02", "s02-001")])
        document["last_updated"] = "2026-99-99"
        document["statistics"][0]["source"] = {
            "name": "Bad source",
            "url": "not a uri",
            "accessed": "yesterday",
        }

        errors, summary = self.run_statistics_validation(
            "s02-observables-stats.json", document
        )

        self.assertTrue(any("schema error" in error for error in errors), errors)
        self.assertEqual(summary["total_points"], 0)

    def test_rejects_duplicate_ids_and_filename_section_mismatch(self) -> None:
        document = statistics_document(
            "s03",
            [statistic("s03", "s03-001"), statistic("s03", "s03-001")],
        )

        errors, _ = self.run_statistics_validation(
            "s02-observables-stats.json", document
        )

        self.assertTrue(any("filename implies s02" in error for error in errors), errors)
        self.assertTrue(any("duplicate statistic id s03-001" in error for error in errors), errors)

    def test_unverified_records_must_be_low_confidence_or_withdrawn(self) -> None:
        low = statistic("s02", "s02-001")
        low.update({"verified": False, "confidence": "low"})
        withdrawn = statistic("s02", "s02-002")
        withdrawn.update({"verified": False, "value": "not defined"})
        unexplained = statistic("s02", "s02-003")
        unexplained.update({"verified": False})
        errors, summary = self.run_statistics_validation(
            "s02-observables-stats.json",
            statistics_document("s02", [low, withdrawn, unexplained]),
        )
        self.assertEqual(summary["low_unverified_points"], 1)
        self.assertEqual(summary["withdrawn_points"], 1)
        self.assertTrue(any("unverified statistics" in error for error in errors), errors)

    def test_rejects_out_of_range_section(self) -> None:
        document = statistics_document("s99", [statistic("s99", "s99-001")])

        errors, summary = self.run_statistics_validation(
            "s99-invalid-stats.json", document
        )

        self.assertTrue(any("schema error" in error for error in errors), errors)
        self.assertEqual(summary["total_points"], 0)


class UrlValidationTests(unittest.TestCase):
    def test_static_url_safety_rejects_non_https_and_private_hosts(self) -> None:
        self.assertIsNone(validator.validate_public_https_url("https://example.com/path"))
        rejected_urls = (
            "http://example.com",
            "https://localhost/test",
            "https://service.internal/test",
            "https://127.0.0.1/test",
            "https://[::1]/test",
            "https://example.com:8443/test",
            "https://user:password@example.com/test",
        )
        for url in rejected_urls:
            with self.subTest(url=url):
                self.assertIsNotNone(validator.validate_public_https_url(url))

    def test_dns_private_address_check_is_live_only(self) -> None:
        registry = {
            "metadata": {"total_urls": 1, "last_audit": "2026-01-01"},
            "urls": [
                {
                    "url": "https://example.com/test",
                    "source_id": "src-001",
                    "status": "reachable",
                }
            ],
        }
        errors: list[str] = []
        with mock.patch.object(validator, "load_json", return_value=registry), mock.patch.object(
            validator.socket,
            "getaddrinfo",
            side_effect=AssertionError("offline validation attempted DNS"),
        ):
            validator.validate_source_registry(errors)
        self.assertEqual(errors, [])

        private_resolution = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("10.0.0.5", 443))
        ]
        with mock.patch.object(
            validator.socket, "getaddrinfo", return_value=private_resolution
        ):
            safety_error = validator.validate_public_https_url(
                "https://example.com/test", resolve_host=True
            )
        self.assertIn("non-public address", safety_error or "")

    def test_curl_uses_protocol_guards_and_option_separator(self) -> None:
        completed_process = mock.Mock(stdout="204", returncode=0)
        with mock.patch.object(
            validator, "validate_public_https_url", return_value=None
        ), mock.patch.object(validator.shutil, "which", return_value="/usr/bin/curl"), mock.patch.object(
            validator.subprocess, "run", return_value=completed_process
        ) as run:
            status = validator.fetch_status("https://example.com/test", 20)

        self.assertEqual(status, 204)
        arguments = run.call_args.args[0]
        self.assertIn("%{http_code} %{size_download}", arguments)
        self.assertIn("--proto", arguments)
        self.assertIn("--proto-redir", arguments)
        self.assertEqual(arguments[-2:], ["--", "https://example.com/test"])

    def test_curl_zero_status_is_transient(self) -> None:
        completed_process = mock.Mock(stdout="000", returncode=28)
        with mock.patch.object(
            validator, "validate_public_https_url", return_value=None
        ), mock.patch.object(validator.shutil, "which", return_value="/usr/bin/curl"), mock.patch.object(
            validator.subprocess, "run", return_value=completed_process
        ):
            self.assertIsNone(validator.fetch_status("https://example.com/test", 20))

    def test_empty_202_is_access_restricted(self) -> None:
        completed_process = mock.Mock(stdout="202 0", returncode=0)
        with mock.patch.object(
            validator, "validate_public_https_url", return_value=None
        ), mock.patch.object(validator.shutil, "which", return_value="/usr/bin/curl"), mock.patch.object(
            validator.subprocess, "run", return_value=completed_process
        ):
            code, body_bytes = validator.fetch_url("https://example.com/test", 20)
        self.assertEqual((code, body_bytes), (202, 0))
        self.assertEqual(validator.status_to_category(code, body_bytes), "access_restricted")
        self.assertEqual(validator.status_to_category(202, 512), "reachable")

    def test_live_results_are_not_compared_to_historical_docs(self) -> None:
        registry = {
            "metadata": {"total_urls": 1, "last_audit": "2026-01-01"},
            "urls": [
                {
                    "url": "https://example.com/test",
                    "source_id": "src-001",
                    "status": "reachable",
                }
            ],
        }
        errors: list[str] = []
        with mock.patch.object(validator, "load_json", return_value=registry), mock.patch.object(
            validator, "fetch_url", return_value=(404, 0)
        ), mock.patch.object(
            validator,
            "read_text",
            side_effect=AssertionError("live URL audit read historical docs"),
        ), contextlib.redirect_stdout(io.StringIO()):
            summary = validator.check_urls(20, False, errors)

        self.assertEqual(summary["404"], 1)
        self.assertEqual(errors, [])

    def test_persisted_registry_counts_validate_historical_docs(self) -> None:
        summary = {
            "total_urls": 2,
            "audit_date": "2026-01-01",
            "status_counts": Counter({"reachable": 1, "missing": 1}),
        }
        documents = {
            "docs/en/verification-report.md": "\n".join(
                (
                    "| Reachable (HTTP 2xx/3xx with content) during 2026-01-01 automated spot check | 1/2 |",
                    "| Restricted or missing (HTTP 401/403/404/410 or empty 202) during 2026-01-01 automated spot check | 1/2 |",
                )
            ),
            "docs/zh-TW/verification-report.md": "\n".join(
                (
                    "| 2026-01-01 自動 HTTP 抽查之可存取回應（HTTP 2xx/3xx 且有內容） | 1/2 |",
                    "| 2026-01-01 自動 HTTP 抽查之受限或遺失回應（HTTP 401/403/404/410 或空白 202） | 1/2 |",
                )
            ),
        }
        errors: list[str] = []
        with mock.patch.object(
            validator, "read_text", side_effect=lambda path: documents[path]
        ):
            validator.validate_persisted_url_docs(summary, errors)
        self.assertEqual(errors, [])

    def test_status_categories_distinguish_transient_responses(self) -> None:
        self.assertEqual(validator.status_to_category(204), "reachable")
        self.assertEqual(validator.status_to_category(302), "reachable")
        self.assertEqual(validator.status_to_category(401), "access_restricted")
        self.assertEqual(validator.status_to_category(410), "missing")
        self.assertEqual(validator.status_to_category(429), "transient")
        self.assertEqual(validator.status_to_category(503), "transient")
        self.assertEqual(validator.status_to_category(None), "transient")


class ReferenceValidationTests(unittest.TestCase):
    def test_note_map_requires_each_language_to_have_canonical_ids(self) -> None:
        note_map = {
            "metadata": {
                "total_notes": 1,
                "total_key_judgments": 1,
                "total_auxiliary_sources": 0,
            },
            "notes": {
                "ref-001": {
                    "section": "s01",
                    "src_ids": ["src-001"],
                    "auxiliary_ids": [],
                }
            },
            "key_judgments": {
                "KJ-1": {"src_ids": ["src-001"], "auxiliary_ids": []}
            },
            "auxiliary_sources": {},
        }
        bibliography = {"sources": [{"id": "src-001"}]}

        def load_json(path: str) -> object:
            return note_map if path == "references/note-map.json" else bibliography

        documents = {
            "docs/en/full-text.md": "[ref-001] [KJ-1]",
            "docs/zh-TW/full-text.md": "[KJ-1]",
        }
        errors: list[str] = []
        with mock.patch.object(validator, "load_json", side_effect=load_json), mock.patch.object(
            validator, "read_text", side_effect=lambda path: documents[path]
        ):
            validator.validate_note_map(errors)

        self.assertTrue(
            any("docs/zh-TW/full-text.md is missing canonical note ids" in error for error in errors),
            errors,
        )
        self.assertTrue(any("bilingual note occurrence mismatch" in error for error in errors), errors)

    def test_note_map_rejects_noncanonical_ids_and_unmapped_sources(self) -> None:
        note_map = {
            "metadata": {
                "total_notes": 1,
                "total_key_judgments": 0,
                "total_auxiliary_sources": 0,
            },
            "notes": {
                "ref-001": {"section": "s01", "src_ids": ["src-001"], "auxiliary_ids": []}
            },
            "key_judgments": {},
            "auxiliary_sources": {},
        }
        bibliography = {
            "metadata": {"further_reading": ["src-003"]},
            "sources": [{"id": "src-001"}, {"id": "src-002"}, {"id": "src-003"}],
        }

        def load_json(path: str) -> object:
            return note_map if path == "references/note-map.json" else bibliography

        documents = {
            "docs/en/full-text.md": "[ref-001] [ref-NEW-fuchs2024]",
            "docs/zh-TW/full-text.md": "[ref-001]",
        }
        errors: list[str] = []
        with mock.patch.object(validator, "load_json", side_effect=load_json), mock.patch.object(
            validator, "read_text", side_effect=lambda path: documents[path]
        ):
            validator.validate_note_map(errors)

        self.assertTrue(
            any("non-canonical note ids: ref-NEW-fuchs2024" in error for error in errors), errors
        )
        self.assertTrue(
            any("not mapped by any note or key judgment" in error and "src-002" in error for error in errors),
            errors,
        )
        self.assertFalse(any("src-003" in error for error in errors), errors)

    def test_latex_integrity_detects_mutants(self) -> None:
        documents = {
            "latex/references.bib": """
@article{known, title={One}}
@article{known, title={Duplicate}}
""",
            "latex/main.tex": r"""
\cite{missing}
\label{duplicate}\label{duplicate}
\ref{undefined}
""",
        }
        errors: list[str] = []
        with mock.patch.object(
            validator, "read_text", side_effect=lambda path: documents[path]
        ):
            validator.validate_latex_integrity(1, errors)

        self.assertTrue(any("duplicate key known" in error for error in errors), errors)
        self.assertTrue(any("cites keys missing" in error for error in errors), errors)
        self.assertTrue(any("duplicate labels" in error for error in errors), errors)
        self.assertTrue(any("undefined labels" in error for error in errors), errors)

    def test_latex_integrity_flags_uncited_keys_unless_nocite_star(self) -> None:
        bibliography = "@article{cited, title={One}}\n@article{uncited, title={Two}}\n"
        for main_text, expect_error in (
            (r"\cite{cited}", True),
            (r"\cite{cited}\nocite{*}", False),
            (r"\cite{cited}\nocite{uncited}", False),
        ):
            documents = {"latex/references.bib": bibliography, "latex/main.tex": main_text}
            errors: list[str] = []
            with mock.patch.object(
                validator, "read_text", side_effect=lambda path: documents[path]
            ):
                validator.validate_latex_integrity(2, errors)
            with self.subTest(main_text=main_text):
                self.assertEqual(
                    any("never cited" in error for error in errors), expect_error, errors
                )

    def test_bibtex_metadata_cross_check_detects_mutants(self) -> None:
        bibliography = {
            "sources": [
                {"id": "src-001", "title": "A paper", "date": "2020", "doi": "10.1/abc"},
                {"id": "src-002", "title": "DIRD #13: A Report", "date": "2010", "doi": None},
                {"id": "src-003", "title": "Missing DOI in JSON", "date": "1999", "doi": None},
            ]
        }
        bib = """
@article{One, title = {A paper},
  year = {2021},
  doi = {10.1/abc}
}
@misc{Two,
  title = {A {Report}},
  year = {2010}
}
@article{Three,
  title = {Missing {DOI} in {JSON}},
  year = {1999},
  doi = {10.1/xyz}
}
@misc{Orphan,
  title = {Nobody cites this},
  year = {2000}
}
"""
        errors: list[str] = []
        with mock.patch.object(validator, "load_json", return_value=bibliography), mock.patch.object(
            validator, "read_text", return_value=bib
        ):
            validator.validate_bibtex_metadata(errors)
        self.assertTrue(any("src-001 year=2020" in error for error in errors), errors)
        self.assertTrue(any("src-003 doi=None" in error for error in errors), errors)
        self.assertTrue(any("entry Orphan matches no bibliography source" in error for error in errors), errors)
        self.assertFalse(any("src-002" in error for error in errors), errors)

    def test_current_latex_inventory_is_consistent(self) -> None:
        total_sources = len(validator.load_json("references/bibliography.json")["sources"])
        errors: list[str] = []
        validator.validate_latex_integrity(total_sources, errors)
        self.assertEqual(errors, [])


class PerSectionReferenceTests(unittest.TestCase):
    def test_prose_gap_column_is_not_scanned(self) -> None:
        text = "\n".join(
            (
                "| Domain | Theory Status | Gap |",
                "|--------|--------------|-----|",
                "| Negative stress-energy | Exists | No universal Casimir-to-warp ratio |",
                "| Target control | Coupled | Foundational/model-dependent |",
            )
        )
        self.assertEqual(validator.extract_per_section_references(text), [])

    def test_related_sources_column_is_scanned(self) -> None:
        text = "\n".join(
            (
                "| Unknown | Significance | Related Sources |",
                "|---------|-------------|-----------------|",
                "| Energy budget? | No ratio | src-001, src-002, nif-ignition |",
                "",
                "Prose mentioning [src-055] in brackets.",
            )
        )
        self.assertEqual(
            validator.extract_per_section_references(text),
            [("src-001", 3), ("src-002", 3), ("nif-ignition", 3), ("src-055", 5)],
        )


class DocumentationExpectationTests(unittest.TestCase):
    def test_verified_count_wording_matches_audit_statement(self) -> None:
        expectations = validator.build_doc_expectations(
            {"total_sources": 71, "books": 7},
            {"total_urls": 34},
            {
                "total_points": 45,
                "verified_points": 42,
                "low_unverified_points": 2,
                "withdrawn_points": 1,
                "confidence_by_section": {},
            },
        )
        self.assertIn(
            "42 of 45 quantitative records are marked as source-cross-checked in repository metadata",
            expectations["README.md"],
        )
        self.assertIn(
            "45 筆定量紀錄中，有 42 筆在 repo metadata 中標記為已完成來源交叉檢查",
            expectations["README.md"],
        )
        self.assertIn(
            "two model-dependent estimates are retained as low-confidence analysis",
            expectations[".zenodo.json"],
        )
        self.assertIn("| Books / Monographs | 7 | 9.9% |", expectations["docs/en/verification-report.md"])
        self.assertFalse(
            any("independently cross-checked" in snippet for snippets in expectations.values() for snippet in snippets)
        )

    def test_withdrawn_claim_tokens_are_rejected(self) -> None:
        documents = {
            "docs/en/full-text.md": "clean text",
            "docs/zh-TW/full-text.md": "舊稿：約 10⁶⁸ 倍之轉導差距",
        }
        errors: list[str] = []
        with mock.patch.object(validator, "read_text", side_effect=lambda path: documents[path]):
            validator.validate_withdrawn_claims(errors)
        self.assertEqual(len(errors), 2, errors)
        self.assertTrue(all("docs/zh-TW/full-text.md" in error for error in errors), errors)


class RepositorySmokeTests(unittest.TestCase):
    def test_validator_main_passes_on_repository(self) -> None:
        stdout, stderr = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, "argv", ["validate_repository.py"]), contextlib.redirect_stdout(
            stdout
        ), contextlib.redirect_stderr(stderr):
            status = validator.main()
        self.assertEqual(status, 0, stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
