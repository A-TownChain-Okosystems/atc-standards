# ATC Standards

> Die normative Governance-Schicht der A-TownChain-Organisation — Registry,
> Standards, Schemata, Validatoren und Governance-Entscheidungen.

> **ATC COMPLIANCE: R3 · Standard ATC-STD-201 v1.0.0 · GATE: AUDITED (07.09.2026) · README: ATC-STD-README-001 CONFORM (13/13)**

**Project:** atc-standards
**Organization:** A-TownChain-Okosystems
**Status:** `release-candidate`
**Version:** `1.2.0`
**License:** `Proprietary — A-TownChain-Okosystems (Governance-Dokument)`

<!-- atc metadata block (ATC-STD-README-001 §14) -->
<!--
atc:
  standard: ATC-STD-README-001
  version: 1.0.0
repository:
  id: ATC-REPO-GOV-001
  name: atc-standards
  type: governance
  status: release-candidate
ownership:
  organization: A-TownChain-Okosystems
technology:
  primary_language: YAML/Markdown/Python (Validator)
governance:
  security_class: S3 — Governance-Dokument
  criticality: CRITICAL (Registry = SSOT)
-->

## Overview

atc-standards ist das Governance-Repository der A-TownChain-Okosystems: die
kanonische Ablage (SSOT) aller 82 registrierten Standards inklusive Verfassung,
Validator-Suite, Naming-Schema, Change-Requests (SCR) und Findings-Registry.
Jedes Repository der Organisation richtet sich nach den hier definierten Regeln.

## Purpose

ATC Standards provides the canonical normative governance layer of the
A-TownChain ecosystem. It is responsible for:

- Verfassung **ATC-STD-000** v1.2.0 (ID-System, Lifecycle, SCR, §30 Immutabilität)
- Standard-Registry (**113 Standards**: 112 APPROVED + 1 DRAFT, REPO-AUDIT-001) mit
  Versionierung, Dependencies (DAG) und Findings (BUG-001..004)
- Maschinelle Qualitätssicherung: `atc-std-validator` (113/113 COMPLIANT),
  Mutationssuite (12/12), `atc-repo-audit` (R3, 100/100 GATE PASS),
  Agent-Manifest-Gate (`check_agent_manifest.py`)
- Naming-SSOT (`naming-conventions.schema.json`), Change-Requests (SCR-0001..0007)
- Governance-Ableitungen: Enterprise-Layer (ATC-ENT-001..015), Agenten-Standards
  (ATC-AAS-001..025), AI-Development-Familie (AI-DEV-001..012)

Davon hängen ab: **alle 26 aktiven Repositories** der Organisation (Registry-First:
kein Standard ohne Eintrag; kein Repository ohne Standards-Bezug).

## Status

**Status:** `release-candidate` — Governance-Freeze abgeschlossen
(07.09.2026): 112 der 113 Standards APPROVED und normativ in Kraft — REPO-AUDIT-001
als einziger DRAFT (§9-Freigabe ausstehend); FRAMEWORK-001 als 112. APPROVED 23:48
(v1.0.1-PATCH via SCR-0020) (README-001 20:36,
SC-Framework 001..020 21:00, MD-001 21:05). Übergangsfristen
(Commit-Trailer, Repo-Manifeste, Interface-Test-Suiten) laufen bis 07.10.2026.

## Architecture

### Components

- `registry/` — SSOT: standards.yaml, versions.yaml, dependencies.yaml,
  findings.yaml, categories.yaml
- `standards/` — 82 Standard-Dateien in 10 Familien (000, 100, 201–204, 300,
  bug, net, zkp, ai, aas, enterprise, readme)
- `schemas/` — naming-conventions.schema.json (ID-/Dateinamen-/REQ-Muster)
- `tools/` — atc-std-validator, atc-repo-audit, atc-readme-validator,
  Mutationstests
- `governance/` + `approval/` + `change-requests/` — Verfassung, Freigaben, SCR
- `.github/ai/` — Agent-Manifest (AAS-025), AGENTS.md, AUD-Records (AI-DEV-009)

### Data Flow

Änderungsantrag → SCR (§19–33) → Owner-Freigabe (§9) → Registry-Eintrag →
CI-Validierung (113/113 + Gates) → APPROVED → normativ in Kraft (§30 Immutabilität).

### Dependencies

| Component | Purpose | Required |
|---|---|---|
| registry/standards.yaml | SSOT aller Standards | Yes |
| schemas/naming-conventions.schema.json | ID-/Namens-Muster (§7.11) | Yes |
| tools/atc-std-validator | Struktur-Validierung (S-01..S-19) | Yes |
| tools/atc-repo-audit | Repository-Audit R1–R3 | Yes |
| tools/atc-readme-validator | README-Gates (ATC-STD-README-001) | Yes |

## Features

- 82 Standards in 11 Familien, vollständige REQ-ID-Struktur (BUG/NET/ZKP/README)
- Voll-Compliance-Mandat für Agenten (AGENT_MANIFEST.md, AAS-003/004)
- CI-Gates: Standards-Validierung, Mutationssuite, Repo-Audit R3,
  Agent-Manifest-Enforcement
- Findings-Lifecycle (F-001..F-018) mit Severity S0–S4
- **Smart Contract Standards Framework** ATC-STD-SC-001..020 (Gates SC-G0..G13) mit Contract Registry (contracts/)

## Repository Structure

