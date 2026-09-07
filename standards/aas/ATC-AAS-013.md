---
standard:
  id: ATC-AAS-013
  title: "ATC-AAS-013 — Agent Conflict Resolution Standard"
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

# ATC-AAS-013 — Agent Conflict Resolution Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Konflikt-Leiter (Welche Quelle gewinnt)

```
Standard > Architecture > Specification > Requirement > Issue > Implementation
```

(konsistent mit der Wahrheits-Priorität, ATC-AAS-006 §2)

## 2. Verfahren

1. Konflikt erkennen (zwei Quellen widersprechen sich in einer Aussage).
2. Konflikt DARF NICHT stillschweigend gelöst werden.
3. Finding F-NNN anlegen (AI-DEV-005; Quelle A vs. B, Fundstellen) — bei
   Standard-Widerspruch zusätzlich SCR-XXXX (ATC-STD-000 §19-§33).
4. Eskalation an Owner, wenn das Finding eine normative Ebene betrifft
   (AI-DEV-011 §2).
5. Arbeit an betroffener Task → BLOCKED bis Konflikt entschieden.

## 3. Short-Circuit

Bei rein inner-tasklichen Widersprüchen (Implementation vs. Issue-Text)
ohne normative Wirkung: dokumentierte Entscheidung nach AI-DEV-006
(observation/decision/reason) ausreichend — kein Finding nötig.
