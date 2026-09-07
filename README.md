# ATC Standards — Die normative Governance-Schicht der A-TownChain-Organisation

> **Standard-Repo:** ATC-STD-REPO-002 Typ SPEC · Level R3 · Chain-ID 658467 · AD-030 (07.09.2026)

## 1. Purpose

Dieses Repository ist DIE kanonische Heimat aller definierten Standards der
A-TownChain-Okosystems-Organisation: Blockchain-Standards (ATC-01…ATC-99),
System-/Hardware-Lizenzen (ATS), Repository-Governance (ATC-STD-REPO-001/002/003)
sowie die .atc-Referenzimplementierungen. Jedes Repository der Organisation
richtet sich nach den hier definierten Regeln.

## 2. Scope

Offiziell verbindlich fuer alle Repositories der Organisation (AD-029/AD-030).
Das Repositorium selbst erfuellt den ATC-STD-REPO-001 (self-compliant).

## 3. Architecture

- `atc/` — 102 Blockchain-/AI-/ATCLang-Standards (ATC-01 bis ATC-99, ATC-LIC,
  ATC_ECOSYSTEM_STANDARDS)
- `ats/` — ATS-Standards (ATS-LIC System-/Hardware-Lizenz)
- `governance/` — ATC-STD-REPO-001 (Structure), -002 (Naming & Classification),
  -003 (Security & Release)
- `registry/` — STANDARDS_REGISTRY.md (Master-Registry), OVERVIEW.md
- `references/` — .atc-Referenzimplementierungen (registry.atc, Standards-
  Vertragsmuster) + ATC-Modul-Doku

## 4. Features

- 109 Standard-Dokumente vollstaendig zentralisiert
- Normative 22-Repository-Klassifizierung (ATC-STD-REPO-002)
- Governance-Standards mit Compliance-Level R0-R4
- Maschinenlesbare Referenzvertraege (.atc)

## 5. Repository Structure

Gemaess ATC-STD-REPO-001; siehe docs/REPOSITORY_STANDARD.md.

## 6. Installation

Standards sind Markdown-Dokumente — kein Build. Klonen und lesen:
`git clone https://github.com/A-TownChain-Okosystems/atc-standards.git`

## 7. Development

Aenderungen an Standards NUR hier (kanonisch), nie mehr im Docs-Hub
(Hub-Kopie ist Archiv-Snapshot). Aenderungen an Governance-Standards
erfolgen via AD-Eintrag im zentralen DECISIONS_REGISTER (Hub) + Commit hier.

## 8. Testing

Standards werden ueber die STANDARDS_REGISTRY validiert (Status-Tracking:
FINAL/ACCEPTED/DRAFT/PROPOSED). .atc-Referenzen sind via atc-contracts
ausfuehrbar pruefbar.

## 9. Security

Siehe SECURITY.md. Sicherheitsrelevante Standardregeln: ATC-STD-REPO-003.

## 10. Roadmap

- Governance-Standards (ATC-STD-REPO-001/002/003): PROPOSED → STABLE nach
  erstem vollstaendigen R2+-Compliance-Nachweis zweier Repositories
- Laufende Ergaenzung neuer Standards entsprechend der Sprint-Planung

## 11. Versioning

Repository: Semantic Versioning (v1.0.0 Initial-Bestand, AD-030).
Einzelstandards tragen eigene Versionen; Protocol-/Implementation-/
Specification-Version sind unabhaengig (ATC-STD-REPO-003).

## 12. License

Copyright (c) 2026 Michael Wroblewski / ShivaCore / A-TownChain-Okosystems.
All Rights Reserved. Siehe LICENSE.
