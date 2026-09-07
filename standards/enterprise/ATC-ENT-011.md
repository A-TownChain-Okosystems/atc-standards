---
standard:
  id: ATC-ENT-011
  title: "ATC-ENT-011 — Risiko-Management Standard"
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

# ATC-ENT-011 — Risiko-Management Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## Abstract

ATC-ENT-011 (Risiko-Management Standard) — Owner-Sammelfreigabe 07.09.2026 20:20 UTC+2 (alles freigeben): CANDIDATE -> APPROVED, normativ in Kraft; dokumentiert in approval/APPROVAL-DECISION-2026-09-07-AAS-ENT-AUDIT.md.
Normative Aussagen sind verbindlich (MUSS/SOLLTE/DARF im Sinne von RFC 2119).

## Scope

**Scope:** Gilt für: Organisationsebene von A-TownChain Ökosystems — oberhalb der technischen Familien, unterhalb der Verfassung ATC-STD-000.
Nicht-Gilt: normative Standardtexte (Änderungen via SCR, ATC-STD-000 §19-33); technische Domäneninhalte (NET/ZKP/AI-DEV).

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
