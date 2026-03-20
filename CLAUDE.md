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
│   │   └── s06-materials-stats.json
│   ├── timelines/                    # Historical event CSVs
│   │   ├── uap-investigation-history.csv
│   │   └── dird-publications.csv
│   └── comparisons/                  # Cross-domain comparative data
│       ├── energy-density-comparison.csv
│       └── materials-gap-analysis.csv
├── references/
│   ├── bibliography.json             # Master bibliography (54 sources)
│   ├── source-registry.json          # URL verification registry
│   └── per-section/                  # Per-section reference lists
│       ├── s01-references.md
│       ├── s02-references.md
│       ├── s03-references.md
│       ├── s04-references.md
│       ├── s05-references.md
│       ├── s06-references.md
│       ├── s07-references.md
│       └── s08-references.md
├── latex/
│   ├── main.tex                      # REVTeX 4-2 formatted paper
│   ├── references.bib                # BibTeX bibliography (54 entries)
│   └── figures/                      # Placeholder for diagrams
├── report-en.md                      # Original English report (legacy)
├── report-zh-TW.md                   # Original Chinese report (legacy)
├── transcription.md                  # Original transcription (legacy)
├── CLAUDE.md                         # This file
├── CITATION.cff                      # Machine-readable citation
├── CHANGELOG.md                      # Version history
└── README.md                         # Project overview (bilingual)
```

## Naming Conventions

### Statistics Files
- Pattern: `sNN-descriptor-stats.json`
- ID format: `sNN-NNN` (section + 3-digit sequential number)
- Sections: s01–s08 (main), sA1–sA4 (appendices)

### Reference Files
- Per-section: `sNN-references.md`
- Master: `bibliography.json` (JSON), `references.bib` (BibTeX)

### Timeline/Comparison Files
- Descriptive slug + `.csv`
- Example: `uap-investigation-history.csv`

## Data Standards

- **Dates**: ISO 8601 (`YYYY-MM-DD`)
- **Units**: SI units preferred; scientific notation for extreme values
- **Sources**: Government > peer-reviewed > expert reports > preprints
- **Confidence levels**: Following ICD 203 (High / Moderate / Low)
- **Verification markers**: `[VERIFIED]` / `[THEORETICAL]` / `[SPECULATIVE]`

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
| sA1 | Glossary of Terms (bilingual) |
| sA2 | Key Equations Reference |
| sA3 | Complete DIRD List |
| sA4 | Confidence Level Definitions |

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
python3 scripts/validate_repository.py
python3 scripts/validate_repository.py --check-urls
```

## Commit Convention

Follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/):
- `docs(s02)`: Documentation changes to Section 2
- `data(statistics)`: Statistics data updates
- `fix(references)`: Reference corrections
- `feat(latex)`: LaTeX structure additions
