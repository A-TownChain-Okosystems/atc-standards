---
standard:
  id: ATC-ENT-002
  title: "ATC-ENT-002 — Rollen & Verantwortlichkeiten Standard"
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
  effective_date: "2026-09-07"
  review_date: "2027-09-08"
  license: "Copyright (c) 2026 Michael Wroblewski"
---

# ATC-ENT-002 — Rollen & Verantwortlichkeiten Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## Abstract

ATC-ENT-002 (Rollen & Verantwortlichkeiten Standard) — Owner-Sammelfreigabe 07.09.2026 20:20 UTC+2 (alles freigeben): CANDIDATE -> APPROVED, normativ in Kraft; dokumentiert in approval/APPROVAL-DECISION-2026-09-07-AAS-ENT-AUDIT.md.
Normative Aussagen sind verbindlich (MUSS/SOLLTE/DARF im Sinne von RFC 2119).

## Scope

**Scope:** Gilt für: Organisationsebene von A-TownChain Ökosystems — oberhalb der technischen Familien, unterhalb der Verfassung ATC-STD-000.
Nicht-Gilt: normative Standardtexte (Änderungen via SCR, ATC-STD-000 §19-33); technische Domäneninhalte (NET/ZKP/AI-DEV).

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
