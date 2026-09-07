---
standard:
  id: ATC-ENT-003
  title: "ATC-ENT-003 — Entscheidungsmanagement Standard"
  version: "1.0.0"
  status: approved
  category: enterprise
  authority: A-TownChain Ecosystems
  owner: ShivaCoreDev
  created: "2026-09-07"
  updated: "2026-09-07"
  normative: true
  supersedes: []
  superseded_by: null
---

# ATC-ENT-003 — Entscheidungsmanagement Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Kernregel

**Jede kritische Entscheidung muss einen Verantwortlichen, einen Status,
eine Begründung und eine nachvollziehbare Historie besitzen.** Keine
kritische Architekturentscheidung darf „irgendwo im Chat verschwinden".

## 2. Decision Record (DEC-NNNN)

```
DEC-0001
├── Problem
├── Optionen
├── Bewertung
├── Entscheidung
├── Verantwortlicher (ROLE-XXX)
├── Datum
├── Auswirkungen
├── Abhängigkeiten (DEC-/SCR-/Standard-Referenzen)
└── Review-Date
```

## 3. Status-Lifecycle

PROPOSED → UNDER_REVIEW → APPROVED | REJECTED → SUPERSEDED → ARCHIVED.

## 4. Verhältnis zu bestehenden Instrumenten

- Freigaben normativer Standards: unverändert ATC-STD-000 §9 mit
  approval/APPROVAL-DECISION-*.md (diese SIND DEC-Records in
  Kanon-Form; künftig zusätzlich DEC-ID vergeben).
- Bestands-Entscheidungen AD-016..AD-046 (Owner-Mandate, AGENT_MANIFEST)
  bleiben gültig und werden als DEC-Records anerkannt (grandfathered,
  keine Rückmigration erzwungen).
- SCR-XXXX (Standard-Änderungen): formale Änderungsspur bleibt SCR;
  DEC deckt Organisations-/Produkt-/Architektur-Entscheidungen ab.
- Priorisierungskonflikte zwischen Entscheidungen → AAS-013.
