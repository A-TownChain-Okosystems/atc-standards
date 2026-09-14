---
standard:
  id: ATC-STD-MAINT-017
  title: "ATC-STD-MAINT-017 — Upgrade & Migration Standard"
  version: "1.0.0"
  status: draft
  category: maint
  authority: A-TownChain Ecosystems
  owner: ShivaCoreDev
  created: "2026-09-14"
  updated: "2026-09-14"
  normative: true
  supersedes: []
  superseded_by: null
  effective_date: "pending §9-Freigabe"
  review_date: null
  applies_to: "Alle Upgrades/Migrationen (Version Upgrades, Datenmigrationen, Schemaaenderungen)"
  license: "Copyright (c) 2026 Michael Wroblewski"
---

# ATC-STD-MAINT-017 — Upgrade & Migration Standard (v1.0.0, DRAFT)

> **Status:** DRAFT — wartet auf §9-Freigabe (ATC-STD-000). Dach: ATC-STD-MAINT-000 ·
> Klassifikation: MAINT-001 · Lifecycle: MAINT-002 · Evidence: MAINT-019.

## Abstract

Version Upgrades, Migrationen und Schemaaenderungen als planbare, evidenced Maintenance.

## §1 Pruefbereiche

Version Upgrades (Toolchain, Runtime, OS) · Migrationen (Daten, Formate, APIs) ·
Schemaaenderungen (Synchron mit Consumer-Repos; Registry-Schemas via SCR).

## §2 Regeln

1. Jedes Upgrade/Migration hat Plan, Rollback (MAINT-018) und Migrations-Evidence (vorher/nachher).
2. Schemaaenderungen koordinieren alle Consumer (Registry-Abhaengigkeitspruefung).
3. Upgrades sind M0/M1; abbrechende Inkompatibilitaet eskaliert nach MAINT-009/016.

## REQ-Matrix (normativ)

| REQ | Anforderung | Pflicht |
|---|---|---|
| REQ-MAINT-017-001 | Upgrades/Migrationen haben Rollback und Vorher/Nachher-Evidence | MUST |
| REQ-MAINT-017-002 | Schemaaenderungen koordinieren alle Consumer | MUST |

## Implementierungsstatus (ehrlich, SCR-0080-Doktrin)

**SPECIFICATION_ONLY.** Einzelne Upgrades sind durchlaufen (z.B. setuptools-Fixes); ein formaler Migrations-Prozess ist NICHT implementiert. CLAIMED != PASS.

## Compliance

Dach: ATC-STD-MAINT-000; Kernprofil: ATC-STD-000, ATC-STD-201/202/203, ATC-STD-ENG-001.
