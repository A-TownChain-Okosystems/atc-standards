---
standard:
  id: ATC-STD-100
  title: "Language & Technology Stack Standard"
  version: "2.1.0"
  status: candidate
  category: architecture
  authority: "A-TownChain Ecosystems"
  owner: "Michael Wroblewski (Owner-Entwurf) / Standards Governance"
  created: "2026-09-07"
  updated: "2026-10-01"
  normative: true
  applies_to: "Alle ATC-Repositories"
  mandate: "Owner-Entwurf 11.09.2026 (Language Architecture, SCR-0093)"
----

# ATC-STD-100 — Language & Technology Stack Standard (v2.1.0, CANDIDATE)

> **Status:** CANDIDATE (v2.1.0) — Owner-Entwurf Language Architecture 11.09.2026
> (SCR-0093): Hierarchische Language Architecture L0-L8 mit Entscheidungskaskade
> und Repo-Matrix; ersetzt das 5-Layer-Modell von v1.0.0 (Mapping §7). par.9-freigegeben 11.09.2026 (Owner-Direktive, SCR-0102) — v2.0.0 APPROVED als MAJOR (Migration par.7 dokumentiert, COMPAT-001). **Scope:** ATC-STD-100 · Sprache- und
> Technologieauswahl aller Repositories · **Governance:** ATC-STD-000

## Abstract

ATC-STD-100 definiert die verbindliche Language Architecture des
A-TownChain-Ökosystems: keine zufällige Polyglot-Architektur, sondern eine
hierarchisch definierte Sprach- und Technologieauswahl je Layer und Repository.
Kern: Rust als Default- und normative Implementierungssprache überall dort, wo Rust die
technische Anforderung erfüllt. ATCLang ist die native Anwendungssprache für
ATC-Programme (ATC-99). TypeScript ist auf Browser-/UI-Grenzen beschränkt.
Python ist auf AI/ML-Research und nicht-normative Tooling-/Analyseaufgaben
beschränkt. C/C++/Assembly sind Boundary-Technologien und benötigen eine
konkrete technische Begründung. WASM ist ein Target, keine Primärsprache; SQL
ist Query-/Persistence-Technologie und niemals Consensus Truth.

Schlüsselwörter: MUSS/MUSS NICHT, SOLLTE, DARF/KANN — RFC 2119 gemäß ATC-STD-000 §10.

## 1. Language Architecture L0-L8 (REQ-STD-105: MUST)

Die Ökosystem-Architektur MUSS dem folgenden Layer-Modell folgen; jede
Komponente MUSS ihrem Layer zugeordnet sein:

| Layer | Bereich | Sprachen |
|---|---|---|
| L0 — Hardware | Firmware, Boot, CPU-Schnittstellen | Rust-first; Assembly/C nur wenn technisch erforderlich |
| L1 — Kernel | ShivaCore-Kernel, Memory, Capabilities | Rust |
| L2 — Runtime | ATC Runtime, ATC-VM, Deterministic Execution | Rust |
| L3 — Blockchain | Node, Consensus, Networking, Kryptografie, ZKP, Storage | Rust |
| L4 — Native ATC Programming | Smart Contracts, On-chain Logic, ATC-Programme | ATCLang |
| L5 — AI | Modelle, Research, Agents | Rust für Production Runtime/Control; Python nur Research/Model Tooling |
| L6 — SDK | Client-Libraries, Bindings | Rust Core; TypeScript/Python nur Bindings/SDK-Surfaces |
| L7 — Applications | Wallet, Explorer, Marketplace, OS-UI | Rust Core; TypeScript nur UI; ATCLang für On-chain Logic |
| L8 — Data | Indexer, Analytics, Off-chain State | Rust Core; SQL Query Layer; Python nur Analytics/Research |

Kette: ShivaCore → Rust → ATC Runtime → ATC-VM → A-TownChain Node → Consensus.

## 2. Sprachbindungen (REQ-STD-106: MUST)

