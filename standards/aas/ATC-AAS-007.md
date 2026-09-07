---
standard:
  id: ATC-AAS-007
  title: "ATC-AAS-007 — Agent Task Standard"
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

# ATC-AAS-007 — Agent Task Standard (v1.0.0, CANDIDATE)

> **Status:** CANDIDATE · **Priorität:** P0 · **Erweitert:** ATC-STD-AI-DEV-004 (Task-Record/Lifecycle)

## 1. Feldstruktur (Zusatzfelder zu AI-DEV-004 §1)

```yaml
task_id: ATC-TASK-00427
title: ...
objective: ...                      # messbares Ziel
repository: ...                     # Ziel-Repo (muss im Scope, ATC-AAS-004)
requirements: [REQ-...]             # Verweis auf Anforderungsquellen
dependencies: [ATC-TASK-NNNN]
allowed_files: []                   # Verfeinerung von ATC-AAS-004
forbidden_files: []
acceptance_criteria: []             # prüfbare Kriterien
test_requirements: {}                # Mindest-Validierung, ATC-AAS-011
documentation_requirements: {}      # Sync-Pflicht, AI-DEV-010
status: <AI-DEV-004 §2 Lifecycle>
```

## 2. Regeln

- Task-ID-Format und Allokation unverändert AI-DEV-004 §3 (fortlaufend,
  nie wiederverwendet, ATC-STD-000 §37).
- Datei-Arbeitsbereich einer Task ist die Schnittmenge aus Scope
  (AAS-004) und allowed_files; forbidden_files hat Vorrang.
- COMPLETED nur bei erfüllten acceptance_criteria UND grüner Validierung
  UND Audit-Record (AI-DEV-009).
