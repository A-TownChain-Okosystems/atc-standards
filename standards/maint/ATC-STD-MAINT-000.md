---
standard:
  id: ATC-STD-MAINT-000
  title: "ATC-STD-MAINT-000 — Maintenance Governance Standard"
  version: "1.0.0"
  status: draft
  category: maint
  authority: A-TownChain Ecosystems
  owner: "Michael (Owner-Entwurf)"
  created: "2026-09-14"
  updated: "2026-09-14"
  normative: true
  supersedes: []
  superseded_by: null
  effective_date: "pending §9-Freigabe"
  review_date: null
  applies_to: "Gesamtes KAI-OS-/GlobusOS-Oekosystem als Querschnittsfamilie: OS, Kernel, Blockchain, VM/Runtime, AI, Standards, Infrastruktur, Repositories — alle Releases"
  license: "Copyright (c) 2026 Michael Wroblewski"
---

# ATC-STD-MAINT-000 — Maintenance Governance Standard (v1.0.0, DRAFT)

> **Status:** DRAFT — wartet auf §9-Freigabe (ATC-STD-000). Dach- und Meta-Standard der
> Querschnittsfamilie ATC-STD-MAINT-000..024.
>
> **Kern-Governance-Regel:** Maintenance ist kein Post-Release-Prozess.
> **Maintenance Capability ist eine Release-Voraussetzung.**

## Abstract

Dieser Standard definiert das Gesamtmodell der Maintenance-Disziplin als Querschnittsfamilie fuer
das gesamte A-TownChain-Oekosystem: Gruppenstruktur, Rollen, Lifecycle, Klassifikations-Gates,
**Maintenance Readiness Gate**, KAI-OS-Maintenance-Grenzen, Metriken, Evidence, Repository-Anforderungen
und die Zielarchitektur (ATC-STD-MAINT-* → GSEPF → Maintenance Engine → Evidence → Verified State).
Die Spezialstandards MAINT-001..024 bauen hierauf auf; ab MAINT-025 sind IDs frei (via SCR).

## §1 Familienstruktur mit Gruppen (normativ)

| Gruppe | ID | Standard | Zweck | Prioritaet |
|---|---|---|---|---|
| Governance & Classification | MAINT-000 | Maintenance Governance | Gesamtmodell, Rollen, Lifecycle, Regeln, Readiness Gate | P0 |
| Governance & Classification | MAINT-001 | Classification | M0-M3 verbindlich | P0 |
| Governance & Classification | MAINT-002 | Lifecycle | Detect..Close (13 Phasen) | P0 |
| Engineering | MAINT-003 | Code | Refactoring, Technical Debt, Deprecation | P1 |
| Engineering | MAINT-004 | Dependency | Dependencies, Lockfiles, SBOM, Updates | P0 |
| Engineering | MAINT-006 | Infrastructure | CI/CD, Runner, Build-/Release-Infrastruktur | P1 |
| Engineering | MAINT-014 | Performance | CPU, RAM, I/O, Netzwerk, Latenz | P1 |
| Security | MAINT-005 | Security | CVEs, Hardening, Secrets, Keys | P0 |
| Security | MAINT-018 | Rollback & Recovery | Rollback, Restore, Failover | P0 |
| Security | MAINT-021 | Emergency | M3-Emergency-Pfad, Incident Records | P1 |
| Platform | MAINT-007 | OS | Kernel, Treiber, Runtime, Systemdienste | P0 |
| Platform | MAINT-008 | Blockchain | Node, P2P, State, Storage, Consensus | P0 |
| Platform | MAINT-009 | VM & Runtime | ATC-VM, ABI/API, 7-Stufen-Pruefkette | P0 |
| Platform | MAINT-010 | AI | Modelle, Registry, Inference, Evaluation | P1 |
| Governance Assets | MAINT-011 | Repository | Bindung an REPO-MAINT-001-SSOT | P1 |
| Governance Assets | MAINT-012 | Standards | Standards, Registry, Schemas, Conformance | P1 |
| Governance Assets | MAINT-013 | Documentation | README, Wiki, API, Architektur | P2 |
| Lifecycle | MAINT-016 | Compatibility | Backward-/Forward-Compatibility | P1 |
| Lifecycle | MAINT-017 | Upgrade & Migration | Upgrades, Migrationen, Schemaaenderungen | P0 |
| Lifecycle | MAINT-022 | End-of-Life / Retirement | Deprecation → Sunset → Retirement | P2 |
| Assurance | MAINT-015 | Reliability | Monitoring, Backup, Recovery, Regression | P0 |
| Assurance | MAINT-019 | Evidence | Nachweisfuehrung, Record-Schema | P0 |
| Assurance | MAINT-020 | Automation | Scanner, Gates, Maintenance Engine | P1 |
| Supply & Ecosystem | MAINT-023 | Vendor & Supply-Chain | Vendor-Abhaengigkeiten, Provenance, Third-Party-Risiken | P2 |
| Supply & Ecosystem | MAINT-024 | Cross-Ecosystem | Multi-Repo-/Schicht-Koordination | P2 |

