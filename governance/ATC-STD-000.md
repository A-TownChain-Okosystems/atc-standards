standard:
  id: ATC-STD-000
  title: ATC Standards Governance & Specification Standard
  version: "1.0.0"
  status: candidate
  category: governance
  owner: ShivaCoreDev
  created: "2026-09-07"
  updated: "2026-09-07"
  normative: true
  supersedes: []
  superseded_by: null
---

# ATC-STD-000 — ATC Standards Governance & Specification Standard

> **Der Standard fuer Standards.** ATC-STD-000 definiert den verbindlichen
> Rahmen, wie ATC-Standards erstellt, versioniert, geprueft, verabschiedet,
> geaendert und ausser Kraft gesetzt werden. Alle anderen ATC Standards
> MUSSSEN diesem Rahmen folgen.

## 1. Status

CANDIDATE v1.0.0 (07.09.2026). Review-Chain nach §15 bestanden (Technical,
Security, Architecture: alle PASS, 0 blockierende Befunde; Berichte:
governance/APPROVAL_PACKAGE_ATC-STD-000.md). Pfad: DRAFT → REVIEW → CANDIDATE.
Offen: formale Owner-Approval → APPROVED → STABLE. Bootstrapping-Regel:
ATC-STD-000 befolgt seine eigenen Regeln ab Errichtung.

## 2. Abstract

Diese Spezifikation definiert den Governance-Rahmen des gesamten
ATC-Standardsystems: Standard-IDs, maschinenlesbare Metadaten, den
Standard-Lifecycle (IDEA bis RETIRED), die normative Struktur von Standards,
Requirement-IDs und -Klassifizierung, Compliance-Verfahren, Semantic
Versioning mit Breaking-Change-Definition, Change Control ueber Standard
Change Requests (SCR), Review-Pflichten, Supersession und Migration —
sowie die zentrale Standard-Registry und den Validator
(tools/atc-std-validator).

## 3. Scope

GILT FUER: alle normativen Standards der A-TownChain-Okosystems (ATC-STD-*
sowie die Legacy-Serien ATC-01…99, ATC-0001…0008, ATS-1000…1007 inklusive
ihrer Pflege und kuenftiger Aenderungen), das atc-standards-Repository als
kanonische Heimat, alle Standards-Registry-Dateien und Validator-Tools.

DEFINIERT NICHT: fachliche Inhalte einzelner Standards (Protokolle,
Repository-Struktur, Security-Regeln), Produktdokumentation, ADRs.

## 4. Goals

- Eine einzige Wahrheit: Registry + Repo schlagen README/Wiki/Issue/Chat.
- Maschinenlesbare, automatisch validierbare Standard-Landschaft.
- Nachvollziehbare Entscheidungs- und Aenderungshistorie je Standard.
- Skalierbare ID-Kategorien (000–1000+).

## 5. Non-Goals

- Festlegung fachlicher Architekturentscheidungen (dafuer: AD-Register).
- Ersetzung des zentralen DECISIONS_REGISTER (Zwei-Ebenen-Modell AD-029:
  ATC-STD-000 = formale Norm, DECISIONS_REGISTER = Organisations-Entscheidungen).
- Werkzeug- oder Sprachauswahl fuer Implementierungen.

## 6. Terminologie (RFC 2119)

MUST / MUST NOT / REQUIRED / SHALL = zwingend. SHOULD / SHOULD NOT =
empfohlen (Abweichung begruendungspflichtig). MAY = optional. Jeder
normative Standard MUSS diese Begriffe in diesem Sinne verwenden.

## 7. Standard-ID-System

Jeder Standard erhaelt eine unverwechselbare ID `ATC-STD-XXX` im
kategorisierten Nummernraum (Scalability-Bereiche):

| Bereich | Domaine |
|---|---|
| ATC-STD-000 | Standard Governance (diese Verfassung) |
| ATC-STD-100-199 | Architecture |
| ATC-STD-200-299 | Repository & Git |
| ATC-STD-300-399 | Development / Coding |
| ATC-STD-400-499 | Security |
| ATC-STD-500-599 | Protocol |
| ATC-STD-600-699 | Blockchain |
| ATC-STD-700-799 | AI |
| ATC-STD-800-899 | OS / Runtime |
| ATC-STD-900-999 | Infrastructure |
| ATC-STD-1000+ | Applications / Ecosystem |

