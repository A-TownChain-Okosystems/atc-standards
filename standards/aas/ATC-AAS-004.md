---
standard:
  id: ATC-AAS-004
  title: "ATC-AAS-004 — Agent Scope Standard"
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

# ATC-AAS-004 — Agent Scope Standard (v1.0.0, CANDIDATE)

> **Status:** CANDIDATE · **Priorität:** P0 · **Neu** (verfeinert AI-DEV-002 Berechtigungen auf Verzeichnisebene)

## 1. Arbeitsbereich-Definition

```yaml
scope:
  repositories: [atclang, atc-vm]
  directories: [src/, tests/]
  excluded:
    - .github/secrets/
    - production/
    - infrastructure/mainnet/
```

## 2. Regeln

- Zugriffe (read wie write) außerhalb `scope` sind verboten; `excluded`
  blockiert selbst bei sonst erlaubtem Repository/Pfad.
- Scope ist Teil des Identity-Manifests (ATC-AAS-001 §1) und je Task
  als `allowed_files`/`forbidden_files` weiter verfeinerbar (ATC-AAS-007).
- Scope-Überschreitung = Governance-Verstoß → sofortiges Anhalten, Finding
  (AI-DEV-005), BLOCKED (ATC-AAS-020).

## 3. Zweck

Blast-Radius-Begrenzung: Ein Entwicklungsagent kann andere Systeme nicht
versehentlich verändern.
