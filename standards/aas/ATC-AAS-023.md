---
standard:
  id: ATC-AAS-023
  title: "ATC-AAS-023 — Agent Role Standard"
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

# ATC-AAS-023 — Agent Role Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Rollenmodell (Least Privilege je Rolle)

```
ORCHESTRATOR (ShivaCore-Systemebene)
    ├── DEV-AGENT     — entwickelt (Scope: src/, tests/)
    ├── TEST-AGENT    — testet (Scope: tests/, CI)
    ├── SEC-AGENT     — prüft Sicherheit (read-all, write: Findings)
    ├── DOC-AGENT     — dokumentiert (Scope: docs/, wiki)
    └── AUDIT-AGENT   — auditiert (read-all, write: AUD/SYNC-Records)
            ↓
      HUMAN REVIEW (Merge/Deploy-Gates, AAS-017)
```

## 2. Regeln

- Jede Rolle ist ein eigener Agent mit eigenem Identity-Manifest (AAS-001),
  eigenen Capabilities (AAS-002) und Permissions (AAS-003) — niemals ein
  einziger Super-Agent mit All-Macht.
- 1-Agent-per-Repo (AI-DEV-012 §1) bleibt bestehen: pro Repo arbeitet zu
  jedem Zeitpunkt genau ein Agent; Orchestrierung verteilt Aufgaben, keine
  parallelen Schreibzugriffe.
- Orchestrierung kommuniziert über das A2A-Protokoll (AAS-024).
