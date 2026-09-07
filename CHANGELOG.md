# Changelog

## [1.4.36] - 2026-09-08

### Added

- **ATC-PROTO-P2P-001 v1.0.0 DRAFT** (SCR-0027) — erste formale Protokoll-Spezifikation
  unter dem Dachstandard ATC-STD-PROTOCOL-001, Musterbildner für alle 26 Familien:
  - 22 REQ-P2P instanzieren alle 19 Dachstandard-Paragraphen
  - v1.0.0-Envelope (9+1 Pflichtfelder inkl. Chain-ID 658467), kanonische Serialisierung
    mit Signatur-Domain-Separation (ATC-P2P-v1)
  - 13 Message-Types (9 aus ShivaCore K14 Ist + 4 NEU für den 6-Phasen-Handshake nach
    PROTOCOL-001 §8: CapabilityExchange, AuthChallenge, AuthResponse, KeyExchange)
  - Peer-Lifecycle (Disconnected/Connecting/Connected + NEU Banned/Verified),
    Discovery mit Eclipse-/Subnetz-Regel, Gossip mit Seen-Set-Deduplizierung
  - DID-basierte Authentication (K6/K6b Ed25519) + Capability-Authorization
  - Threat Model mit ehrlichem Implementierungs-Status je der 12 Pflichtprüfungen
  - Fehlerkatalog ATC-PROTO-P2P-001..019 (K14-Errors vollständig gemappt)
  - Timeout-/Rate-Limiting-Defaults, Replay-Schutz (nonce/message_id/timestamp-window),
    Observability- und Audit-Kopplung, 8 Kompatibilitätsarten, Upgrade-Kette mit
    Human Gate, Deprecation v0.9 → v1.1.0 (Abschaltung v2.0.0)
  - Ehrlichkeitsregel (REQ-PROTO-021): K14-Ist-Zustand als v0.9-Kompatibilitätsmodus
    dokumentiert; Registry-Status bleibt `draft` bis zur verifizierten v1.0.0-Implementierung
