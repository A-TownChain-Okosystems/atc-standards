# External SCR source bindings — 2026-11-01

## Scope and verification boundary

This report records direct GitHub source-file retrievals at the exact historical commit refs listed below. For each row, the GitHub file-content endpoint returned the listed Git blob SHA for the path at that commit.

This is stronger than a commit-message-only reference: it binds a repository, immutable commit, path, and returned blob object ID. The controlled verifier added to this PR now independently acquires each pinned external commit and checks the commit object, tree object, and path-level blob using Git object operations. The exact-head SCR Registry Gate completed this verification successfully (details below).

GitHub file retrieval confirms the object identifiers exposed by the source API. It does not establish signer trust, Owner authority, SCR allocation, normative force, or lifecycle closure.

## Exact-head CI verification — 2026-11-01

- PR head tested: `86a5f1db7bb1049d82ad7568ed60068147b201cf`
- SCR Registry Gate: run `41254589687`, job `124694951819` — PASS
- External verifier: `EXTERNAL SOURCE VERIFICATION: PASS — 15 path/blob bindings across exact commit trees`
- Regression suite: `46/46` passed, including four external-verifier tests
- Registry validator: `SCR REGISTRY: PASS — 140 entries, 31 unresolved entries, 0 unresolved ranges; no ID auto-allocation`
- Evidence artifact: `scr-registry-evidence-41254589687-1`, artifact ID `13062284090`
- Artifact ZIP SHA-256: `3b74ef7e6566b9601cddcfa06852826398cbd9aa98ca4de88785bc58e38a20d8`

The 15 external pins cover all cross-repository commit/path bindings in the machine-readable manifest. The additional SCR-0139 standards-file path in this report is in the current `atc-standards` repository and is checked by the existing local blob-binding validator. This verifies source object identity; it does not establish signer trust or decision authority.

## SCR-0133 — dependency/security remediation

| Repository | Commit | Path | Git blob SHA |
|---|---|---|---|
| `A-TownChain-Okosystems/aurora-ai` | `15f328faf735d2a4d9abd3b0fec547fa14897335` | `modules/atc-aistudio/package-lock.json` | `1d1ac89ad09a59b970289b800a16449ff53426db` |
| `A-TownChain-Okosystems/aurora-ai` | `15f328faf735d2a4d9abd3b0fec547fa14897335` | `modules/atc-aistudio/package.json` | `926885560c104f997637980fc416b5ae568c4a93` |
| `A-TownChain-Okosystems/a-townchain-os-docs` | `8acd969e0467a3d770595c2946573cff7ca0e6ea` | `docs/wiki/kai-os/code/backend/requirements.txt` | `5e689580fbb69a53fe7a814f2032b1f0042ebbde` |
| `A-TownChain-Okosystems/a-townchain-ecosystem` | `ecdba9ec478737d4f7b25e80c8ed7c31d96d7a83` | `components/indexer/modules/atc-analytics/package.json` | `41e71937dd967368ac728958373a588d0874ecb7` |
| `A-TownChain-Okosystems/a-townchain-os-docs` | `68478c45bf3a2d555f4c6a5d9c06e5c3bbd1e8fe` | `aistudio/package-lock.json` | `a495456df5cb3f648e8c7e40ae875b330abbc3fc` |
| `A-TownChain-Okosystems/a-townchain-os-docs` | `68478c45bf3a2d555f4c6a5d9c06e5c3bbd1e8fe` | `aistudio/package.json` | `ba5ee9012d04d02764d869cfbb18ca2a535f7b62` |
| `A-TownChain-Okosystems/a-townchain-os-docs` | `68478c45bf3a2d555f4c6a5d9c06e5c3bbd1e8fe` | `docs/wiki/kai-os/code/backend/requirements.txt` | `72e305008ae9eb7a680691da0fc16f2a8a7cead8` |

The commit messages and changed-file lists directly reference SCR-0133. These sources evidence dependency/security remediation activity, not the formal allocation or closure of SCR-0133.

## SCR-0134 — exact-SHA census and ZKP formatting

