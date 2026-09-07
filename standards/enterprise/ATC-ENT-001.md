---
standard:
  id: ATC-ENT-001
  title: "ATC-ENT-001 — Enterprise Governance Standard"
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

# ATC-ENT-001 — Enterprise Governance Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft
> **Block:** ATC-ENT (Enterprise Standards Layer) · **Priorität:** P0 · **Position:** zwischen ATC-STD-000 (Verfassung) und den technischen Familien (AI-DEV, AAS, 201-204, BUG, NET, ZKP, 100/300)

## 1. Zweck des Enterprise-Layers

Einheitliche Regeln dafür, wie das Unternehmen organisiert, entscheidet,
entwickelt, dokumentiert, prüft, verändert und auditiert wird — getrennt
von technischen Standards. ATC-ENT legt fest:

Wer darf was entscheiden? · Wer trägt Verantwortung? · Wie werden Änderungen
genehmigt? · Wie werden Risiken behandelt? · Wie wird Wissen verwaltet? ·
Wie wird auditiert? · Wie werden Menschen UND KI-Agenten organisatorisch
eingebunden?

## 2. Standard-Hierarchie (verbindlich)

```
ATC-STD-000 (Verfassung, Meta-Ebene)
    └── ATC-ENT (Enterprise-Layer, dieser Block)
            ├── ATC-GOV  — in ATC-STD-000 §14.1 verankert
            ├── ATC-AI   — ATC-STD-AI-DEV-001..012 + ATC-AAS-001..025
            ├── ATC-DEV  — ATC-STD-100, 300, 201-204, BUG-001..004
            ├── ATC-SEC  — ATC-STD-203 (+ ENT-011 Risiko-Registry)
            ├── ATC-ARCH — ATC-STD-100 (Language/Stack) + ARCH-Entscheidungen (DEC-NNNN)
            ├── ATC-QA   — ENT-015 (DoD) + AI-DEV-008
            ├── ATC-OPS  — offen (DevOps/Betrieb, eigene Familie später)
            ├── ATC-BLOCK— ATC-STD-NET-001..008, ZKP-001..010
            ├── ATC-DATA — offen (Datenstandards, später)
            └── ATC-DOC  — Wiki/Dokumentation (BUG-004, AI-DEV-010)
```

Technische Standards dürfen ENT-Regeln nie konterkarieren; Konflikt →
ATC-AAS-013 (Konflikt-Leiter: Standard > Architecture > …).

## 3. Dokumentenstandard (Metadaten-Pflicht)

Jedes Unternehmensdokument trägt:

```yaml
document:
  id: ATC-ENT-001          # Namensraum gem. §37/Schema entStandardId
  title: "Enterprise Governance Standard"
  version: 1.0.0
  status: draft|candidate|approved|stable|deprecated|archived
  owner: ROLE-CEO           # Rollen: ATC-ENT-002
  approver: ROLE-CTO
  created: 2026-09-07
  updated: 2026-09-07
  review_cycle: annual       # Pflicht: jährung Review-Termin
```

Dokumente ohne gültige Identität haben keinen normativen Status.

## 4. Geltungsbereich

ATC-ENT bindet alle Organisationseinheiten (ENT-008), Rollen (ENT-002),
Entscheidungen (ENT-003), Repositories (ENT-009) — menschliche wie
KI-Agenten-Mitglieder gleichermaßen (§7 Einbindung über AAS/AI-DEV).
