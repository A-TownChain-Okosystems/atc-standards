---
standard:
  id: ATC-ENT-014
  title: "ATC-ENT-014 — Audit & Nachvollziehbarkeit Standard"
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

# ATC-ENT-014 — Audit & Nachvollziehbarkeit Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Nachvollziehbarkeits-Pflicht (je kritischer Aktion)

```
WHO (Rolle/Agent) · WHAT (Aktion) · WHEN (Timestamp) · WHERE (Repo/Branch/
Commit) · WHY (Begründung/DEC-/Task-Referenz) · WITH WHICH VERSION · RESULT
```

## 2. Audit-Event (Standardstruktur)

```yaml
audit_event:
  id: AUD-000123
  actor: ROLE-AI-AGENT          # Rollen-ID (Mensch) oder Agenten-ID (AAS-001)
  action: MODIFY_CODE
  repository: atc-core
  branch: feature/zkp-layer
  commit: <sha>
  reason: "Implement ZKP verification"    # Task/DEC-Bezug
  approval: DEC-0042
  tests: PASS
  security_scan: PASS
  timestamp: "<ISO-8601>"
```

## 3. Ebenen (zweistufig, unverändert an AAS-018 angelehnt)

1. **Ereignisprotokoll** je Operation (append-only,
   `.github/ai/audit/` bzw. org-weit `registry/audit/`).
2. **Abschluss-Records** AUD-NNN (AI-DEV-009 §1) je Task/Änderung.

## 4. Prüfung

- Audit-Pflicht je Rolle: `audit_required` (ENT-002 §1); Agenten immer.
- Stichproben-Audits (ROLE-AUDITOR) je review_cycle; Beanstandungen als
  Findings (BUG-001) mit Risiko-Referenz (ENT-011 §3).
- Defensives Design: Audit-Records sind Evidenz (AAS-010 §3);
  fehlende Records = fehlender Nachweis = Governance-Verstoß (S2).
