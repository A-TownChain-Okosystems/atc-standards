# ATC Standards — Die normative Governance-Schicht der A-TownChain-Organisation

> **ATC COMPLIANCE: R3 · BETA · Standard ATC-STD-201 v1.0.0 · GATE: AUDITED (07.09.2026)**

**Governance Chain (AD-031/034):** ATC-STD-000 (Verfassung) → Standard Registry
→ Standards → Validator (atc-std) → Repository Schema → Template → Repository
Creation → ATC Repo Auditor → (PASS → Development → CI → Security Gates →
Architecture Gate → Release Gate → Production | FAIL → NO-GO).

> **Grundsatz (ATC-STD-000 §22):** No ATC Standard is normative unless it is
> registered, versioned, reviewed and explicitly approved according to this
> specification. Registry + Repo schlagen README/Wiki/Issue/Chat.

> **Standard-Repo:** ATC-STD-202 Typ SPEC · Level R3 · Chain-ID 658467 · AD-030 (07.09.2026)

## 1. Purpose

Dieses Repository ist DIE kanonische Heimat aller definierten Standards der
A-TownChain-Okosystems-Organisation: Blockchain-Standards (ATC-01…ATC-99),
System-/Hardware-Lizenzen (ATS), Repository-Governance (ATC-STD-201/002/003)
sowie die .atc-Referenzimplementierungen. Jedes Repository der Organisation
richtet sich nach den hier definierten Regeln.

## 2. Scope

Offiziell verbindlich fuer alle Repositories der Organisation (AD-029/AD-030).
Das Repositorium selbst erfuellt den ATC-STD-201 (self-compliant).

## 3. Architecture

- `governance/` — ATC-STD-000 v1.0.0 (Verfassung) + CHANGE_CONTROL.md
  (SCR-Verfahren mit Registry) + APPROVAL_PROCESS.md (Freigabe-Ablauf
  CANDIDATE→STABLE)
- `approval/` — Formales Review-Paket ATC-STD-000 v1.0.0 (Snapshot, 3
  Reviews, Requirement-Matrix, Decision: PENDING)
- `change-requests/` — SCR-Registry-Dokumente SCR-0001…0004
  (ID-Raeder 000-1000+, Lifecycle IDEA…RETIRED, Metadaten-Pflicht, REQ-IDs,
  SemVer/Breaking Changes, SCR-Prozess, Review-Chain, Supersession,
  Registry-Pflicht, Validator-Anforderung)
- `atc/` — 105 Standards: ATC-01…99 + ATC-0001…0008 (ATC_STANDARDS.md,
  Core-Protokolle) + ATC_TOKEN_STANDARD + ATC-LIC + ATC_ECOSYSTEM_STANDARDS
- `ats/` — ATS-Standards: ATS-1000…1007 (ATS_STANDARDS.md, ShivaOS Kernel/Stack) + ATS-LIC System-/Hardware-Lizenz
- `standards/repository/` — ATC-STD-201 v1.0.0 FORMALE SPEZIFIKATION
  (MUST/SHOULD/MAY, Compliance-Matrix R0-R4, Validator-Regeln V-01…V-16),
  -002 (Naming, Classification, Ownership, Lifecycle, S0-S4, Dependency Graph),
  -003 (Security, Release, Branching, Commits, PRs, Gates, Reproducible Builds)
- `schemas/` — repository/compliance/ownership/lifecycle.schema.yaml
- `registry/` — standards.yaml (Standard-Registry, ATC-STD-000 §20),
  categories.yaml, versions.yaml, lifecycle.yaml, dependencies.yaml
  (Repository- + Standard-Graph, Zyklenerkennung), repositories.yaml
  (23 Repos), teams.yaml, findings.yaml (F-Registry) + STANDARDS_REGISTRY/OVERVIEW
- `tools/` — atc-repo-audit v0.1.0 (Repository-Validator, 16 Regeln) und
  atc-std-validator v0.1.0 (Standard-Validator, 15 Regeln S-01…S-15)
- `templates/` — repository- (.atc-Vorlagen, PR-Template) und workflow-Vorlagen
- `docs/governance/` — Governance-Chain-Doku
- `registry/` — STANDARDS_REGISTRY.md (Master-Registry), OVERVIEW.md
- `licensing/` — Lizenz-Standard-Spezifikationen: ATVM License Gate, IP & License
  Dashboard (GlobusOS), Smart-Contract-Richtlinie (BaFin)
- `references/` — .atc-Referenzimplementierungen (registry.atc, Standards-
  Vertragsmuster) + ATC-Modul-Doku

## 4. Features

- 119 Standard-Dokumente vollstaendig zentralisiert (inkl. ATC-STD-000)
- Normative 22-Repository-Klassifizierung (ATC-STD-202)
- Governance-Standards mit Compliance-Level R0-R4
- Maschinenlesbare Referenzvertraege (.atc)

## 5. Repository Structure

Gemaess ATC-STD-201; siehe docs/REPOSITORY_STANDARD.md.

## 6. Installation

Standards sind Markdown-Dokumente — kein Build. Klonen und lesen:
`git clone https://github.com/A-TownChain-Okosystems/atc-standards.git`

## 7. Development

Aenderungen an Standards NUR hier (kanonisch), nie mehr im Docs-Hub
(Hub-Kopie ist Archiv-Snapshot). Aenderungen an Governance-Standards
erfolgen via AD-Eintrag im zentralen DECISIONS_REGISTER (Hub) + Commit hier.

## 8. Testing

Standards werden ueber die STANDARDS_REGISTRY validiert (Status-Tracking:
FINAL/ACCEPTED/DRAFT/PROPOSED — historische Begriffe, normative Abbildung in registry/lifecycle.yaml legacy_status_map). .atc-Referenzen sind via atc-contracts
ausfuehrbar pruefbar.

## 9. Security

Siehe SECURITY.md. Sicherheitsrelevante Standardregeln: ATC-STD-203.

## 10. Roadmap

- Governance-Standards (ATC-STD-201/202/203): PROPOSED → STABLE nach
  erstem vollstaendigen R2+-Compliance-Nachweis zweier Repositories
- Laufende Ergaenzung neuer Standards entsprechend der Sprint-Planung

## 11. Versioning

Repository: Semantic Versioning (v1.0.0 Initial-Bestand, AD-030).
Einzelstandards tragen eigene Versionen; Protocol-/Implementation-/
Specification-Version sind unabhaengig (ATC-STD-203).

## 12. License

Copyright (c) 2026 Michael Wroblewski / ShivaCore / A-TownChain-Okosystems.
All Rights Reserved. Siehe LICENSE.
