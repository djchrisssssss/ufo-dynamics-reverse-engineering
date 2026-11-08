# CLAUDE.md — UFO Dynamics Reverse Engineering

## Overview

A physics-based assessment of unidentified aerial phenomena (UAP) flight characteristics, evaluating whether known or theoretically plausible physical mechanisms can account for reported observables. Bilingual (EN / ZH-TW).

## File Structure

```text
UFO-dynamics-reverse-engineering/
├── docs/
│   ├── en/
│   │   ├── full-text.md              # Complete English assessment
│   │   └── verification-report.md    # Data verification audit (EN)
│   └── zh-TW/
│       ├── full-text.md              # Complete Traditional Chinese assessment
│       ├── transcription.md          # Source book transcription (ZH-TW)
│       └── verification-report.md    # Data verification audit (ZH-TW)
├── data/
│   ├── schemas/
│   │   └── statistics-schema.json    # JSON Schema for data validation
│   ├── statistics/                   # Per-section quantitative data
│   │   ├── s02-observables-stats.json
│   │   ├── s03-propulsion-stats.json
│   │   ├── s04-energy-stats.json
│   │   ├── s06-materials-stats.json
│   │   └── s09-theoretical-foundations-stats.json
│   ├── timelines/                    # Historical event CSVs
│   │   ├── uap-investigation-history.csv
│   │   └── dird-publications.csv
│   └── comparisons/                  # Cross-domain comparative data
│       ├── energy-density-comparison.csv
│       └── materials-gap-analysis.csv
├── references/
│   ├── bibliography.json             # Master bibliography (71 sources)
│   ├── source-registry.json          # URL verification registry
│   ├── note-map.json                 # ref-*/KJ-* note IDs → src-* + auxiliary IDs
│   └── per-section/                  # Per-section reference lists
│       ├── s01-references.md
│       ├── s02-references.md
│       ├── s03-references.md
│       ├── s04-references.md
│       ├── s05-references.md
│       ├── s06-references.md
│       ├── s07-references.md
│       ├── s08-references.md
│       └── s09-references.md
├── latex/
│   ├── main.tex                      # REVTeX 4-2 formatted paper
│   ├── references.bib                # BibTeX bibliography (71 entries)
│   └── figures/                      # Placeholder for diagrams
├── scripts/
│   └── validate_repository.py        # Repository validator
├── tests/
│   └── test_validate_repository.py   # Validator unit tests
├── assets/
│   └── uap-public-release-still.jpg  # README banner image
├── .github/workflows/
│   ├── validate.yml                  # Required CI: unit tests + offline validation + LaTeX build
│   └── url-audit.yml                 # Weekly live URL audit
├── requirements.txt                  # Pinned validator dependency (jsonschema)
├── transcription.md                  # Byte-identical mirror of docs/zh-TW/transcription.md
├── .zenodo.json                      # Zenodo deposit metadata
├── CLAUDE.md                         # This file
├── CITATION.cff                      # Machine-readable citation
├── CHANGELOG.md                      # Version history
└── README.md                         # Project overview (bilingual)
```

## Naming Conventions

### Statistics Files
- Pattern: `sNN-descriptor-stats.json`
- ID format: `sNN-NNN` (section + 3-digit sequential number)
- Sections: s01–s09 (main), sA1–sA4 (appendices A–D; Appendix E has no statistics file)

### Reference Files
- Per-section: `sNN-references.md`
- Master: `bibliography.json` (JSON), `references.bib` (BibTeX)

### Timeline/Comparison Files
- Descriptive slug + `.csv`
- Example: `uap-investigation-history.csv`

## Data Standards

- **Dates**: ISO 8601 (`YYYY-MM-DD`)
- **Units**: SI units preferred; scientific notation for extreme values
- **Sources**: peer-reviewed for physical claims; official documents for institutional facts; DIRDs as commissioned analyses; preprints only with caveat
- **Confidence levels**: Following ICD 203 (High / Moderate / Low)
- **Verification markers**: `[VERIFIED]` / `[THEORETICAL]` / `[SPECULATIVE]` / `[ASSESSED]` (analytic judgment by the author)

## Section Structure

| Section | Topic |
|---------|-------|
| s01 | Introduction and Historical Context |
| s02 | Observable Characteristics — Physics Framework |
| s03 | Propulsion Mechanisms — Spacetime Engineering |
| s04 | Energy Sources — Nuclear Fusion and Beyond |
| s05 | Electromagnetic Signatures |
| s06 | Advanced Materials and Structural Analysis |
| s07 | Integrated Propulsion Model — Synthesis |
| s08 | Intelligence Gaps and Research Directions |
| s09 | Mathematical and Relativistic Foundations for Anomalous Flight |
| sA1 | Glossary of Terms (bilingual) |
| sA2 | Key Equations Reference |
| sA3 | Complete DIRD List |
| sA4 | Confidence Level Definitions |
| E | Falsification Criteria (no statistics ID) |

## Bilingual Parity

- Every document in `docs/en/` has a counterpart in `docs/zh-TW/`
- Data and references are language-neutral (shared)
- LaTeX version is English-only; Markdown versions are bilingual

## LaTeX Compilation

```bash
cd latex/
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Validation

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests
python3 scripts/validate_repository.py
python3 scripts/validate_repository.py --check-urls --enforce-url-status   # weekly url-audit.yml
```

## Commit Convention

Follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/):
- `docs(s02)`: Documentation changes to Section 2
- `data(statistics)`: Statistics data updates
- `fix(references)`: Reference corrections
- `feat(latex)`: LaTeX structure additions
