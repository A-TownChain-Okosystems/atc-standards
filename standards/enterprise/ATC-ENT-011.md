---
standard:
  id: ATC-ENT-011
  title: "ATC-ENT-011 — Risiko-Management Standard"
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

# ATC-ENT-011 — Risiko-Management Standard (v1.0.0, CANDIDATE)

> **Status:** CANDIDATE · **Priorität:** P0 · **Nutzt:** Severity-Skala S0-S4 (ATC-STD-BUG-002) · **Registry:** registry/risks.yaml

## 1. Risiko-Registry (Zentral, RISK-NNNN)

```yaml
risk:
  id: RISK-0001
  category: Security        # Kategorie-Schema §3
  severity: Critical        # Critical|High|Medium|Low (→S0..S3)
  probability: High
  impact: Critical
  owner: ROLE-CISO
  mitigation: "..."
  status: OPEN             # OPEN|MITIGATED|ACCEPTED|CLOSED
  review: <Datum>          # Pflicht-Wiedervorlage
```

## 2. Pflichten

- Jedes identifizierte Risiko (aus Findings, Audits, Reviews, AAS-020
  Failures) wird zentral registriert — Findings deckeln technische
  Vorfälle, Risiken das Unternehmensniveau.
- S0/Critical-Risiken: Eskalation E3 (ENT-007 §1), Review spätestens
  monatlich; Accept nur mit Owner-Entscheidung (DEC-Record).
- Risiko-Kategorien: Strategic, Financial, Technical, Security,
  Operational, Legal, Compliance, AI, Infrastructure, Blockchain,
  Supply Chain.

## 3. Verzahnung

F-NNN (Findings, BUG-001) ↔ RISK-NNNN: ein Finding ab Severity S1 kann
ein Risiko eröffnen (`risk_ref`); Findings schließen nicht Risiken.
Doppeltellungen vermeiden (Registry-First, §37).