- **Rust** MUSS die Default-Sprache sein, sobald eine Komponente System-, Security-, Performance-, Determinismus-, Netzwerk-, Storage-, Runtime-, SDK-Core- oder Execution-Verantwortung besitzt. Alles innerhalb des Security-/Consensus-/Execution-TCB MUSS Rust sein, sofern keine nachgewiesene technische Boundary dagegen spricht.
- **ATCLang** MUSS die native Anwendungssprache der Plattform sein (ATC-99
  ATCLang First). Trennung: Rust = Implementierung der Plattform, ATCLang =
  Programmierung für die Plattform (Application → ATCLang → ATC Compiler →
  ATC Bytecode → ATC-VM → Rust → A-TownChain). ATCLang MUSS NICHT Rust
  ersetzen; der ATCLang-Compiler/Toolchain selbst SOLLTE Rust-first sein (AD-021).
- **C** DARF nur an einer nachgewiesenen Hardware-/Vendor-/ABI-Grenze eingesetzt werden. Wenn Rust die konkrete Grenze vollständig abbilden kann, MUSS Rust verwendet werden. Die Begründung MUSS technisch sein, nicht „C ist schnell“.
- **Assembly** DARF nur verwendet werden, wenn Rust die konkrete CPU-/ABI-Operation nicht vollständig abbilden kann: Boot Entry, CPU-Initialization, Trap/Interrupt Entry, Context Switching oder unvermeidbare Registeroperationen. Assembly MUSS NICHT normale Business Logic enthalten.
- **C++** DARF nur als Boundary zu einer zwingend benötigten bestehenden externen Bibliothek/Engine eingesetzt werden. Neue ATC-Kernkomponenten MUSS Rust implementieren.
- **Python** DARF für AI/ML-Research, Prototyping, Analyse, Testautomation und Tooling eingesetzt werden. Für produktive Runtime-, Security-, Consensus- oder deterministische Ausführung MUSS Rust verwendet werden, sofern keine dokumentierte technische Boundary dagegen spricht.
- **TypeScript** ist die Standard-Frontend-/UI-Sprache dort, wo Browser-/JS-Interoperabilität erforderlich ist. Security-, Protocol-, SDK-Core- und Runtime-Logik MUSS außerhalb dieser UI-Grenze Rust bleiben.
- **JavaScript** SOLLTE vermieden werden (nur Legacy-/Runtime-Zwang).
- **WASM** IST Deployment-/Execution Target (keine Primärsprache): Browser,
  portable Tools, Plugins, Sandbox, SDK-Komponenten. ATC Bytecode und WASM
  MÜSSEN NICHT ungeprüft gleichgesetzt werden — das ATC-Execution-Modell
  behält seine eigenen Semantics.
- **SQL** DARF für Query-/Index-/Persistence-Layer eingesetzt werden (Indexer,
  Explorer, Analytics); der kanonische Blockchain-State MUSS NICHT mit SQL
  gleichgesetzt werden — SQL ist nicht Consensus Truth.
- **Go** DARF nicht für neue ATC-Kernkomponenten eingeführt werden. Bestehende Go-Boundaries benötigen eine dokumentierte technische Ausnahme und einen Migrationsentscheid.

## 3. Rust-First-Entscheidungskaskade (REQ-STD-107: MUST)

Die Kaskade gilt für jede neue Komponente, jedes neue Modul und jede Migration.
Die erste zutreffende Regel gewinnt:

1. **Kann Rust die technische Anforderung erfüllen? → JA → Rust.**
2. Rust kann die konkrete Hardware-/Vendor-/ABI-Grenze nicht vollständig abbilden? → **minimaler C/Assembly/C++-Boundary**, isoliert und dokumentiert.
3. On-chain Application/Contract? → **ATCLang**.
4. Browser-/Web-UI benötigt JavaScript-Ökosystem? → **TypeScript**.
5. ML-Training/Research-Ökosystem benötigt Python? → **Python**, außerhalb des TCB.
6. Datenbankabfrage/Persistence-Schnittstelle? → **SQL** als Query-Sprache, Rust als kontrollierende Anwendung.
7. Kein Treffer → SCR + ATC-STD-TUD-001.

Eine Sprache DARF NICHT allein wegen vorhandener Libraries, Entwicklerpräferenz,
vermeintlicher Geschwindigkeit oder historischer Nutzung gewählt werden, wenn
Rust die Anforderung erfüllt.

Boundary-Code MUSS:
- die technische Grenze dokumentieren,
- keine Consensus-/Security-/Kernel-Truth definieren,
- eine minimale stabile ABI besitzen,
- reproduzierbar testbar sein,
- und eine Ownership-/Migrationsentscheidung besitzen.

