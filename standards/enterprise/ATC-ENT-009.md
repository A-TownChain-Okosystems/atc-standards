---
standard:
  id: ATC-ENT-009
  title: "ATC-ENT-009 — Repository Governance Standard"
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

# ATC-ENT-009 — Repository Governance Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## Abstract

ATC-ENT-009 (Repository Governance Standard) — Owner-Sammelfreigabe 07.09.2026 20:20 UTC+2 (alles freigeben): CANDIDATE -> APPROVED, normativ in Kraft; dokumentiert in approval/APPROVAL-DECISION-2026-09-07-AAS-ENT-AUDIT.md.
Normative Aussagen sind verbindlich (MUSS/SOLLTE/DARF im Sinne von RFC 2119).

## Scope

**Scope:** Gilt für: Organisationsebene von A-TownChain Ökosystems — oberhalb der technischen Familien, unterhalb der Verfassung ATC-STD-000.
Nicht-Gilt: normative Standardtexte (Änderungen via SCR, ATC-STD-000 §19-33); technische Domäneninhalte (NET/ZKP/AI-DEV).

## 1. Unternehmens-Repo-Registry (Pflichtfelder)

```yaml
repository:
  id: REPO-001
  name: atc-core
  domain: blockchain              # ENT-008-Einheit
  owner: ROLE-ARCH                # fachlich
  technical_owner: ROLE-DEV
  security_owner: ROLE-CISO
  classification: INTERNAL        # PUBLIC|INTERNAL|RESTRICTED
  canonical: true                 # kanonische Ablage (keine Fork-Divergenz)
  standards: [ATC-STD-000, ATC-STD-201, ATC-STD-203, ATC-AAS-025]
  documentation: {wiki: required, readme: required, architecture: required}
```

## 2. Regeln

- Ein Repository ohne Registry-Eintrag hat keinen Unternehmensstatus;
  neue Repos über ENT-010 + §37 ID-Allokation (REPO-NNN fortlaufend).
- `canonical: true` markiert die SSOT-Ablage; Sync-Ziele (Wiki, Docs)
  sind abgeleitet (BUG-004, AI-DEV-010).
- Dokumentations-Pflichten sind Merge-Gate-relevant (Consistency-Gate,
  ENT-012 §2): fehlende Pflicht-Doku blockiert Release.
- Überschneidungsfreie Zuständigkeit: ein Repo = eine Organisationseinheit
  = ein zuständiger Agent (1-Agent-per-Repo, AI-DEV-012 §1).

## 3. Rollout

Nach APPROVED: `registry/org-units.yaml` + `registry/repositories.yaml`
als ableitende Sichten aus der existierenden 26-Repo-Struktur generieren;
Zuordnung mit bestehender AgentAssignment-DB verzahnen.