**MAINT-021..024 sind fest eingeplante Familienmitglieder** (nicht nur reserviert). Ab MAINT-025
sind IDs frei (Vergabe nur via SCR).

**Prioritaeten KAI-OS:** P0 (unverzichtbar): 000, 001, 002, 004, 005, 007, 008, 009, 015, 017,
018, 019. P1 (produktionsrelevant): 003, 006, 010, 011, 012, 014, 016, 020, 021. P2 (Ecosystem
Maturity): 013, 022, 023, 024.

## §2 Zielarchitektur (normativ)

```
ATC Standards
      │
      ▼
     GSEPF
      │
      ├── Development Governance
      ├── Security Governance
      ├── Release Governance
      └── Maintenance Governance
                         │
                         ▼
                Maintenance Engine
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
             M0         M1        M2/M3
              │          │          │
              ▼          ▼          ▼
           Automate    Review     Escalate
                         │
                         ▼
                    Evidence
                         │
                         ▼
                  Verified State
```

ATC-STD-MAINT-* definiert die normative Ebene, GSEPF setzt sie als kontrollierten Prozess um,
CI/CD bzw. Maintenance Automation (MAINT-020) erzeugen die tatsaechlichen Evidence-Records
(MAINT-019). Dadurch ist Maintenance ein Bestandteil der Systemintegritaet — nicht bloss ein
organisatorisches To-do.

## §3 Maintenance Readiness Gate (normativ — Release-Voraussetzung)

```
RELEASE REQUEST
       │
       ▼
MAINTENANCE READY?
       │
   ┌───┴───┐
  NO      YES
   │       │
   ▼       ▼
 BLOCK   RELEASE
```

**Mindestanforderungen (alle required):**

```yaml
maintenance_readiness:
  maintenance_owner: required
  maintenance_documentation: required
  dependency_inventory: required
  security_process: required
  test_suite: required
  rollback_strategy: required
  compatibility_strategy: required
  monitoring: required
  evidence_collection: required
  lifecycle_status: required
```

**Zusaetzlich fuer M2/M3-Releases (alle required):**

```yaml
critical_maintenance:
  independent_validation: required
  security_review: required
  rollback_test: required
  incident_record: required
  audit_evidence: required
```

Regel: Ein Release ohne vollstaendige maintenance_readiness wird BLOCKIERT. Der Gate ist
Teil der Release Governance (GSEPF) und maschinenpruefbar (MAINT-020).

## §4 Gesamtmodell

Maintenance deckt den **gesamten Lifecycle** ab: praeventiv, korrektiv, adaptiv und
sicherheitskritisch. Maintenance ist kein paralleles Chaos-System, sondern ein spezialisierter
Lifecycle **innerhalb** der bestehenden Engineering-Governance (ATC-STD-ENG-001, GSEPF-Kette).

## §5 Rollen und Separation of Duties

Rollen: Owner (Governance-Freigabe) · Maintainer (Bereichsverantwortung je MAINT-Standard) ·
Implementer · Validator · Auditor · Release Authority.

**Separation of Duties (verbindlich fuer M2/M3):**

```
Implementer ≠ Validator ≠ Auditor
Release Authority ≠ Implementer (bei besonders kritischen Aenderungen)
```

## §6 Maintenance Lifecycle (13 Phasen — Detail: MAINT-002)

```
DETECT → ASSESS → CLASSIFY → PLAN → APPROVE → IMPLEMENT → TEST
   → VALIDATE → DEPLOY → MONITOR → EVIDENCE → CLOSE
```

## §7 Klassifikations-Gates (Detail: MAINT-001)

```
Maintenance Request → Classification
   M0 → Standard Review        M1 → Operational Review
   M2 → Security Review        M3 → Emergency Governance (ATC-STD-000 §32)
```

## §8 KAI-OS-Maintenance-Grenzen (harte Grenzen)

