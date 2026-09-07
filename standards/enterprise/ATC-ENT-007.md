---
standard:
  id: ATC-ENT-007
  title: "ATC-ENT-007 — Eskalationsmanagement Standard"
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

# ATC-ENT-007 — Eskalationsmanagement Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Eskalationsstufen (Organisation)

E1 Ausführende Rolle (DEV/QA/Agent) → E2 Fachverantwortlicher
(ARCH/SEC/CISO) → E3 CTO/CEO → E4 Owner-Entscheidung (Verfassung §14.1).
Agenten-Eskalationen münden immer in E2+ (menschliche Rolle).

## 2. Eskalationsgründe (Pflichtliste)

Blocker ohne Selbstbehebung (AAS-020), Governance-Konflikte (AAS-013),
Autorisierungsbedarf (AAS-017 §2-Pflichtliste), Risiken ab Schwelle
(ENT-011, S0/S1), Konfliktinteressen (ENT-006).

## 3. Eskalations-Record

`{id: ESC-NNNN, from_role, to_role, reason, evidence, decision_ref
(DEC-NNNN), timestamp}` — append-only (ENT-014); Antwortpflicht mit
befristeter Reaktionszeit (S0/S1: 24h, S2/S3: 72h, sonst review_cycle).

## 4. Verhältnis zu AI-DEV-011

Agenten-Eskalationen nutzen unverändert AI-DEV-011; ESC-Records werden
bei Rollen-Eskalation (E2+) gebildet. Keine parallele Agenten-Eskalation
ohne menschliche Rolle.
