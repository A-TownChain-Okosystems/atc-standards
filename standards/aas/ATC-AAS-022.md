---
standard:
  id: ATC-AAS-022
  title: "ATC-AAS-022 — Agent Versioning Standard"
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
  effective_date: "2026-09-07"
  review_date: "2027-09-08"
  license: "Copyright (c) 2026 Michael Wroblewski"
---

# ATC-AAS-022 — Agent Versioning Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## Abstract

ATC-AAS-022 (Agent Versioning Standard) — Owner-Sammelfreigabe 07.09.2026 20:20 UTC+2 (alles freigeben): CANDIDATE -> APPROVED, normativ in Kraft; dokumentiert in approval/APPROVAL-DECISION-2026-09-07-AAS-ENT-AUDIT.md.
Normative Aussagen sind verbindlich (MUSS/SOLLTE/DARF im Sinne von RFC 2119).

## Scope

**Scope:** Gilt für: alle KI-Agenten der A-TownChain-Organisation und deren Betrieb in sämtlichen R2+-Repositories (Identität bis Repository-Manifest).
Nicht-Gilt: menschliche Rollen (ATC-ENT-002); Mainnet-Betrieb (ATC-STD-NET).

## 1. Schema

Agenten sind SemVer-versioniert: `ATC-AI-DEV-001 v1.0.0`. Rollen-Familien
aus AI-DEV-001 §2: DEV, TEST, SEC, DOC, AUDIT (je NNN fortlaufend,
ATC-STD-000 §37).

## 2. Revisionssicherheit

- Änderung an Agenten-Instruktionen (`instructions.md`, AAS-005 §2) =
  Versions-Bump (MINOR bei Erweiterung, PATCH bei Korrektur, MAJOR bei
  Capability/Permission-Änderung).
- Jede `agent_version` ist im Identity-Manifest und je Task/Commit/PR/
  Audit-Record referenziert (AI-DEV-007 §1 Trailer, AI-DEV-009 §1).

## 3. Lifecycle

ACTIVE → DEPRECATED (keine neuen Tasks) → RETIRED (nur Lesen der Historie).
MAJOR-Wechsel erfordert neue Capability-Prüfung (AAS-002); Retirement wird
im AGENT_MANIFEST dokumentiert und KPI-Historie bleibt erhalten.
