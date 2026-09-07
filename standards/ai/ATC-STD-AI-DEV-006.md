---
standard:
  id: ATC-STD-AI-DEV-006
  title: "ATC-STD-AI-DEV-006 — AI Decision & Action Standard"
  version: "1.0.0"
  status: approved
  category: ai-dev
  authority: A-TownChain Ecosystems
  owner: ShivaCoreDev
  created: "2026-09-07"
  updated: "2026-09-07"
  normative: true
  supersedes: []
  superseded_by: null
---

# ATC-STD-AI-DEV-006 — AI Decision & Action Standard (v1.0.0, APPROVED)

> **Status:** APPROVED — Owner-Sammelfreigabe 07.09.2026 (ATC-STD-000 §9)
> **Reihe:** ATC-STD-AI-DEV-001…012 · **Basiert auf:** AI-DEV-001 §9 (OBSERVATION vs. DECISION), §8 (Actions)

## 1. Trennungsgrundsatz

Jede Entscheidung besteht aus drei getrennten Feldern:
- `observation`: Verifizierter Sachverhalt (mit Fundstelle, AI-DEV-005 §2)
- `decision`: Die daraus abgeleitete Handlung
- `reason`: Warum — mit REQ-/Standard-/Task-Bezug

Eine Modellannahme wird nie als Fakt behandelt; Fakt und Annahme sind
unterschieden (`based_on: evidence` vs. `based_on: ASSUMPTION-ANNN`).

## 2. Action-Struktur (ACT-NNN)

`{id, based_on: [F-NNN], action_type, target, objective, reason,
depends_on: [ACT-NNN], required_before, completion_condition}` —
IDs fortlaufend je Task, nie wiederverwendet.

## 3. Next-Action-Pflicht

Nach jeder abgeschlossenen Aktion existiert eine explizite `next_action`
(AI-DEV-001 §8) oder der Task ist COMPLETED mit Audit-Record (AI-DEV-009).
Implizite "weiter sehen wir dann" ist unzulässig.

## 4. Entscheidungsverbund

Autonome Code-Änderungen ohne dokumentierte Entscheidung+reason sind
Governance-Verstoß. Bei Unsicherheit: ASSUMPTION-Register + ggf. Eskalation
an Owner (AI-DEV-011 §2).
