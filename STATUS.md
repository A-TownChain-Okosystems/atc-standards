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
| **Summe** | **82 Standards** | **82 APPROVED, 0 offen** |

## Qualitätssicherung (CI, self-compliant)

- Standards-Validierung: **82/82 COMPLIANT** (82 APPROVED, 0 offen)
- Mutationssuite S-19: **12/12** (synthetische Fixtures)
- Repository-Audit R3: **100/100, GATE PASS** · README-Gate: **13/13 CONFORM**
- Abhängigkeitsgraph: 81 Knoten, azyklisch (DAG)

## Offene Punkte

| ID | Thema | Zuständigkeit |
|---|---|---|
| F-017 / SCR-0007 | REQ-ID-Rollout AI-DEV/AAS/ENT (§9-Reststruktur) | Owner-Entscheidung, Frist 07.10.2026 |
| F-009/F-010 | workflow-Scope-Token für CI-Fix | Owner-Aktion |
| #111 | Repo-Manifeste .github/ai/ in allen R2+-Repos | Agenten (atc-standards: erledigt — Vorreiter) |
| #116 | README-Konformitäts-Rollout auf 26 Repos (§9-Freigabe 07.09. erledigt) | Agenten, Frist 07.10.2026 |
| #112 | Commit-Trailer-Rollout | Agenten, Frist 07.10.2026 |
| IFC-0001..0010 | Interface-Test-Suiten (P0) | Agenten, Frist 07.10.2026 |
