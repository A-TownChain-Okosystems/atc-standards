# ATC Standards

<!-- GENERATED-BY generate_views.py — NICHT MANUELL BEARBEITEN -->
## Registry-Kennzahlen (GENERIERT — Quelle: `registry/standards.yaml`)

| Kennzahl | Wert |
|---|---|
| Registry Standards | **432** |
| Registry APPROVED | **395** |
| Registry CANDIDATE (§33) | **37** |
| Standard-Dateien (`standards/`) | **431** |
| Familien | **50** |
| Registry SHA-256 | `3f8efb252a8c6351…` (vollständig: `registry/registry.lock`) |
| Stand | 2026-09-08 17:32 UTC+2 |

Implementierungs-Matrix: [`registry/standard-implementation.yaml`](registry/standard-implementation.yaml) (ATC-STD-IMPLEMENTATION-001).

**Implementierungs-KPI:** 432 Standards normativ definiert — 62 enforced, 129 implemented, 240 specification-only (Zielsysteme im qualitätsgetriebenen Rebuild AD-023/AD-045). Die Aussage „432 Standards implementiert“ ist unzulässig (SCR-0048).

**ATC COMPLIANCE: YES** — Repository-Audit R3 · Naming/Versioning/Ownership/Lizenz konform ([Audit-Details](#standards--compliance))

---

## Status

**Status:** `release-candidate` — Governance technisch weit fortgeschritten
(externes Audit 08.09.: B/AMBER, SCR-0052). 431 Standards normativ definiert;
191 nachweisbar umgesetzt/enforced; 240 specification-only.

## Purpose

ATC Standards is the canonical normative governance layer of the A-TownChain ecosystem. It maintains:

- **Registry:** SSOT für alle 431 Standards mit Versionierung, Dependencies (DAG) und Findings
- **Verfassung:** ATC-STD-000 v1.2.0 (ID-System, Lifecycle, Change Control, Immutabilität)
- **Validator-Suite:** atc-std-validator, atc-repo-audit (R3), atc-readme-validator
- **Governance Framework:** 49 Familien, Enterprise-Ebenen (ATC-ENT-001..015), AI-Standards (ATC-AAS-001..025)

All 26 organizational repositories follow these standards (Registry-First principle).

---

## Scope

Governance-Root der A-TownChain-Organisation: Registry, Standards,
Schemata, Validatoren, Audits und Change-Requests. In Scope: normative
Standards (430 Dateien, 49 Familien) und ihre Metadaten/Validierung.
Out of Scope: Implementierung der Standards (liegt in den 26 Repos und
deren CI-Gates; Nachweis via Implementierungs-Matrix).

## Features

- Registry-SSOT (`standards.yaml`, SHA-Lock) mit 431 Standards und
  schema-validierten Metadaten (SCR-0050)
- Validatoren: S-01..S-17, Meta-Sweep, Meta-Daten-Audit, README-Validator
- Implementierungs-Matrix (SCR-0048) — kein Status ohne Evidence
- Repository-Audit R1-R3 (ATC-STD-201ff) und Governance-CI
- Discovery-Familie (REPO-DISCOVERY-001..010) fuer neue Inhalte

## Architecture

### Core Components
- `registry/` — SSOT (standards.yaml, versions.yaml, dependencies.yaml, findings.yaml)
- `standards/` — 431 Standard-Dateien in 50 Familien
- `schemas/` — naming-conventions.schema.json, milestone.schema.json, etc.
- `tools/` — Validators, Auditors, Generators
- `governance/`, `approval/`, `change-requests/` — Verfassung, Freigaben, SCR-System

### Usage

```bash
python3 tools/atc-std-validator/validate_all.py
# Expected: RESULT: ALL COMPLIANT
python3 tools/atc-repo-audit/atc_repo_audit.py . --level R3
# Expected: GATE: PASS
```

## Governance Flow
Change Request → SCR (§19–33) → Owner-Freigabe (§9) → Registry-Eintrag → CI-Validierung → APPROVED → normativ in Kraft (§30 Immutabilität).

---

## Quick Start

### Installation
```bash
git clone https://github.com/A-TownChain-Okosystems/atc-standards.git
cd atc-standards
python3 -m pip install pyyaml
```

### Validation
```bash
python3 tools/atc-std-validator/validate_all.py          # Alle Standards
python3 tools/atc-repo-audit/atc_repo_audit.py . --level R3   # Repository-Audit
python3 tools/atc-readme-validator/check_readme.py .     # README-Compliance
```

### Key Files
| Datei | Zweck |
|---|---|
| `registry/standards.yaml` | SSOT — Alle Standards |
| `governance/ATC-STD-000.md` | Verfassung |
| `CHANGELOG.md` | Änderungshistorie |
| `STATUS.md` | Audit-Trail & Snapshot |

---

## Governance

This repository is governed according to ATC-STD-000 v1.2.0 (A-TownChain Enterprise Governance Framework):

- **Changes to APPROVED Standards:** via SCR only (§30 Immutabilität)
- **New Standards:** Registry-First (Eintrag → Validierung → §9-Owner-Freigabe)
- **AI Agents:** Voll-Compliance-Mandat, CI-Enforcement, AUD-Records (AI-DEV-009)
- **CI Gates:** Standards-Validierung, Mutationssuite, Repo-Audit R3, Agent-Manifest-Enforcement

See `CONTRIBUTING.md` and `governance/ATC-STD-000.md` for details.

---

## Standards & Compliance

| Standard | Version | Status |
|---|---|---|
| ATC-STD-000 | 1.2.0 | ✅ APPROVED |
| ATC-STD-201 | 1.0.0 | ✅ APPROVED |
| ATC-STD-202 | 1.1.0 | ✅ APPROVED |
| ATC-STD-203 | 1.0.0 | ✅ APPROVED |
| ATC-STD-204 | 1.0.0 | ✅ APPROVED |
| ATC-STD-README-001 | 1.0.0 | ✅ APPROVED |

See [`registry/standards.yaml`](registry/standards.yaml) for the complete registry.

---

## Development

Aenderungen laufen ueber SCR (`change-requests/SCR-*.md`); Registry-Aenderungen
nur via kontrolliertem Change-Request. Views (README/AGENT_MANIFEST/STATUS) sind
GENERIERT — regeneration: `python3 tools/gen_views/generate_views.py`.
Commits: Conventional Commits + Agent-Signatur.

## Testing

Lokal vor Push: `python3 tools/atc-std-validator/validate_all.py` (alle
Standards, S-Gates) · `python3 tools/atc-repo-audit/atc_repo_audit.py . --level R3`
· `python3 tools/atc-readme-validator/check_readme.py .` (13 Gates).
CI: beide Workflows muessen gruen sein (Push = Gate).
Erwartete Ergebnisse: `RESULT: ALL COMPLIANT`, `GATE: PASS`, README-Validator CONFORM.

## Roadmap

Governance-Hardening (SCR-0052-P2): Registry-Integritaets-Gate, Discovery->Audit->
SCR-Kopplung, Evidence-L3 fuer kritische Standards, CI-Evidence-Kopplung der
Implementierungs-Matrix. V2S-Phasen-Standards V2S-001..026 (FAM-45) folgen dem
Implementierungs-Pivot (kein Standard ohne Implementierungsstatus).

## Repository Structure

```text
├── approval/        # §9-Freigabe-Protokolle (Owner-Signaturen)
├── atc/             # ATC-Governance-Kernartefakte
├── ats/             # ATC-Test-Spezifikationen
├── audits/          # Audit-Berichte (META-SWEEP, Audits AUD-*)
├── change-requests/ # SCR-*.md (Change-Requests)
├── contracts/       # Smart-Contract-Framework (Referenz)
├── docs/            # Patches, ADR, REPOSITORY_STANDARD, Audits
├── governance/      # ATC-STD-000 Verfassung + Governance-Doku
├── licenses/        # Lizenz-Texte
├── licensing/       # ATC-LICENSE-Standards (Code/Marke/Assets/Doku)
├── protocols/       # Prozessprotokolle
├── references/      # Normative Referenzen
├── registry/        # SSOT: standards.yaml, Matrix, Lock, Schemata-Reg
├── schemas/         # JSON/YAML-Schemata (standard.schema.yaml)
├── standards/       # 431 Standard-Dateien in 50 Familien
├── templates/       # Dokumentvorlagen
└── tools/           # Validatoren, Generatoren, Audits (Python)
```

## Documentation

Full documentation:
- **Governance:** `governance/`, `STATUS.md`, `ROADMAP.md`
- **Audits:** `docs/audits/`
- **Change History:** `change-requests/`, `CHANGELOG.md`
- **Wiki:** [A-TownChain-Okosystems/a-townchain-os-docs](https://github.com/A-TownChain-Okosystems/a-townchain-os-docs)

---

## Security

Security issues **must NOT** be disclosed via GitHub Issues. Report vulnerabilities through:
- **GitHub Private Vulnerability Reporting** (Security tab → "Report a vulnerability")
- **Direct contact:** Owner (ATC-STD-203, SECURITY.md)

See [`SECURITY.md`](SECURITY.md) for the full disclosure policy.

---

## Maintainers

**Organization:** A-TownChain-Okosystems · **Owner:** Michael Wroblewski
(GitHub: ShivaCoreDev) · Agent: Aurora (Base44 Superagent)

## License

**Apache-2.0** (see [`LICENSE`](LICENSE)) — unified organizational license as of 08.09.2026.

Additional ATC usage terms (separate from Apache-2.0) are governed by the ATC-LICENSE-Familie (ATC-STD-LICENSE-001..009). Governance documents, trademarks, and organizational assets follow separate policies.

**No Apache-2.0 claims** conflict with the LICENSE file.

---

## Metadata

- **Project:** atc-standards
- **Organization:** A-TownChain-Okosystems
- **Status:** `release-candidate`
- **Version:** 1.2.0
- **Registry ID:** ATC-REPO-GOV-001
- **Owner:** Michael Wroblewski (§9-Freigaben)
- **Maintainer:** Aurora #1 (operative Pflege, AUD-pflichtig)

Machine-readable metadata: see HTML comment block at top (ATC-STD-README-001 §14).
