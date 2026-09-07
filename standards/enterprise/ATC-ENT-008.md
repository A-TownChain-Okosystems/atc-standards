---
standard:
  id: ATC-ENT-008
  title: "ATC-ENT-008 — Organisationsstruktur Standard"
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

# ATC-ENT-008 — Organisationsstruktur Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Organisationshierarchie (verbindlich)

```
A-TownChain Ökosystems
├── Executive / Governance
├── Architecture
├── Blockchain (L1, Consensus, ZKP, Token, Interoperability)
├── Software Engineering (Backend, Frontend, Infrastructure, QA)
├── AI Engineering (AI Agents, Model Infrastructure, Agent Governance, AI Security)
├── Security
├── DevOps / Infrastructure
├── Game / GameFi
├── Wallet / DeFi
├── Marketplace
├── Documentation / Wiki
└── Compliance / Audit
```

## 2. Pflichtattribute je Organisationseinheit (Registry `registry/org-units.yaml`)

```yaml
org_unit:
  id: UNIT-BLOCKCHAIN
  name: Blockchain
  owner: ROLE-ARCH          # ENT-002-Rolle
  deputy: ROLE-DEV
  responsibility: "..."
  permissions: [...]        # abgeleitet aus ENT-004
  kpis: [...]               # ENT-013
  repositories: [atc-blockchain, atc-node, atc-zkp]   # ENT-009
  standards: [ATC-STD-NET-003, ATC-STD-ZKP-001]       # required
  documentation: {...}       # Wiki/Architektur-Pflichten
  audit_requirements: {...}  # ENT-014
```

## 3. Regeln

- Jedes Repository gehört zu genau einer Organisationseinheit (Mapping in
  ENT-009 Repo-Registry); jede Einheit hat Owner UND Deputy.
- 26 aktive Repos: Zuordnung bestehender 5-Produktlinien-Struktur
  (Governance, Docs, Core, Protocol Services, User Products, Integration)
  auf die obigen Einheiten; Doppelposten dokumentieren (ENT-002 §4).
- Änderungen nur über ENT-010 mit Registry-Update und Notion-/Wiki-Sync
  (AI-DEV-010).
