# ATC Code Quality Matrix — Ist-Erhebung (2026-11-17 10:22)

Standard: ATC-STD-ENG-001 (REQ-ENG-011) · SSOT: registry/code-quality-matrix.yaml · Exit: 0

| Repository | Layer | Det.-Klasse | Ist-Sprache (Anteile) | Lang | CI-Gates (Soll) | Fehlt | Verdict |
|---|---|---|---|---|---|---|---|
| atclang | L0 | D-CRITICAL | Rust (rust 88.6%, python 11.4%) | ✅ | format, lint, build, unit, integration, security, dependency-audit, determinism | — | PASS |
| atc-vm | L0 | D-CRITICAL | Rust (rust 100.0%) | ✅ | format, lint, build, unit, integration, security, dependency-audit, determinism | — | PASS |
| atc-shivacore | L1 | D-CRITICAL | Rust (rust 81.4%, python 18.6%) | ✅ | format, lint, build, unit, integration, security, dependency-audit, determinism | — | PASS |
| atc-zkp | L1 | D-CRITICAL | Rust (rust 74.9%, python 25.1%) | ✅ | format, lint, build, unit, security, dependency-audit, determinism | — | PASS |
| aurora-ai | L2 | D-STANDARD | TypeScript (typescript 83.2%, rust 15.5%, javascript 0.8%) | ✅ | format, lint, build, unit, integration, security, dependency-audit | — | PASS |
| a-townchain | L3 | D-CRITICAL | TypeScript (typescript 39.8%, rust 30.4%, python 28.3%) | ✅ | format, lint, build, unit, integration, security, dependency-audit, determinism | — | PASS |
| atc-algorithm | L3 | D-CRITICAL | Rust (rust 74.1%, python 25.9%) | ✅ | format, lint, build, unit, security, dependency-audit, determinism | — | PASS |
| globus-os | L4 | D-HIGH | Rust (rust 98.0%, python 1.3%, typescript 0.6%) | ✅ | format, lint, build, unit, integration, security, dependency-audit | — | PASS |
| atc-contracts | L5 | D-CRITICAL | JavaScript (javascript 84.0%, shell 13.3%, python 2.7%) | ✅ | format, lint, build, unit, security, dependency-audit, determinism | — | PASS |
| atc-sdk | L5 | D-HIGH | Rust (rust 45.4%, python 28.1%, typescript 26.5%) | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| atc-wallet | L5 | D-CRITICAL | Python (python 63.9%, rust 36.1%) | ✅ | format, lint, build, unit, security, dependency-audit, determinism | — | PASS |
| atc-explorer | L5 | D-STANDARD | TypeScript (typescript 100.0%) | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| atc-indexer | L5 | D-HIGH | TypeScript (typescript 100.0%) | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| atc-interop | L5 | D-HIGH | Rust (rust 60.5%, python 39.5%) | ✅ | format, lint, build, unit, security, dependency-audit, determinism | — | PASS |
| atc-node | L5 | D-CRITICAL | Rust (rust 90.5%, python 9.5%) | ✅ | format, lint, build, unit, integration, security, dependency-audit, determinism | — | PASS |
| atc-storage | L5 | D-CRITICAL | Python (python 64.0%, rust 36.0%) | ✅ | format, lint, build, unit, integration, security, dependency-audit, determinism | — | PASS |
| atc-compute | L5 | D-HIGH | Rust (rust 100.0%) | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| atc-mining | L5 | D-CRITICAL | Rust (rust 66.3%, python 33.7%) | ✅ | format, lint, build, unit, security, dependency-audit, determinism | — | PASS |
| atc-oracle | L5 | D-HIGH | Rust (rust 100.0%) | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| atc-launchpad | L5 | D-STANDARD | Rust (rust 100.0%) | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| atc-marketplace | L5 | D-STANDARD | Rust (rust 83.3%, typescript 16.7%) | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| genesis-engine | L6 | D-CRITICAL | Rust (rust 78.8%, python 21.2%) | ✅ | format, lint, build, unit, security, dependency-audit, determinism | — | PASS |
| genesis-chronicles | L6 | D-STANDARD | Python (python 95.2%, rust 4.8%) | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| a-townchain-os | L7 | D-HIGH | Rust (rust 98.6%, powershell 0.8%, inno setup 0.6%) | ✅ | format, lint, build, unit, integration, security, dependency-audit | — | PASS |
| a-townchain-os-docs | L7 | D-STANDARD | TypeScript (typescript 64.3%, python 29.2%, html 5.2%) | ✅ | format, build, docs | — | PASS |
| atc-standards | L7 | D-STANDARD | Python (python 99.8%, rust 0.2%) | ✅ | format, lint, build, unit, cross-registry, security, dependency-audit | — | PASS |

**Ergebnis: 26/26 PASS, 0 FINDING(s)** (Fail Closed; Findings → ATC-STD-BUG-001)
