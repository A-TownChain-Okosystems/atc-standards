---
standard:
  id: ATC-AAS-021
  title: "ATC-AAS-021 — Agent Quality Standard"
  version: "1.0.0"
  status: candidate
  category: aas
  authority: A-TownChain Ecosystems
  owner: ShivaCoreDev
  created: "2026-09-07"
  updated: "2026-09-07"
  normative: true
  supersedes: []
  superseded_by: null
---

# ATC-AAS-021 — Agent Quality Standard (v1.0.0, CANDIDATE)

> **Status:** CANDIDATE · **Priorität:** P2 · **Neu**

## 1. KPIs je Agent (aus Audit-Records ableitbar)

| KPI | Bedeutung |
|---|---|
| Task Success Rate | erfolgreiche Aufgaben / alle Aufgaben |
| Test Pass Rate | bestandene Tests / ausgeführte Tests |
| Regression Rate | verursachte Regressionen |
| Rework Rate | nachträgliche Korrekturen an eigener Arbeit |
| Security Findings | S0/S1-Findings des Agenten |
| Documentation Compliance | Sync-Pflicht-Erfüllung (AI-DEV-010) |
| False Claim Rate | unbelegte Behauptungen (AAS-012-Verstöße) |
| Human Escalation Rate | notwendige Eskalationen |

## 2. Erhebung

Automatisch aus Task-/Audit-Records (AI-DEV-004/009) und dem
Aktionsprotokoll (AAS-018); kein manuelles Scoring. Report je Agent
an den Owner (kadenz: monatlich, automatisierbar über Workflow).

## 3. Konsequenzen

False-Claim-Rate > 0 oder Security-Findings S0 → Capability-Review
(AAS-002 §1) und ggf. Deaktivierung (AAS-022 §3 Retirement).
