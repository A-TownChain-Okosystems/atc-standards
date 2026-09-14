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
  applies_to: "Gesamtes KAI-OS-/GlobusOS-Oekosystem: OS, Kernel, Blockchain, VM/Runtime, AI, Standards, Infrastruktur, Repositories"
  license: "Copyright (c) 2026 Michael Wroblewski"
---

# ATC-STD-MAINT-000 — Maintenance Governance Standard (v1.0.0, DRAFT)

> **Status:** DRAFT — wartet auf §9-Freigabe (ATC-STD-000). Dach- und Meta-Standard der Familie
> ATC-STD-MAINT-000..024. Maintenance ist eine vollstaendige normative Betriebsdisziplin —
> praeventiv, korrektiv, adaptiv und sicherheitskritisch — und maschinenpruefbar fuer KAI-OS,
> GlobusOS, Blockchain, AI, Kernel und Repositories.

## Abstract

Dieser Standard definiert das Gesamtmodell der Maintenance-Disziplin: Familienstruktur, Rollen,
Lifecycle, Klassifikations-Gates, KAI-OS-Maintenance-Grenzen, Metriken, Evidence, Repository-Anforderungen
und Automatisierung. Die Spezialstandards MAINT-001..020 bauen hierauf auf; MAINT-021..024 sind reserviert.

## §1 Familienstruktur (normativ)

| ID | Standard | Zweck | Prioritaet |
|---|---|---|---|
| MAINT-000 | Maintenance Governance | Gesamtmodell, Rollen, Lifecycle, Regeln | P0 (Kern) |
| MAINT-001 | Maintenance Classification | M0-M3-Klassifizierung verbindlich | P0 (Kern) |
| MAINT-002 | Maintenance Lifecycle | Detect..Close (13 Phasen) | P0 (Kern) |
| MAINT-003 | Code Maintenance | Refactoring, Technical Debt, Deprecation | P1 |
| MAINT-004 | Dependency Maintenance | Dependencies, Lockfiles, SBOM, Updates | P0 |
| MAINT-005 | Security Maintenance | CVEs, Hardening, Secrets, Keys | P0 |
| MAINT-006 | Infrastructure Maintenance | CI/CD, Runner, Build-/Release-Infrastruktur | P1 |
| MAINT-007 | OS Maintenance | Kernel, Treiber, Runtime, Systemdienste | P0/P1 |
| MAINT-008 | Blockchain Maintenance | Node, P2P, State, Storage, Consensus | P0 |
| MAINT-009 | VM & Runtime Maintenance | ATC-VM, ABI/API, Runtime, Compatibility | P0 |
| MAINT-010 | AI Maintenance | Modelle, Registry, Inference, Evaluation | P1 |
| MAINT-011 | Repository Maintenance | Git, Branches, Issues, Actions, CODEOWNERS | P1 (SSOT: REPO-MAINT-001) |
| MAINT-012 | Standards Maintenance | Standards, Registry, Schemas, Conformance | P1 |
| MAINT-013 | Documentation Maintenance | README, Wiki, API, Architektur | P1 |
| MAINT-014 | Performance Maintenance | CPU, RAM, I/O, Netzwerk, Latenz | P1 |
| MAINT-015 | Reliability Maintenance | Monitoring, Backup, Recovery, Regression | P1 |
| MAINT-016 | Compatibility Maintenance | Backward-/Forward-Compatibility | P1 (SSOT: COMPAT-001) |
| MAINT-017 | Upgrade & Migration | Version Upgrades, Migrationen, Schemaaenderungen | P1 |
| MAINT-018 | Rollback & Recovery | Rollback, Restore, Failover | P0 |
| MAINT-019 | Maintenance Evidence | Nachweisfuehrung und Audit Evidence | P0 |
| MAINT-020 | Maintenance Automation | Automatisierte Detection, Gates, Remediation | P1 |

**Reserviert (RESERVED, Belegung nur via SCR):** MAINT-021 Emergency Maintenance · MAINT-022
End-of-Life / Retirement · MAINT-023 Vendor & Supply-Chain Maintenance · MAINT-024 Cross-Ecosystem Maintenance.

## §2 Gesamtmodell

Maintenance deckt den **gesamten Lifecycle** ab: praeventiv (geplante Pflege, Updates, Hardening),
korrektiv (Fixes nach Findings), adaptiv (Anpassung an neue Umgebungen/Requirements) und
sicherheitskritisch (M2/M3). Maintenance ist kein paralleles Chaos-System, sondern ein
spezialisierter Lifecycle **innerhalb** der bestehenden Engineering-Governance (ATC-STD-ENG-001,
GSEPF-Kette DISCOVER..MERGE).

## §3 Rollen und Separation of Duties

Rollen: Owner ( Governance-Freigabe) · Maintainer (Bereichsverantwortung je MAINT-Standard) ·
Implementer · Validator · Auditor · Release Authority.

**Separation of Duties (verbindlich fuer M2/M3):**

```
Implementer ≠ Validator ≠ Auditor
Release Authority ≠ Implementer (bei besonders kritischen Aenderungen)
```

## §4 Maintenance Lifecycle (13 Phasen, normativ — Detail: MAINT-002)

