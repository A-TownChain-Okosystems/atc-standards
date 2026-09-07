---
standard:
  id: ATC-ENT-012
  title: "ATC-ENT-012 — Wissensmanagement & Consistency-Gate Standard"
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

# ATC-ENT-012 — Wissensmanagement & Consistency-Gate Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Kernregel

**Code, Standards, Wiki, Architektur und Roadmap dürfen nicht
auseinanderlaufen.** (AI-DEV-010 §1 als Unternehmensgrundsatz)

## 2. Consistency Gate (Release-blockierend)

```
CODE CHANGE
  ├── Wiki  ├── Architecture  ├── Standards  ├── API Specification
  ├── Roadmap  └── Changelog
        ↓
  CONSISTENCY CHECK → PASS: RELEASE | FAIL: BLOCK
```

FAIL blockiert den Release (Merge-Gate AI-DEV-007 §6); Abweichungen
werden synchronisiert (SYNC-NNNN, BUG-004) oder als BLOCKED mit
Finding dokumentiert. Kein „Release jetzt, Doku später".

## 3. Wissensarchive (SSOT-Kette)

registry/*.yaml (Standards, Abhängigkeiten, Versionen, Org, Repos,
Risiken) = Maschinen-SSOT → abgeleitete Sichten (STANDARDS_REGISTRY.md,
Wiki, Notion, Roadmap). Generierte Sichten sind als abgeleitet markiert
(F-005-Präzedenz); Änderungen an Sichten ohne SSOT-Update sind ungültig.

## 4. Automatisierung

Wiederkehrende Konsistenzprüfungen sind als Workflow/Automatisierung
umzusetzen (AI-DEV-010 §4); Ausnahmen dokumentiert begründen.
