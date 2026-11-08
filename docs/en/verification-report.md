# Data Provenance and Consistency Report

**DOI:** [10.5281/zenodo.19138270](https://doi.org/10.5281/zenodo.19138270)
**Report Date:** 2026-11-07
**Auditor:** Automated consistency checks + source-critical manual review

---

## 1. Overview

This report documents data provenance, source quality, reproducibility checks, and known limitations for quantitative claims in the UAP Physics Assessment. A source being located does not by itself validate the physical claim made from it.

### Summary Statistics

| Metric | Value |
|--------|-------|
| Total bibliography sources | 71 |
| Total quantitative data points | 45 |
| Sections with statistics | 4 (s02, s03, s04, s06) |
| Records marked source-cross-checked in metadata | 42/45 (93.3%) |
| Tracked URLs in source registry | 34 |
| Reachable (HTTP 2xx/3xx with content) during 2026-11-07 automated spot check | 19/34 |
| Restricted or missing (HTTP 401/403/404/410 or empty 202) during 2026-11-07 automated spot check | 15/34 |

---

## 2. Source Quality Breakdown

| Source Type | Count | Percentage | Appropriate Evidentiary Use |
|-------------|-------|-----------|-----------------------------|
| Peer-reviewed articles | 42 | 59.2% | Strongest category for claims within the paper's tested scope |
| Government documents | 9 | 12.7% | Primary for institutional facts and official findings; not automatic validation of physics claims |
| Defense Intelligence Reference Documents | 12 | 16.9% | Commissioned technical analyses; not treated as peer review |
| Books / Monographs | 7 | 9.9% | Secondary or academic synthesis, assessed title by title |
| Preprints | 1 | 1.4% | Not peer-reviewed; used only with an explicit caveat |

---

## 3. Verification Methodology

### Layer 1 — Source Identification

Each record identifies a citable source. Provenance category and claim support are evaluated separately: an official document is authoritative for what an agency reported, while a peer-reviewed experiment supports only the system and regime it actually tested.

### Layer 2 — Claim and Calculation Review

1. **Source located** — Bibliographic identity and stable identifier checked.
2. **Claim supported** — Source inspected for the proposition attributed to it.
3. **Calculation reproduced** — Formula, inputs, units, and arithmetic recomputed where the repository derives a value.
4. **Status classified** — Empirical measurement, theoretical/model-dependent result, or speculative extrapolation recorded distinctly.

The current `verified` Boolean means that a record received the repository's source cross-check; it does **not** mean independent empirical confirmation. This audit reproduced the Section 3 arithmetic and corrected the Casimir benchmark and Pfenning–Ford interpretation.

### Layer 3 — JSON Schema and Cross-File Enforcement

All statistics files validated against `data/schemas/statistics-schema.json`:
- ID pattern: `^(s0[1-9]|sA[1-4])-[0-9]{3}$`
- Required fields: `id`, `metric`, `value`, `unit`, `date`, `source`, `confidence`, `verification_status`, `verified`, `verification_note`
- Confidence levels: `high`, `moderate`, `low`
- Verification status: `verified`, `theoretical`, `speculative`
- ISO dates and structured-source URIs are format-checked under JSON Schema Draft 2020-12
- Statistic IDs must be unique across files and match both the declared section and filename
- English and Traditional Chinese note inventories must each be complete and occurrence-matched

---

## 4. Per-Section Verification Summary

### Section 2: Observable Characteristics (13 data points)

| Confidence | Count |
|-----------|-------|
| High | 8 |
| Moderate | 3 |
| Low | 2 |

Key verification notes:
- USS Nimitz modal 5,370 g figure retained as a low-confidence scenario estimate derived from witness-reported inputs and a symmetric acceleration/deceleration model, not an official DoD measurement
- MICROSCOPE EP precision (10⁻¹⁵) verified via PRL publication (Touboul et al. 2022)
- Shuttle reentry temperature from NASA thermal protection system data

### Section 3: Propulsion Mechanisms (4 data points)

| Confidence | Count |
|-----------|-------|
| High | 2 |
| Moderate | 2 |
| Low | 0 |

Key verification notes:
- Pfenning & Ford (1997) wall bound (~1.6 × 10⁻³³ m for v_b ~ c) is model-dependent; their 100 m example scales linearly with v_b
- The former 10⁶⁸ Casimir-to-warp ratio is withdrawn; s03-004 is retained as "not defined"

### Section 4: Energy Sources (16 data points)

| Confidence | Count |
|-----------|-------|
| High | 14 |
| Moderate | 1 |
| Low | 1 |

Key verification notes:
- NIF record data come from LLNL's official ignition page: the April 7, 2025 shot remains the 8.6 MJ / target-gain 4.13 record; LLNL reported 11 ignition shots through June 20, 2026. Target gain is not wall-plug gain.
- Energy densities from standard nuclear physics data tables (NNDC/BNL)
- Vacuum energy density is theoretical (QFT calculation with Planck-scale cutoff)

### Section 6: Advanced Materials (12 data points)

| Confidence | Count |
|-----------|-------|
| High | 12 |
| Moderate | 0 |
| Low | 0 |

Key verification notes:
- CNT ~80 GPa from Bai et al. (2018) in Nature Nanotechnology, for centimetre-long bundles on a wall-area basis (≈43 GPa engineering strength)
- Individual structure-defined SWCNTs: 25–66 GPa (Takakura et al. 2019); the former "up to 85%" defect-reduction figure does not appear in that paper and was removed
- Graphene 130 GPa from Lee et al. (2008) in Science
- The former comparison between the QCD coupling and macroscopic material strength was removed because dimensionless, scale-dependent couplings are not tensile-strength multipliers

---

## 5. Government Document Verification

| Document | Publisher | URL Status | Access Verified |
|----------|----------|------------|----------------|
| ODNI Preliminary Assessment (2021) | ODNI | HTTP 403 (bot-restricted) | 2026-11-07 |
| ODNI 2022 Annual Report | ODNI | HTTP 403 (bot-restricted) | 2026-11-07 |
| AARO Historical Record Vol I (2024) | DoD | HTTP 403 (bot-restricted) | 2026-11-07 |
| AARO/ORNL Metallic Specimen (2024) | AARO | HTTP 403 (bot-restricted) | 2026-11-07 |
| ICD 203 Analytic Standards | ODNI | HTTP 403 (bot-restricted; also served from archive.dni.gov) | 2026-11-07 |

---

## 6. DIRD Collection Verification

- **37 DIRDs** (1,473 pages) released by DIA under FOIA on March 25, 2022 (FOIA-00159-2018); marked UNCLASSIFIED//FOR OFFICIAL USE ONLY and withheld in part (e.g., author names) under exemptions (b)(3) and (b)(6)
- **Entry #38** on the DIA list is the SECRET/NOFORN version of the high-energy laser weapons DIRD (#23) and has not been released
- Collection mirrors checked on November 7, 2026:
  - The Black Vault directory: HTTP 200
  - The Black Vault ZIP archive: HTTP 200
  - FAS master list: HTTP 202 with an empty body (bot challenge; recorded as access-restricted)

---

## 7. Confidence Assessment Methodology

Following ICD 203 (Intelligence Community Directive 203, "Analytic Standards"):

| Level | Definition |
|-------|-----------|
| **High** | Established physics, extensive experimental verification, broad consensus |
| **Moderate** | Theoretically sound, partial experimental support, novel application |
| **Low** | Mathematically consistent but unverified, limited data, speculative extrapolation |

Verification status markers:
- **[VERIFIED]** — Experimentally confirmed and peer-reviewed or, for observational and policy facts, documented in an authoritative primary government record
- **[THEORETICAL]** — Mathematically consistent, not experimentally verified
- **[SPECULATIVE]** — Hypothetical extrapolation beyond established theory; no mathematical proof or experimental basis
- **[ASSESSED]** — Analytic judgment by the author drawn from the cited sources; not itself an experimental or peer-reviewed result

---

## 8. Known Limitations

1. **Automated HTTP checks are observational** — Valid official or DOI endpoints may return HTTP 403, 429, or transient errors to scripts. Required CI validates persisted registry data offline; live checks run separately.
2. **DIRD content verification** — Individual DIRD technical claims are not independently validated; DIRDs are commissioned analyses rather than peer-reviewed evidence.
3. **Metadata status is not empirical replication** — The 42/45 count records repository source checks. It must not be read as 42 independently reproduced experiments or validated physical claims.
4. **NIF data currency** — Fusion progress changes rapidly. The stated record was checked against LLNL information available on 2026-08-02.
5. **USS Nimitz acceleration** — Detailed radar tracks are not public; the quoted acceleration is a model result from reported inputs, not a calibrated measurement.
6. **Subscription sources** — Some DOI-linked papers require journal subscriptions for full access.
7. **Registry coverage** — The URL registry is a spot-check artifact, not a guarantee that every cited source remains browser-accessible from every region or network.

---

*Last updated: 2026-11-07*
