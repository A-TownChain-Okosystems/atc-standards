# ATC Standards

<!-- GENERATED-BY generate_views.py — NICHT MANUELL BEARBEITEN -->
## Current State (GENERIERT — Quelle: `registry/standards.yaml`)

| Kennzahl | Wert |
|---|---|
| Registry Standards | **431** |
| APPROVED / CANDIDATE | **395 / 36** |
| Familien | **49** |
| Registry SHA-256 | `ff2117a62088cb0d…` ([Vollständig](registry/registry.lock)) |
| Stand | 2026-09-08 16:36 UTC+2 |

**Implementierungs-KPI:** 431 Standards normativ definiert — 62 enforced, 129 implemented, 240 specification-only. Details: [`standard-implementation.yaml`](registry/standard-implementation.yaml) (ATC-STD-IMPLEMENTATION-001).

---

## Purpose

ATC Standards is the canonical normative governance layer of the A-TownChain ecosystem. It maintains:

- **Registry:** SSOT für alle 431 Standards mit Versionierung, Dependencies (DAG) und Findings
- **Verfassung:** ATC-STD-000 v1.2.0 (ID-System, Lifecycle, Change Control, Immutabilität)
- **Validator-Suite:** atc-std-validator, atc-repo-audit (R3), atc-readme-validator
- **Governance Framework:** 49 Familien, Enterprise-Ebenen (ATC-ENT-001..015), AI-Standards (ATC-AAS-001..025)

All 26 organizational repositories follow these standards (Registry-First principle).

---

## Architecture

### Core Components
- `registry/` — SSOT (standards.yaml, versions.yaml, dependencies.yaml, findings.yaml)
- `standards/` — 430 Standard-Dateien in 49 Familien
- `schemas/` — naming-conventions.schema.json, milestone.schema.json, etc.
- `tools/` — Validators, Auditors, Generators
- `governance/`, `approval/`, `change-requests/` — Verfassung, Freigaben, SCR-System

### Governance Flow
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

## License

**Apache-2.0** (see [`LICENSE`](LICENSE)) — unified organizational license as of 08.09.2026.

Additional ATC usage terms (separate from Apache-2.0) are governed by the ATC-LICENSE-Familie (ATC-STD-LICENSE-001..009). Governance documents, trademarks, and organizational assets follow separate policies.

**No proprietary claims** conflict with the LICENSE file.

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
