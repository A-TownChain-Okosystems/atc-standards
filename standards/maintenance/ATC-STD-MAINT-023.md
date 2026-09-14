---
standard:
  id: ATC-STD-MAINT-023
  title: "ATC-STD-MAINT-023 — Vendor & Supply-Chain Maintenance Standard"
  version: "1.0.0"
  status: draft
  category: maint
  authority: A-TownChain Ecosystems
  owner: "Michael (Owner-Entwurf)"
  created: "2026-09-14"
  updated: "2026-09-14"
  normative: true
  supersedes: []
  superseded_by: null
  effective_date: "pending §9-Freigabe"
  review_date: null
  applies_to: "Alle Vendor-/Third-Party-Komponenten des Oekosystems (Actions, Toolchains, Crates, Pakete, externe Dienste)"
  license: "Copyright (c) 2026 Michael Wroblewski"
---

# ATC-STD-MAINT-023 — Vendor & Supply-Chain Maintenance Standard (v1.0.0, DRAFT)

> **Status:** DRAFT — wartet auf §9-Freigabe (ATC-STD-000). Dach: ATC-STD-MAINT-000 ·
> Klassifikation: MAINT-001 · Lifecycle: MAINT-002 · Evidence: MAINT-019.

## Abstract

Vendor- und Supply-Chain-Pflege: Provenance, Vendor-Risiken und Ersatz-Strategien als Teil der Dependency-Disziplin. Prioritaet P2.

## §1 Pruefbereiche

Vendor-Abhaengigkeiten (GitHub Actions, Toolchains, externe Crates/Pakete, Dienste) ·
Provenance & SBOM (Herkunftsnachweis fuer Releases) · Vendor-Risiken (Ausfall, Uebernahme,
License-Aenderung, Abandonment) · Ersatz-Strategie (Fork-, Pin- oder Migrations-Pfad).

## §2 Regeln

1. Vendor-Komponenten werden wie eigene Abhaengigkeiten gepflegt und M0-M3 klassifiziert (MAINT-001);
   gepinnt und versioniert (kein floating tags).
2. Releases erzeugen SBOM mit Provenance-Angabe (Verkettung MAINT-004).
3. Supply-Chain-Angriff oder kompromittierte Vendor-Komponente = M2, mit Kernel-/Chain-Bezug M3.
4. Vendor-Risiken werden bewertet und mit Ersatz-Strategie im Maintenance-Backlog gefuehrt.

## REQ-Matrix (normativ)

| REQ | Anforderung | Pflicht |
|---|---|---|
| REQ-MAINT-023-001 | Vendor-Komponenten sind gepinnt, versioniert und M-klassifiziert | MUST |
| REQ-MAINT-023-002 | Releases erzeugen SBOM mit Provenance | MUST |
| REQ-MAINT-023-003 | Kompromittierte Vendor-Komponente = M2 (mit Kernel-/Chain-Bezug M3) | MUST |
| REQ-MAINT-023-004 | Vendor-Risiken haben eine dokumentierte Ersatz-Strategie | MUST |

## Implementierungsstatus (ehrlich, SCR-0080-Doktrin)

**SPECIFICATION_ONLY.** cargo audit (RustSec) deckt Supply-Chain-Risiken der Rust-Abhaengigkeiten ab; Provenance-Nachweise und Vendor-Risikoregister sind NICHT implementiert. CLAIMED != PASS.

## Compliance

Dach: ATC-STD-MAINT-000; Kernprofil: ATC-STD-000, ATC-STD-201/202/203, ATC-STD-ENG-001.
