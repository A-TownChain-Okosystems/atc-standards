---
standard:
  id: ATC-STD-444
  title: "WebSocket Standard"
  version: "1.1.0"
  status: approved
  category: development
  authority: A-TownChain-Okosystems
  owner: "Michael (Owner-Entwurf) / Standards Governance"
  created: "2026-09-08"
  updated: "2026-09-08"
  normative: true
  effective_date: "2026-09-08"
  review_date: "2027-09-08"
  classification: PUBLIC
  language: de-DE
  supersedes: null
  superseded_by: null
  dependencies:
    - ATC-STD-000
  related_standards: []
  license: "Copyright (c) 2026 Michael Wroblewski"
----

# ATC-STD-444 — WebSocket (v1.1.0, APPROVED)

> **Status:** APPROVED (v1.1.0, §30-eingefroren) — Grundgerüst-Standard aus Katalog-Slot der Familie
> API Standards (FAM-26); §9-FREIGEGEBEN 08.09.2026, 02:15 UTC+2 — APPROVED, normativ,
> §30-eingefroren. Struktur-Elaboration v1.1.0 via SCR-0031 (08.09.2026, 02:30 UTC+2):
> familien-spezifische Kernregeln, Ökosystem-Verortung, Schnittstellen, Metriken und
> Security-Bedrohungen additiv ergänzt (MINOR, ATC-STD-UPDATE-001 UPD-G03).

## Abstract

ATC-STD-444 (WebSocket) ist der Standard für den gleichnamigen Katalog-Slot der Familie
**API Standards** (FAM-26, Range ATC-STD-440..450) im ATC Enterprise Standards Framework. Er
definiert den Gegenstand, seine Verortung im Ökosystem, die verbindlichen
Kernregeln, Compliance- und Verifikationspflichten sowie Security-Betrachtungen.
Der Standard ist APPROVED, normativ in Kraft und §30-eingefroren (Owner-§9-Freigabe
08.09.2026, 02:15 UTC+2, SCR-0030-Batch); die Struktur-Elaboration erfolgte via
SCR-0031 als MINOR v1.1.0. Besondere Engineering-Vertiefung erfolgt inkrementell
via eigener SCR/MINOR-Kette (ATC-STD-UPDATE-001).

Schlüsselwörter: MUSS/MUSS NICHT, SOLLTE, DARF/KANN — RFC-2119 gemäß ATC-STD-000 §10.

## Scope

**Gilt:** Der durch den Slot-Titel (WebSocket) bezeichnete Gegenstandsbereich im
Zuständigkeitsfeld der Familie API Standards. **Gilt nicht:** Bereiche, die durch
fachlich konkretere Standards derselben Familie verbindlich geregelt sind
(Subsidiarität: der konkrete Standard geht vor).

## §1 Gegenstand & Ökosystem-Verortung

Dieser Standard adressiert **WebSocket** im Katalog-Slot ATC-STD-444 der Familie API Standards
(FAM-26); die Zuordnung folgt registry/framework.yaml (S-21) und darf nur via SCR
geändert werden.

API-Schicht (atc-gateway): versionierte Schnittstellen, Rate-Limiting, vollständige Fehlerkataloge.

**Katalog-Referenz:** keine zusätzliche Katalog-Notiz; Verortung ausschließlich über Familie und Slot.

## §2 Kernregeln (elaboriert)

1. **KR-1:** APIs MÜSSEN versioniert sein (Version im Pfad/Header, Deprecation-Fenster definiert).
2. **KR-2:** Fehlercodes MÜSSEN 100 % katalogisiert und stabil sein (keine Umbenennung ohne MAJOR).
3. **KR-3:** Rate-Limits MÜSSEN je Endpunkt definiert und durchgesetzt sein.
4. **KR-4:** Authentisierung MUSS über die Identity-Schicht (DID/Session) laufen.
5. **KR-5:** API-Änderungen erfordern Kompatibilitätsprüfung (COMPAT-001, Interop-Klasse).
6. **KR-6:** Dokumentation MUSS synchron zur Implementierung sein (keine Ghost-Endpunkte).

## §3 Schnittstellen & Kopplungen

- **Registry-Kopplung:** standards.yaml/versions.yaml (Version/Status S-14/S-19),
  Katalog-Slot in registry/framework.yaml.
- **Governance-Kette:** SCR → VERSION → UPDATE (UPD-G03 MINOR) → COMPAT (bei MAJOR)
  → AUDIT; Findings via registry/findings.yaml (F-NNN).
- **Nachbarfamilien:** Familie API Standards — Subsidiarität: konkretere Standards gehen vor.
- **Agenten-Bindung:** Vollmandat via .github/ai/agent.yaml; Umsetzungspflicht nach
  AGENT_MANIFEST.

## §4 Metriken & Akzeptanzkriterien

- **M1:** Fehlerkatalog-Abdeckung 100 %
- **M2:** Rate-Limit-Treue
- **M3:** Doku-Sync 100 %

Akzeptanz gilt als nachgewiesen, wenn die genannten Kriterien in einem AUD-Record
oder Validator-Lauf dokumentiert sind; fehlende Nachweise werden als Findings
geführt und nach ATC-STD-BUG-005 (RCA) bearbeitet.

## §5 Compliance & Verifikation

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
- **REQ-STD-006** (§2/§4): Gegenstand im Ökosystem verortet (§1-Verortung).
- **REQ-STD-007** (§2/§4): Familien-Kernregeln deklariert und verifizierbar (§2).
- **REQ-STD-008** (§2/§4): Schnittstellen zu Registry/Governance-Kette/Agenten gebunden (§3).
- **REQ-STD-009** (§2/§4): Metriken/Akzeptanzkriterien definiert, Nachweis via AUD-Record (§4).
- **REQ-STD-010** (§2/§4): Familienspezifische Security-Bedrohungen katalogisiert (§5).

## Security Considerations

Breaking Changes ohne Versionsfenster; Endpoint-Enumeration über undokumentierte Routen.

Bis zur Engineering-Vertiefung gilt die Ehrlichkeitsregel: Sicherheitszustände
MÜSSEN ehrlich benannt sein (ACTIVE/PARTIAL/PLANNED); erfundene Sicherheitszusagen
sind verboten (vgl. ATC-STD-PROTOCOL-003).

## Changelog (Standard-intern)

- **1.1.0** (2026-09-08): MINOR via SCR-0031 — Struktur-Elaboration: familien-spezifische
  Kernregeln (§2), Ökosystem-Verortung (§1), Schnittstellen (§3), Metriken/
  Akzeptanzkriterien (§4) und Security-Bedrohungen ergänzt; REQ-STD-006..010
  additiv. Additiv und abwärtskompatibel (ATC-STD-UPDATE-001 UPD-G03).
- **1.0.0** (2026-09-08): Initial Release — Grundgerüst-Standard aus
  Katalog-Slot ATC-STD-444 (Familie API Standards, FAM-26) via SCR-0030; §9-FREIGEGEBEN
  08.09.2026, 02:15 UTC+2 — APPROVED, normativ, §30-eingefroren.

## References

- ATC-STD-000 (Standards Governance & Specification), ATC-STD-FRAMEWORK-001
- ATC-STD-UPDATE-001/CHANGE-001 (Change-Control), ATC-STD-BUG-005 (RCA)
- registry/framework.yaml (FAM-26), registry/standards.yaml + versions.yaml

*ATC-STD-444 v1.1.0 · Struktur-Elaboration via SCR-0031 · Aurora (Superagent) · 08.09.2026*