```
DETECT → ASSESS → CLASSIFY → PLAN → APPROVE → IMPLEMENT → TEST
   → VALIDATE → DEPLOY → MONITOR → EVIDENCE → CLOSE
```

Mapping auf die GSEPF-Governance-Kette: DISCOVER/UNDERSTAND≈DETECT/ASSESS, PLAN≈CLASSIFY/PLAN,
APPROVE≈HUMAN APPROVAL, IMPLEMENT/TEST≈IMPLEMENT/TEST, AUDIT≈VALIDATE, DEPLOY/REVIEW/COMMIT≈DEPLOY,
EVIDENCE/CLOSE≈DOCUMENT/MERGE. Keine Maintenance-Aufgabe schliesst ohne EVIDENCE-Phase (§8).

## §5 Klassifikations-Gates (normativ — Detail: MAINT-001)

```
Maintenance Request → Classification
   M0 → Standard Review        M1 → Operational Review
   M2 → Security Review        M3 → Emergency Governance (ATC-STD-000 §32)
   → Implementation → Testing → Independent Validation → Release → Evidence → Close
```

## §6 KAI-OS-Maintenance-Grenzen (harte Grenzen)

```
Aurora AI / GlobusOS / ShivaCore / ATC-VM / A-TownChain / ATCLang / Hardware-Firmware
```

Jede Schichtgrenze ist eine Maintenance-Grenze: Updates einer Schicht MUSSEN Kompatibilitaet
zur darunterliegenden und darueberliegenden Schicht nachweisen (Beispiel-Pruefkette:
MAINT-009). Kernel Security Boundary gebrochen = M3.

## §7 Maintenance-Metriken (verbindliche KPIs — Detail: MAINT-019/020)

MTTA · MTTD · MTTR · MTBF · Patch Latency · Dependency Freshness · Technical Debt ·
Maintenance Backlog · Rollback Success Rate · Regression Rate · Evidence Completeness ·
Recovery Readiness. Kennzahlen werden generiert (CI/Registry), nie handgezahlt.

## §8 Maintenance Evidence („No Evidence, No Trust")

Jede Maintenance-Aufgabe schliesst mit maschinenlesbarem Evidence-Record (Schema: MAINT-019):
Klassifikation, change before/after, validation (unit/integration/security/compatibility/performance),
rollback available/tested, commit/PR/test_report/audit_report, status CLOSED. Ohne vollstaendige
Evidence: kein CLOSE.

## §9 Repository-Level Requirement

Kritische Repositories (C1/C2, S3/S4): Pflichtdatei `MAINTENANCE.md` (Bereichszuordnung §1,
aktive Maintenance-Items, KPI-Links) plus `docs/maintenance/`. Kleinere Repositories:
Maintenance-Abschnitt in README.md. Verweis-Struktur wie SECURITY.md/ROADMAP.md/CHANGELOG.md.

## §10 Automatisierung (Zielbild — Detail: MAINT-020)

```
Repository-Scanner (Dependency/Vuln/SBOM/License/Static/Test/Perf/Compat)
   → Maintenance Engine → M0: Auto | M1: Review | M2/M3: Escalate
```

Bestehende Referenz-Implementierung: org-weites cargo audit (RustSec), README-/Views-Drift-Checks,
Version-Gate, Evidence-Commits.

## REQ-Matrix (normativ)

| REQ | Anforderung | Pflicht |
|---|---|---|
| REQ-MAINT-000-001 | Die Familienstruktur §1 (000-020, RESERVED 021-024) ist verbindlich; Belegung reservierter IDs nur via SCR | MUST |
| REQ-MAINT-000-002 | Separation of Duties (§3) gilt fuer alle M2/M3-Aenderungen | MUST |
| REQ-MAINT-000-003 | Der 13-Phasen-Lifecycle (§4) ist fuer alle Maintenance-Aufgaben verbindlich | MUST |
| REQ-MAINT-000-004 | Kein CLOSE ohne vollstaendigen Evidence-Record (§8, MAINT-019) | MUST |
| REQ-MAINT-000-005 | Schichtgrenzen des KAI-OS-Stacks sind Maintenance-Grenzen; Kompatibilitaetsnachweis pflichtig | MUST |
| REQ-MAINT-000-006 | KPIs (§7) werden generiert, nicht handgeschrieben | MUST |
| REQ-MAINT-000-007 | Kritische Repositories besitzen MAINTENANCE.md + docs/maintenance/ | MUST |
| REQ-MAINT-000-008 | P0-Standards der Familie (004, 005, 008, 009, 018, 019) werden vor P1-Standards implementiert | MUST |

## Implementierungsstatus (ehrlich, SCR-0080-Doktrin)

**SPECIFICATION_ONLY.** Bestehende CI-Evidence (cargo audit, Drift-Checks, Test-Suiten) ist
referenziert; Maintenance Engine, Evidence-Records und MAINTENANCE.md-Rollout sind NICHT
implementiert. CLAIMED != PASS.

## Compliance

Kernprofil: ATC-STD-000, ATC-STD-201/202/203, ATC-STD-ENG-001. Ueber- und Unterordnung:
MAINT-000 ist Dach der MAINT-Familie; REPO-MAINT-001/UPDATE-001/COMPAT-001/BUG/ERR bleiben
SSOT ihrer Durchfuehrungsdomaenen.
