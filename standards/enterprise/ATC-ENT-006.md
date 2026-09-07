---
standard:
  id: ATC-ENT-006
  title: "ATC-ENT-006 — Interessenkonflikte Standard"
  version: "1.0.0"
  status: candidate
  category: enterprise
  authority: A-TownChain Ecosystems
  owner: ShivaCoreDev
  created: "2026-09-07"
  updated: "2026-09-07"
  normative: true
  supersedes: []
  superseded_by: null
---

# ATC-ENT-006 — Interessenkonflikte Standard (v1.0.0, CANDIDATE)

> **Status:** CANDIDATE · **Priorität:** P2 · **Basiert auf:** ENT-002, ENT-003

## 1. Konfliktklassen

Rollen-Kumulation (Autor ≠ Approver für dieselbe Entscheidung), wirtschaftliche
Interessen, emotionale/verantwortliche Doppelpflichten, Agenten-Zielkonflikte
(Task-Ziel vs. Governance-Regel).

## 2. Kernregeln

- Wer eine Entscheidung vorbereitet (Autor/Agent), ist nicht deren Approver
  (Verfassung §14.1; Agenten nie Approver).
- Bei erkanntem Konflikt: Offenlegung im DEC-Record vor der Entscheidung;
  Entscheider entscheidet über Abgabe der Entscheidung an nächsthöhere Rolle.
- Agenten-Zielkonflikte: Task-Ziel verliert gegen Governance — Eskalation
  nach AI-DEV-011 §2, Dokumentation als Finding.

## 3. Dokumentation

Konflikt-Fälle fließen in den Audit-Trail (ENT-014, Feld `conflict_flag`)
und den KPI-Report (ENT-013, Human Escalation Rate).
