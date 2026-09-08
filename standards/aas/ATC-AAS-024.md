---
standard:
  id: ATC-AAS-024
  title: "ATC-AAS-024 — Agent-to-Agent Protocol Standard"
  version: "1.0.0"
  status: approved
  category: aas
  authority: A-TownChain Ecosystems
  owner: ShivaCoreDev
  created: "2026-09-07"
  updated: "2026-09-07"
  normative: true
  supersedes: []
  superseded_by: null
  effective_date: "2026-09-07"
  review_date: "2027-09-08"
  license: "Copyright (c) 2026 Michael Wroblewski"
---

# ATC-AAS-024 — Agent-to-Agent Protocol Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## Abstract

ATC-AAS-024 (Agent-to-Agent Protocol Standard) — Owner-Sammelfreigabe 07.09.2026 20:20 UTC+2 (alles freigeben): CANDIDATE -> APPROVED, normativ in Kraft; dokumentiert in approval/APPROVAL-DECISION-2026-09-07-AAS-ENT-AUDIT.md.
Normative Aussagen sind verbindlich (MUSS/SOLLTE/DARF im Sinne von RFC 2119).

## Scope

**Scope:** Gilt für: alle KI-Agenten der A-TownChain-Organisation und deren Betrieb in sämtlichen R2+-Repositories (Identität bis Repository-Manifest).
Nicht-Gilt: menschliche Rollen (ATC-ENT-002); Mainnet-Betrieb (ATC-STD-NET).

## 1. Nachrichtentypen

AGENT→TASK · AGENT→FINDING · AGENT→RESULT · AGENT→REQUEST ·
AGENT→HANDOFF · AGENT→BLOCKER · AGENT→REVIEW.

## 2. Nachrichtenstruktur (Pflichtfelder)

```yaml
message_id: A2A-000001         # fortlaufend, nie wiederverwendet (§37)
sender_agent: ATC-AI-DEV-001
receiver_agent: ATC-AI-TEST-001
task_id: ATC-TASK-00427
timestamp: "<ISO-8601>"
message_type: AGENT->RESULT
payload: {...}
evidence: [F-NNN / AUD-NNN / CI-Run]
priority: P0|P1|P2
```

## 3. Regeln

- Nachrichten sind persistente Artefakte (`.github/ai/messages/` je Repo,
  append-only) — kein flüchtiger Chat-Kanal.
- Jede Nachricht referenziert Evidenz (AAS-010) und Task (AI-DEV-004).
- Antwortpflicht: BLOCKER- und REQUEST-Nachrichten beantwortet der
  Empfänger mit RESULT oder BLOCKED — niemals Schweigen (Timeout = Eskalation
  an Owner, AI-DEV-011 §2).
