---
standard:
  id: ATC-AAS-008
  title: "ATC-AAS-008 — Agent Workflow Standard"
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

# ATC-AAS-008 — Agent Workflow Standard (v1.0.0, CANDIDATE)

> **Status:** CANDIDATE · **Priorität:** P0 · **Konkretisiert:** ATC-STD-AI-DEV-001 §7 (State Machine), AI-DEV-007 (Git/PR)

## 1. Makro-Lifecycle (Pflichtreihenfolge)

```
DISCOVER → UNDERSTAND → PLAN → IMPLEMENT → TEST → AUDIT → DOCUMENT →
REVIEW → COMMIT → PULL REQUEST → HUMAN APPROVAL → MERGE
```

## 2. Mapping auf die State Machine (AI-DEV-001 §7)

DISCOVER/UNDERSTAND = DISCOVERING · PLAN/IMPLEMENT = IMPLEMENTING ·
TEST/VALIDIERUNG = TESTING/VALIDATING · AUDIT = AUDITING ·
COMMIT/PR/HUMAN APPROVAL/MERGE = Git-Gates aus AI-DEV-007 (§1-§6).
Rücksprünge: TEST→IMPLEMENT (FAIL), REVIEW→IMPLEMENT (CHANGES_REQUESTED),
jede Stufe → BLOCKED (ATC-AAS-020).

## 3. Schrittklassen (Teilschritt der betroffenen Makro-Stufe)

DISCOVER → UNDERSTAND → PLAN → IMPLEMENT → TEST → AUDIT → DOCUMENT →
REVIEW → COMMIT → PULL REQUEST → HUMAN APPROVAL → MERGE — kein
Stufenübergang ohne dokumentierten Stufenwechsel im Task-Record
(`history`, AI-DEV-004 §2).
