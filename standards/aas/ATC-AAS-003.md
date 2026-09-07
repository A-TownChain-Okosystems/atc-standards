---
standard:
  id: ATC-AAS-003
  title: "ATC-AAS-003 — Agent Permission Standard"
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
---

# ATC-AAS-003 — Agent Permission Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Berechtigungsstufen

READ · WRITE · EXECUTE · MERGE · DEPLOY · ADMIN. Jede Stufe ist separat
zu erteilen; keine implizite Stufenhierarchie (WRITE beinhaltet NICHT EXECUTE).

## 2. Operationsmatrix (Beispiel Entwicklungsagent)

READ ✓ · WRITE ✓ · TEST ✓ · COMMIT ✓ · PUSH ✓ · PR ✓ ·
MERGE ✗ · DEPLOY ✗ · ADMIN ✗

→ Der Agent entwickelt selbstständig, kann aber keinen Mainnet-Code deployen
und nicht eigenständig mergen (Merge-Gate: AI-DEV-007 §6).

## 3. Eskalation

Merge/Deploy/ADMIN nur per dokumentierter Owner-Freigabe mit Befristung
(AI-DEV-002 §2); nach Ablauf automatische Rückstufung.
