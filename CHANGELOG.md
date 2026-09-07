# Changelog

## [1.4.0] - 2026-09-07

### Added

- ATC Smart Contract Standards Framework: ATC-STD-SC-001..020 v1.0.0
  CANDIDATE (Owner-Entwurf Michael) — Kategorien SC-CORE..SC-SYSTEM,
  SSOT-Kette, Compliance-Gates SC-G0..G13 (kein Gate — kein Mainnet),
  REQ-SC-001..058
- Contract Registry (contracts/registry/{contracts,deployments,versions}.yaml
  + 9 Kategorie-Verzeichnisse), Seed: ATC-SC-TOKEN-001..003 (ATC-001/8300/9900)
- tools/atc-sc-validator/check_contracts.py (Registry-Gate, CONFORM)
- Geplant (ROADMAP): Deep-Standards ATC-STD-SC-BRIDGE-001, ATC-STD-FEE-001

## [1.3.0] - 2026-09-07

### Added

- ATC-STD-MD-001 v1.0.0 CANDIDATE (Owner-Entwurf): ATC Markdown &
  Documentation Standard — REQ-MD-001..016, MD-Compliance-Validator
  (tools/atc-md-validator/check_md.py)
- ATC-STD-README-001 v1.0.0 APPROVED (Owner-Freigabe 20:36)
- GOVERNANCE.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md nach MD-001

## 2026-09-07 — ATC-STD-README-001 APPROVED (Owner-Freigabe „Freigeben", 20:36 UTC+2)
- CANDIDATE → APPROVED per ATC-STD-000 §9; normativ in Kraft, Immutabilität
  per §30.
