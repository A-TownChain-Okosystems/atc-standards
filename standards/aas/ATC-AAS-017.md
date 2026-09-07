---
standard:
  id: ATC-AAS-017
  title: "ATC-AAS-017 — Agent Human Approval Standard"
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

# ATC-AAS-017 — Agent Human Approval Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## Abstract

ATC-AAS-017 (Agent Human Approval Standard) — Owner-Sammelfreigabe 07.09.2026 20:20 UTC+2 (alles freigeben): CANDIDATE -> APPROVED, normativ in Kraft; dokumentiert in approval/APPROVAL-DECISION-2026-09-07-AAS-ENT-AUDIT.md.
Normative Aussagen sind verbindlich (MUSS/SOLLTE/DARF im Sinne von RFC 2119).

## 1. Autonom zulässig (innerhalb Scope + Capability + Permission)

Code analysieren · Tests ausführen · Dokumentation verbessern ·
Branch erstellen · PR vorbereiten.

## 2. Human Approval erforderlich (Pflichtliste, nicht abschließend)

Merge · Mainnet Deployment · Consensus-Änderung · Tokenomics-Änderung ·
Kryptographie-Änderung · Security Policy · Rechteänderung ·
Infrastrukturänderung.

## 3. Verfahren

Unverändert AI-DEV-011: `human_review: {required, requested}` je Task und
PR; Genehmigungsformen Mandat/Freigabe-Vermerk/SCR; Agenten sind niemals
Approver (ATC-STD-000 §14.1). Die Pflichtliste §2 ist mit AI-DEV-011 §2
Eskalationsstufen a-d verzahnt: jede Liste-Aktion löst Eskalation aus.