Spezialisierte Legacy-Erweiterungen (ATC-STD-REPO-001 usw.) sind ALIASE,
die langfristig auf einheitliche Registry-IDs abzubilden sind. Vollzogen:
ATC-STD-201/202/203 superseden ATC-STD-REPO-001/002/003 (v1.0.x).

Legacy-Serien behalten ihre historische Nummerierung (ATC-01…99,
ATC-0001…0008, ATS-1000…1007), werden aber fuer ALLE Aenderungen durch
diesen Standard regiert.

## 8. Standard-Metadaten (MUST)

Jeder Standard MUSS einen maschinenlesbaren YAML-Header besitzen:

```yaml
standard:
  id: ATC-STD-XXX          # MUST, eindeutig, Registry-konform
  title: <Titel>           # MUST
  version: "MAJOR.MINOR.PATCH"  # MUST, SemVer
  status: <lifecycle>     # MUST, gemaess Abschnitt 9
  category: <domaine>      # MUST, gemaess Abschnitt 7 Tabelle
  owner: <owner>           # MUST
  created: "YYYY-MM-DD"    # MUST
  updated: "YYYY-MM-DD"    # MUST
  normative: true|false    # MUST
  supersedes: [...]         # SHOULD (bei Ablaesung Pflicht)
  superseded_by: <id>       # SHOULD (nach Ablaesung Pflicht)
```

Tools koennen damit die komplette Standardlandschaft automatisch auswerten.

## 9. Standardstatus (Lifecycle)

```
IDEA → PROPOSED → DRAFT → REVIEW → CANDIDATE → APPROVED → STABLE → DEPRECATED → RETIRED
```

Nur sequenzielle Uebergaenge; Springen ist UNZULAESSIG (ausgenommen
Rueckstufung nach abgelehntem Review: CANDIDATE/REVIEW → DRAFT).
- IDEA: nur Konzept · PROPOSED: formaler Vorschlag · DRAFT: ausgearbeiteter
  Entwurf · REVIEW: aktive Pruefung · CANDIDATE: bereit zur Freigabe ·
  APPROVED: offiziell angenommen · STABLE: produktiv · DEPRECATED: nicht
  mehr fuer neue Implementierungen · RETIRED: ausser Kraft.
Ein Standard DARF NICHT allein durch Existenz normativ werden (Abschnitt 29).

## 10. Standardstruktur (SHOULD, normative Standards MUESSEN relevante
Abschnitte tragen)

Vollstruktur: 1 Status · 2 Abstract · 3 Scope · 4 Goals · 5 Non-Goals ·
6 Terminology · 7 Normative Requirements · 8 Architecture · 9 Requirements ·
10 Security Considerations · 11 Compatibility · 12 Validation · 13
Compliance · 14 Migration · 15 Versioning · 16 References · 17 Changelog.
Abstract (maximal praezise) und Scope (Gilt/Nicht-Gilt, gegen Scope Creep)
sind MUST; Goals/Non-Goals MUSS jeder grosse Standard definieren.

## 11. Normative Requirements & IDs

Jede Anforderung erhaelt eine eindeutige ID `REQ-XXX` (grosse Standards:
`REQ-<DOM>-NNN`, z.B. REQ-REPO-001) und eine Klassifizierung:

- MANDATORY (MUST) · RECOMMENDED (SHOULD) · OPTIONAL (MAY)
- CONDITIONAL mit Bedingung, z.B. `Condition: criticality >= S3`

Beispiel:
```yaml
requirement:
  id: REQ-REPO-001
  level: MUST
  description: Repository MUST contain README.md
```

## 12. Compliance

Jeder Standard MUSS definieren, wie seine Einhaltung geprueft wird.
Ergebnisse: PASS / FAIL / PARTIAL / NOT-APPLICABLE — je REQ-ID messbar.
Compliance-Level (L0 Informational, L1 Basic, L2 Compliant, L3 Production,
L4 Critical) erlauben abgestufte Konformitaet statt binaer.

## 13. Versionierung & Breaking Changes

Semantic Versioning MAJOR.MINOR.PATCH. MAJOR = breaking normative Aenderung
(MUST→MUST NOT, SHOULD→MUST, API-Format, Pflichtfeld entfernt,
Anforderungs-Semantik oder Compliance-Auslegung geaendert). MINOR = neue
kompatible Anforderungen. PATCH = Korrekturen ohne normative Aenderung.
Breaking Changes MUESSEN im Changelog explizit dokumentiert werden.

