standard:
  id: ATC-STD-100
  title: "ATC-STD-100 — Language & Technology Stack Standard"
  version: "1.0.0"
  status: candidate
  category: architecture
  authority: A-TownChain Ecosystems
  owner: ShivaCoreDev
  created: "2026-09-07"
  updated: "2026-09-07"
  normative: true
  supersedes: null
  superseded_by: null

---

# ATC-STD-100 — Language & Technology Stack Standard

> **Version:** 1.0.0 (FORMAL)
> **Status:** CANDIDATE (Owner-Entwurf 07.09.2026; Normativkraft entsteht mit APPROVED gemaess ATC-STD-000 §9)
> **Reihe:** ATC-STD-100–199 (Architektur-Block, categories.yaml) · **Autoren:** Michael Wroblewski (Owner), Aurora (Superagent)
> **Kernprinzip:** Eine Sprache je Ebene — Rust ist das System of Record der ATC-Kerntechnologie.
> **Scope:** Alle Repositories der Organisation A-TownChain-Okosystems (25 aktive Repos, AD-044-Stand).
> **Verweise:** ATC-STD-000 (§7 IDs, §24 Registry), ATC-STD-201/202/203, ATC-STD-300, AD-021 (Rust-first), AD-001 (SHA-256)

---

## Abstract

Dieser Standard schreibt die verbindliche Programmiersprachen- und Stack-Strategie der A-TownChain-Plattform fest. Die Plattform ist mehrschichtig (Protocol/Core, Application, AI, OS, Governance); jede Ebene erhlt genau eine kanonische Implementierungssprache. **Rust ist das System of Record fuer die ATC-Kerntechnologie** (Blockchain, Konsens, VM, Kryptografie, Storage, OS/Kernel), **Python** ist die Sprache der AI/ML-Forschung und des Model-Layers, **TypeScript** traegt die Application-/UI-Schicht, und **Markdown/YAML/JSON** bilden den Spezifikations- und Governance-Layer.

## 1. Layer-Modell (REQ-STD-101: MUST)

Die Plattform gliedert sich in fuenf technische Ebenen. Jedes Repository MUSS genau einer Ebene zugeordnet sein (registry/repositories.yaml: domain-Feld).

| Layer | Repositories | Kanonische Sprache |
|---|---|---|
| **L1 — Protocol / Core** | atc-node, atc-shivacore, atc-vm, atc-algorithm, atc-contracts, atc-compute, atc-storage, atc-oracle, atc-interop, atc-indexer, a-townchain | Rust |
| **L2 — Application** | atc-explorer, atc-marketplace, atc-launchpad | TypeScript (+ React) |
| **L3 — AI** | aurora-ai (Core: Rust / AI-ML-Layer: Python) | Rust + Python (getrennt) |
| **L4 — OS** | a-townchain-os, globus-os | Rust |
| **L5 — Specification / Governance** | atc-standards, a-townchain-os-docs, genesis-chronicles (Lore/World) | Markdown, YAML, JSON |

## 2. Sprachbindungen (REQ-STD-102: MUST)

Die folgende Tabelle ist normativ. Neue Implementierungen in den genannten Kategorien MUESSEN in der kanonischen Sprache erfolgen; bestehende Nicht-Kanon-Implementierungen sind Migrations-Kandidaten (Technology Profile Audit, §4).

| Kategorie | Verbindliche Sprache |
|---|---|
| Blockchain Core | Rust |
| Node | Rust |
| Konsens (ATC-Algorithmus) | Rust |
| VM (ATVM) | Rust |
| Smart Contracts | ATCLang (AD-006/99); ABI-Definition: Rust |
| Kryptografie | Rust |
| Storage | Rust |
| Networking | Rust |
| OS / Kernel / Treiber | Rust |
| Mining Core | Rust |
| SDK Core | Rust |
| AI Runtime | Rust |
| AI/ML Research & Model Layer | Python |
| Web Frontend | TypeScript |
| Explorer / Marketplace / Launchpad | TypeScript |
| Web Backend/API | Rust (L1-Kontext) oder TypeScript (L2-Kontext) — je nach Layer-Zuordnung |
| Dokumentation | Markdown |
| Konfiguration | YAML / TOML / JSON |
| CI/CD | YAML + Shell |

**Kurzregel:** Rust = System of Record der ATC-Kerntechnologie. Python = AI/ML-Experimentation. TypeScript = Application/UI. Markdown/YAML/JSON = Specification & Governance.

## 3. Ausnahmen & Referenz-Implementierungen (REQ-STD-103)