Abweichungen von der Kaskade MÜSSEN als Finding (ATC-STD-BUG-001) oder Exception
(ATC-STD-EXC-Familie) dokumentiert sein.

## 4. Repository-Matrix (REQ-STD-108: MUST)

| Repository | Primär | Sekundär |
|---|---|---|
| atc-shivacore | Rust | Assembly, C (Boot/HAL) |
| atclang | Rust (Compiler/Toolchain) | ATCLang (Zielsprache) |
| atc-vm | Rust | Python nur Referenz/Conformance, nie TCB |
| a-townchain | Rust | Python nur Tests/Tooling; keine normative Semantik |
| atc-node | Rust | — |
| atc-zkp | Rust | Python (Research) |
| atc-algorithm | Rust | Python (Benchmark/Research) |
| atc-storage | Rust | SQL (Query) |
| atc-compute | Rust | Python (Workloads/Research) |
| atc-oracle | Rust | Adapter je externem System |
| atc-interop | Rust | Adapter je Protokoll |
| atc-wallet | Rust (Core) | TypeScript (UI), WASM (Browser) |
| atc-indexer | Rust (Core) | SQL (Database) |
| atc-explorer | Rust (Backend/Core) | TypeScript (Frontend) |
| atc-marketplace | Rust (Core/Backend) | TypeScript (Frontend), ATCLang (On-chain Logic) |
| atc-launchpad | Rust (Core/Backend) | TypeScript (Frontend), ATCLang (On-chain Logic) |
| atc-contracts | ATCLang | — |
| aurora-ai | Rust (Production Runtime/Authority) | Python (Research/Model Tooling), TypeScript (UI) |
| globus-os | Rust (System) | TypeScript (UI); Kernel: ShivaCore; AI: Aurora |
| genesis-engine | Rust | C++ nur bestehende externe Engine/ABI; ATCLang für Game Logic; TypeScript für Tools/UI |

Repository-Rollen (Scope/Write) regelt ATC-STD-202; die Matrix hier ist
sprachseitig verbindlich.

## 5. Governance-Kopplungen (REQ-STD-109: MUST)

- Neue Technologie-Entscheidungen MÜSSEN durch ATC-STD-TUD-001
  (Technology Uniqueness & Differentiation) laufen: keine Sprache/Framework
  ohne Technology-Registry-Eintrag und Klassifikation.
- Sprach-Policy-Drift (Repo weicht von Matrix ab) MUSS vom Repository-Audit
  (ATC-STD-REPO-AUDIT-003) als Finding gemeldet werden; CI-Sprach-Gate als
  Validator-Erweiterung SOLLTE folgen.
- v1.0.0-Regeln bleiben wirksam, soweit nicht durch §1-§4 ersetzt (§7).

## 6. Migration v1 → v2 (Mapping, REQ-STD-110)

v1.0.0-Layer → v2.0.0-Layer: L1 Protocol/Core Rust → L1-L3; L2 Application
TypeScript → L7; L3 AI Rust+Python → L5; L4 OS Rust → L0-L1; L5 Spec/Governance
Markdown → ATC-STD-000 (nicht mehr Sprach-Layer, sondern Dokumentationsform).
Neu in v2.0.0: L0 Hardware (Assembly/C), L4 ATCLang als eigene Stufe, L6 SDK,
L8 Data. Das Ökosystem-Layer-Modell (AD-026, L0-L12) bleibt davon unberührt —
Sprach-Layer ≠ Ökosystem-Layer.

## REQ-Matrix (normative Anforderungen)

- id: REQ-STD-105 — Language Architecture L0-L8: Layer-Zuordnung jeder Komponente MUSS vollständig sein.
- id: REQ-STD-106 — Sprachbindungen: MUST/VERBOT-Regeln je Sprache inkl. TCB-Regel (Rust), ATCLang-Trennung (ATC-99), Python-TCB-Verbot, JS-Vermeidung, WASM-Semantik-Trennung, SQL-nicht-Consensus-Truth.
- id: REQ-STD-107 — Entscheidungskaskade: Auswahl MUSS der Kaskade folgen; Abweichungen MÜSSEN dokumentiert sein.
- id: REQ-STD-108 — Repository-Matrix: Sprachzuordnung je Repository MUSS der Matrix entsprechen; Drift MUSS als Finding gemeldet werden.
- id: REQ-STD-109 — Governance-Kopplung: Neue Sprachen/Technologien MÜSSEN via TUD-001 laufen; REPO-AUDIT-003 meldet Drift.
- id: REQ-STD-110 — Migration: v1-Layer-Mapping MUSS dokumentiert bleiben; Ökosystem-Layer (AD-026) MUSS NICHT umbenannt werden.

