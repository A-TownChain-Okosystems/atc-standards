---
standard:
  id: ATC-STD-MAINT-001
  title: "ATC-STD-MAINT-001 — Maintenance Discipline Standard"
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
  applies_to: "Alle Komponenten des KAI-OS-/GlobusOS-Oekosystems ueber alle Lebenszyklusphasen (SPECIFIED bis RETIRED)"
  license: "Copyright (c) 2026 Michael Wroblewski"
---

# ATC-STD-MAINT-001 — Maintenance Discipline Standard (v1.0.0, DRAFT)

> **Status:** DRAFT — wartet auf §9-Freigabe (ATC-STD-000). Maintenance ist eine eigene,
> verbindliche Betriebsdisziplin des KAI-OS-/GlobusOS-Oekosystems — nicht Nachbereitung nach Release.

## Abstract

Dieser Standard definiert Maintenance als verbindliche Betriebsdisziplin: 12 Maintenance-Bereiche,
vier Maintenance-Klassen (M0-Routine bis M3-Critical) und das Prinzip
**Maintenance-from-Development**: Jede Komponente erhaelt WAEHREND der Entwicklung
Maintenance-Metriken, Tests, Upgrade-Pfade, Rollback und Observability — nicht erst nach dem Release.

## Scope & Abgrenzung (Kollisionspruefung, Evidence-First)

- **ATC-STD-REPO-MAINT-001** (Repository-Pflegezyklus, SCR-0043): Git-/Repository-Ebene. MAINT-001
  referenziert REPO-MAINT-001 fuer Repository Maintenance — keine Doppelnormierung.
- **ATC-STD-UPDATE-001** (Change Control): Aenderungsklassen und Lifecycle von UPDATES. MAINT-001
  nutzt UPDATE-001 fuer die Durchfuehrung; MAINT-001 klassifiziert und eskaliert.
- **ATC-STD-BUG-001..004 / ERR-Familie**: Findings und Fehlerausbreitung. MAINT-001 klassifiziert
  Findings in M0-M3 und verweist fuer Lifecycle auf BUG/ERR.
- **ATC-STD-ENG-001 / ATC-STD-000 §32**: Engineering-Disziplin bzw. Emergency-Prozess fuer M3.

Kaskade: MAINT-001 klassifiziert und priorisiert; die Durchfuehrungsnormen (REPO-MAINT, UPDATE,
BUG, ERR) bleiben SSOT ihrer Domäne.

## §1 Zweck und Zielzustand

Maintenance ist eine eigene Betriebsdisziplin neben Entwicklung, Security und Governance.
Zielzustand: Keine Komponente des Oekosystems ohne zugeordnete Maintenance-Bereiche,
Klassifizierung, Metriken und Eskalationspfad.

## §2 Die 12 Maintenance-Bereiche (verbindlich)

| # | Bereich | Aufgabe | Primaere Repos (Registry-Bezug) |
|---|---|---|---|
| 1 | Code Maintenance | Refactoring, technische Schulden, Deprecations | alle; Metrik via code-quality-matrix |
| 2 | Dependency Maintenance | Updates, CVE-Patches, Lockfiles, SBOM | alle; cargo-audit-Workflows, Dependabot |
| 3 | Security Maintenance | Vulnerability Fixes, Hardening, Key Rotation | security-/S4-Repos, atc-shivacore, atc-wallet |
| 4 | Infrastructure Maintenance | CI/CD, Runner, Build-System, Releases | .github (Org-Governance), alle Workflow-Files |
| 5 | OS Maintenance | Kernel, Treiber, Runtime, Systemdienste | atc-shivacore, globus-os (ATC-DOC-ARC-GLOB-002) |
| 6 | Blockchain Maintenance | Node, P2P, State, Storage, VM-Kompatibilitaet | a-townchain, atc-algorithm, atc-vm, atc-node |
| 7 | AI Maintenance | Modelle, Registry, Inference Runtime, Evaluation | aurora-ai |
| 8 | Standards Maintenance | Standards, Schemas, Registry, Governance | atc-standards (Registry-SSOT) |
| 9 | Documentation Maintenance | README, Wiki, API-/Architekturdokumentation | a-townchain-os-docs, alle Repos (README-Drift-Check) |
| 10 | Repository Maintenance | Dateien, Branches, Issues, Actions, CODEOWNERS | alle; SSOT ATC-STD-REPO-MAINT-001 |
| 11 | Performance Maintenance | CPU, RAM, I/O, Netzwerk, Latenz | atc-vm, atc-node, atc-compute, globus-os |
| 12 | Reliability Maintenance | Monitoring, Backups, Recovery, Regressionstests | alle; Test-Suiten, Observability (lokal) |

Jedes Repo weist in seiner Registry- und Evidence-Struktur aus, welche Bereiche (1-12) auf es
zutreffen (implizit via Domain/Layer; explizit im Maintenance-Report, §7).

## §3 Maintenance-Klassen M0-M3 (verbindlich)

