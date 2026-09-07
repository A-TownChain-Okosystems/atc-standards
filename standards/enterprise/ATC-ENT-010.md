---
standard:
  id: ATC-ENT-010
  title: "ATC-ENT-010 — Enterprise Change Management Standard"
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

# ATC-ENT-010 — Enterprise Change Management Standard (v1.0.0, CANDIDATE)

> **Status:** CANDIDATE · **Priorität:** P0 · **Erweitert:** ATC-STD-000 §19-33 (SCR, Standard-Änderungen) auf Organisations-/Architektur-/Richtlinien-Änderungen

## 1. Change-Pipeline (Pflichtreihenfolge)

```
CHANGE REQUEST → IMPACT ANALYSIS → TECHNICAL REVIEW → SECURITY REVIEW →
APPROVAL → IMPLEMENTATION → TEST → AUDIT → DOCUMENTATION UPDATE → RELEASE
```

Keine Ausnahmeschritte; Parallelisierung nur zwischen den Reviews.

## 2. Änderungsklassen

- Standards: unverändert SCR (ATC-STD-000 §19-33) — SCR bleibt die
  formale Änderungsspur für normative Texte.
- Organisation (Rollen, Einheiten, Zuständigkeiten): ENT-010 mit
  DEC-Record (ENT-003) + Registry-Update.
- Architektur/Produkt: ENT-010 mit Impact auf Dependency-Graph
  (ATC-STD-204) + betroffene Interface-Tests (IFC-NNNN).
- Richtlinien: ENT-010 §-Pipeline mit POL-Update (ENT-005).

## 3. Impact-Analyse (Pflichtinhalte)

Betroffene Repos (ENT-009), Standards, Interfaces (ATC-STD-204),
Risiken (ENT-011), Abhängigkeiten, Migrations-/Rollback-Plan
(Rollback-Pflicht nach AAS-009 §1).

## 4. Notfall-Änderung (Emergency)

Wie Verfassung §32: nachgelagerte Dokumentation binnen 72h, volle
Pipeline rückwirkend; Owner-Benachrichtigung sofort. Kein Stillstand
kritischer Systeme erzwingbar.
