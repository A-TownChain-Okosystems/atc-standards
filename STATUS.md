# STATUS — atc-standards

Stand: 07.09.2026, 15:00 (Europe/Berlin)

## Standards-System

| Standard | Version | Status | Naechster Schritt |
|---|---|---|---|
| ATC-STD-000 (Verfassung) | 1.0.0 | CANDIDATE | Owner-Approval -> APPROVED -> STABLE |
| ATC-STD-201 Structure | 1.0.1 | draft | Review-Passage + Co-Approval |
| ATC-STD-202 Naming | 1.0.1 | proposed | Review-Passage + Co-Approval |
| ATC-STD-203 Security | 1.0.1 | proposed | Review-Passage + Co-Approval |
| ATC-01…99 / ATC-0001…0008 / ATS-1000…1007 | Legacy | final (historisch) | Aenderungen nur via ATC-STD-000 |

## Review- und Change-Status

- ATC-STD-000 v1.0.0: Review-Chain 3/3 PASS (07.09., gegen die Owner-
  Formalfassung, 35 Abschnitte). Approval BLOCKED -> Owner.
- SCR-0001 (ID-Allokation): PROPOSED/PENDING. SCR-0002: OBSOLETE (durch §22
  aufgeloest). SCR-0003 (§33-Integritaet): PENDING, CODEOWNERS angelegt,
  Branch-Absicherung wartet auf Owner-Option A/B. SCR-0004 (Rollenmodell):
  PENDING.

## Infrastruktur

- CI: Repository-Audit (16/16 PASS, Score 100) + Standard-Validation (4/4
  COMPLIANT) bei jedem Push. Validatoren: atc-repo-audit v0.1.0,
  atc-std-validator v0.1.0.

## Metriken

- 119 Standard-Dokumente + Verfassung; 5 Registry-, 7 Schema-, 6 Template-
  Dateien; 2 Tools; 23 Repos in repositories.yaml.