```text
/
├── approval/            # Owner-Freigaben (§9)
├── atc/                 # Legacy ATC-01..99
├── ats/                 # ATS System Standards
├── change-requests/    # SCR-0001..0007
├── docs/                # Audits & Berichte
├── governance/          # Verfassung ATC-STD-000
├── licensing/           # System-/Hardware-Lizenzen
├── references/          # Referenzen
├── registry/            # SSOT (standards, versions, dependencies, findings, categories)
├── schemas/             # Naming-/Metadaten-Schemata
├── standards/           # 82 Standards in 10 Verzeichnissen
├── templates/           # Standard-Templates
├── contracts/           # Contract Registry (SC-019) + Kategorie-Specs (SC-Framework)
├── tools/               # Validator, Audit, README/MD/SC-Gates, Tests
├── .github/ai/          # Agent-Manifest, AGENTS.md, AUD-Records
├── AGENT_MANIFEST.md    # Agenten-Identität + Voll-Compliance-Mandat
├── AGENTS.md            # Repo-Agenten-Regeln
├── CHANGELOG.md
├── ROADMAP.md
├── STATUS.md
├── SECURITY.md
└── LICENSE
```text

## Requirements

- Python >= 3.11 (PyYAML, py_compile) für Validatoren
- Git >= 2.30
- Keine Runtime-Abhängigkeiten — reines Governance-Dokumenten-Repository

## Installation

### Setup

```bash
git clone https://github.com/A-TownChain-Okosystems/atc-standards.git
cd atc-standards
python3 -m pip install pyyaml
```

## Configuration

Keine Konfiguration nötig — Validatoren laufen stand-alone gegen die Registry.

## Usage

Standards validieren (alle 82):

```bash
python3 tools/atc-std-validator/validate_all.py
# Expected: RESULT: ALL COMPLIANT
```text

Repository-Audit R3:

```bash
python3 tools/atc-repo-audit/atc_repo_audit.py . --level R3
# Expected: GATE: PASS
```

README-Compliance eines Repos prüfen (ATC-STD-README-001):

```bash
python3 tools/atc-readme-validator/check_readme.py /pfad/zum/repo
# Expected: RESULT: CONFORM — alle 13 Gates bestanden
```text

## Development

Änderungen an APPROVED-Standards ausschließlich via SCR (ATC-STD-000 §19–33,
§30 Immutabilität). Neue Standards: Registry-First (Eintrag + Validierung +
§9-Freigabe). Agenten folgen dem Voll-Compliance-Mandat (AGENT_MANIFEST.md)
und dem AAS-008-Workflow; Commits nach AI-DEV-007 v1.0.1.

## Testing

Run the complete test suite:

```bash
python3 tools/atc-std-validator/validate_all.py        # 113/113 COMPLIANT
python3 tools/atc-std-validator/tests/test_s19_mutation.py  # 12/12 OK
python3 tools/atc-repo-audit/atc_repo_audit.py . --level R3    # GATE PASS
python3 tools/atc-std-validator/check_agent_manifest.py       # GATE PASS
python3 tools/atc-readme-validator/check_readme.py .           # CONFORM
```

Expected result: PASS (alle Gates grün — siehe STATUS.md)

## Security

Security issues must not be disclosed publicly through GitHub Issues.

Report security vulnerabilities through the official ATC security reporting
process (ATC-STD-203, SECURITY.md). Governance-Dokumente sind S3-classifiziert;
die Registry enthält keine Secrets, Tokens oder Zugangsdaten.

## Documentation

Vollständige Dokumentation liegt außerhalb dieses README:

- `docs/` — Audit- und Self-Compliance-Berichte
- `governance/` — Verfassung ATC-STD-000 v1.2.0
- `STATUS.md` / `ROADMAP.md` — kanonischer Stand
- Wiki: A-TownChain-Okosystems/a-townchain-os-docs
- Standards Registry: `registry/standards.yaml` (SSOT)

## Governance

This repository is governed according to the A-TownChain Enterprise Governance
Framework (ATC-STD-000 v1.2.0, ATC-ENT-001..015). Changes affecting
architecture, APIs, standards, security or consensus-critical functionality
require the applicable review and approval process (§9-Owner-Freigabe, SCR).
Agenten: Voll-Compliance-Mandat, CI-Enforcement, AUD-Records (AI-DEV-009).

## Standards & Compliance

This repository follows applicable A-TownChain standards:

| Standard | Version | Compliance |
|---|---:|---|
| ATC-STD-000 | 1.2.0 | ✅ |
| ATC-STD-201 | 1.0.0 | ✅ |
| ATC-STD-202 | 1.1.0 | ✅ |
| ATC-STD-203 | 1.0.0 | ✅ |
| ATC-STD-204 | 1.0.0 | ✅ |
| ATC-STD-README-001 | 1.0.0 | ✅ APPROVED (konforme Referenzimplementierung) |

## Roadmap

See the canonical roadmap:

- `ROADMAP.md` (Repo-wurzel)
- ATC Development Management (Notion Master Roadmap)
- GitHub Issues / Projects

## Contributing

Beiträge ausschließlich über den Governance-Prozess: SCR für Standard-
Änderungen (§19–33), Findings nach ATC-STD-BUG-001, neue Standards via
Registry-First. Details: `CONTRIBUTING.md`, ATC-STD-000 §22.

## License

Proprietary — A-TownChain-Okosystems. Governance-Dokument; Weitergabe und
Ableitung nur mit Owner-Freigabe (siehe LICENSE).

## Maintainers

**Organization:** A-TownChain-Okosystems

Repository ownership and authorized maintainers are defined through the
repository governance configuration: Owner Michael (§9-Freigaben),
ATC-AI-ARCH-001 (Aurora #1, operative Pflege, AUD-pflichtig).

## Repository Metadata

Maschinenlesbar: siehe HTML-Metadaten-Block im Header (ATC-STD-README-001 §14).
Zielzustand: Generierung aus `repositories.yaml` (ATC-ENT-009-Rollout) statt
manueller Pflege. Registry-ID: ATC-REPO-GOV-001.