## Compliance

Prüfung im Governance-Validator: S-06/S-07 (Struktur), MD-Gates (Frontmatter),
REQ-IDs deklariert und eindeutig. Repository-Audit (ATC-STD-REPO-AUDIT-003)
prüft Repository-Sprachprofil gegen die Matrix (REQ-STD-108) und meldet
Abweichungen als Finding.

## Security Considerations

- TCB-Schutz: Nur Rust in L1-L3 (Memory Safety, no_std, deterministische
  Ausführung); Python/AI MUSS NICHT Konsens oder Kernel kontrollieren —
  KI-Governance per ATC/ATS-Trennung (ATC-STD-TUD-001 §ATC-TECH-004).
- Supply Chain: Neue Sprachen/Frameworks = neue Angriffsfläche → TUD-001-
  Klassifikation + ATC-STD-019 (Supply Chain Security) vor Einführung.
- WASM-Sandbox: WASM-Komponenten gelten als untrusted code; ATC Bytecode
  behält eigene Semantics (keine ungeprüfte Gleichsetzung).
- FFI/C-Grenze: Jede C-ABI/FFI-Stelle MUSS technisch begründet und im
  Repository-Audit sichtbar sein.

## Implementierungsstatus

**Status: CANDIDATE** — v2.1.0 implementiert die Rust-First-Verschärfung und wartet auf die formale §9-Freigabe;
Implementierungs-Evidence entsteht über Technology Profile Audits je Repository
(S. ATC-STD-REPO-AUDIT-003): aktuelle R1-Skelette sind Soll-Zustand; bekannte
Policy-Drifts (atclang nur Python, a-townchain ohne Rust-Chain-Code) sind
als Findings zu führen und über SCR zu beheben. Kein Status ohne Evidence
(ATC-STD-000 §14). SSOT für Implementierungsstand: registry/standard-
implementation.yaml.

## Changelog

- v2.1.0 (2026-10-01): Rust-First-Prinzip als vorrangige Auswahlregel; C/C++/Assembly auf technische Boundaries begrenzt; Python aus produktiven TCB-/Runtime-Pfaden ausgeschlossen; SDK-, AI-, Indexer- und Game-Engine-Matrix auf Rust-Core korrigiert; maschinenlesbare Enforcement-Policy und Validator ergänzt.
- v2.0.0 (2026-09-11): Owner-Entwurf Language Architecture — L0-L8-Layer-
  Modell, Entscheidungskaskade, Repository-Matrix, Governance-Kopplung an
  TUD-001/REPO-AUDIT-003, Migration von v1.0.0 (5-Layer) dokumentiert.
  Status CANDIDATE (SCR-0093).
- v1.0.0 (2026-09-07): 5-Layer-Modell (L1 Rust Core, L2 TypeScript App,
  L3 AI, L4 OS Rust, L5 Markdown), Sprachbindungen, Ausnahmen, Technology
  Profile Audit. Status APPROVED.

## References

- ATC-STD-000 — Governance Root (§9 Lifecycle, §10 RFC 2119, §14 Evidence)
- ATC-99 / ATCLang First Policy — native Programmierung
- ATC-STD-202 — Repository Naming & Classification (Rollen/Scope)
- ATC-STD-TUD-001 — Technology Uniqueness & Differentiation (Technologieauswahl)
- ATC-STD-REPO-AUDIT-003 — Repository-Audit (Sprachprofil-Drift)
- AD-021/AD-022 — ATCLang Rust-first, 21-Crate-Layout
- AD-026 — Ökosystem-Layer-Modell (unberührt, Mapping §6)
- audits/PRIOR-ART-2026-09-11.md — Technologie-Klassifikationen des Stacks