- Python-Referenz-Implementierungen (z.B. ATCLang-Interpreter, PoH-Referenz in a-townchain) DÜRFEN bis zur Rust-Canonical-Umsetzung (AD-021) weitergefuehrt werden; sie SOLLEN als `reference/`-Verzeichnis klar gekennzeichnet sein und KEINE produktiven Pfade ersetzen.
- ATCLang (AD-006, ATC-99) ist als eigenstaendige Sprache von dieser Policy nicht erfasst; sein Tooling folgt AD-021 (Rust-first Compiler, Python als Referenz).
- Eine Ausnahme von der kanonischen Sprache erfordert einen Architecture Decision (AD) mit Owner-Freigabe.

## 4. Technology Profile Audit (REQ-STD-104: SHOULD)

Je Repository SOLL ein Technology Profile gepflegt werden (Wiki: REPOSITORY_MAP.md): tatsaechliche Dateien, tatsaechliche Sprachverteilung, Frameworks, Build-System, Abhaengigkeiten, Zweck, Ueberschneidungen und Empfehlung (behalten / zusammenlegen / umbenennen / verschieben). Vorgesehene Sprache (registry) und tatsaechlicher Codebestand MUESSEN unterschieden werden. Skelett-Repositories (R1 ohne Implementierung) werden als solche gekennzeichnet.

## 5. Verweise

- AD-021: ATCLang Rust-first, Python = Referenz — Modell fuer alle Migrationspfade.
- AD-001: SHA-256 als einziger Hash-Algorithmus (Kryptografie-Bindung).
- ATC-STD-202: Naming & Classification (`atc-<domain>-<component>`).
- registry/repositories.yaml: maschinenlesbare Repo-/Layer-/Domain-Zuordnung.

## REQ-Matrix (normative Anforderungen)

| ID | Anforderung | Verweis |
|----|-------------|---------|
| id: REQ-STD-101 | Jedes Repository MUSS genau einem Layer (L1–L5) zugeordnet sein. | §1 |
| id: REQ-STD-102 | Neue Implementierungen MUESSEN der kanonischen Sprache ihrer Kategorie folgen. | §2 |
| id: REQ-STD-103 | Nicht-kanonische Bestands-Implementierungen MUESSEN als Migrations-Kandidaten gefuehrt werden; Ausnahmen erfordern AD mit Owner-Freigabe. | §3 |
| id: REQ-STD-104 | Je Repository SOLLEN tatsaechlicher Stack und vorgesehener Stack getrennt dokumentiert sein (Technology Profile). | §4 |
| id: REQ-STD-105 | Die Registry (repositories.yaml) MUSS die Layer-/Domain-Zuordnung maschinenlesbar fuehren. | §5 |

## Compliance

Die Einhaltung wird geprueft durch: (1) atc-std-validator (Registry-Sync S-14, Head-Sync S-19), (2) Technology Profile Audit je Repository ( Soll-/Ist-Vergleich), (3) Repo-Audit R3 (ATC-STD-201ff). Abweichungen werden als Findings (ATC-STD-BUG-001) und ggf. Change Requests (SCR) gefuehrt.

## Security Considerations

Sprachwahl ist sicherheitsrelevant: Kryptografie-, Konsens- und VM-Komponenten (S4) MUESSEN in Rust (Memory-Safety) erfolgen; unsicherer Fremdcode in diesen Pfadketten ist unzulaessig. Der Language-Policy-Check ist Teil des G18-Security-Audits (AD-023).

## Changelog

- 1.0.0 (2026-09-07): Initiale Fassung. Layer-Modell L1–L5, Sprachbindungen, Ausnahme-Regelung fuer Referenz-Implementierungen, Technology Profile Audit als SHOULD-Regel. Status: CANDIDATE (wartet auf APPROVED gemaess ATC-STD-000 §9).

## References

**NORMATIVE**
- ATC-STD-000 — Standards Governance & Specification Standard (Verfassung; v1.1.0, APPROVED)
- registry/categories.yaml — ID-Raeume (100er-Block: Architektur)
- registry/repositories.yaml — maschinenlesbare Layer-/Domain-Zuordnung

**INFORMATIVE**
- AD-021/AD-022 — Rust-first ATCLang, 21-Crate-Layout, Gates G0–G19
- AD-043/AD-044 — atc-vm, atc-algorithm (Beispiel-Repos fuer S-14-Kernkomponenten)
- REPOSITORY_MAP.md (a-townchain-os-docs) — Technology Profile je Repository
