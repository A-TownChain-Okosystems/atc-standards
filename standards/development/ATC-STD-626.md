---
standard:
  id: ATC-STD-626
  title: "Package System Standard"
  version: "1.0.0"
  status: draft
  category: development
  authority: A-TownChain-Okosystems
  owner: "Michael (Owner-Entwurf) / Standards Governance"
  created: "2026-09-08"
  updated: "2026-09-08"
  normative: false
  effective_date: ""
  review_date: ""
  classification: PUBLIC
  language: de-DE
  supersedes: null
  superseded_by: null
  dependencies:
    - ATC-STD-000
  related_standards: []
  license: "Copyright (c) 2026 Michael Wroblewski"
----

# ATC-STD-626 — Package System (v1.0.0, DRAFT)

> **Status:** DRAFT (v1.0.0) — Grundgerüst-Standard aus Katalog-Slot der Familie
> ATCLang (FAM-35); erstellt via SCR-0030. Inhaltliche Elaborierung (Volltext,
> fachliche REQs) erfolgt via eigenem SCR; Owner-§9-Freigabe ausstehend.

## Abstract

ATC-STD-626 (Package System) ist der Grundgerüst-Standard für den gleichnamigen Katalog-Slot
der Familie **ATCLang** (FAM-35, Range ATC-STD-620..629) im ATC Enterprise Standards
Framework. Er schafft die normative Hülle: Definition des Gegenstandes, Verortung
im Katalog, Kernpflichten, Compliance- und Verifikationsregeln sowie die
Change-Control-Bindung. Der Standard ist DRAFT und entfaltet keine normative
Wirkung, bis die inhaltliche Elaborierung erfolgt und der Owner nach §9
freigibt (ATC-STD-000 §9/§19: Kein Registry-Eintrag ohne Verfahren — Eintrag
erfolgt mit SCR-0030 als DRAFT; APPROVED nur mit Freigabe).

Schlüsselwörter: MUSS/MUSS NICHT, SOLLTE, DARF/KANN — RFC-2119 gemäß ATC-STD-000 §10.

## Scope

**Gilt:** Der durch den Slot-Titel (Package System) bezeichnete Gegenstandsbereich im
Zuständigkeitsfeld der Familie ATCLang. **Gilt nicht:** Bereiche, die durch
fachlich konkretere Standards derselben Familie verbindlich geregelt sind
(Subsidiarität: der konkrete Standard geht vor).

## §1 Gegenstand & Verortung

Dieser Standard adressiert **Package System**. Er ist dem Katalog-Slot ATC-STD-626 der
Familie ATCLang (FAM-35) zugeordnet; die Zuordnung folgt registry/framework.yaml
(S-21) und darf nur via SCR geändert werden.

## §2 Kernpflichten (Grundgerüst)

1. Der Gegenstand MUSS eindeutig definiert und gegen benachbarte Standards
   derselben Familie abgegrenzt sein.
2. Fachliche Regeln MÜSSEN als REQ-IDs deklariert und maschinell prüfbar oder
   dokumentiert nachweisbar sein (ATC-STD-000 §11).
3. Compliance MUSS über die Validator-Gates bzw. dokumentierte Prüfung
   nachweisbar sein (AUD-Record bei Abweichung).
4. Jede Änderung folgt der Change-Control-Kette SCR → VERSION → UPDATE →
   COMPAT → AUDIT (ATC-STD-CHANGE-001, ATC-STD-UPDATE-001).
5. Sicherheitsrelevante Aspekte MÜSSEN in den Security Considerations
   benannt werden (ATC-STD-000 §12).

## §3 Compliance & Verifikation

Compliance wird über die Gesamt-Validierung (CI, S-01..S-25) je Registry-Eintrag
geprüft: Metadaten-Vollständigkeit, Naming, Status-/Version-Konsistenz und
Registry-Konsistenz. Abweichungen werden als Findings (F-NNN) geführt und nach
ATC-STD-BUG-005 (RCA) bearbeitet.

## Requirements (normativ)

- **REQ-STD-001** (§1): Gegenstand eindeutig definiert und im Katalog verortet.
- **REQ-STD-002** (§2): Fachliche Regeln als deklarierte, verifizierbare REQ-IDs.
- **REQ-STD-003** (§2): Compliance nachweisbar über Validator-Gates oder Prüfung.
- **REQ-STD-004** (§2): Änderungen ausschließlich über die Change-Control-Kette.
- **REQ-STD-005** (§2): Sicherheitsaspekte dokumentiert (Security Considerations).

## Security Considerations

Bis zur Elaborierung gilt: Sicherheitsrelevante Auswirkungen des Gegenstandes
(Package System) sind bei der Elaborierung zwingend zu bewerten; bis dahin werden keine
Sicherheitsaussagen getroffen (Ehrlichkeitsregel — kein erfundener Status).

## Changelog (Standard-intern)

- **1.0.0** (2026-09-08): Initial Release DRAFT — Grundgerüst-Standard aus
  Katalog-Slot ATC-STD-626 (Familie ATCLang, FAM-35) via SCR-0030. Elaborierung und
  §9-Freigabe ausstehend; bis dahin nicht normativ.

## References

- ATC-STD-000 (Standards Governance & Specification)
- ATC-STD-FRAMEWORK-001 (Katalog/Slots), ATC-STD-CHANGE-001/UPDATE-001 (Change-Control)
- registry/framework.yaml (FAM-35), registry/standards.yaml (Eintrag via SCR-0030)

*ATC-STD-626 v1.0.0 · Grundgerüst via SCR-0030 · Aurora (Superagent) · 08.09.2026*
