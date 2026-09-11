<!-- GENERATED-BY generate_views.py — NICHT MANUELL BEARBEITEN -->
# ATC Standards

[![ATC COMPLIANCE](https://img.shields.io/badge/ATC-COMPLIANCE-green) ](README.md) <!-- formal: PASS, R12-enforced (SCR-0096; Scan-Konvention ATC-COMPLIANCE) -->

## State (GENERIERT — Quelle: `registry/standards.yaml`, SCR-0090/ATC-STD-003)

```yaml
state:
  id: ATC-STATE-20260911-4894fb05
  generated_at: "2026-09-11 18:46 UTC+2"
  registry_version: "1.0.0"
  registry_sha256: "4894fb05289a937703b353ba5aa864d14d8cba4d9c931c962e34c1c76c4840cb"
  standards_total: 475
  standards_approved: 463
  standards_candidate: 0
  standards_other: 12
  standard_files: 472
  families: 51
```

**Diese Zahlen sind die EINZIG maschinenverbindliche Auskunft** (ATC-STD-003 §2 Ein-Zahl-Regel).
Historische Zahlenstände: ausschließlich `STATUS.md` / `CHANGELOG.md` / `audits/`.

**Implementierungs-KPI:** 475 Standards normativ definiert — 65 enforced, 129 implemented, 265 specification-only (Zielsysteme im qualitätsgetriebenen Rebuild AD-023/AD-045). Die Aussage „475 Standards implementiert“ ist unzulässig (SCR-0048, ATC-STD-003 §8: APPROVED ≠ IMPLEMENTED).

**FORMALE COMPLIANCE: PASS** (Repository-Audit R3: Naming/Versioning/Ownership/Lizenz + Cross-Registry-Test R1-R12) · **IMPLEMENTATION: PARTIAL** (41 % code-backed: 65 enforced + 129 implemented von 475 Matrix-Eintraegen erfassten (Registry-Gesamt: 475)) · **PRODUCTION READINESS: NOT_READY** (Release-/Mainnet-Gates, registry/milestones.yaml) — ein Zustand behauptet nie den anderen ([Audit-Details](#standards--compliance))

---

## Status

**Status:** `release-candidate` — Governance technisch weit fortgeschritten
(externes Audit 08.09.: B/AMBER, SCR-0052). Aktueller normativer Bestand und
Umsetzungsgrad: ausschließlich State-Block oben (SCR-0090).

## Purpose

ATC Standards is the canonical normative governance layer of the A-TownChain ecosystem. It maintains:

- **Registry:** SSOT für alle 475 Standards mit Versionierung, Dependencies (DAG) und Findings
- **Verfassung:** ATC-STD-000 v1.3.0, APPROVED (ID-System, Lifecycle, Change Control, Immutabilität)
- **Validator-Suite:** atc-std-validator, atc-repo-audit (R3), atc-readme-validator
- **Governance Framework:** 51 Familien, Enterprise-Ebenen (ATC-ENT-001..015), AI-Standards (ATC-AAS-001..025)
- **Governance-Determinismus:** ATC-STD-003 (SSOT-Matrix, State-ID, Ein-Zahl-Regel)

All 26 organizational repositories follow these standards (Registry-First principle).

---

## Scope

Governance-Root der A-TownChain-Organisation: Registry, Standards,
Schemata, Validatoren, Audits und Change-Requests. In Scope: normative
Standards (472 Dateien, 51 Familien) und ihre Metadaten/Validierung.
Out of Scope: Implementierung der Standards (liegt in den 27 governed Repos und
deren CI-Gates; Nachweis via Implementierungs-Matrix).

## Features

- Registry-SSOT (`standards.yaml`, SHA-Lock) mit schema-validierten Metadaten (SCR-0050)
- Validatoren: S-01..S-17, Meta-Sweep, Meta-Daten-Audit, README-Validator
- Implementierungs-Matrix (SCR-0048) — kein Status ohne Evidence
- Repository-Audit R1-R3 (ATC-STD-201ff) und Governance-CI
- Discovery-Familie (REPO-DISCOVERY-001..010) fuer neue Inhalte

## Architecture

### Core Components
- `registry/` — SSOT (standards.yaml, versions.yaml, dependencies.yaml, findings.yaml, families/ = Familien-SSOT, standards/ = generierte Per-Standard-Records)
- `standards/` — 472 Standard-Dateien in 51 Familien
- `profiles/` — 27 verbindliche Standards-Profile je Repository (Compliance-Vertrag, ATC-STD-LIB-001 §8) + `docs/architecture/` — Zielarchitektur
- `schemas/` — naming-conventions.schema.json, milestone.schema.json, etc.
- `tools/` — Validators, Auditors, Generators
- `governance/` (constitution/, authority/, decision-rights/, repository-governance/), `approval/`, `change-requests/` — Verfassung, Freigaben, SCR-System

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

This repository is governed according to ATC-STD-000 v1.3.0 (APPROVED, A-TownChain Enterprise Governance Framework):

- **Changes to APPROVED Standards:** via SCR only (§30 Immutabilität)
- **New Standards:** Registry-First (Eintrag → Validierung → §9-Owner-Freigabe); ATC-STD-003 §7: No standard because a slot exists
- **AI Agents:** Voll-Compliance-Mandat, CI-Enforcement, AUD-Records (AI-DEV-009); ATC-STD-003 §9: Agenten sind Executor/Auditor/Maintainer, nie Approver
- **CI Gates:** Standards-Validierung, Mutationssuite, Repo-Audit R3, Agent-Manifest-Enforcement

See `CONTRIBUTING.md` and `governance/ATC-STD-000.md` for details.

---

## Standards & Compliance

| Standard | Version | Status |
|---|---|---|
| ATC-STD-000 | 1.3.0 | ✅ APPROVED (Verfassung; par.9-freigegeben 11.09.2026 — Bootstrap-EXEMPT beendet, R11 waecht weiter) |
| ATC-STD-003 | 1.0.0 | ✅ APPROVED (Governance Determinism & SSOT Matrix) |
| ATC-STD-201 | 1.0.1 | ✅ APPROVED |
| ATC-STD-202 | 1.2.0 | ✅ APPROVED |
| ATC-STD-203 | 1.0.1 | ✅ APPROVED |
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
├── evidence/        # Security & Technology Evidence Store (ATC-GATE-SEC-001 §4)
├── governance/      # ATC-STD-000 Verfassung + Governance-Doku
├── licenses/        # Lizenz-Texte
├── licensing/       # ATC-LICENSE-Standards (Code/Marke/Assets/Doku)
├── profiles/       # 27 Standards-Profile je Repository (Compliance-Vertrag, ATC-STD-LIB-001 §8)
├── protocols/       # Prozessprotokolle
├── references/      # Normative Referenzen
├── registry/        # SSOT: standards.yaml, Matrix, Lock, Schemata-Reg
├── schemas/         # JSON/YAML-Schemata (standard.schema.yaml)
├── standards/       # 472 Standard-Dateien in 51 Familien
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
(GitHub: ShivaCoreDev) · Agent: Aurora (Base44 Superagent — Executor/Auditor/Maintainer, ATC-STD-003 §9)

## License

**Apache-2.0** (see [`LICENSE`](LICENSE)) — unified organizational license as of 08.09.2026.

Additional ATC usage terms (separate from Apache-2.0) are governed by the ATC-LICENSE-Familie (ATC-STD-LICENSE-001..009). Governance documents, trademarks, and organizational assets follow separate policies.

**No Apache-2.0 claims** conflict with the LICENSE file.

---

## Metadata

- **Project:** atc-standards
- **Organization:** A-TownChain-Okosystems
- **Status:** `release-candidate`
- **Version:** 1.0.0
- **Registry ID:** ATC-REPO-GOV-001
- **Owner:** Michael Wroblewski (§9-Freigaben)
- **Maintainer:** Aurora #1 (operative Pflege, AUD-pflichtig)

Machine-readable metadata: State-Block oben (SCR-0090); Registry-SSOT: `registry/standards.yaml`.

## Registry-vs-Dateien-Relation (zeitlose Regel, SCR-0086/SCR-0090)

Regel: Jeder Registry-Eintrag besitzt eine Datei in `standards/` ODER eine dokumentierte
EXEMPT-Begruendung (aktuell einzig: `ATC-STD-000` als Master-Dokument außerhalb `standards/`,
Bootstrap-EXEMPT mit Sunset, ATC-STD-003 §6). Die GUltigkeit dieser Relation wird je Lauf geprueft;
alle Zahlen hierzu ausschließlich im State-Block oben. Historische Zustaende (z.B. 08.09.):
`STATUS.md` (Audit-Trail).
