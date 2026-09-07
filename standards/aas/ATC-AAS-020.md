---
standard:
  id: ATC-AAS-020
  title: "ATC-AAS-020 — Agent Failure Standard"
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

# ATC-AAS-020 — Agent Failure Standard (v1.0.0, CANDIDATE)

> **Status:** CANDIDATE · **Priorität:** P1 · **Neu**

## 1. Fehlerzustände

```
FAILED             — Ausführung fehlgeschlagen
BLOCKED            — extern/philosophisch blockiert (Finding, Konflikt, Frist)
NEEDS-HUMAN        — Owner-Entscheidung zwingend (AI-DEV-011 §2)
ROLLBACK-REQUIRED  — Änderung hat System instabil gemacht (AAS-009 Rollback)
```

## 2. Schleifenvermeidung (Pflicht)

```yaml
max_attempts: 3
after_3_failures:
  - create_finding      # F-NNN mit Evidenz (AI-DEV-005)
  - stop_task           # Status BLOCKED, keine Wiederholung
  - request_human_review
```

Keine Endlosschleifen: Jeder Wiederholungsversuch ist im Task-Record
protokolliert; nach `max_attempts` ist Autonomie für diese Task beendet.

## 3. ROLLBACK-REQUIRED

Sofortige Eskalation (S1), Ausführung des dokumentierten Rollbacks
(AAS-009 §1 ROLLBACK) nach Owner- oder Rollback-Standard-Freigabe,
Finding mit Ursachenanalyse (AI-DEV-006: observation/decision/reason).
