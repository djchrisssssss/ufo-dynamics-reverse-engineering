# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.1.0] — 2026-03-21

### Added
- **Section 1.1 — Background and Motivation**: Origin story referencing Luis Elizondo's *Imminent: Inside the Pentagon's Hunt for UFOs* (2024), explaining how the Five Observables and DIRD physics motivated this assessment
- **Section 1.2 — Terminology**: Formal definitions of UFO and UAP with set-theoretic relationship (UFO ⊂ UAP); usage convention for the document
- **Section 3.x — Warp Bubble Morphology**: New subsection on warp bubble intensity profiles, observed shape paradox, and morphology classification matrix
- **Bibliography entry #53/54**: Elizondo's *Imminent* added to all reference lists and BibTeX
- **Background section in README**: Bilingual (EN/ZH-TW) origin story
- **Certificate of Authorship**: Five-point declaration in report footers
- **`.zenodo.json`**: Zenodo metadata for automated DOI minting

### Changed
- **Document headers**: Reformatted from intelligence-report style to academic paper style (title, author with ORCID, abstract, methodology & scope)
- **Titles**: Changed from "UAP" to "UFO" in main titles for precision and recognizability
- **Section numbering**: Renumbered §1 subsections (Background → 1.1, Terminology → 1.2, Blue Book → 1.3, AAWSAP → 1.4, Scope → 1.5)
- **CITATION.cff**: Updated with full author metadata (name, email, ORCID, affiliation)
- **README.md**: Academic format with author section, documents table, BibTeX citation

### Fixed
- **Transformation optics formula** (§6.1): Empty `\frac{}{}`  denominator replaced with correct flat notation
- **Inline math rendering** (§2–§6): Added spaces between CJK punctuation and `$` delimiters to fix GitHub math parser failures (10 instances)

## [1.0.0] — 2026-03-20

### Added
- **Project restructuring** following academic repository best practices
  - `data/` directory with JSON Schema validation, per-section statistics, timelines, and comparisons
  - `references/` directory with master bibliography (53 sources), URL registry, and per-section reference files
  - `latex/` directory with REVTeX 4-2 formatted paper and BibTeX bibliography
  - `docs/` directory with bilingual (EN/ZH-TW) full texts and verification reports
- **Data infrastructure**
  - `data/schemas/statistics-schema.json` — JSON Schema v2020-12 for data validation
  - `data/statistics/s02-observables-stats.json` — 12 data points on observable characteristics
  - `data/statistics/s03-propulsion-stats.json` — 4 data points on spacetime engineering constraints
  - `data/statistics/s04-energy-stats.json` — 16 data points on energy sources and fusion progress
  - `data/statistics/s06-materials-stats.json` — 12 data points on advanced materials
  - `data/timelines/uap-investigation-history.csv` — 23 events from 1947 to 2025
  - `data/timelines/dird-publications.csv` — Complete 38 DIRD catalog
  - `data/comparisons/energy-density-comparison.csv` — 8 energy source comparisons
  - `data/comparisons/materials-gap-analysis.csv` — 7 theoretical-vs-practical gap analyses
- **Reference management**
  - `references/bibliography.json` — Master bibliography with 53 sources, DOIs, URLs
  - `references/source-registry.json` — 29 tracked URLs with verification status
  - `references/per-section/s01-references.md` through `s08-references.md` — Per-section source documentation
- **LaTeX academic paper**
  - `latex/main.tex` — REVTeX 4-2 two-column paper (~1400 lines) with full content
  - `latex/references.bib` — 53 BibTeX entries (30 peer-reviewed, 5 government, 12 DIRD, 5 books, 1 preprint)
- **Verification reports** in English and Traditional Chinese
- **Project metadata**: `CLAUDE.md`, `CITATION.cff`, `CHANGELOG.md`, `README.md`

### Changed
- Reports reorganized from root to `docs/en/` and `docs/zh-TW/` bilingual structure
- Original `report-en.md`, `report-zh-TW.md`, `transcription.md` retained at root for backwards compatibility

## [0.1.0] — 2026-03-19

### Added
- Initial assessment report (English) — `report-en.md`
- Traditional Chinese translation — `report-zh-TW.md`
- Source book transcription — `transcription.md`
- 10 JPEG photographs of source material
