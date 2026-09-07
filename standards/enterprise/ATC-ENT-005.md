---
standard:
  id: ATC-ENT-005
  title: "ATC-ENT-005 — Unternehmensrichtlinien Standard"
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

# ATC-ENT-005 — Unternehmensrichtlinien Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Richtlinien-Hierarchie

1. ATC-STD-000 (Verfassung) — nicht überlagerbar
2. ATC-ENT-Richtlinien ( Policies, ENT-Block)
3. Domänen-Standards (AI-DEV, AAS, 201-204, …)
4. Repo-interne Richtlinien (CONTRIBUTING, AGENTS.md)

Niedrigere Ebene darf höhere Ebene präzisieren, nie aufweichen.

## 2. Richtlinien-Registry

Jede Richtlinie ist ein Dokument nach ENT-001 §3 (Metadaten) mit
`policy: {id: POL-NNNN, scope, enforcement, owner}` — enforcement:
automatisiert (CI/Workflow) bevorzugt, sonst Audit-Stichprobe (ENT-014).

## 3. Mindest-Policies (Initialbestand)

- Security-Policy (Secrets: AAS-014; Scanning: ATC-STD-203)
- Data-Policy (Datenklassifikation, Offenlegung)
- AI-Policy (Agenten-Einsatz nach AAS/AI-DEV; False-Claim-Verbot: AAS-012)
- Release-Policy (NET-003/004 Mainnet/Release-Gates)

## 4. Änderungen

Nur über ENT-010 (Change) mit Impact auf betroffene Standards;
Richtlinien-Änderungen lösen Review-Pflicht abhängiger Dokumente aus
(review_cycle, ENT-001 §3).
