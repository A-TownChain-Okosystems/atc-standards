# Changelog — atc-standards

## [1.5.0] — 2026-09-07 (Naming Convention, ATC-STD-000 §36)
- ATC-STD-000 §36 Naming Convention per Owner-Mandat verankert
  (Candidate-Revision): ID-Tabelle (ATC-STD-NNN, REQ-<DOM>-NNN, F-NNN, SCR-NNN,
  ADR-/AD-NNN, ATC-SA-NNN, TC-/TS-/GATE-NNN, ATC-SCHEMA/-PROTO/-SPEC/-DOC-NNN,
  ATC-REL-X.Y.Z), Repository-Namen (atc-<domain>-<component>; Bestand-Brand-Repos
  immutable), Dateinamen (ATC-STD-NNN.md, *.schema.json, *.integrity/review/
  compliance.yaml), ID-Immutabilitaet + Version-Pinning.
- schemas/naming-conventions.schema.json: maschinenpruefbare Norm (valides JSON).
- atc-std-validator v0.1.1: Regel S-16 Naming Compliance (Dateiname==ID,
  3-stellige Mindest-IDs, Schema-Existenz) — CI lehnt ungueltige Namen ab.
- registry/findings.yaml: Findings-Registry F-001…F-005 (kanonische IDs,
  Aliase T-F01/S-F01…/A-F01, SCR-Verweise).
- ATC-STD-203: Gate-IDs auf 3-stellige Form migriert (GATE-01…10 →
  GATE-001…010, Naming-konform).
- Approval-Paket: Snapshot + Requirement-Matrix um REQ-STD-017 erweitert
  (17/17 PASS); Validator-Re-Lauf 4/4 COMPLIANT.


## [1.4.0] — 2026-09-07 (fehlende Governance-Komponenten)
- governance/CHANGE_CONTROL.md: SCR-Verfahren operationalisiert (Lebenszyklus
  PROPOSED→REVIEW→DECIDED→IMPLEMENTED→CLOSED, SCR-Registry, Emergency-Rückkopplung).
- governance/APPROVAL_PROCESS.md: Freigabe-Ablauf CANDIDATE→STABLE mit
  Pflichten je Entscheidung (APPROVE/REQUEST CHANGES/REJECT) + Übergangs-Rollen.
- change-requests/: SCR-0001 (ID-Allokation, PENDING), SCR-0002 (OBSOLETE —
  durch Formalfassung §22 aufgelöst), SCR-0003 (§33-Integritätsumsetzung,
  PENDING, Teilumsetzung CODEOWNERS), SCR-0004 (Rollenmodell, PENDING).
- CODEOWNERS (§33-Teilumsetzung, SCR-0003).
- Root-Metadateien vervollständigt (§27-Soll-Layout): ARCHITECTURE.md
  (Repo-Architektur + Governance-Fluss), STATUS.md (Standard-/SCR-Status),
  ROADMAP.md (Q3/2026 + Ausbau je Bereich).


## [1.3.0] — 2026-09-07 (AD-034)
- ATC-STD-000 v1.0.0: Standards Governance & Specification Standard — die
  Verfassung des Standardsystems (Owner-Mandat). ID-System mit Domain-Raedern
  (000 Governance, 100 Architecture, 200 Repository & Git, 300 Development,
  400 Security, 500 Protocol, 600 Blockchain, 700 AI, 800 OS/Runtime,
  900 Infrastructure, 1000+ Applications), Lifecycle-Zustandsmaschine
  (IDEA…RETIRED, kein Springen), Metadaten-Header-Pflicht, REQ-IDs mit
  Klassifizierung (MANDATORY/RECOMMENDED/OPTIONAL/CONDITIONAL), Compliance-
  Verfahren + Level L0-L4, SemVer mit Breaking-Change-Definition, Change
  Control via SCR, Review-Chain, Evidence-Requirement, Supersession/Migration,
  Registry-Pflicht (Kein Eintrag = kein Standard), Governance-Grundsatz §21.
- Umnummerierung: ATC-STD-REPO-001/002/003 → ATC-STD-201/202/203 (v1.0.1,
  supersede-Vermerke). 14 Dateien references-umgestellt.
- registry/: standards.yaml (Standard-Registry), categories.yaml,
  versions.yaml, lifecycle.yaml; dependencies.yaml um Standard-Graph ergänzt.
- schemas/: standard/requirement/change-request.schema.yaml.
- templates/: STANDARD/REQUIREMENT/SCR-Vorlagen.
- tools/atc-std-validator v0.1.0: 15 Pruefregeln S-01…S-15 inkl. Zyklenerkennung;
  Selbsttest: ATC-STD-000, 201, 202, 203 alle COMPLIANT.
- CI erweitert: Governance-Workflow validiert jetzt auch alle vier Standards.


## [1.2.0] — 2026-09-07 (AD-032)
- Wiki-Konsolidierung II: 6 weitere Standards aus dem Docs-Hub uebernommen —
  ats/ATS_STANDARDS.md (ATS-1000…1007 ShivaOS Kernel/Stack, vollstaendige
  283-Zeilen-Fassung), atc/ATC_STANDARDS.md (ATC-0001…0008 Core-Protokolle,
  vollstaendige 233-Zeilen-Fassung mit ATC-9000-Sektion),
  atc/ATC_TOKEN_STANDARD.md (ATC-001/8300/9000/9900-Referenz),
  licensing/ATVM_LICENSE_GATE_SPEC.md, licensing/IP_LICENSE_DASHBOARD_SPEC.md,
  licensing/SMART_CONTRACT_RICHTLINIE.md (BaFin-Richtlinie)
- README-Struktur und Std.-Zaehler aktualisiert (115 Dokumente)


## [1.1.0] — 2026-09-07 (AD-031)
- ATC-STD-201 v1.0.0 FORMALE SPEZIFIKATION: MUST/SHOULD/MAY (RFC 2119),
  Compliance-Matrix R0-R4 (M-01…M-16), Validator-Regeln V-01…V-16
- ATC-STD-202 v1.0.1: Ownership-Standard, Lifecycle-Uebergangsregeln,
  Security-Klassifizierung S0-S4, zentraler Dependency Graph, Repository-Registry
- ATC-STD-203 v1.0.1: Branching, Conventional Commits, PR-Standard,
  Release-Gates GATE-01…GATE-10, Dependency Policy, Third-Party, API-Stability,
  Breaking Changes, Reproducible Builds, Artifact Management, Health Score
- registry/: repositories.yaml (23 Repos mit R- und S-Klassen), teams.yaml,
  dependencies.yaml (L0-L7-Graph)
- schemas/: 4 Metadaten-Schemas; templates/: Repository-/PR-/CI-Vorlagen
- tools/atc-repo-audit v0.1.0: lauffaehiger Validator (stdlib-only), GATE: PASS/NO-GO
- Self-Compliance: .atc/-Metadaten, CODEOWNERS, Governance-CI (Auditor prueft sich selbst)


## [1.0.0] — 2026-09-07 (AD-030)
- Initial-Bestand: 109 Standard-Dokumente aus dem Docs-Hub ueberfuehrt
  (ATC-01…99 inkl. ATC-LIC + ATC_ECOSYSTEM_STANDARDS, ATS-LIC, OVERVIEW,
  STANDARDS_REGISTRY)
- Governance-Standards ATC-STD-201/002/003 (AD-029, 07.09.2026)
- .atc-Referenzimplementierungen (registry.atc + 4 Standards-Vertraege,
  aus atc-contracts modules/atc-standards-refs)
- Repo ist SPEC-Typ R3 gemaess eigener Klassifizierung (self-compliant)