- **protocols/p2p/** als Ablageort für Protokoll-Spezifikationen (getrennt von
  standards/ — Schichtentrennung Governance vs. Spezifikation)
- **Generator:** SPEC_OVERRIDES-Hook in gen_protocol_registry.py — Registry-Eintrag
  referenziert jetzt die formale Spezifikation (SSOT, keine Hand-Edits)


## [1.4.35] - 2026-09-08

### Added

- **AUD-2026-0003 Selbst-Audit** (SCR-0026): Prüfung, ob atc-standards seine eigenen
  Standards einhält — 16 Prüfbereiche / 54 von 64 Checks bewertet (10 SKIP mit
  Begründung), Health Score IST 86/100 → **B**, nach den Fixes dieses Releases
  projiziert 91/100 → **A**. Bericht: docs/AUD-2026-0003_SELF_AUDIT.md.
- **Validator NEU S-25 (Frontmatter-Strict-YAML)**: Frontmatter jeder Standard-Datei
  wird je CI-Lauf mit strictem YAML-Parsing geprüft — schließt die Erkennungslücke,
  durch die ein YAML-Bruch in ATC-STD-CHANGE-001 unentdeckt blieb.
- **requirements.txt (pyyaml>=6.0)**: Laufzeit-Abhängigkeit der Validator-Suite erstmals
  deklariert. Die Workflow-Härtung (pip install im naming-governance-Workflow) liegt
  bereit, ist aber vom Agent-Token nicht pushbar (GH013, kein workflow-Scope) — als
  Owner-Aktion via Issue dokumentiert. CI läuft bis dahin im geprüften Fallback-Modus
  (ALL COMPLIANT ohne PyYAML, lokal verifiziert).

### Fixed

- **CI rot auf main** (F-037): naming-governance-Workflow schlug seit 22:19 in 4+
  konsekutiven Runs fehl — Ursachenkette: fehlendes PyYAML auf dem Runner (F-035,
  undeklarierte Abhängigkeit) + TypeError im S-20-Fallback (F-033, Format-String mit
  2 Platzhaltern/1 Argument). Beide gefixt.
- **ATC-STD-CHANGE-001 v1.0.0 → v1.0.1 (PATCH, F-032)**: inneres ASCII-
  Anführungszeichen im Frontmatter-Titel brach strictes YAML-Parsing; normalisiert,
  redaktionell ohne semantische Änderung.

### Changed

- **registry/findings.yaml:** +9 Findings (F-032..F-040): 6 RESOLVED in diesem Release,
  3 OPEN mit Empfehlungen (F-034 Altbau-Frontmatter-Backfill 107/119 ohne review_date
  seit STDDEV-001 in Kraft — P2, Owner-Entscheidung; F-036 verwaister GitHub-Release
  v1.1.0 vs. CHANGELOG v1.4.x — Owner-Entscheidung; F-039/F-040 Backfill-Begleitpunkte).


## [1.4.34] - 2026-09-08

### Changed

- **Standards Governance Core §9-FREIGEGEBEN → APPROVED** (Owner-Freigabe Michael
  Wroblewski, Builder-Chat 08.09. 00:36 UTC+2). Alle normativ in Kraft ab
  08.09.2026, §30-eingefroren (ATC-STD-000). SCR-0025: IMPLEMENTED → APPROVED.
  versions.yaml: drei 1.0.0-Approval-Einträge:
  - **ATC-STD-STDDEV-001** (119.): Standards Development — Erstellungsprozess,
    §9-Human-Gate, Lifecycle, Wartung, 365-Tage-Review-Zyklus.
  - **ATC-STD-REGISTRY-001** (120.): Registry Management — SSOT-Inventar,
    Generator-Pflicht, Konsistenz-Gates, Neuanlage-Prozess, Schutzregeln.
  - **ATC-STD-CHANGE-001** (121.): Change Control Dachnorm — Änderungsarten-Matrix,
    eine Pipeline, Gate-Landkarte, RACI, Emergency-Pfad, 13 Nachweis-Fragen;
    ordnet zu, ersetzt keine Fachnorm.
- **Gebündelt genehmigt: ATC-STD-FRAMEWORK-001 v1.0.6-PATCH** (FAM-43 komplett
  BELEGT; 10 BELEGT, 3 GEPLANT).
- **Registry FINAL: 121 Standards, 121 APPROVED, 0 DRAFT, 0 offen — alle
  normativ.** Der Standards Governance Core (TAXONOMY-001 + STDDEV-001 +
  REGISTRY-001 + CHANGE-001 + AUDIT-001) ist damit vollständig in Kraft.
  Offene Katalog-Flanken: REPO-AUDIT-003, PROTOCOL-002 (Conformance-Tests),
  PROTOCOL-003 (Threat-Model). Nächste Züge: ATC-PROTO-P2P-001 (erste formale
  Protokoll-Spezifikation), ATC-M-003 / K-Sprint 41 (aurora-ai via
  Kernel-Event-Bridge), Issues #94–98 aus dem Org-Audit.


## [1.4.33] - 2026-09-08

### Added

- **Standards Governance Core KOMPLETT (SCR-0025, 119.-121. Standard):** Die drei
  verbleibenden Core-Standards aus FAM-43, Ausarbeitung nach Owner-Direktive
  „Core bauen" — alle v1.0.0 DRAFT, §9-Freigabe ausstehend:
  - **ATC-STD-STDDEV-001** (Standards Development): verbindlicher Lebenszyklus für
    Standards — 10-Schritte-Erstellungsprozess, §9-Human-Gate als einzige
    Freigabe-Instanz, Lifecycle IDEA→RETIRED, PATCH/MINOR/MAJOR-Wartung mit
    COMPAT-Kopplung, 365-Tage-Review-Zyklus (Überfälligkeit = Finding),
    Deprecation/Retirement, KI-Autoren-Regeln (14 REQ-SD).
  - **ATC-STD-REGISTRY-001** (Registry Management): SSOT-Verwaltung aller
    ATC-Registries — Inventar mit Generator/Gate-Tabelle (10 Registries +
    Naming-Schema), SSOT-Prinzip ohne Parallelstrukturen, Generator-Pflicht
    (Hand-Edits an generierten Dateien = P1-Finding), 5 Konsistenz-Gates je
    CI-Lauf, 7-Schritte-Prozess für neue Registries, Manipulationsschutz (9 REQ-RM).
  - **ATC-STD-CHANGE-001** (Change Control Dachnorm): eine Änderung, ein Kanal,
    eine Gate-Landkarte — Änderungsarten-Matrix (6 Artefakttypen × PATCH/MINOR/
    MAJOR), Pipeline SCR→VERSION→UPDATE→COMPAT→AUDIT→REGISTRY, RACI, Emergency
    mit 48h-Nachholpflicht, lex specialis, die 13 Change-Nachweis-Fragen des
    Master-Audits als Prüfraster je Änderung; ordnet ZU, ersetzt KEINE Fachnorm
    (11 REQ-CH).
- **Registry:** 121 Standards (118 APPROVED + 3 DRAFT); Kategorie governance-core
  (neu); Taxonomie 34 Familien (SGC), alle 121 Standards zugeordnet; 9 Naming-
  Patterns (REQ-SD/RM/CH); 3 DAG-Knoten; Agent-Manifest 121 gebunden.
- **FRAMEWORK-001 v1.0.6 (PATCH, SCR-0025):** FAM-43 komplett BELEGT (10 BELEGT,
  3 GEPLANT — offen: REPO-AUDIT-003, PROTOCOL-002, PROTOCOL-003); Genehmigung
  gebündelt mit §9-Freigabe der drei Core-Standards.


## [1.4.32] - 2026-09-08

### Changed

- **ATC-STD-TAXONOMY-001 v1.0.0: §9-FREIGABE → APPROVED** (Owner-Freigabe Michael
  Wroblewski, Builder-Chat 08.09. 00:27 UTC+2). Normativ in Kraft ab 08.09.2026,
  §30-eingefroren (ATC-STD-000). SCR-0024: IMPLEMENTED → APPROVED. versions.yaml:
  1.0.0-Approval-Eintrag. **Gebündelt genehmigt: ATC-STD-FRAMEWORK-001 v1.0.5-PATCH**
  (FAM-43 Standards Governance Core, 43 Familien, 433 Slots).
- **Registry FINAL: 118 Standards, 118 APPROVED, 0 DRAFT, 0 offen — alle normativ.**
  Meta-Governance ab sofort verbindlich: Familien-/Kategorie-Erstellung nur via
  ATC-FAM-REQ/ATC-CAT-REQ (Pflichtprüfung, Mindestkriterium, Owner-Human-Gate),
  Taxonomie-Änderungen via ATC-TCR, ID-Vergabe nur über die siebenstufige Kette,
  TAX-CHECK-001..018 je Request (S-24 automatisiert je CI-Lauf). Standards
  Governance Core FAM-43: offene Flanken STDDEV-001, REGISTRY-001, CHANGE-001
  (GEPLANT, P1) — daneben REPO-AUDIT-003, PROTOCOL-002/003, Requirements Registry,
  ATC-M-003/K-Sprint 41.


## [1.4.31] - 2026-09-08

### Added

- **ATC-STD-TAXONOMY-001 v1.0.0 DRAFT (SCR-0024, 118. Standard):** ATC Standards
  Taxonomy & Family Creation Standard — Meta-Governance ÜBER der Taxonomie: wie
  Familien, Kategorien, Namensräume und Abhängigkeiten kontrolliert entstehen,
  verschoben, zusammengeführt, aufgeteilt, umbenannt und archiviert werden.
  16 REQ-TAX: vierstufige Hierarchie (Domain→Familie→Kategorie→Standard) mit
  Grandfathering (Bestand behält IDs, §30), ATC-FAM-REQ (8-Punkte-Pflichtprüfung,
  Mindestkriterium ≥3 Standards oder eigenständige Domäne), ATC-CAT-REQ, ATC-TCR
  (CREATE/RENAME/MERGE/SPLIT/MOVE/RETIRE — nie Standard-IDs ändernd), Lifecycle
  PROPOSED→RETIRED, siebenstufige automatische ID-Vergabekette, KI-Agenten-GAP-Prozess
  mit Owner-Human-Gate (dokumentierter Negativfall: Owner-Beispielfamilie AIA
  überlappt Bestands-Familie AAS → Request würde zurückgewiesen), TAX-CHECK-001..018.
- **Standards Governance Core (FAM-43):** TAXONOMY-001 + GEPLANT: ATC-STD-STDDEV-001
  (Standards-Development), ATC-STD-REGISTRY-001 (Registry-Management),
  ATC-STD-CHANGE-001 (Change-Control-Dachnorm, konsolidiert ATC-STD-000 §19–33 +
  UPDATE-001 + COMPAT-001) + bestehendes ATC-STD-AUDIT-001.
- **Taxonomie-Registry:** `registry/taxonomy.yaml` (SSOT via tools/taxonomy/
  gen_taxonomy.py) — Bestands-Abbild: 5 Domains (GOV/SW/CHAIN/AI/TRUST), 33 Familien
  (12 numerische ID-Bereiche + 21 benannte), alle 118 Standards zugeordnet
  (Registry-Konsistenz verifiziert). **Validator NEU S-24** (TAX-CHECK-Untermenge:
  Domain-/Familien-/Kategorie-Eindeutigkeit, Lifecycle, Registry-Konsistenz —
  Negativtest verifiziert).
- **FRAMEWORK-001 v1.0.5 (PATCH, SCR-0024):** FAM-43 → 43 Familien, 433 Slots
  (7 BELEGT, 6 GEPLANT); Genehmigung gebündelt mit §9-Freigabe TAXONOMY-001.
- **Registry:** 118 Standards (117 APPROVED + 1 DRAFT); Kategorie taxonomy;
  7 Naming-Patterns (ATC-FAM-REQ/ATC-CAT-REQ/ATC-TCR/TAX-CHECK-IDs); DAG-Knoten;
  Agent-Manifest 118 gebunden.


## [1.4.30] - 2026-09-08

### Changed

- **Dreifache §9-FREIGABE → APPROVED** (Owner-Freigabe Michael Wroblewski,
  Builder-Chat 08.09. 00:18 UTC+2). Alle normativ in Kraft ab 08.09.2026,
  §30-eingefroren (ATC-STD-000):
  - **ATC-STD-AOS-001 v1.0.0** (115. Standard) — Agent Operating Standard:
    14-Fragen-Session-Mandat verbindlich; Session-Records (AOS-SESS) Pflicht bei
    governance-relevanten Agenten-Sessionen; Mandatsverstoß = Finding.
  - **ATC-STD-999 v1.0.0** (116. Standard) — Master-Audit: MAUD-Records (Typ
    MASTER) bei MAJOR/Release-Kandidat/Quartals-Audit; 16-Stufen-Kette + 13
    Nachweis-Fragen orchestrieren S-01..S-22/Health-Scores/RR-Gates; MAJOR ohne
    Master-Audit-PASS verboten.
  - **ATC-STD-PROTOCOL-001 v1.0.0** (117. Standard) — Protocol Standards:
    Protocol-Registry verbindlich (Registry-Eintrag = Autorisierung); Envelope-,
    Encoding-, Kompatibilitäts-, Handshake-, Security- und Upgrade-Regeln für
    alle ATC-Protokolle; S-23 erzwingt Registry-Integrität je CI-Lauf.
- **Gebündelt genehmigt: ATC-STD-FRAMEWORK-001 v1.0.3-PATCH** (FAM-20/FAM-40
  BELEGT) **und v1.0.4-PATCH** (FAM-42 Protocol Standards, 42 Familien, 429
  Slots).
- **Registry FINAL: 117 Standards, 117 APPROVED, 0 DRAFT, 0 offen — alle
  normativ.** SCR-0022 + SCR-0023: IMPLEMENTED → APPROVED. P1 der
  FRAMEWORK-Gap-Roadmap (AOS-001, ATC-STD-999) und P0-Fundament der
  Protokoll-Agenda komplett. Offen: REPO-AUDIT-003 (P2), PROTOCOL-002/003
  (GEPLANT), Requirements Registry (P1-Rest), ATC-M-003/K-Sprint 41.


## [1.4.29] - 2026-09-08

### Added

- **ATC-STD-PROTOCOL-001 v1.0.0 DRAFT (SCR-0023, 117. Standard):** ATC Protocol
  Standards — Dachstandard ÜBER allen Einzelprotokollen des Ökosystems. 21 REQ-PROTO:
  Protocol Governance (12+ Pflichtfelder), 7-Schichten-Architektur, ID-Schema
  ATC-PROTO-[DOMAIN]-[NUMBER], 9-Felder-Nachrichten-Envelope, Encoding-Standard
  (JSON/YAML/TOML human-readable, CBOR/Protobuf machine, deterministische
  Serialisierung für Blockchain), SemVer + Versionsfenster (supported/minimum/
  maximum/deprecated), 7 Kompatibilitätsdimensionen mit Compatibility-Layer-Pflicht,
  6-Phasen-Handshake mit Capability Exchange, Authentication (niemals nur IP/
  Hostname) + Authorization (Capability-Modell), Threat-Model-Pflicht (12 Angriffe),
  Cryptographic Abstraction Layer, maschinenlesbare Fehlercodes (13 Klassen),
  Timeout/Retry/Circuit-Breaker, Rate-Limiting, Replay-Schutz mit Chain-ID-Pflicht,
  Observability (11 Felder), Audit (AUD-Records), 13-Schritte-Upgrade-Prozess.
- **Protocol-Registry:** `registry/protocol-registry.yaml` (SSOT via
  tools/protocol/gen_protocol_registry.py) — 26 ATC-PROTO-Familien gem. Owner-Matrix
  (P2P, NODE, CONSENSUS, BLOCK, TX, MEMPOOL, VALIDATOR, STAKING, MINING, WALLET,
  IDENTITY, REPUTATION, GOVERNANCE, ORACLE, ZKP, BRIDGE, IBC, DATA, STORAGE, AI,
  AGENT, API, EVENT, AUDIT, UPGRADE + KERNEL als 26.); Status-Ehrlichkeitsregel:
  10 draft (Impl.-Spuren: ShivaCore K6/K9/K12/K14/K15/K16, a-townchain,
  mempool.rs, Dev-Plattform-Repos), 16 planned, 0 active. **Validator NEU S-23**
  (Integrität: ID-Pattern, Status, SemVer, Prioritäten, ≥20 Familien — Negativtest
  verifiziert). Ein Protokoll ohne Registry-Eintrag ist kein ATC-Protokoll.
- **FAM-42 „Protocol Standards"**: neue Katalog-Familie (42 Familien, 429 Slots —
  6 BELEGT, 3 GEPLANT). **ATC-STD-FRAMEWORK-001 v1.0.4 (PATCH, SCR-0023):**
  Zähler-Synchronisation; Genehmigung gebündelt mit §9-Freigabe PROTOCOL-001.
- **Registry:** 117 Standards (114 APPROVED + 3 DRAFT); Kategorie protocol;
  5 Naming-Patterns (protocolStandardId, protocolId, protocolErrorCode,
  protocolRequirementId, Datei-Muster); DAG-Knoten; Agent-Manifest 117 gebunden.


## [1.4.28] - 2026-09-08

### Added

- **ATC-STD-AOS-001 v1.0.0 DRAFT (SCR-0022, 115. Standard):** ATC Agent Operating
  Standard — Ausarbeitung des 14-Fragen-Mandats aus FRAMEWORK-001 §8 (Owner-Entwurf
  „20. KI-Softwareentwicklungsagent"). 17 REQ-AOS: Session-Lifecycle (SESSION_START →
  14 Fragen → Record → Aktionsreihe → Verifikation → Doku-Sync → Audit-Nachweis →
  SESSION_END), 14 Fragen mit autorisierten Quellen (Manifest, Registry, SCR, AD,
  MILESTONE), maschinenlesbarer Session-Record `AOS-SESS-YYYYMMDD-NNN` (YAML/JSON),
  Fragen 1–10 vor der ersten Aktion / 11–14 bis SESSION_END, Mandatsverstoß =
  Finding (BUG-005); Human Gates übergeordnet (AI-DECISION-001).
- **ATC-STD-999 v1.0.0 DRAFT (SCR-0022, 116. Standard):** ATC Master-Audit —
  Enterprise Completeness & Consistency Audit (Owner-Entwurf „40. Master-Audit").
  12 REQ-MA: 16-Stufen-Audit-Kette (Requirement → Specification → Architecture →
  Code → Tests → Build → Deployment → Runtime → Security → Documentation → Wiki →
  README → CHANGELOG → Roadmap → Standards → Audit Evidence) mit Status je Stufe
  (CONSISTENT/PARTIAL/INCONSISTENT/MISSING) und P0/P1-Blockade; 13 Change-Nachweis-
  Fragen (WHAT … AUDIT EVIDENCE) je Änderung; MAUD-YYYY-NNNN als AUD-Record Typ
  MASTER (keine Parallelstruktur); Register-Abdeckung (11 Register); Orchestrierung
  statt Duplikation (S-01..S-22, REPO-AUDIT Health Scores, RR-G01..G08,
  MILESTONE/COMPAT-Gates); MAJOR ohne Master-Audit-PASS verboten; Audit-der-Audits
  als Continuous-Improvement-Schleife.
- **FRAMEWORK-001 v1.0.3 (PATCH, SCR-0022):** FAM-20 + FAM-40 GEPLANT → BELEGT
  (5 BELEGT, 1 GEPLANT — offen: REPO-AUDIT-003); Genehmigung gebündelt mit §9-Freigabe
  beider neuen Standards.
- **Registry:** 116 Standards (114 APPROVED + 2 DRAFT); Kategorien +agent-operating,
  +master-audit; 7 Naming-Patterns (AOS-SESS-Session-IDs, REQ-AOS/REQ-MA);
  2 DAG-Knoten; Agent-Manifest 116 Standards gebunden. P1 der Gap-Roadmap damit
  abgearbeitet (Requirements Registry folgt).


## [1.4.27] - 2026-09-08

### Changed

- **ATC-STD-REPO-AUDIT-002 v1.0.0: §9-FREIGABE → APPROVED** (Owner-Freigabe Michael
  Wroblewski, Builder-Chat 08.09. 00:05 UTC+2). Normativ in Kraft ab 08.09.2026,
  §30-eingefroren (ATC-STD-000). SCR-0021: IMPLEMENTED → APPROVED. versions.yaml:
  1.0.0-Approval-Eintrag. **Gebündelt genehmigt: ATC-STD-FRAMEWORK-001 v1.0.2-PATCH**
  (FAM-41 Slot 002 BELEGT, Zähler-Referenz auf stats-Block).
- **Registry FINAL: 114 Standards, 114 APPROVED, 0 DRAFT, 0 offen — alle normativ.**
  Repository-Audits ab sofort mit verbindlichem CHECK-Katalog (CHECK-001..064, 64
  Checks, AUTO(30)/HYBRID(19)/MANUAL(15)) und standardisiertem Health Score (0–100 →
  A–E, P0→E-Blockade); Validator S-22 erzwingt Katalog-Integrität je CI-Lauf.
  Offen in der Familie: REPO-AUDIT-003 (Auditor-Agent) GEPLANT (P2).


## [1.4.26] - 2026-09-08

### Added

- **ATC-STD-REPO-AUDIT-002 v1.0.0 DRAFT (SCR-0021):** Audit-Checklisten- & Health-
  Score-Standard (Owner-Richtung aus REPO-AUDIT-001 §28) — 12 REQ-RB. CHECK-Katalog
  `registry/repo-audit-checks.yaml` (SSOT, generiert von tools/repo-audit/gen_checks.py):
  **64 Checks (CHECK-001..064)**, je 4 je Prüfbereich, Methoden AUTO(30)/HYBRID(19)/
  MANUAL(15), Checkgewichte 1–3, 16 Bereichsgewichte (Summe 100; Sicherheit 12,
  Tests 10, Build 9). Ergebnis je Check PASS/WARN/FAIL/SKIP mit Evidence-Pflicht;
  SKIP ohne Begründung = P1-Finding. Scoring-Formel (Bereichs-/Gesamtscore 0–100);
  Health-Score→A-E-Mapping mit P0→E-Regel; maschinenlesbarer Health-Report mit
  AUD-Record-Kopplung (AUDIT-001); Human-Gate für Agenten-Audits (AI-DECISION-001);
  CI-Integration (governance-ci); Katalog-Governance via SCR.
- **Validator NEU S-22:** Katalog-Integrität (≥48 Checks, ≥3 je Bereich, Gewichte,
  eindeutige CHECK-IDs, Bereichsgewichte Summe 100) — Negativtest FAIL verifiziert.
- **FRAMEWORK-001 v1.0.2 (PATCH, SCR-0021):** FAM-41 Slot 002 GEPLANT→BELEGT
  (3 BELEGT, 3 GEPLANT); Zähler-Angabe auf stats-Block-Referenz umgestellt;
  Genehmigung mit §9-Freigabe REPO-AUDIT-002 gebündelt (ausstehend).
- **Registry:** 114 Standards (113 APPROVED + 1 DRAFT REPO-AUDIT-002);
  Naming +repoAuditCheckId; DAG-Knoten; Agent-Manifest 114 Standards gebunden.


## [1.4.25] - 2026-09-07

### Changed

- **ATC-STD-REPO-AUDIT-001 v1.0.0: §9-FREIGABE → APPROVED** (Owner-Freigabe Michael
  Wroblewski, Builder-Chat 07.09. 23:58 UTC+2). Normativ in Kraft ab 07.09.2026,
  §30-eingefroren (ATC-STD-000). SCR-0020: IMPLEMENTED → APPROVED. versions.yaml:
  1.0.0-Approval-Eintrag. **Gebündelt genehmigt: ATC-STD-FRAMEWORK-001 v1.0.1-PATCH**
  (FAM-41 Katalog-Erweiterung, Zähler-Synchronisation).
- **Registry FINAL: 113 Standards, 113 APPROVED, 0 DRAFT, 0 offen — alle normativ.**
  Repository-Audits ab sofort verbindlich über die 21-Schritte-Pipeline mit
  AUD-Records (AUDIT-001), globalen F-NNN-Findings (F-032+), P0-Release-Block,
  Health-Status A-E. Nächste Ebene REPO-AUDIT-002 (CHECK-NNN + Repository Health
  Score) GEPLANT (P1).


## [1.4.24] - 2026-09-07

### Added

- **ATC-STD-REPO-AUDIT-001 v1.0.0 DRAFT (SCR-0020):** Verbindlicher Repository-Audit-
  Standard (Owner-Entwurf, Builder-Chat 23:54) — 25 REQ-RA; reproduzierbarer Repository
  Health Check über 16 Prüfbereiche; 26-Zeilen-Prüfmatrix; ATC-REPOSITORY-AUDIT-RULE;
  SOLL/IST (13 Quellen, 8 Status); GAP-<KAT>-NNN-Kategorien; 11 kritische Code-Prüfungen;
  Build 4-Status + Runtime-Regel (kompiliert ≠ fertig); Security-Mindestumfang mit
  Verschärfung (Blockchain/Wallet/Contracts/Bridges/Mining/Admin APIs/KI-Agenten);
  Dependency-Audit (9 Felder); 5-Ebenen-Sync; CI/CD- + GitHub-Audit; 8 Versionsquellen;
  Kompatibilität 4-Status mit COMPAT-001-Kopplung (UNKNOWN bei Release verboten);
  IMP-NNN-Verbesserungsaudit; P0-P4-Priorisierung (P0 blockiert Release); F-NNN auf
  globalen findings.yaml-Namespace gemappt (Fortschreibung F-032+); RCA via BUG-005;
  Health-Status A-E; 23 Abschlusskriterien; verbindliche 21-Schritte-Pipeline mit
  AUD-Records (AUDIT-001). REPO-AUDIT-002 (CHECK-NNN + Health Score) und
  REPO-AUDIT-003 (Auditor-Agent) GEPLANT.
- **FAM-41 „Repository Audit"**: neue Katalog-Familie im Enterprise-Framework
  (41 Familien, 426 Slots — 264 NEU / 150 VERWEIST / 2 BELEGT / 6 KONFLIKT /
  4 GEPLANT). **ATC-STD-FRAMEWORK-001 v1.0.1 (PATCH, SCR-0020):** Zähler-
  Synchronisation, keine semantischen Änderungen, Genehmigung gebündelt mit der
  §9-Freigabe von REPO-AUDIT-001.
- **Registry:** 113 Standards (112 APPROVED + 1 DRAFT REPO-AUDIT-001); Kategorie
  repo-audit; 5 Naming-Patterns; DAG-Knoten; Agent-Manifest 113 Standards gebunden.


## [1.4.23] - 2026-09-07

### Changed

- **ATC-STD-FRAMEWORK-001 v1.0.0: §9-FREIGABE → APPROVED** (Owner-Freigabe Michael
  Wroblewski, Builder-Chat 07.09. 23:48 UTC+2). Normativ in Kraft ab 07.09.2026,
  §30-eingefroren (ATC-STD-000). Frontmatter: status approved, normative true,
  effective_date 2026-09-07, review_date 2027-09-07, approved_by Owner. SCR-0019:
  IMPLEMENTED → APPROVED. versions.yaml: 1.0.0-Approval-Eintrag.
- **Registry FINAL: 112 Standards, 112 APPROVED, 0 DRAFT, 0 offen — alle normativ.**
  Das Enterprise-Control-System ist verbindlich: Neue Standards folgen dem
  40-Familien-Katalog (registry/framework.yaml, 423 Slots — Slot-Pflicht), den
  einheitlichen Status-/Change-/Traceability-Modellen und der 11-Register-
  Zielarchitektur; KONFLIKT-Slots (100/201-204/300) werden je Familie via SCR
  aufgelöst. Gap-Roadmap P1: ATC-STD-AOS-001 (Agent Operating Standard),
  ATC-STD-999 (Master-Audit), Requirements Registry.


## [1.4.22] - 2026-09-07

### Added

- **ATC-STD-FRAMEWORK-001 v1.0.0 DRAFT (SCR-0019):** ATC Enterprise Standards
  Framework — das Master-Dokument (ATC-STANDARDS-MASTER). 12 REQ-FW; führt alle
  111 Standards in eine Zielarchitektur: maschinenlesbarer 40-Familien-Katalog
  (registry/framework.yaml, 423 Slots — 264 NEU, 150 VERWEIST auf Bestand,
  1 BELEGT, 6 KONFLIKT, 2 GEPLANT); Kollisionsauflösung für §30-eingefrorene
  Slots 100/201-204/300 dokumentiert; einheitliche Status-/Change-/Traceability-
  Modelle auf den normativen Bestand abgebildet (kein Parallelprozess);
  11-Register-Architektur (Standards/Milestones/Repos/Framework-Katalog/SCR/Audit
  existieren, Requirements/Architecture/Agent/Security/Release&Evidence GEPLANT);
  Release-Readiness RR-G01..G08; Agent Operating Mandate (14 Session-Fragen,
  ATC-STD-AOS-001 reserviert); Master-Audit ATC-STD-999 reserviert (16-Stufen-
  Audit-Kette); Gap-Roadmap P1-P3.
- **Maschinenlesbarkeit:** registry/framework.yaml (SSOT-Katalog, generiert von
  tools/framework/gen_framework.py) + Validator NEU S-21 (Familien/Slots,
  Status-Enums, eindeutige IDs, Registry-Referenz-Auflösung, KONFLIKT-Pflicht-Note;
  Negativtest FAIL verifiziert); Kategorien +framework; Naming 4 Patterns;
  DAG-Knoten; Agent-Manifest 112 Standards gebunden.
- **Registry:** 112 Standards (111 APPROVED + 1 DRAFT FRAMEWORK-001).


## [1.4.21] - 2026-09-07

### Changed

- **ATC-STD-MILESTONE-001 v1.0.0: §9-FREIGABE → APPROVED** (Owner-Freigabe Michael
  Wroblewski, Builder-Chat 07.09. 23:38 UTC+2). Normativ in Kraft ab 07.09.2026,
  §30-eingefroren (ATC-STD-000). Frontmatter: status approved, normative true,
  effective_date 2026-09-07, review_date 2027-09-07, approved_by Owner. SCR-0018:
  IMPLEMENTED → APPROVED. versions.yaml: 1.0.0-Approval-Eintrag.
- **Registry FINAL: 111 Standards, 111 APPROVED, 0 DRAFT, 0 offen — alle normativ.**
  Mit MILESTONE-001 sind Roadmap (AD-027 M1–M8 als ATC-M-001..008), Sprints, Releases,
  Audits und KI-Agentensteuerung über die Meilenstein-Governance verbunden:
  kein Abschluss ohne überprüfbaren Nachweis (ATC-MILESTONE-GOVERNANCE-RULE),
  maschinell durchgesetzt via milestone.schema.json, registry/milestones.yaml
  und Validator S-20 bei jedem CI-Lauf.


## [1.4.20] - 2026-09-07

### Added

- **ATC-STD-MILESTONE-001 v1.0.0 DRAFT (SCR-0018):** Verbindlicher Meilenstein-
  Standard (Owner-Entwurf, Builder-Chat 23:31) — 19 REQ-MS; Meilenstein = nachweisbar
  erreichter Systemzustand; 13-Status-Lifecycle ohne Sprünge; 19 Pflichtfelder;
  Reifeklassen M0-M8; Evidence Packs; 8 Acceptance Gates (ATC-MILESTONE-ACCEPTANCE-
  GATE); Dependency-Deklaration (kein ACCEPTED bei offener kritischer Dependency);
  Sprint-/Release-Trennung; MAJOR-Revalidation (Kopplung COMPAT-001/UPD-G04);
  Risikomodell (4 Level, 6 Arten); KI-Agenten-Regeln (kein agentisches ACCEPTED ohne
  Human Gate); 18-Punkte-DoD; ATC-MILESTONE-GOVERNANCE-RULE als Hartregel.
- **Maschinenlesbarkeit:** schemas/milestone.schema.json (inkl. if/then: ACCEPTED+
  erzwingt Evidence/Audit/actual_completion/compatibility ≠ UNKNOWN);
  registry/milestones.yaml als SSOT mit AD-027-Migration ATC-M-001..008 (M1/M2
  ACCEPTED mit Evidence, M3 IN_PROGRESS, M4-M8 PLANNED); Validator S-20 neu
  (Pflichtfelder, ID-Pattern, Status/Kategorie-Enums, Evidence-Pflicht bei
  ACCEPTED+, Dependency-Auflösung — Negativtest FAIL verifiziert).
- **Registry:** 111 Standards (110 APPROVED + 1 DRAFT MILESTONE-001); Kategorie
  milestone; Naming-Patterns milestoneStandardId/milestoneId/milestoneProgramId/
  milestoneRequirementId/milestoneStandardDoc; DAG-Knoten; Agent-Manifest 111/111.
- **§9-Freigabe ausstehend** (Registry FINAL wäre 111/111 APPROVED).


## [1.4.19] - 2026-09-07

### Changed

- **ATC-STD-UPDATE-001 v1.0.0: §9-FREIGABE → APPROVED** (Owner-Freigabe Michael
  Wroblewski, Builder-Chat 07.09. 23:28 UTC+2). Normativ in Kraft ab 07.09.2026,
  §30-eingefroren (ATC-STD-000). Frontmatter: status approved, normative true,
  effective_date 2026-09-07, review_date 2027-09-07, approved_by Owner. SCR-0015:
  IMPLEMENTED → APPROVED. versions.yaml: 1.0.0-Approval-Eintrag. Registry:
  normative true. UPD-G04 (MAJOR) bindet COMPAT-001 als Pflicht-Gate — mit dieser
  Freigabe ist die komplette Change-Control-Kette
  SCR → VERSION → UPDATE → COMPAT → AUDIT normativ in Kraft.
- **Registry FINAL: 110 Standards, 110 APPROVED, 0 DRAFT, 0 offen — alle normativ.**
  Standards-System damit vollständig ohne offene Lifecycle-Posten.


## [1.4.18] - 2026-09-07

### Fixed

- **Tiefenanalyse-Fixlauf (23:24-23:40):** Stale Zaehlstaende konsolidiert —
  STATUS.md (105/105, 108 Standards FINAL, 103/103 Voll-Audit, 105/105 Q&A-Sektion,
  Mangel 'Issues #94..5') und README.md (81/81, 82/82, 103 APPROVED, 'alle 103',
  Registry-Header) auf Ist-Zustand 110/110 (109 APPROVED + 1 DRAFT UPDATE-001)
  synchronisiert; historische Audit-Vermerke datiert erhalten.
- **Agent-Manifest-Gate A1 repariert:** required_standards in .github/ai/agent.yaml
  um 7 fehlende Standards ergänzt (DESC-001, VERSION-001, BUG-005, AUDIT-001,
  AI-DECISION-001, UPDATE-001, COMPAT-001) — Manifest deckt Registry wieder
  vollständig ab (110/110), check_agent_manifest GATE PASS (A1-A4).
- **Tiefenanalyse verifiziert (kein Handlungsbedarf):** versions.yaml vollständig
  (110/110 unter versions:-Key), categories.yaml vollständig (governance/
  architecture/repository/development unter categories:-Key), dependencies.yaml
  DAG intakt, SCR-0001..0016 lückenlos (SCR-0017 gemäß Issue #98 geplant),
  0 tote Markdown-Links in 147 Dateien, Dreieck Frontmatter↔Registry↔versions
  konsistent, keine zukünftigen effective_dates.


## [1.4.17] - 2026-09-07

### Fixed

- **Registry-Fehlerpruefung (Fehlercheck-Lauf 23:25):** findings.yaml — F-024-Eintrag
  hatte durch strip() die Block-Einrueckung verloren (YAML-Parse-Fehler, vom CI-Validator
  im Fallback-Modus nicht erkannt); Einrueckung restauriert, 31 Findings F-001..F-031
  parsen sauber. versions.yaml — ATC-STD-COMPAT-001 v1.0.0 Eintrag nachgetragen
  (§13-Versionshistorien-Pflicht, wie F-008-Muster).
- **Validator S-18 erweitert (Voll-Modus):** prueft jetzt ALLE registry/*.yaml
  (10 Dateien) strukturell statt nur standards.yaml — Negativtest mit absichtlich
  gebrochener findings.yaml laeuft korrekt auf FAIL, regulärer Lauf PASS
  (110 Eintraege, 10 Registry-Dateien).


## [1.4.16] - 2026-09-07

### Added

- **AUD-2026-0002: ATC Enterprise GitHub Organization Audit** (Owner-Auftrag,
  18 Prüfbereiche, 26 Repos + Org): CONDITIONAL_PASS. Klassifizierung 4 ACTIVE /
  12 DEVELOPMENT / 10 EXPERIMENTAL. Findings F-024..F-031 in registry/findings.yaml:
  F-024 Org-Settings (SKIP per Owner 23:13), F-025 Dependabot/CodeQL (Dependabot in
  16 Repos in diesem Lauf eingerichtet, CodeQL offen), F-026 Version-Baseline,
  F-027 verwaister Tag v2.0.0 (a-townchain-os), F-028 ATC-STD-202 zählt 22 statt 26,
  F-029 governance-ci fehlt in atc-vm/atc-algorithm/atc-zkp (GH013 workflow-Scope,
  kongruent F-010), F-030 atc-whitepaper-Referenz existiert nicht, F-031
  POSITIV-Befund Governance-Hygiene 26/26 + 0 Secrets. Cleanup-Roadmap als Issues
  #AUD-1..5 in a-townchain-os. Report: docs/AUD-2026-0002_ORG_AUDIT.md.


## [1.4.15] - 2026-09-07

### Changed

- **ATC-STD-COMPAT-001 v1.0.0: §9-FREIGABE → APPROVED** (Owner-Freigabe Michael
  Wroblewski, Builder-Chat 07.09. 23:02 UTC+2). Normativ in Kraft ab 07.09.2026,
  §30-eingefroren (ATC-STD-000). Frontmatter: status approved, normative true,
  effective_date 2026-09-07, review_date 2027-09-07, approved_by Owner. SCR-0016:
  IMPLEMENTED → APPROVED. Registry-Eintrag aktualisiert (normative: true).
  Standards-Bilanz: 110 Standards, 109 APPROVED + 1 DRAFT (UPDATE-001).

### Fixed

- **Validator-Abdeckung COMPAT-Familie:** atc_std_validator S-02-Regex um COMPAT-
  Präfix ergänzt; CATS-Liste um Kategorie `compat` erweitert;
  naming-conventions.schema.json um compatStandardId, compatRequirementId,
  compatRestorationId (COMP-NNN, REQ-COMPAT-009) und compatStandardDoc ergänzt.
  Ergebnis: ALL COMPLIANT (inkl. COMPAT-001, Mutationssuite M1-M12 12/12).


## [1.4.14] - 2026-09-07

### Added

- **ATC-STD-COMPAT-001 v1.0.0 (DRAFT):** ATC Major Version Compatibility & Recovery
  Standard — verbindliche Kompatibilitätsprüfung des gesamten abhängigen
  Ökosystems nach MAJOR-Version-Updates. 14 REQ-COMPAT; 2 harte Kernregeln
  (ATC-MAJOR-COMPATIBILITY-GATE: Major-Version gilt erst als freigegeben, wenn
  Kompatibilität geprüft/dokumentiert und bestätigt oder wiederhergestellt;
  ATC-COMPATIBILITY-RESTORATION: jede kritische Inkompatibilität muss behoben,
  migriert, überbrückt oder als formal freigegebener Breaking Change akzeptiert
  werden). 6 Kompatibilitätsklassen (COMPATIBLE, COMPATIBLE_AFTER_MIGRATION,
  INCOMPATIBLE, BLOCKED, UNKNOWN, DEPRECATED — kein UNKNOWN verbleibt bei
  Release), 5 Prüfebenen (Syntax/Semantik/Daten/Runtime/System), 6
  Wiederherstellungsmethoden (A Adapter, B Migration, C Wrapper, D
  Compatibility Layer, E kaskadiertes Upgrade, F Breaking Change nur mit
  Owner-Freigabe), COMP-NNN-Wiederherstellungs-IDs (keine versteckten
  Kompatibilitäts-Fixes durch Agenten), Compatibility Matrix, YAML-Reportformat
  (compatibility_audit), 18-Punkte-MAJOR-Definition-of-Done. Als Pflicht-Gate in
  ATC-STD-UPDATE-001 verankert (UPD-G04 Compatibility bei MAJOR, REQ-UPD-008
  verstärkt); Change-Control-Kette erweitert: SCR → VERSION → UPDATE →
  COMPAT → AUDIT. Neue Kategorie `compat` (ATC-STD-COMPAT-001..999) in
  registry/categories.yaml; Registry-Eintrag in registry/standards.yaml.
  Owner-Entwurf Michael Wroblewski (Builder-Chat 07.09. 22:55); §9-Freigabe
  ausstehend.


## [1.4.13] - 2026-09-07

### Added

- **ATC-STD-UPDATE-001 v1.0.0 (DRAFT):** ATC Update Standard — Change Control für
  Artefakt-Updates. Update-Kategorien (PATCH/MINOR/MAJOR gekoppelt an
  ATC-STD-VERSION-001; SECURITY/EMERGENCY/GOVERNANCE prozessoral), 13-stufiger
  Lifecycle, UPD-NNN-Update-Requests (Schema updateRequestId), Impact Analysis
  (direkt/indirekt/Governance), Dependency Check (dependencies.yaml-DAG-Basis),
  Source-of-Truth-Regel + Synchronisationspflicht (13 Artefakte), 9 Update-Gates
  (UPD-G01..G09, abgegrenzt zu AUD-G01..G08), Statusmodell mit Fehler- und
  Notfallpfad, Rollback-Standard mit 5 Blockchain-Rollback-Typen
  (Software/State/Daten/Contract-Migration/Consensus-Migration), Emergency-
  Prozess (Auditierbarkeit entfällt nie; Post-Mortem-Pflichten via BUG-005),
  AI-Agent-Update-Regel (kein autonomes normatives Publishing; Human Gates via
  AI-DECISION-001), Update Manifest (VERSION-001-Release-Manifest-Kopplung),
  CHANGELOG-Pflicht, Update Audit (15 Fragen), Integrity Manifest,
  regelmäßige Standard-Reviews (Kadenzen: Critical/High jährlich, Normal 2J,
  Low-Risk 2–3J), Update Control Matrix (Rollen per ATC-STD-000 §14.1),
  No-Silent-Update-Kernregel. 19 REQ-UPD, 6 COM-UPD-Gates.
  SCR-0015: UPD↔SCR-Kopplung (SCR bleibt Pflicht für normative Standard-
  änderungen per §30; UPD deckt Release-Tracking) — keine Doppelspur;
  Hierarchie-Diagramm auf den tatsächlichen Bestand korrigiert (ERROR-001→
  BUG-005, AGENT-001→AAS, REPOSITORY-001→201..204, CODING/CHANGE→geplant).
  Owner-Entwurf Michael Wroblewski (22:40). Status DRAFT — §9-Freigabe ausstehend.
- **Schema:** UPDATE-Familie allockiert (updateStandardId, updateRequirementId,
  updateRequestId, updateGateId, updateStandardDoc).

## [1.4.12] - 2026-09-07

### Added

- **AUD-2026-0001 — erster Audit-Lauf unter ATC-STD-AUDIT-001** (Owner-Auftrag
  „Prüfe ob alle Standards umgesetzt werden", 22:30): Standards-Umsetzungs-Audit
  mit Audit Manifest (AUD-YYYY-NNNN), 20 Domänen (AUD-C01..C20), Evidence-Kette,
  Unabhängigkeits-Notiz, DoD-Checkliste und Audit Trail. Ergebnis:
  CONDITIONAL_PASS, Completeness Score C — Governance-Schicht vollständig
  (108/108 validiert, DAG, CI grün), Durchsetzungsschicht bei 23% Umsetzungs-
  decke: 8 Standards automatisiert erzwungen (ATC-STD-000, 201..204,
  README/MD-001, AAS-025), 18 teilumgesetzt, 82 nur dokumentiert.
- **Findings F-019..F-023** gemäß BUG-001: F-019 Enforcement-Lücke (S2),
  F-020 DEC-Records-Infrastruktur (S2), F-021 Audit-Engine/Cross-System-Scanner
  (S3), F-022 BUG-005-Analyse-Felder im Finding-Workflow (S3),
  F-023 Cross-System-Stichprobe: atc-shivacore fehlen STATUS.md/ROADMAP.md/
  ARCHITECTURE.md (MD-001-Verstoß, S2). Kein Release-Blocker (0× S0/S1).
- **audits/AUD-2026-0001.md**: Audit-Report + Manifest, erste revisionsfähige
  Audit-Historie unter REQ-AUDIT-027/028.

## [1.4.11] - 2026-09-07

### Added

- **ATC-STD-AI-DECISION-001 v1.0.0 (APPROVED):** ATC Agent Decision-Making Standard —
  das Entscheidungsmodell ÜBER den AAS-Betriebsstandards und AI-DEV-Entwicklungsstandards.
  15-stufige Pipeline, Identitätspflichtfelder, Entscheidungstypen D0–D5, Autonomie-Level
  L0–L5 (L5 Governance ohne uneingeschränkte Kontrolle), Evidence-First, Confidence/
  Eligibility, Risiko RK0–RK5 auf 10 Risikoachsen, Reversibility, Option-Scoring,
  Policy-First, Authority Check, Human Approval Gates, Conflict-Resolution-Priorität,
  Decision Records DEC-NNNNNN, kein Hidden Decision Making (kein Chain-of-Thought als
  Audit), Fail-Safe, Multi-Agent Separation of Duties, Vier-Augen-Prinzip,
  Post-Decision Verification. 23 REQ-AIDEC, 6 COM-AIDEC-Gates.
  SCR-0014: Die vorgeschlagene Familie ATC-STD-AI-001..015 wurde auf den Bestand
  gemappt (12/15 durch AAS/AI-DEV abgedeckt — KEINE Parallel-Familie); Kill-Switch
  als dokumentierte Lücke. RK-Skala statt R (Kollision mit Reproduzierbarkeit
  R0–R3, BUG-005). Owner-Entwurf Michael Wroblewski (22:15).
- **Schema:** AI-DECISION-Familie allockiert (aiDecisionStandardId,
  aiDecisionRequirementId, decisionRecordId, aiDecisionStandardDoc).

### Changed

- **Sammelfreigabe (Owner-Mandat „Freigabe", 22:25):** ATC-STD-BUG-005 und
  ATC-STD-AUDIT-001 von DRAFT auf APPROVED gesetzt (normativ, §30-eingefroren).
  Registry FINAL: 108 Standards, 108 APPROVED, 0 offen, alle normativ.
  Approval-Dokument: approval/APPROVAL-DECISION-2026-09-07-BUG005-AUDIT-AIDECISION-v1.0.0.md.
  SCR-0011/0012/0013/0014 Owner-§9-Checkboxen gesetzt.

## [1.4.10] - 2026-09-07

### Added

- **ATC-STD-AUDIT-001 v1.0.0 (DRAFT):** ATC Completeness & Audit Standard — die
  Kontrollschicht über allen anderen ATC-Standards. 20 Audit-Domänen (AUD-C01..C20:
  Anforderungen bis Gesamtintegrität), Completeness Score A–F, Pflichtprüfungskatalog
  (Anforderungen/Architektur/Implementierung/Tests/Dokumentation), Traceability Matrix
  (REQ→STD→ARCH→DESIGN→CODE→TEST→AUDIT→RELEASE→CHANGELOG), Artefakt-Vollständigkeit,
  Open-Point-Indikatoren (TODO/FIXME/stub/mock/...), Dokumentations-Konsistenz,
  Repository-/Versionierungs-/CHANGELOG-Prüfung (VERSION DRIFT, TRACEABILITY GAP),
  Sicherheits-Audit (Code/Infra/Blockchain), Smart-Contract-Vollständigkeit (15 Artefakte),
  KI-Agenten-Audit-Blöcke, Audit Gates AUD-G01..G08 (Release-Kette), Audit-Pyramide
  (ATC-STD-000 → AUDIT-001 → Fach-Audits → Cross-System Integrity → Release Gate),
  Audit Evidence (No Evidence → No Compliance), maschinenlesbares Audit Manifest,
  Audit Trail AUD-YYYY-NNNN, Cross-System Integrity Audit (Standards↔Wiki↔Repo↔Code↔
  Tests↔CI/CD↔Release↔CHANGELOG↔Roadmap↔Issues), Audit-DoD (17 Punkte).
  30 REQ-AUDIT-Anforderungen, 6 COM-AUDIT-Gates. SCR-0013 (Harmonisierungen:
  Severity-Aliase CRITICAL..INFO auf kanonisch S0..S4 gemappt, Audit-Lauf-ID auf
  AUD-YYYY-NNNN konsolidiert, Findings im bestehenden F-NNN-System), Owner-Entwurf
  Michael Wroblewski (Builder-Chat 22:15). Status DRAFT — §9-Freigabe ausstehend.
- **Schema:** AUDIT-Familie allockiert (auditStandardId, auditRequirementId,
  auditDomainId, auditGateId, auditRunId, auditStandardDoc).
- **BUG-005:** Planungsreferenz AUD-001 → ATC-STD-AUDIT-001 konsolidiert.

### Fixed

- **S-14-Härtung (SCR-0013):** Registry-Check prüft jetzt per YAML-Parsing gegen die
  standards-Liste statt per Rohtext-Suche. Zuvor meldete S-14 fälschlich PASS für einen
  Eintrag, der außerhalb der Liste (in legacy_series) stand — während der AUDIT-001-
  Registrierung entdeckt und per Negativtest verifiziert (FAIL bei Fehlposition,
  PASS bei korrekter Position).

## [1.4.9] - 2026-09-07

### Changed

- **ERR in Bug integriert (SCR-0012):** ATC-STD-ERR-001 (DRAFT, nie approbiert)
  zurückgezogen und als **ATC-STD-BUG-005** in die Bug-Familie integriert
  (Owner-Entscheid „ERR in Bug einarbeiten", Builder-Chat 22:35). REQ-IDs auf den
  Familienblock REQ-STD-141..164 umgestellt, Gates auf COM-BUG-501..506.
  Bug-Familie damit vollständig: BUG-001 Finding · BUG-002 Documentation ·
  BUG-003 Fix Lifecycle · BUG-004 Merge Gate · BUG-005 Error Analysis/RCA/QMS.
  Schema: err-Familie aufgelöst; errorClassId + rootCauseCategoryId (familienagnostisch)
  und bugComplianceId allockiert. SCR-0011: SUPERSEDED mit Nachtrag.
  Inhalt unverändert — reine Neu-Identifizierung. Status DRAFT — §9-Freigabe ausstehend.

## [1.4.8] - 2026-09-07

### Added

- **ATC-STD-ERR-001 v1.0.0 (DRAFT):** ATC Fehleranalyse- und Root-Cause-Analysis-Standard —
  Analyse-Schicht über dem bestehenden Bug-Lifecycle (BUG-001..004). 18 Fehlerklassen
  (ERR-CL-CODE..GOV), 4-Ebenen-Analyse (Symptom → unmittelbare Ursache → Root Cause →
  systemische Ursache), Five Whys, Fault Tree (S0/S1), Reproduzierbarkeit R0–R3,
  Evidence-Standard, Timeline T0–T9, Impact-Analyse, Regression-Standard, Error Metrics
  (MTTD/MTTA/MTTR/MTTV), Closure Gate mit S0-Zusatzgates, Corrective vs. Preventive
  Action, KI-Agenten-Metadaten, 13 Root-Cause-Kategorien. 24 REQ-ERR-Anforderungen,
  6 COM-ERR-Gates. SCR-0011 (inkl. F-NNN-Konsolidierung: keine separaten
  BUG-/SEC-/SCBUG-/AIBUG-ID-Serien), Owner-Entwurf Michael Wroblewski (Builder-Chat
  22:06). Status DRAFT — §9-Freigabe ausstehend.
- **Schema:** ERR-Familie allockiert (errStandardId, errRequirementId, errErrorClassId,
  errRootCauseCategoryId, errStandardDoc).

## [1.4.7] - 2026-09-07

### Fixed

- **Fehler-Audit (SCR-0010):** COM-ID-Patterns für die DESC- und VERSION-Familie
  ins Schema übernommen (descComplianceId, versionComplianceId). effective_date
  bei DESC-001/VERSION-001 nach APPROVAL gesetzt (reine Metadaten-Komplettierung,
  §30 nicht berührt). Kategorien-Bestand verifiziert: alle 15 genutzten Kategorien
  waren bereits allockiert (erster Scan-Verdacht: Methodik-Fehlalarm des Audit-Skripts;
  kurzzeitig ergänzte Duplikate entfernt).
  Alle übrigen Prüfungen grün: Dateipfade, Orphans, Versions-/Abhängigkeits-Deckung,
  REQ-Abdeckung, SCR-Kontinuität 0001-0010, S-02↔Schema-Synchronität, keine
  Titel-Duplikate.

## [1.4.6] - 2026-09-07

### Changed

- **ATC-STD-DESC-001 + ATC-STD-VERSION-001: APPROVED.** Owner-§9-Sammelfreigabe
  07.09.2026, 21:57 UTC+2 (Builder-Chat). Beide Standards sind ab sofort normativ
  (`normative: true`), eingefroren gemäß ATC-STD-000 §30 — Änderungen nur via SCR.
  Dokumentiert in approval/APPROVAL-DECISION-2026-09-07-DESC-VERSION-v1.0.0.md;
  SCR-0008 und SCR-0009 geschlossen. Registry: 105 Standards, 105 APPROVED, 0 offen.

## [1.4.5] - 2026-09-07

### Added

- **ATC-STD-VERSION-001 v1.0.0 (DRAFT):** ATC Versioning Standard — SemVer 2.0.0,
  Pre-Release-Kette, getrennte Ebenen (Software/API/Protokoll/Konsens/State/Network/
  Contracts/Agents/Doku), Git-Tags, kanonische Versionsquelle, Release-/Build-IDs,
  Release-Manifest, Monorepo-Regel, Kompatibilitäts-Deklaration, Verbotene Praktiken,
  Golden Rule. 22 REQ-VERSION-Anforderungen, 5 COM-VERSION-Gates. SCR-0009,
  Owner-Entwurf Michael Wroblewski (Builder-Chat 21:50). Status DRAFT — §9-Freigabe ausstehend.
- **Schema:** version-Familie allockiert (versionStandardId, versionRequirementId,
  versionStandardDoc); releaseId-Dualformat (versionsbasiert + datumsbasiert);
  buildId-Pattern (ATC-BUILD-NNN) neu.

## [1.4.4] - 2026-09-07

### Added

- **ATC-STD-DESC-001 v1.0.0 (DRAFT):** Standard Description Standard — Pflichtstruktur,
  erweitertes Metadatenmodell, 7-Status-Lifecycle-Mapping auf Registry-Lifecycle,
  14 REQ-DESC-Anforderungen, 5 COM-DESC-Compliance-Gates, Ausnahmeverfahren,
  Quality Gate (17 Kriterien), Maschinenlesbarkeits-Modell. SCR-0008, Owner-Entwurf
  Michael Wroblewski (Builder-Chat 21:42), harmonisiert mit ATC-STD-000 v1.2.0.
  Status DRAFT — Owner-§9-Freigabe ausstehend.
- **Schema:** desc-Familie allockiert (descStandardId, descRequirementId,
  descStandardDoc) gemäß §37 ID-Allokation (AD-034).

## [1.4.3] - 2026-09-07

### Fixed

- **AUD-FIX validate_all:** `file_id()`-Regex erkannte die Präfixe `MD-`, `SC-`,
  `README-` nicht — dadurch wurden 22 Standards (ATC-STD-MD-001,
  ATC-STD-SC-001..020, ATC-STD-README-001) von der CI-Validierung stillschweigend
  übersprungen (81 statt 103 geprüft). Regex um die drei Präfixe erweitert.
- **S-01 Metadaten:** `updated`-Feld in 22 Standard-Headern ergänzt
  (ATC-STD-MD-001, ATC-STD-SC-001..020, ATC-STD-README-001) — alle 103 Standards
  jetzt vollständig S-01-konform.
- **Code-Hygiene:** Doppelter Registry-Cross-Check-Block in `validate_all.py`
  entfernt (Copy-Paste-Duplikat).

### Validation

- Standards-Validierung: **103/103 COMPLIANT** (vorher real 81/103, MASKIERT)
- S-17 Duplicate Detection: PASS · S-18 Registry-Parse: PASS · S-19 Mutation: 12/12

## [1.4.2] - 2026-09-07

### Added

- Owner-Freigabe: ATC-STD-MD-001 v1.0.0 APPROVED (§9, 21:05 UTC+2) —
  ATC Markdown & Documentation Standard normativ in Kraft, Immutabilität
  per §30
- Registry: **103 Standards, 103 APPROVED, 0 offen — GOVERNANCE-KOMPLETT**

## [1.4.1] - 2026-09-07

### Added

- Owner-Freigabe: ATC-STD-SC-001..020 v1.0.0 APPROVED (§9, 21:00 UTC+2)
  — Smart Contract Standards Framework normativ in Kraft, Immutabilität
  per §30; Approval-Dokument in approval/ dokumentiert
- Registry: 102 APPROVED + 1 CANDIDATE (MD-001)

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
