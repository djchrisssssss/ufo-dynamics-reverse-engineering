# Data Verification Report

**DOI:** [10.5281/zenodo.19138271](https://doi.org/10.5281/zenodo.19138271)
**Report Date:** 2026-03-20
**Auditor:** Automated + Manual Review

---

## 1. Overview

This verification report documents the data provenance, source quality, and cross-referencing methodology applied to quantitative claims in the UAP Physics Assessment.

### Summary Statistics

| Metric | Value |
|--------|-------|
| Total bibliography sources | 59 |
| Total quantitative data points | 45 |
| Sections with statistics | 4 (s02, s03, s04, s06) |
| Data points independently cross-checked | 43/45 (95.6%) |
| Tracked URLs in source registry | 34 |
| HTTP 200/202 during 2026-03-21 automated spot check | 20/29 |
| HTTP 403/404 during 2026-03-21 automated spot check | 9/29 |

---

## 2. Source Quality Breakdown

| Source Type | Count | Percentage | Reliability Tier |
|-------------|-------|-----------|-----------------|
| Peer-reviewed articles | 31 | 52.5% | Tier 1 (highest) |
| Government documents | 9 | 15.3% | Tier 1 (highest) |
| Defense Intelligence Reference Documents | 12 | 20.3% | Tier 2 (expert-authored, govt-commissioned) |
| Books / Monographs | 6 | 10.2% | Tier 2 (academic) |
| Preprints | 1 | 1.7% | Tier 3 (not yet peer-reviewed) |

---

## 3. Verification Methodology

### Tier 1 — Source Selection Criteria

1. **Peer-reviewed literature** — Published in recognized journals (Nature, Science, Physical Review, Classical and Quantum Gravity)
2. **Government documents** — Official publications from ODNI, AARO, DoD
3. **DIRDs** — Expert-authored technical papers commissioned by DIA under AAWSAP
4. **Textbooks** — Standard references (Misner-Thorne-Wheeler, Wald, Visser)

### Tier 2 — Four-Step Data Point Verification

1. **Source identification** — Primary authoritative source identified for each statistic
2. **Cross-referencing** — Figure compared against ≥1 secondary source (documented in `verification_note`)
3. **Contextual plausibility** — Consistency with related data points checked
4. **Documentation** — Citation string or source object, access date, and verification notes recorded in JSON

### Tier 3 — JSON Schema Enforcement

All statistics files validated against `data/schemas/statistics-schema.json`:
- ID pattern: `^(s[0-9]{2}|sA[0-9])-[0-9]{3}$`
- Required fields: `id`, `metric`, `value`, `unit`, `date`, `source` (citation string or structured object)
- Confidence levels: `high`, `moderate`, `low`
- Verification status: `verified`, `theoretical`, `speculative`

---

## 4. Per-Section Verification Summary

### Section 2: Observable Characteristics (13 data points)

| Confidence | Count |
|-----------|-------|
| High | 8 |
| Moderate | 3 |
| Low | 1 |

Key verification notes:
- USS Nimitz 5,300 g figure retained as a low-confidence third-party estimate (Knuth et al. 2019), not an official DoD measurement
- MICROSCOPE EP precision (10⁻¹⁵) verified via PRL publication (Touboul et al. 2022)
- Shuttle reentry temperature from NASA thermal protection system data

### Section 3: Propulsion Mechanisms (4 data points)

| Confidence | Count |
|-----------|-------|
| High | 2 |
| Moderate | 2 |
| Low | 0 |

Key verification notes:
- Planck-length wall thickness from Pfenning & Ford (1997), peer-reviewed in CQG
- 10⁶⁸ energy gap is a derived quantity (Casimir density vs. warp requirements)

### Section 4: Energy Sources (16 data points)

| Confidence | Count |
|-----------|-------|
| High | 14 |
| Moderate | 1 |
| Low | 1 |

Key verification notes:
- NIF data from official LLNL press releases and DOE confirmations. April 2025 gain 4.13 (2.08 MJ → 8.6 MJ, shot date April 7, 2025) independently verified against LLNL ignition achievements page as of March 2026.
- Energy densities from standard nuclear physics data tables (NNDC/BNL)
- Vacuum energy density is theoretical (QFT calculation with Planck-scale cutoff)

### Section 6: Advanced Materials (12 data points)

| Confidence | Count |
|-----------|-------|
| High | 12 |
| Moderate | 0 |
| Low | 0 |

Key verification notes:
- CNT 80 GPa from Bai et al. (2018) in Nature Nanotechnology
- Graphene 130 GPa from Lee et al. (2008) in Science
- QCD coupling constant from Particle Data Group

---

## 5. Government Document Verification

| Document | Publisher | URL Status | Access Verified |
|----------|----------|------------|----------------|
| ODNI Preliminary Assessment (2021) | ODNI | HTTP 200 | 2026-03-21 |
| ODNI 2022 Annual Report | ODNI | HTTP 200 | 2026-03-21 |
| AARO Historical Record Vol I (2024) | DoD | HTTP 403 (bot-restricted) | 2026-03-21 |
| AARO/ORNL Metallic Specimen (2022) | AARO | HTTP 403 (bot-restricted) | 2026-03-21 |
| ICD 203 Analytic Standards | ODNI | HTTP 200 (updated official path) | 2026-03-21 |

---

## 6. DIRD Collection Verification

- **37 of 38 DIRDs** declassified via FOIA (March 25, 2022)
- **DIRD #38** (High-Energy Laser Weapons) retains SECRET/NOFORN
- Collection mirrors checked on March 21, 2026:
  - The Black Vault directory: HTTP 200
  - The Black Vault ZIP archive: HTTP 200
  - FAS master list: HTTP 202

---

## 7. Confidence Assessment Methodology

Following ICD 203 (Intelligence Community Directive 203, "Analytic Standards"):

| Level | Definition |
|-------|-----------|
| **High** | Established physics, extensive experimental verification, broad consensus |
| **Moderate** | Theoretically sound, partial experimental support, novel application |
| **Low** | Mathematically consistent but unverified, limited data, speculative extrapolation |

Verification status markers:
- **[VERIFIED]** — Experimentally confirmed, peer-reviewed
- **[THEORETICAL]** — Mathematically consistent, not experimentally verified
- **[SPECULATIVE]** — Hypothetical extrapolation beyond established theory

---

## 8. Known Limitations

1. **Automated HTTP checks are imperfect** — Some valid official or DOI endpoints return HTTP 403 to scripted requests because of bot restrictions
2. **DIRD content verification** — Individual DIRD technical claims not independently verified; DIRDs are treated as expert opinion
3. **NIF data currency** — Fusion progress data subject to rapid updates. The April 2025 gain 4.13 figure has been independently verified against LLNL and DOE sources as of March 2026 (src-059). Future shots may surpass this record.
4. **USS Nimitz acceleration** — Derived from radar tracking data whose calibration and interpretation remain debated in the UAP research community
5. **Subscription sources** — Some DOI-linked papers require journal subscriptions for full access
6. **Registry coverage** — The URL registry is a spot-check artifact, not a guarantee that every cited source remains browser-accessible from every region or network

---

*Last updated: 2026-03-21*
