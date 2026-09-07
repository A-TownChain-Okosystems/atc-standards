# STATUS — atc-standards

Stand: 07.09.2026, 20:30 (Europe/Berlin) · Self-Compliance: R3 100/100 GATE PASS

## Standards-System

| Ebene | Umfang | Status |
|---|---|---|
| Verfassung ATC-STD-000 | v1.2.0 | APPROVED, normativ, eingefroren (§30) |
| ATC-STD-AI-DEV-001..012 | AI-DEV-Familie (007: v1.0.1 per SCR-0006) | APPROVED |
| ATC-AAS-001..025 | AI Agent Standards (P0/P1/P2) | APPROVED |
| ATC-ENT-001..015 | Enterprise Standards Layer | APPROVED |
| ATC-STD-100/201-204/300 | Repository/Development/Architecture | APPROVED |
| ATC-STD-BUG-001..004 | Bug & Konsistenz | APPROVED |
| ATC-STD-NET-001..008 | Netzwerk-Umgebungen | APPROVED |
| ATC-STD-ZKP-001..010 | ZKP-Layer | APPROVED |
| ATC-STD-README-001 | README als Einstiegsschnittstelle (REQ-README-001..015, Gates README-01..13) | APPROVED — normativ in Kraft (07.09., 20:36) |
| ATC-STD-MD-001 | ATC Markdown & Documentation Standard (REQ-MD-001..016, Gates MD-01..10) | CANDIDATE — §9-Freigabe ausstehend (Todo #117) |
| ATC-STD-SC-001..020 | ATC Smart Contract Standards Framework (Kategorien, Gates SC-G0..G13, Contract Registry) | CANDIDATE — §9-Freigabe ausstehend (Todo #118) |
| **Summe** | **103 Standards** | **82 APPROVED + 21 CANDIDATE** |

## Qualitätssicherung (CI, self-compliant)

- Standards-Validierung: **103/103 COMPLIANT** (82 APPROVED + 21 CANDIDATE: MD-001 + SC-001..020)
- Mutationssuite S-19: **12/12** (synthetische Fixtures)
- Repository-Audit R3: **100/100, GATE PASS** · README-Gate: **13/13 CONFORM** · MD-Gate: **CONFORM** · Contract-Registry-Gate: **CONFORM**
- Abhängigkeitsgraph: 81 Knoten, azyklisch (DAG)

## Offene Punkte

| ID | Thema | Zuständigkeit |
|---|---|---|
| F-017 / SCR-0007 | REQ-ID-Rollout AI-DEV/AAS/ENT (§9-Reststruktur) | Owner-Entscheidung, Frist 07.10.2026 |
| F-009/F-010 | workflow-Scope-Token für CI-Fix | Owner-Aktion |
| #111 | Repo-Manifeste .github/ai/ in allen R2+-Repos | Agenten (atc-standards: erledigt — Vorreiter) |
| #116 | README-Konformitäts-Rollout auf 26 Repos (§9-Freigabe 07.09. erledigt) | Agenten, Frist 07.10.2026 |
| #117 | ATC-STD-MD-001 §9-Freigabe + MD-Konformitäts-Rollout auf 26 Repos | Owner + Agenten |
| #118 | ATC-STD-SC-001..020 §9-Freigabe + SC-Gate-Rollout auf Contract-Repos + Registry-Befüllung | Owner + Agenten |
| #112 | Commit-Trailer-Rollout | Agenten, Frist 07.10.2026 |
| IFC-0001..0010 | Interface-Test-Suiten (P0) | Agenten, Frist 07.10.2026 |
