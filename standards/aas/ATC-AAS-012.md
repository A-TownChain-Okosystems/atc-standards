---
standard:
  id: ATC-AAS-012
  title: "ATC-AAS-012 — Agent Hallucination / Assumption Standard"
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

# ATC-AAS-012 — Agent Hallucination / Assumption Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Aussagen-Klassifikation (Pflicht)

```
FACT       — mit Fundstelle verifiziert
EVIDENCE   — aus Evidenz abgeleitet (AAS-010 §3)
INFERENCE  — logische Folgerung aus verifizierten Fakten
ASSUMPTION — nicht verifizierte Annahme (ASSUMPTION-ANNN, AI-DEV-001 §10)
UNKNOWN    — keine Evidenz vorhanden
```

Beispiel:
```yaml
statement: "ATCLang VM uses Rust."
classification: FACT
evidence: {repository: atclang, file: Cargo.toml}
```

## 2. Kernregeln

- Ohne Evidenz: classification `UNKNOWN` — niemals „probably …".
- ASSUMPTION mit verification.required blockiert COMPLETED (AI-DEV-001 §10);
  Bestätigung hebt die Klassifikation auf FACT/verifiziert.
- Aussagen in Findings, Audit-Records und PR-Bodies tragen ihre
  Klassifikation implizit über die Fundstellen-Pflicht (AI-DEV-005 §2).
- Verwechslung von INFERENCE mit FACT ist ein Governance-Verstoß (S2).
