# STATUS — atc-standards

Stand: 07.09.2026, 17:15 (Europe/Berlin)

## Standards-System

| Standard | Version | Status | Naechster Schritt |
|---|---|---|---|
| ATC-STD-000 (Verfassung) | 1.1.0 | APPROVED (07.09., Owner-Freigabe; Release+Tag v1.1.0) | STABLE nach Bewaehrung (§9) |
| ATC-STD-201 Structure | 1.0.1 | draft | Review-Passage + Co-Approval |
| ATC-STD-202 Naming | 1.0.1 | proposed | Review-Passage + Co-Approval |
| ATC-STD-203 Security | 1.0.1 | proposed | Review-Passage + Co-Approval |
| ATC-01…99 / ATC-0001…0008 / ATS-1000…1007 | Legacy | final (historisch) | Aenderungen nur via ATC-STD-000 |
| ATC-STD-BUG-001 | 1.0.0 | candidate (Owner-Mandat) | Live-Uebung: Findings nach G2/Parser-Bug |
| ATC-STD-BUG-002 | 1.0.0 | candidate (Owner-Mandat) | Vorlage genutzt ab naechstem Finding |
| ATC-STD-BUG-003 | 1.0.0 | candidate (Owner-Mandat) | SCR-Verkettung ab naechstem Fix |
| ATC-STD-BUG-004 | 1.0.0 | candidate (Owner-Mandat) | Merge-Gate: SYNC-Nachweis-Pflicht |
| ATC-STD-NET-001 | 1.0.0 | candidate (Owner-Mandat) | Devnet-Betrieb ab M4 |
| ATC-STD-NET-002 | 1.0.0 | candidate (Owner-Mandat) | Testnet nach Devnet-GATE-011 |
| ATC-STD-NET-003 | 1.0.0 | candidate (Owner-Mandat) | Mainnet nur via GATE-013 |
| ATC-STD-NET-004 | 1.0.0 | candidate (Owner-Mandat) | Pipeline: GATE-011/012/013 |
| ATC-STD-NET-005 | 1.0.0 | candidate (Owner-Mandat) | registry/networks.yaml aktiv |
| ATC-STD-NET-006 | 1.0.0 | candidate (Owner-Mandat) | Erste Anwendung: Protokoll-Upgrades |
| ATC-STD-NET-007 | 1.0.0 | candidate (Owner-Mandat) | Matrix mit GATE-012/013 verdrahtet |
| ATC-STD-NET-008 | 1.0.0 | candidate (Owner-Mandat) | Recovery-Tests vor Promotion |

## Review- und Change-Status

- ATC-STD-000 v1.1.0: APPROVED (07.09., Owner-Freigabe Michael; Review-Chain
  3/3 PASS, REQ-Matrix 21/21). Release v1.1.0 + immutables Tag erstellt.
- SCR-0001 (ID-Allokation): PROPOSED/PENDING. SCR-0002: OBSOLETE (durch §23
  aufgeloest). SCR-0003 (Branch/Tag-Integritaet): CLOSED — Branch-Protection
  aktiv (Option B), Tag-Ruleset immutable-release-tags, Secret-Scanning +
  Push-Protection enabled. SCR-0004 (Rollenmodell): CLOSED — §14.1 in v1.1.0.
- ATC-STD-300 (Development & PM Standard, DTC): candidate v1.0.0, wartet auf
  Owner-Freigabe (ATC-STD-000 §9).
- ATC-STD-SELF-001 (Self-Governance): VORSCHLAG (07.09.), nicht priorisiert —
  erst nach Governance-Freeze.

## Infrastruktur

- CI: Repository-Audit (16/16 PASS, Score 100) + Standard-Validation (17/17
  COMPLIANT, registry-getrieben) bei jedem Push. Neuer Check S-19:
  Header-/Frontmatter-/Registry-Versions-Sync. Validatoren: atc-repo-audit v0.1.0,
  atc-std-validator v0.2.0 (S-16 schema-basiert) + validate_all.py (S-17 Duplicate Detection) + CI naming-governance.yml.

## Metriken

- 119 Standard-Dokumente + Verfassung; 6 Registry-, 7 Schema-, 6 Template-
  Dateien; 2 Tools; 26 Repos in repositories.yaml.