| Klasse | Bedeutung | Beispiele | Reaktionsmodell |
|---|---|---|---|
| M0 | Routine | Dependency Updates, Doku-Korrekturen, kleine Refactorings, CI-Optimierung | Standard-PR, normale Review-Pflicht |
| M1 | Operational | Performance, Stabilitaet, Build-/Release-Probleme, Infrastruktur | Priorisierte Behebung, Roadmap-Einordnung |
| M2 | Security | CVEs, Supply-Chain, Secrets/Keys, Sandbox-/Permission-Probleme | Security-Pfad: cargo-audit/CodeQL, ATC-STD-203, Verschwiegenheit bis Fix bei aktiv ausnutzbaren CVEs |
| M3 | Critical | Konsensfehler, Kernel-Sicherheitsproblem, VM-Inkompatibilitaet, Datenverlust, Chain-/State-Korruption | Emergency-Prozess ATC-STD-000 §32; Owner-Eskalation; Hotfix-Pfad |

Klassifizierungsregel: Im Zweifel die HOEHERE Klasse. M3-Verdacht wird SOFORT eskaliert
(kein Abwarten des naechsten Zyklus). Jedes Finding traegt seine Klasse (M0-M3) ab Anlage.

## §4 Maintenance-from-Development (Kernprinzip)

Maintenance beginnt NICHT nach dem Release. Ab Status SPECIFIED (evidence.yaml-Statusleiter,
SCR-0080) erhaelt jede Komponente verpflichtend:

1. **Maintenance-Metriken** (§5) — ab erste Implementierung messbar
2. **Tests** — Regressionsschutz vor jedem Merge (CI-Gates, ATC-STD-ENG-001)
3. **Upgrade-Pfad** — definierte Update-Strategie (UPDATE-001)
4. **Rollback** — dokumentierter und getesteter Rueckweg (A/B-Prinzip fuer OS-Komponenten)
5. **Observability** — lokale Diagnose (Logs, Metrics, Health); keine ungepruefte Telemetrie nach aussen

Regel: IMPLEMENTED ohne diese 5 Elemente gilt als maintenance-incomplete und wird im
Maintenance-Report als Gap gefuehrt.

## §5 Maintenance-Metriken & Evidence (Evidence-First)

SSOT aller Ist-Staende: `.atc/evidence/evidence.yaml` je Repo + CI-Evidence. Kennzahlen
(mindestens): Test-/Build-Gesundheit (CI gruen/rot), CVE-Latenz (M2), Dependency-Aktualitaet
(Deprecations/Outdated), Patch-Latenz je Klasse, MTTR je Bereich. Keine Handzahlen:
Metriken werden aus CI/Registry generiert (REQ-IMP-006-Prinzip).

## §6 Klassifizierungs-Workflow

Finding (Bug/Dependency/Audit) → Klassifizierung M0-M3 (§3) → Bereich (§2) → Zuweisung an
Durchfuehrungsnorm (REPO-MAINT/UPDATE/BUG/ERR) → Durchfuehrung → Evidence → Regression-Check.
M2/M3 zusaetzlich: Security-Audit-Vermerk bzw. Emergency-Record (§32).

## §7 Maintenance-Report & Automatisierung

- Referenz-Implementierung (bestehend): org-weites cargo audit (RustSec) als CI-Gate in allen
  Rust-Repos; woechentlicher Schedule; zero-tolerance fuer M3-relevante Befunde.
- Referenz-Implementierung (bestehend): README-/Views-Drift-Checks, Version-Gate, Evidence-Commits.
- Geplant (nicht implementiert): org-weiter Maintenance-Report ( aggregierte M0-M3-Kennzahlen je
  Bereich/Repo), Maintenance-Workflow mit woechentlicher Klassifizierungs-Pflicht.
- Alle Automatisierung folgt ATC-STD-AI-DEV-001..012 (Agent-Governance).

## REQ-Matrix (normativ)

| REQ | Anforderung | Pflicht |
|---|---|---|
| REQ-MAINT-001 | Jede Komponente hat zugeordnete Maintenance-Bereiche gemaess §2 | MUST |
| REQ-MAINT-002 | Jedes Finding traegt Klasse M0-M3 ab Anlage | MUST |
| REQ-MAINT-003 | M3-Verdacht wird sofort eskaliert (§32-Emergency) | MUST |
| REQ-MAINT-004 | Die 5 Maintenance-from-Development-Elemente (§4) sind ab IMPLEMENTED vorhanden | MUST |
| REQ-MAINT-005 | Maintenance-Ist-Staende folgen ausschliesslich evidence.yaml + CI (keine Handzahlen) | MUST |
| REQ-MAINT-006 | Repository Maintenance folgt ATC-STD-REPO-MAINT-001; keine Doppelnormierung | MUST |
| REQ-MAINT-007 | Sicherheitsrelevante Maintenance (M2) ist an cargo-audit/CodeQL-Gates gebunden | MUST |
| REQ-MAINT-008 | Maintenance-Reports werden generiert, nie handgeschrieben | SHOULD |

## Implementierungsstatus (ehrlich, SCR-0080-Doktrin)

**SPECIFICATION_ONLY** — dieser Standard definiert Soll-Disziplin. Bestehende CI-Evidence
(cargo audit, Drift-Checks, Test-Suiten) ist faktisch vorhanden; der Maintenance-Report und
die org-weite M0-M3-Klassifizierung sind NICHT implementiert und werden erst nach §9-Freigabe
und separatem Implementierungs-PR wirksam. CLAIMED != PASS.

## Compliance

Kernprofil: ATC-STD-000 (Verfassung), ATC-STD-201/202/203 (Repository), ATC-STD-ENG-001.
Konformitaet wird ueber den Repository-Audit und die Standards-Registry geprueft.
