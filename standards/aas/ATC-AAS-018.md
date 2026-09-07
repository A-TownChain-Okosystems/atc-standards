---
standard:
  id: ATC-AAS-018
  title: "ATC-AAS-018 — Agent Audit Trail Standard"
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

# ATC-AAS-018 — Agent Audit Trail Standard (v1.0.0, CANDIDATE)

> **Status:** CANDIDATE · **Priorität:** P0 · **Erweitert:** ATC-STD-AI-DEV-009 (Audit-Record AUD-NNN)

## 1. Aktions-Protokollierung

Jede Agenten-Aktion (nicht nur Task-Abschluss) wird protokolliert:

```
timestamp · agent_id · task_id · repository · action · command ·
files_changed · result · risk_level · human_approval
```

## 2. Zweistufiges Modell

- **Aktionsprotokoll** (feingranular, je Operation): maschinenlesbar, in
  `.github/ai/audit/` als Event-Stream je Task
  (`.github/ai/audit/ATC-TASK-NNNN.events.yaml`), append-only.
- **Abschluss-Record AUD-NNN** (AI-DEV-009 §1, unverändert): Zusammenfassung
  bei COMPLETED/CANCELLED/BLOCKED/HANDOVER.

## 3. Regeln

- Beide Ebenen append-only; Korrektur nur per corrects:-Folgercord.
- risk_level: S0-S4 (ATC-STD-BUG-002); S0/S1-Aktionen triggieren
  Human-Approval-Pflicht (AAS-017 §2).
- Anschluss an LogChain/AuditTrail/DefenderGPT-Konzepte erfolgt über die
  Produkt-Repositories (atc-indexer, aurora-ai); dieser Standard definiert
  nur das Protokollformat.
