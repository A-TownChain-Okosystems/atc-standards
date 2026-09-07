---
standard:
  id: ATC-AAS-010
  title: "ATC-AAS-010 — Agent Evidence Standard"
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

# ATC-AAS-010 — Agent Evidence Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Test-Evidenzblock (Pflichtstruktur)

```yaml
tests:
  command: cargo test --workspace
  result: PASS
  tests_total: 184
  passed: 184
  failed: 0
  ci_run: "#1234"              # Pflicht: nachvollziehbarer CI-Run
  timestamp: "<ISO-8601>"
```

## 2. Kernregel

Eine KI-Aussage ohne Evidenz ist eine Behauptung. „Tests erfolgreich" ohne
Command + CI-Run + Zahlen ist ungültig (AI-DEV-008 §2: „PASS ohne Run"
gilt nicht).

## 3. Evidenzklassen (Vertrauensniveau absteigend)

CI-Run-Artefakt > Repository-Datei (mit Fundstelle) > Issue/PR-Text >
externes Dokument. Jede Evidenz nennt Fundstelle und Erhebungszeitpunkt
(AI-DEV-005 §2).