- Registry: **82 Standards, 82 APPROVED, 0 offen.**
- Approval-Dokument: approval/APPROVAL-DECISION-2026-09-07-README-001.md.
- Übergangsfrist bis 07.10.2026: README-Konformitäts-Rollout auf alle 26
  Repos (Todo #116, Rollout-Komponente offen).

## 2026-09-07 — ATC-STD-README-001 v1.0.0 CANDIDATE (Owner-Entwurf): README als Einstiegsschnittstelle
- **Neue Standard-Familie:** ATC-STD-README-001 (CANDIDATE, §9-Freigabe
  ausstehend, Todo #116) — README = standardisierte Einstiegsschnittstelle
  jedes Repos: Pflichtstruktur (21 Sektionen), Status-Enum (9 Werte),
  Header-Identifikation, Architektur-Pflicht, maschinenlesbarer
  Metadaten-Block, Dokumentationshierarchie (README=Einstiegspunkt),
  kanonische Roadmap-Verlinkung, REQ-README-001..015.
- **Quality Gates README-01..13** mit neuem Validator
  tools/atc-readme-validator/check_readme.py (Gate-13 = automatisierter
  Struktur-Abgleich README vs. Repository-Zustand).
- **Selbstkompliance:** atc-standards-README komplett neu als konforme
  Referenzimplementierung (13/13 CONFORM) — alte README fiel durch alle
  Gates.
- **Registry:** 82 Standards (81 APPROVED + 1 CANDIDATE); Kategorie readme;
  Schema um readmeStandardId/readmeStandardDoc/readmeRequirementId
  erweitert; dependencies: 000/201/202/ENT-009.
- **Vollmandat dynamisiert:** AGENT_MANIFEST/agent.yaml auf "ALLE
  Registry-Standards" (aktuell 82) umgestellt.

## 2026-09-07 — Agent-Manifest: Voll-Compliance-Mandat (alle 81 Standards)
- **AGENT_MANIFEST.md:** Neues verbindliches Mandat — der Agent MUSS saemtliche
  Standards einhalten UND umsetzen; dynamische Bindung an die Registry (SSOT);
  Konfliktregel nach Verfassung §9; Nachweispflicht via AUD-Records/Evidenz.
- **.github/ai/agent.yaml:** required_standards von 6 auf ALLE 81
  Registry-Standards erweitert.
- **AGENTS.md:** Vollmandat statt "Auszug".
- **CI-Enforcement:** Neues Gate check_agent_manifest.py (A1: Vollstaendigkeit
  gegen Registry, A2: Mandat-Klauseln, A3: AGENTS.md, A4: AUD-Records) als
  Schritt in naming-governance.yml.
- **Finding F-018** registriert und RESOLVED.

## 2026-09-07 — Self-Compliance-Audit: atc-standards implementiert jetzt seine eigenen Standards
- **Befund:** Die eigene CI pruefte nur 19/81 Standards (Coverage-Regex),
  die Mutationssuite war von Live-Freigaben abhaengig (9/12), S-09 kannte
  keine deutschen RFC-2119-Keywords, 62 Standards verstiessen gegen die
  §9-Pflichtstruktur (Abstract/Scope), .github/ai/ fehlte komplett,
  STATUS/ROADMAP waren stale.
- **Remediation:** Validator (Coverage 81/81, S-09, S-16 REQ-Union,
  hsv-Regex, S-19 WARN), Mutationssuite synthetisch (12/12), 48 Abstract +
  49 Scope nachgeruestet, categories/Schema erweitert, .github/ai/-Rollout
  (Repo-Manifest AAS-025, AGENTS.md, AUD-001..005 rueckwirkend),
  STATUS/ROADMAP synchronisiert.
- **Endstand: 81/81 COMPLIANT · Mutationssuite 12/12 · Repo-Audit R3
  100/100 GATE PASS.**
- Findings F-012..F-016 RESOLVED; F-017 (REQ-ID-Rollout) OPEN mit SCR-0007
  (Owner-Entscheidung ausstehend, Frist 07.10.2026).
- Bericht: docs/SELF_COMPLIANCE_2026-09-07.md.

## 2026-09-07 — Voll-Audit + Sammelfreigabe: ALLE 81 Standards APPROVED
- **Voll-Audit (Owner-Auftrag) über 81 Standards:** Schema-Lücke ZKP
  (zkpStandardId ergänzt), 28 fehlende Frontmatter-Fences ergänzt,
  3 Tippfehler korrigiert, AAS-008 §3 ersetzt, 49 fehlende
  Dependency-Kanten ergänzt (4 zyklische bewusst ausgenommen) —
  Graph jetzt 81 Knoten, azyklisch; 81/81 Frontmatter/Registry/Versions
  synchron. Bericht: docs/AUDIT_STANDARDS_2026-09-07.md.
- **Owner-Sammelfreigabe „Alles freigeben" (20:20 UTC+2):** ATC-AAS-001..025
  und ATC-ENT-001..015 CANDIDATE -> APPROVED. 81/81 Standards normativ
  in Kraft und eingefroren (§30).
- **SCR-0006 ACCEPTED:** AI-DEV-007 v1.0.1 — Commit-Typ-Set um
  security/build/ci erweitert (nicht-breaking, Vereinheitlichung mit
  AAS-015).
- Entscheidungsdokument:
  approval/APPROVAL-DECISION-2026-09-07-AAS-ENT-AUDIT.md.

## 2026-09-07 — NEU: ATC Enterprise Standards Layer (ATC-ENT) — 15 Standards als CANDIDATE
- **Neuer Layer über den technischen Familien** (Owner-Entwurf Michael
  Wroblewski, 07.09.2026, 20:11 UTC+2): ATC-ENT-001…015 in
  standards/enterprise/, alle v1.0.0 CANDIDATE. Position: zwischen
  Verfassung ATC-STD-000 (Meta-Ebene) und den technischen Familien
  (AI-DEV, AAS, 201-204, BUG, NET, ZKP, 100/300).
- **Unternehmens-Governance:** 001 Governance/Dokumente, 002 Rollen
  (ROLE-XXX, 11 kanonische Rollen, KI-Agenten als Mitarbeiter), 003
  Entscheidungsmanagement (DEC-NNNN, Kernregel), 004 Delegation,
  005 Richtlinien (POL-NNNN), 006 Interessenkonflikte, 007 Eskalation
  (ESC-NNNN, E1-E4), 008 Organisationsstruktur (13 Einheiten,
  UNIT-NNNN), 009 Repository Governance (REPO-NNNN), 010 Change
  Management (Pipeline), 011 Risiko-Management (RISK-NNNN),
  012 Wissensmanagement & Consistency Gate, 013 KPI (DORA/Security/AI/
  Blockchain), 014 Audit & Nachvollziehbarkeit (audit_event), 015
  Definition of Done.
- **Aufbau ohne Duplikate:** Rollen bauen auf Verfassung §14.1 auf;
  Agenten-Governance bleibt bei AI-DEV/AAS (statt parallelem ATC-AI-001);
  Audit vereint AI-DEV-009 + AAS-018; SCR bleibt Änderungsspur für
  Standards (ENT-010 deckt Org/Architektur/Policies ab); AD-Mandate
  (AD-016..046) als DEC-Records grandfathered.
- **Schema-Erweiterung:** entStandardId, roleId, decisionId, riskId,
  repoId, orgUnitId, escalationId.
- **Templates:** role.template.yaml, decision-record.template.md,
  risk.template.yaml.
- Registry: 81 Standards (41 approved + 50 candidate), Graph azyklisch
  (58 Knoten deklariert), Versionshistorie 81/81.

## 2026-09-07 — NEU: Standardblock ATC-AAS (AI Agent Standards) — 25 Standards als CANDIDATE
- **Neuer Standardbereich ATC-AAS** (Owner-Entwurf Michael Wroblewski,
  07.09.2026, Builder-Chat): 25 Agenten-Standards ATC-AAS-001…025 in
  standards/aas/, alle v1.0.0 CANDIDATE (Owner-§9-Freigabe ausstehend).
- **P0 (12):** 001 Identity, 003 Permission, 004 Scope, 005 Discovery,
  007 Task, 008 Workflow, 010 Evidence, 011 Verification, 014 Security,
  016 PR, 017 Human Approval, 018 Audit Trail.
- **P1 (8):** 006 Context, 009 Change, 013 Conflict Resolution, 019 Handoff,
  020 Failure, 022 Versioning, 024 A2A Protocol, 025 Repository Manifest.
- **P2 (2):** 021 Quality/KPIs, 023 Roles; (002 Capability als P0-Zusatz).
- **Aufbau ohne Duplikate:** Jeder AAS-Standard erweitert/konkretisiert die
  freigegebenen AI-DEV-Standards 001…012 per Cross-Referenz; neu sind
  Scope, Context-Priorität, Halluzinations-Taxonomie (FACT/EVIDENCE/
  INFERENCE/ASSUMPTION/UNKNOWN), Conflict Resolution, Failure (max_attempts),
  KPIs, Agent-Versioning, Rollen, A2A-Protokoll, Repo-Manifest.
- **Harmonisierungen:** Ablageort .github/ai/ statt .agent/ (AI-DEV-001 §6
  approved); Commit-Typ-Erweiterung (security/build/ci) via SCR-0006
  (AI-DEV-007 unveränderlich, §30).
- Schema: aasStandardId (^ATC-AAS-NNN) + a2aMessageId (^A2A-NNNNNN)
  ergänzt; Templates: templates/aas/repository-manifest.template.yaml.
- Registry: 66 Standards (41 approved + 25 candidate), Graph azyklisch
  (43 Knoten deklariert), Versionshistorie 66/66.

## 2026-09-07 — Owner-Sammelfreigabe: ALLE restlichen offenen Punkte APPROVED — 41/41 Standards normativ
- **27 bestehende Standards freigegeben** (draft/proposed/candidate →
  APPROVED): ATC-STD-201/202/203, BUG-001..004, NET-001..008, ATC-STD-100,
  ATC-STD-300, ZKP-001..010.
- **AI-DEV-Familie vervollständigt**: 002 Capabilities & Permissions, 003
  Repository Discovery, 005 Finding & Evidence, 006 Decision & Action, 008
  Testing & Validation, 010 Documentation Synchronization, 011 Human
  Approval & Escalation, 012 Multi-Agent Coordination — je v1.0.0, sofort
  APPROVED. Familie 001..012 vollständig.
- **SCR finalisiert:** SCR-0001 ACCEPTED (§37 v1.2.0), SCR-0004 CLOSED (§14.1).
- **Findings:** F-001 und F-004 RESOLVED; F-009/F-010 bleiben als dokumentierte
  Owner-Aktionen (workflow-Scope-Token).
- **Endstand: 41 Standards, alle APPROVED**, Versionshistorie 41/41,
  Standards-Graph azyklisch. Entscheidungsdokument:
  approval/APPROVAL-DECISION-2026-09-07-ALL-REMAINING.md.
- Übergangsfristen bis 07.10.2026 unverändert (Commit-Trailer, Agent-Manifeste
  + AGENTS.md, Interface-Test-Suiten IFC-0001..0010).

## 2026-09-07 — Owner-Freigabe „Alles freigeben": ATC-STD-000 v1.2.0 APPROVED — Governance-Freeze abgeschlossen
- ATC-STD-000 v1.2.0 (§37 ID-Allokation, §38 Security) CANDIDATE →
  APPROVED; v1.2.0 ist die gültige Verfassungsfassung.
- SCR-0003 Option B endgültig dokumentiert (physisch verifiziert: Protected
  main aktiv, Agent-Push als Owner-Ausnahme).
- V-16-WARN (Conventional Commits 75 %) dispositionsakzeptiert; Types ab
  sofort normativ über AI-DEV-007 §1.
- Entscheidungsdokument: approval/APPROVAL-DECISION-2026-09-07-000-v1.2.0.md.
- Verbleibende operative Auflagen (bis 07.10.2026): Interface-Test-Suiten,
  Commit-Trailer-Rollout, Agent-Manifeste + AGENTS.md in R2+-Repos.

## 2026-09-07 — Owner-Freigabe: ATC-STD-204 + AI-DEV-001/004/007/009 APPROVED
- Owner-Direktfreigabe (Builder-Chat 19:53 UTC+2; dokumentiert in
  approval/APPROVAL-DECISION-2026-09-07-204-AI-DEV.md): 5 Standards
  PROPOSED/CANDIDATE → APPROVED (ATC-STD-000 §9), normativ in Kraft.
- Fristen ab 07.09.2026: ATC-STD-204 Interface-Test-Suiten (IFC-0001..0010
  seed → active) bis 07.10.2026; AGENT_PROTOCOL.md-Migration auf
  Commit-Trailer bis 07.10.2026; Agent-Manifeste + AGENTS.md in R2+-Repos
  binnen 30 Tagen.
- Immutabilität ab sofort (§30); Änderungen nur noch via SCR.

## 2026-09-07 — ATC-STD-AI-DEV-004/007/009 (erste Folge-Standards der AI-DEV-Familie)
- **AI-DEV-004 AI Task Management** (candidate): Task-Record
  `.github/ai/tasks/ATC-TASK-NNNN.yaml`, Lifecycle CREATED→COMPLETED mit
  lückenloser history, ID-Allokation (nie wiederverwendet), Traceability
  Issue/Branch/Commits/PR/CI/Tests/AUD, Handover-Regeln, COMPLETED nur mit
  Audit-Record.
- **AI-DEV-007 AI Git Commit & PR** (candidate): Commit-Format mit normativem
  Trailer-Block, Branch-Namen ai/ATC-TASK-NNNN, PR-Pflichtstruktur (8
  Abschnitte), Label-Set, Merge-Gate mit CI-Run-Referenz und
  Human-Review-Bindung, [agent:]-Tag-Übergangsregel 30 Tage.
- **AI-DEV-009 AI Audit Trail** (candidate): Audit-Record AUD-NNN in
  `.github/ai/audit/` (Append-Only, Korrektur nur per corrects:-Folgercord),
  Konsistenzmatrix (Abweichung → BLOCKED), unbegrenzte Aufbewahrung.
- Neue Templates: templates/ai/task.template.yaml,
  templates/ai/audit-record.template.yaml.
- AI-DEV-001 Familientabelle: 004/007/009 planned → candidate.

## 2026-09-07 — ATC-STD-AI-DEV-001 (AI Agent Identity & Workflow, Owner-Entwurf)
- Neuer Standard (candidate): KI-Agenten sind keine unsichtbaren Bots —
  jede Aktion folgt Identität → Kontext → Fundstelle → Entscheidung →
  nächste Aktion → Ergebnis. Agent-Identität (ATC-AI-{ROLE}-NNN, getrennt
  vom GitHub-Bot-Account), Agent-Manifest .github/ai/ (agent/capabilities/
  permissions/workflow/memory-policy), Repository-Discovery-Protocol,
  AGENTS.md je Repo (ab R2), Task-IDs ATC-TASK-NNN, State Machine,
  Evidence-Pflicht, Finding→Action-Kette (F-NNN/ACT-NNN), OBSERVATION-vs-
  DECISION-Grundsatz, Assumption-Register ASSUMPTION-ANNN, Commit-Trailer
  (Agent-ID/Task-ID/Finding-ID/Action-ID), Completion-Gate mit
  Cross-Repository-Konsistenzprüfung, Agent Audit Record.
- Familien-Dach für ATC-STD-AI-DEV-002…012 (planned): Capabilities,
  Discovery, Task Management, Finding & Evidence, Decision & Action,
  Commit/PR, Testing, Audit Trail, Doc-Sync, Human Approval,
  Multi-Agent Coordination.
- Schema-Erweiterung (ATC-STD-000 §7): aiDevStandardId, aiAgentId,
  aiTaskId, aiActionId, aiAssumptionId + aiDevStandardDoc (Datei-Muster).
- Templates: templates/ai/agent-manifest.template.yaml,
  templates/ai/AGENTS.template.md.
- Übergangsregel: [agent: …]-Tag aus AGENT_PROTOCOL.md bleibt 30 Tage
  nach APPROVED gültig, danach Commit-Trailer.

## 2026-09-07 — ATC-STD-204 (Dependency & Interface Standard, F-001/F-002/F-005)
- Neuer Standard (proposed, normativ mit APPROVED): Dependency-Deklaration
  (registry/dependencies.yaml als SSOT, Zyklusfreiheit, SCR-Pflicht),
  Interface-Registry registry/interfaces.yaml (10 Seed-Interfaces IFC-0001..0010,
  Pflichtfelder inkl. api_version/compatibility/security_level/test),
  dreifache Versionierung Protocol/Specification/Implementation,
  SemVer-Kompatibilitaet, Integration-Test-Pflicht je Kante,
  Conformance-Level R0-R4, Validator-Checks DEP-001..003.
- Setzt Findings der externen Bewertung (07.09.2026) um: F-001 (P0),
  F-002 (P0), F-005 (P1).

## 2026-09-07 — ATC-STD-NET-001…008 (Netzwerk-Umgebungen & Promotion, Owner-Mandat AD-041)
- 8 neue Standards (candidate, normativ per Owner-Mandat): NET-001 Devnet,
  NET-002 Testnet (24-Gebiete-Testpflicht), NET-003 Mainnet (658467
  permanent, 7 Verbote), NET-004 Promotion-Pipeline (GATE-011/012/013,
  EIN Code DREI Konfigurationen), NET-005 Genesis, NET-006 Upgrade,
  NET-007 Security-Matrix, NET-008 Recovery.
- Neue ID-Muster: ATC-STD-NET-NNN (+ Dateinamen), REQ-Domain NET.
- schemas/network-environment.schema.json (Tier-Zwangsbedingungen per
  if/then), registry/networks.yaml (Devnet 658469, Testnet 658468,
  Mainnet 658467).

## 2026-09-07 — ATC-STD-BUG-001…004 (Bug- & Konsistenz-Lebenszyklus, Owner-Mandat AD-040)
- 4 neue Standards (candidate, normativ per Owner-Mandat): BUG-001 Finding
  (Pflichtprozess + Pflichtfelder + Severity S0-S4), BUG-002 Documentation
  (F-NNN-Pflichtstruktur, Nachvollziehbarkeit), BUG-003 Fix-Lifecycle
  (12 Stufen + SCR-Pflicht + DoD), BUG-004 Repository Sync & Merge Gate
  (Konsistenzmatrix, SYNC-Statusmodell, Gate-Regel).
- Neue ID-Formen (Schema-Erweiterung §7): ATC-STD-BUG-NNN, TEST-NNN,
  SYNC-NNN, AUD-NNN + Dateinamenmuster ATC-STD-BUG-NNN.md.
- templates/finding.template.md; Registry- und STATUS-Eintraege.

## Changelog — atc-standards (historische Eintraege)

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