```
Aurora AI / GlobusOS / ShivaCore / ATC-VM / A-TownChain / ATCLang / Hardware-Firmware
```

Jede Schichtgrenze ist eine Maintenance-Grenze: Updates einer Schicht MUSSEN Kompatibilitaet
zur darunterliegenden und darueberliegenden Schicht nachweisen (Beispiel-Pruefkette: MAINT-009).
Kernel Security Boundary gebrochen = M3.

## §9 Maintenance-Metriken (verbindliche KPIs)

MTTA · MTTD · MTTR · MTBF · Patch Latency · Dependency Freshness · Technical Debt ·
Maintenance Backlog · Rollback Success Rate · Regression Rate · Evidence Completeness ·
Recovery Readiness. Kennzahlen werden generiert (CI/Registry), nie handgezahlt.

## §10 Maintenance Evidence („No Evidence, No Trust")

Jede Maintenance-Aufgabe schliesst mit maschinenlesbarem Evidence-Record (Schema: MAINT-019).
Ohne vollstaendige Evidence: kein CLOSE, kein Verified State.

## §11 Repository-Level Requirement

Kritische Repositories (C1/C2, S3/S4): Pflichtdatei `MAINTENANCE.md` (Bereichs- und
Readiness-Angaben, aktive Maintenance-Items, KPI-Links) plus `docs/maintenance/`.
Kleinere Repositories: Maintenance-Abschnitt in README.md.

## §12 Automatisierung (Zielbild — Detail: MAINT-020)

```
Repository-Scanner (Dependency/Vuln/SBOM/License/Static/Test/Perf/Compat)
   → Maintenance Engine → M0: Auto | M1: Review | M2/M3: Escalate
```

Bestehende Referenz-Implementierung: org-weites cargo audit (RustSec), README-/Views-Drift-Checks,
Version-Gate, Evidence-Commits, Cross-Registry-Check R1-R15.

## REQ-Matrix (normativ)

| REQ | Anforderung | Pflicht |
|---|---|---|
| REQ-MAINT-000-001 | Die Gruppen-/Familienstruktur §1 (000-024 fest, ab 025 frei via SCR) ist verbindlich | MUST |
| REQ-MAINT-000-002 | Separation of Duties (§5) gilt fuer alle M2/M3-Aenderungen | MUST |
| REQ-MAINT-000-003 | Der 13-Phasen-Lifecycle (§6) ist fuer alle Maintenance-Aufgaben verbindlich | MUST |
| REQ-MAINT-000-004 | Kein CLOSE ohne vollstaendigen Evidence-Record (§10, MAINT-019) | MUST |
| REQ-MAINT-000-005 | Maintenance Capability ist Release-Voraussetzung: kein Release ohne vollstaendige maintenance_readiness (§3) | MUST |
| REQ-MAINT-000-006 | M2/M3-Releases erfordern zusaetzlich vollstaendige critical_maintenance (§3) | MUST |
| REQ-MAINT-000-007 | Schichtgrenzen des KAI-OS-Stacks sind Maintenance-Grenzen; Kompatibilitaetsnachweis pflichtig | MUST |
| REQ-MAINT-000-008 | KPIs (§9) werden generiert, nicht handgeschrieben | MUST |
| REQ-MAINT-000-009 | Kritische Repositories besitzen MAINTENANCE.md + docs/maintenance/ | MUST |
| REQ-MAINT-000-010 | P0-Standards (§1) werden vor P1/P2 implementiert | MUST |
| REQ-MAINT-000-011 | Zielarchitektur (§2): Maintenance ist Bestandteil der Systemintegritaet, kein organisatorisches To-do | MUST |

## Implementierungsstatus (ehrlich, SCR-0080-Doktrin)

**SPECIFICATION_ONLY.** Bestehende CI-Evidence (cargo audit, Drift-Checks, Test-Suiten,
Cross-Registry-Check) ist referenziert; Maintenance Engine, Readiness-Gate-Automatisierung,
Evidence-Records und MAINTENANCE.md-Rollout sind NICHT implementiert. CLAIMED != PASS.

## Compliance

Kernprofil: ATC-STD-000, ATC-STD-201/202/203, ATC-STD-ENG-001. Ueber-/Unterordnung: MAINT-000 ist
Dach der Querschnittsfamilie; REPO-MAINT-001/UPDATE-001/COMPAT-001/BUG/ERR bleiben SSOT ihrer
Durchfuehrungsdomaenen.
