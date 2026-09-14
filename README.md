<!-- GENERATED-BY generate_views.py — NICHT MANUELL BEARBEITEN -->
# ATC Standards

[![ATC COMPLIANCE](https://img.shields.io/badge/ATC-COMPLIANCE-green) ](README.md) <!-- formal: PASS, R12-enforced (SCR-0096; Scan-Konvention ATC-COMPLIANCE) -->

## State (GENERIERT — Quelle: `registry/standards.yaml`, SCR-0090/ATC-STD-003)

```yaml
state:
  id: ATC-STATE-20260914-8ff9ce3b
  generated_at: "2026-09-14 12:54 UTC+2"
  registry_version: "1.0.0"
  registry_sha256: "8ff9ce3b9aba170adbeb0833ad1b7f0ada86f671c036ba152b4aeb7d1f87cf27"
  standards_total: 505
  standards_approved: 505
  standards_candidate: 0
  standards_other: 40
  standard_files: 503
  families: 75
```

**Diese Zahlen sind die EINZIG maschinenverbindliche Auskunft** (ATC-STD-003 §2 Ein-Zahl-Regel).
Historische Zahlenstände: ausschließlich `STATUS.md` / `CHANGELOG.md` / `audits/`.

**Implementierungs-KPI:** 505 Standards normativ definiert — 65 enforced, 131 implemented, 303 specification-only. Die Aussage „505 Standards implementiert“ ist unzulässig (SCR-0048, ATC-STD-003 §8: APPROVED ≠ IMPLEMENTED).

**FORMALE COMPLIANCE: PASS** · **IMPLEMENTATION: PARTIAL** · **PRODUCTION READINESS: NOT_READY** — ein Zustand behauptet nie den anderen.

---

## Status

**Status:** `release-candidate` — Governance technisch weit fortgeschritten. Aktueller normativer Bestand und Umsetzungsgrad: ausschließlich State-Block oben (SCR-0090).

## Purpose

ATC Standards is the canonical normative governance layer of the A-TownChain ecosystem. It maintains:

- **Registry:** SSOT für alle 505 Standards mit Versionierung, Dependencies (DAG) und Findings
- **Verfassung:** ATC-STD-000 v1.3.0, APPROVED (ID-System, Lifecycle, Change Control, Immutabilität)
- **Validator-Suite:** atc-std-validator, atc-repo-audit (R3), atc-readme-validator
- **Governance Framework:** 75 Familien, Enterprise-Ebenen (ATC-ENT-001..015), AI-Standards (ATC-AAS-001..025)
- **Governance-Determinismus:** ATC-STD-003 (SSOT-Matrix, State-ID, Ein-Zahl-Regel)

Repository-Abdeckung wird ausschließlich aus Registry-/Profile-State und den generierten Views abgeleitet; Organisationszahlen werden hier nicht als unabhängige SSOT geführt.

## Scope

Governance-Root der A-TownChain-Organisation: Registry, Standards, Schemata, Validatoren, Audits und Change-Requests. In Scope: normative Standards und ihre Metadaten/Validierung. Out of Scope: Implementierung der Standards in den abhängigen Repositories; Nachweis via Implementierungs-Matrix.

## Features

- Registry-SSOT (`standards.yaml`, SHA-Lock) mit schema-validierten Metadaten
- Validatoren: S-01..S-17, Meta-Sweep, Meta-Daten-Audit, README-Validator
- Implementierungs-Matrix — kein Status ohne Evidence
- Repository-Audit R1-R3 und Governance-CI
- Discovery-Familie für neue Inhalte

## Architecture

### Core Components
- `registry/` — SSOT (`standards.yaml`, versions.yaml, dependencies.yaml, findings.yaml, families/)
- `standards/` — normative Standard-Dateien
- `profiles/` — verbindliche Standards-Profile je Repository
- `schemas/` — JSON/YAML-Schemata
- `tools/` — Validatoren, Auditors, Generatoren
- `governance/`, `approval/`, `change-requests/` — Verfassung, Freigaben und SCR-System

### Usage

```bash
python3 tools/atc-std-validator/validate_all.py
python3 tools/atc-repo-audit/atc_repo_audit.py . --level R3
```

## Governance Flow
Change Request → SCR (§19–33) → Owner-Freigabe (§9) → Registry-Eintrag → CI-Validierung → APPROVED → normativ in Kraft (§30 Immutabilität).

---

## Quick Start

```bash
git clone https://github.com/A-TownChain-Okosystems/atc-standards.git
cd atc-standards
python3 -m pip install pyyaml
```

## Governance

This repository is governed according to ATC-STD-000 v1.3.0 (APPROVED):

- **Changes to APPROVED Standards:** via SCR only (§30 Immutabilität)
- **New Standards:** Registry-First
- **AI Agents:** Executor/Auditor/Maintainer, never Approver
- **CI Gates:** Standards-Validierung, Mutationssuite, Repo-Audit R3, Agent-Manifest-Enforcement

See `CONTRIBUTING.md` and `governance/ATC-STD-000.md` for details.

## Standards & Compliance

| Standard | Version | Status |
|---|---|---|
| ATC-STD-000 | 1.3.0 | ✅ APPROVED |
| ATC-STD-003 | 1.0.0 | ✅ APPROVED |
| ATC-STD-201 | 1.0.1 | ✅ APPROVED |
| ATC-STD-202 | 1.2.0 | ✅ APPROVED |
| ATC-STD-203 | 1.0.1 | ✅ APPROVED |
| ATC-STD-204 | 1.0.0 | ✅ APPROVED |
| ATC-STD-README-001 | 1.0.0 | ✅ APPROVED |

See `registry/standards.yaml` for the complete registry.

## Development

Änderungen laufen über SCR. Registry-Änderungen nur via kontrolliertem Change-Request. Views (README/AGENT_MANIFEST/STATUS) sind generiert.

## Testing

Lokal vor Push:

```bash
python3 tools/atc-std-validator/validate_all.py
python3 tools/atc-repo-audit/atc_repo_audit.py . --level R3
python3 tools/atc-readme-validator/check_readme.py .
```

## Roadmap

Governance-Hardening: Registry-Integritäts-Gate, Discovery→Audit→SCR-Kopplung, Evidence-L3 für kritische Standards und CI-Evidence-Kopplung der Implementierungs-Matrix.

## Documentation

Full documentation:
- **Governance:** `governance/`, `STATUS.md`, `ROADMAP.md`
- **Audits:** `docs/audits/`
- **Change History:** `change-requests/`, `CHANGELOG.md`
- **Wiki:** `a-townchain-os-docs`

## Security

Security issues **must NOT** be disclosed via GitHub Issues. Report vulnerabilities through GitHub Private Vulnerability Reporting or the process defined in `SECURITY.md`.

## Maintainers

**Organization:** A-TownChain-Okosystems · **Owner:** See `governance/authority/authority-matrix.yaml` and the applicable §9 approval record. Historical approval documents may contain former identity metadata and are not by themselves the current authority SSOT.

## License

**Apache-2.0** (see `LICENSE`). Additional ATC usage terms are governed by the ATC-LICENSE family.

## Metadata

- **Project:** atc-standards
- **Organization:** A-TownChain-Okosystems
- **Status:** `release-candidate`
- **Version:** 1.0.0
- **Registry ID:** ATC-REPO-GOV-001

Machine-readable metadata: State-Block oben; Registry-SSOT: `registry/standards.yaml`.

## Registry-vs-Dateien-Relation

Regel: Jeder Registry-Eintrag besitzt eine Datei in `standards/` ODER eine dokumentierte EXEMPT-Begründung. Die Gültigkeit dieser Relation wird je Lauf geprüft; aktuelle Zahlen ausschließlich im State-Block oben. Historische Zustände gehören in `STATUS.md`, `CHANGELOG.md` und Audit-Artefakte.