## 14. Change Control & SCR

Aenderungen an STABLE-Standards erfolgen NICHT direkt. Kette:
Change Proposal → Impact Analysis → Draft Revision → Review → Approval →
New Version. Jede Aenderung erhaelt eine Standard Change Request-ID
`SCR-0001` mit Schema: Affected Standard, Proposed Change, Motivation,
Compatibility Impact, Security Impact, Migration Impact, Decision
(ACCEPTED/REJECTED). Vorlage: templates/SCR_TEMPLATE.md.

## 15. Reviewpflicht

Minimal-Review-Chain vor APPROVED:
Author → Technical Review → Security Review → Architecture Review →
Approval. Bei einfachen Standards DARF dieser Standard einzelne Reviews
ausdruecklich erlassen (Dokumentation im Standard-Header).

## 16. Evidence Requirement

Jeder Standard SHOULD seine Design-Entscheidungen begruenden: Requirement +
Technical/Security/Compatibility Rationale — Standards bestehen nicht aus
Meinungen.

## 17. References & Dependencies

Referenzen werden kategorisiert: NORMATIVE / INFORMATIVE / IMPLEMENTATION /
EXTERNAL. Standards duerfen andere Standards referenzieren (dependencies
im Metadaten-Header); der Validator MUSS zyklische Abhaengigkeiten
erkennen und als ERROR werten.

## 18. Supersession & Migration

Ein neuer Standard KANN einen alten ersetzen (`supersedes` /
`superseded_by` Pflicht ab Ablaesung). Bei jeder MAJOR-Version MUSS eine
Migration Guide definiert werden: Current → Guide → Target.

## 19. Standard Registry (MUST)

registry/standards.yaml im atc-standards-Repository ist das HERZSTUECK:
Jeder Standard MUSS dort registriert sein (id, title, version, status,
category, owner). Ergaenzt durch: categories.yaml (Domainen-Raeder),
versions.yaml (Versionshistorie), dependencies.yaml (Standard-Graph,
Zyklenerkennung), lifecycle.yaml (Zustandsmaschine). Kein Eintrag =
kein Standard.

## 20. Automatischer Standard Validator (SHOULD als Tool, MUST als Verfahren)

tools/atc-std-validator prueft je Standard: ID-Format, Metadaten-Vollstaendigkeit,
SemVer, Lifecycle-Status, Abstract/Scope, REQ-IDs, normative Sprache,
Compliance-/Security-Sektion, Changelog, References, Registry-Eintrag und
Abhaengigkeitszyklen. Ergebnis: COMPLIANT / NON-COMPLIANT (exit-tauglich).

## 21. Der Governance-Grundsatz (Kernanforderung REQ-STD-000)

> **No ATC Standard is normative unless it is registered, versioned,
> reviewed and explicitly approved according to this specification.**

Damit gilt: Registry + Repo sind die einzige Wahrheit; README, Wiki,
Issues, Chat und Code haben bei Widerspruch NACHZUSTEHEN.

## 22. Changelog

- 1.0.0 (07.09.2026): Initiale Verfassung (Owner-Mandat AD-034). Am selben
  Tag: Review-Chain §15 bestanden (3/3 PASS, 5 nicht-blockierende Befunde als
  SCR-Empfehlungen: T-F01, T-F02, S-F01, S-F02, A-F01) → Status CANDIDATE.
  Approval-Paket: governance/APPROVAL_PACKAGE_ATC-STD-000.md.
  ID-System mit Domain-Raedern, Lifecycle-Maschine, Metadaten-Pflicht,
  REQ-IDs, Compliance-Verfahren, SemVer + Breaking-Change-Definition,
  SCR-Prozess, Review-Chain, Supersession/Migration, Registry-Pflicht,
  Validator-Anforderung, Governance-Grundsatz. Vollzogene Umnummerierung:
  ATC-STD-201/202/203 superseden ATC-STD-REPO-001/002/003.

## 23. References

NORMATIVE: ATC-STD-201 (Structure), ATC-STD-202 (Naming & Classification),
ATC-STD-203 (Security & Release) · INFORMATIVE: AD-029/030/031/034
(DECISIONS_REGISTER, Hub), RFC 2119, RFC 2140 (Versioning) ·
IMPLEMENTATION: tools/atc-std-validator, registry/standards.yaml.
