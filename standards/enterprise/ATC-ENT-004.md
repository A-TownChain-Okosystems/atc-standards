---
standard:
  id: ATC-ENT-004
  title: "ATC-ENT-004 — Delegation & Berechtigungen Standard"
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

# ATC-ENT-004 — Delegation & Berechtigungen Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Delegationsmodell

- Delegation erfolgt immer von einer Rolle an eine Rolle (nie an eine
  Person/direkt an einen Agenten ohne Rollenbindung).
- Eine Delegation ist schriftlich (DEC-Record), befristet und zweckgebunden;
  Ablauf = automatische Rückfallung.
- Delegationskette dokumentieren: `delegated_from: ROLE-CTO → ROLE-ARCH,
  scope: X, expires: YYYY-MM-DD`.

## 2. Nicht delegierbar (Invariante)

Approver-Rolle für normative Standards (§14.1: nur Owner), Mainnet-Release,
Verfassungsänderungen, Rollenänderungen an Approver-Positionen.

## 3. Berechtigungsmatrix

Menschliche Rollen: ENT-002 Rollen-Definition + Entgeltungsbereiche.
Agenten: Capability/Permission-Matrix aus AAS-002/003 — Delegation an
Agenten ist immer durch die Matrix gedeckelt (keine Erweiterung durch
Delegation; Ausnahme nur mit Owner-Freigabe + Frist wie AAS-003 §3).

## 4. Review

Delegationen werden je review_cycle geprüft; unbenutzte/abgelaufene
Delegationen stilllegbar (ARCHIVED) mit Audit-Vermerk (ENT-014).