| Repository | Commit | Path | Git blob SHA |
|---|---|---|---|
| `A-TownChain-Okosystems/a-townchain-os-docs` | `ae2fea101b5d2ccb6a5fa6fcb00f3b6f52004953` | `docs/audits/FILE-CENSUS-2026-10-09.md` | `dc40fcc88734a2f7b3ec957f25d8a44e4de2c4bf` |
| `A-TownChain-Okosystems/atc-zkp` | `9771ffed3ac5b3761c4d81e9c4d63cd4d2070108` | `crates/zkp-circuits/src/lib.rs` | `a0217bb0b1d7b48bafa9ec66313ddb154e889a13` |
| `A-TownChain-Okosystems/atc-zkp` | `9771ffed3ac5b3761c4d81e9c4d63cd4d2070108` | `crates/zkp-core/src/lib.rs` | `72d4f03360ba082bbd86deb5a0d81b4c71c712c6` |
| `A-TownChain-Okosystems/atc-zkp` | `9771ffed3ac5b3761c4d81e9c4d63cd4d2070108` | `crates/zkp-crypto/src/lib.rs` | `995143b8d904a054d2690512feedc78182d6db85` |
| `A-TownChain-Okosystems/atc-zkp` | `9771ffed3ac5b3761c4d81e9c4d63cd4d2070108` | `crates/zkp-prover/src/lib.rs` | `6e7f9ceef4697a631c048648e8219419be37fc77` |
| `A-TownChain-Okosystems/atc-zkp` | `9771ffed3ac5b3761c4d81e9c4d63cd4d2070108` | `crates/zkp-verifier/src/lib.rs` | `52415c9fffc2787169b5b379f029ae74b864f252` |
| `A-TownChain-Okosystems/atc-zkp` | `9771ffed3ac5b3761c4d81e9c4d63cd4d2070108` | `crates/zkp-vm/src/lib.rs` | `7bafe3cc3c061ae79b07d32537811d5752f137b4` |

The first commit message explicitly identifies the Exact-SHA File Census and SCR-0134. The ZKP commit message explicitly identifies SCR-0134 and the six changed Rust files. The latter is formatting provenance; it does not independently prove the census scope or an SCR lifecycle decision.

## SCR-0139 — Automation Authority

| Repository | Commit | Path | Git blob SHA |
|---|---|---|---|
| `A-TownChain-Okosystems/.github` | `750d920292149d16f327d8e33260d727599d873a` | `ai/automation-authority.yaml` | `157704b5079df2b38381a8ea57873782da83446c` |
| `A-TownChain-Okosystems/atc-standards` | `bceec03d7acd5bbaad42da10bbc2c75affd39f2f` | `standards/ai-gov/ATC-AI-GOV-AUTH-001.md` | `c91c3aeab59425fda6178fbc87f302a241b25025` |

The organization `.github` commit is implementation/configuration provenance. The standards commit is naming/generator-chain provenance. Neither unsigned commit is treated as a cryptographic Owner attestation. The existing `normative: false` and SCR lifecycle UNKNOWN values remain unchanged.

## Residual closure matrix

| Gap | Current state | Required closure evidence |
|---|---|---|
| External commit/path/blob | CI_VERIFIED for all 15 manifest pins | Exact-head SCR Registry Gate run `41254589687`, job `124694951819`; 15/15 external commit/tree/path/blob bindings verified. The local SCR-0139 standards path is checked by the existing registry blob validator. |
| Production signer trust | BLOCKED | Attributable authoritative public-key fingerprint and trust-root/rotation record; do not populate the allowlist from commit author names or unsigned provenance |
| Relationship graph integrity | BLOCKED | Normative definition of cross-entry target IDs, edge semantics, allowed cardinality and cycle policy before graph validation is implemented |
| Contradictory status metadata | RESIDUAL, surfaced | Separate authorized resolution of each contradiction; validator must continue reporting conflicts without rewriting standards or lifecycle state |

## Governance invariants

- No SCR ID was allocated or reused.
- SCR-0095, SCR-0096 and SCR-0139 remain unresolved where their lifecycle/authority evidence is incomplete.
- SCR-0142 remains PENDING.
- P1-A6 remains OPEN.
- No normative standard, historical source, Owner decision, or lifecycle field was changed by this evidence collection.
