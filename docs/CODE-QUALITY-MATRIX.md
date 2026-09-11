# ATC Code Quality Matrix — Ist-Erhebung (2026-09-11 19:18)

Standard: ATC-STD-ENG-001 (REQ-ENG-011) · SSOT: registry/code-quality-matrix.yaml · Exit: 1

| Repository | Layer | Det.-Klasse | Ist-Sprache | Lang | CI-Gates (Soll) | Fehlt | Verdict |
|---|---|---|---|---|---|---|---|
| atclang | L0 | D-CRITICAL | Python | ✅ | format, lint, build, unit, integration, security, dependency-audit, determinism | determinism | FINDING |
| atc-vm | L0 | D-CRITICAL | Rust | ✅ | format, lint, build, unit, integration, security, dependency-audit, determinism | — | PASS |
| atc-shivacore | L1 | D-CRITICAL | Rust | ✅ | format, lint, build, unit, integration, security, dependency-audit, determinism | determinism | FINDING |
| atc-zkp | L1 | D-CRITICAL | Rust | ✅ | format, lint, build, unit, security, dependency-audit, determinism | determinism | FINDING |
| aurora-ai | L2 | D-STANDARD | TypeScript | ✅ | format, lint, build, unit, integration, security, dependency-audit | — | PASS |
| a-townchain | L3 | D-CRITICAL | Python | ✅ | format, lint, build, unit, integration, security, dependency-audit, determinism | determinism | FINDING |
| atc-algorithm | L3 | D-CRITICAL | Rust | ✅ | format, lint, build, unit, security, dependency-audit, determinism | determinism | FINDING |
| globus-os | L4 | D-HIGH | Rust | ✅ | format, lint, build, unit, integration, security, dependency-audit | — | PASS |
| atc-contracts | L5 | D-CRITICAL | Python | ✅ | format, lint, build, unit, security, dependency-audit, determinism | determinism | FINDING |
| atc-sdk | L5 | D-HIGH | Rust | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| atc-wallet | L5 | D-CRITICAL | Python | ✅ | format, lint, build, unit, security, dependency-audit, determinism | determinism | FINDING |
| atc-explorer | L5 | D-STANDARD | TypeScript | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| atc-indexer | L5 | D-HIGH | TypeScript | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| atc-interop | L5 | D-HIGH | Rust | ✅ | format, lint, build, unit, security, dependency-audit, determinism | determinism | FINDING |
| atc-node | L5 | D-CRITICAL | Rust | ✅ | format, lint, build, unit, integration, security, dependency-audit, determinism | determinism | FINDING |
| atc-storage | L5 | D-CRITICAL | Rust | ✅ | format, lint, build, unit, integration, security, dependency-audit, determinism | determinism | FINDING |
| atc-compute | L5 | D-HIGH | Rust | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| atc-mining | L5 | D-CRITICAL | Rust | ✅ | format, lint, build, unit, security, dependency-audit, determinism | determinism | FINDING |
| atc-oracle | L5 | D-HIGH | Rust | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| atc-launchpad | L5 | D-STANDARD | Rust | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| atc-marketplace | L5 | D-STANDARD | TypeScript | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| genesis-engine | L6 | D-CRITICAL | Python | ✅ | format, lint, build, unit, security, dependency-audit, determinism | determinism | FINDING |
| genesis-chronicles | L6 | D-STANDARD | Python | ✅ | format, lint, build, unit, security, dependency-audit | — | PASS |
| a-townchain-os | L7 | D-HIGH | ? | ❌ | format, lint, build, unit, integration, security, dependency-audit | integration | FINDING |
| a-townchain-os-docs | L7 | D-STANDARD | TypeScript | ✅ | format, build, docs | docs | FINDING |
| atc-standards | L7 | D-STANDARD | Python | ✅ | format, lint, build, unit, cross-registry, security, dependency-audit | — | PASS |

**Ergebnis: 12/26 PASS, 14 FINDING(s)** (Fail Closed; Findings → ATC-STD-BUG-001)
