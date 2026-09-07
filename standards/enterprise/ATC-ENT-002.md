---
standard:
  id: ATC-ENT-002
  title: "ATC-ENT-002 — Rollen & Verantwortlichkeiten Standard"
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

# ATC-ENT-002 — Rollen & Verantwortlichkeiten Standard (v1.0.0, CANDIDATE)

> **Status:** CANDIDATE · **Priorität:** P0 · **Basiert auf:** ATC-STD-000 §14.1 (Owner/Approver/Reviewer/Maintainer/Agent) · **Erweitert:** AI-DEV-001 §2, AAS-001

## 1. Rollen-Definition (Pflichtstruktur)

```yaml
role:
  id: ROLE-DEV
  name: "..."
  purpose: "..."
  responsibilities: [...]
  authority: [...]
  limitations: [...]
  required_approvals: [...]
  audit_required: true
```

## 2. Kanonische Rollen (Initialbestand)

ROLE-CEO · ROLE-CTO · ROLE-CISO · ROLE-ARCH · ROLE-DEV · ROLE-QA ·
ROLE-SEC · ROLE-DEVOPS · ROLE-AI-ENGINEER · ROLE-AI-AGENT · ROLE-AUDITOR.

Mapping zur Verfassung: Owner = ROLE-CEO/CTO-Ebene; Approver ausschließlich
menschliche Rollen (ATC-STD-000 §14.1: Agenten sind NIE Approver); Agenten
tragen ALWAYS `audit_required: true`.

## 3. KI-Agenten als Unternehmensmitglieder

Agenten sind kontrollierte technische Entitäten innerhalb der
Unternehmens-Governance — identifiziert über ATC-AAS-001 (agent_id),
berechtigt über AAS-002/003, eingebunden als ROLE-AI-AGENT mit denselben
Pflichten wie menschliche Rollen: Verantwortlicher, Status, Begründung,
Historie (ENT-003 Kernregel), Audit-Pflicht (ENT-014). KEINE separaten
parallelen Standards (statt eines eigenen „ATC-AI-001" gelten
AI-DEV-001..012 + AAS-001..025 unverändert).

## 4. Regeln

- Neue Rollen nur über ENT-010 (Change) mit Registry-Eintrag; IDs nach
  Schema `roleId` (^ROLE-[A-Z][A-Z0-9-]*$), fortlaufend (§37).
- Eine Person/ein Agent kann mehrere Rollen tragen — Ausübung je Rolle
  getrennt dokumentieren; Approver-Rolle nie durch Agenten (§14.1).
- Rollen-Reviews im review_cycle (ENT-001 §3): annual.
