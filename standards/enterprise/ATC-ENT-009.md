---
standard:
  id: ATC-ENT-009
  title: "ATC-ENT-009 — Repository Governance Standard"
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

# ATC-ENT-009 — Repository Governance Standard (v1.0.0, CANDIDATE)

> **Status:** CANDIDATE · **Priorität:** P1 · **Erweitert:** ATC-STD-201/202 (Struktur/Naming), AAS-025 (Repo-Manifest .github/ai/)

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
