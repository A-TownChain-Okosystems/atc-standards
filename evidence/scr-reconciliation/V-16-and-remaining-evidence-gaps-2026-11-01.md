# V-16 Reverification and Remaining Evidence Gaps

Date: 2026-11-01
Repository: A-TownChain-Okosystems/atc-standards
Pull request: #120 — [Draft][SCR-0142] SCR registry implementation
Branch: governance/scr-registry-0142

## 1. Exact verification snapshot

This report records the completed verification snapshot before this documentation commit.

- PR head: `327cc40d07467effcecc6c389ee8779dc755e8d1`
- PR state at inspection: OPEN / DRAFT / unmerged
- Branch ref was read directly from GitHub: `refs/heads/governance/scr-registry-0142`
- The earlier reference `38efcb275b7adbf37c7feb937d1e4f992bbad755` is an ancestor, not the current head.

## 2. V-16 result

V-16 was re-evaluated against the actual Git history at the exact snapshot above.

| Check | Result |
|---|---:|
| Non-merge commits in the sample | 20 |
| Conventional Commit subjects | 20 |
| Compliance ratio | 100% |
| Required threshold | 80% |
| V-16 result | PASS |
| V-16 regression tests | 4/4 PASS |
| ATC Repository Audit | 100/100 |
| MUST-FAILs | 0 |

The V-16 implementation excludes merge commits before taking the 20-commit sample. It fails closed when the available non-merge history is insufficient (two or fewer commits). Regression tests cover 79% => FAIL, 80% => PASS, insufficient history => FAIL, and empty history => FAIL.

Direct CI evidence:
- ATC Governance CI run: 41255477697
- V-16 / repository audit job: 124697625332
- The job completed successfully. Its log reports: `[PASS] V-16 (CI/CD): Conventional Commits: 100% der letzten 20`.
- The same log reports `R3 COMPLIANT · Score: 100/100 [EXCELLENT] · MUST-FAILs: 0`.

## 3. Exact-head CI and registry evidence

At the inspected head, all 13 PR workflow runs completed successfully (13 success, 0 failure, 0 pending).

SCR Registry Gate:
- Run: 41255477622
- Job: 124697624817
- Registry validation: PASS — 140 entries, 31 unresolved entries, 0 unresolved ranges; no ID auto-allocation.
- Deterministic source identities: 153.
- External source verification: PASS — 15 path/blob bindings verified against exact external commit trees.
- SCR registry positive/negative test suite: 47/47 passed.
- Evidence artifact: `scr-registry-evidence-41255477622-1`
- Artifact ID: 13062679052
- Uploaded ZIP SHA-256: `4d283447c32c84cf5f4179185c143bb2e2b9f8975bca2f5da8a313feaa944ed5`

This is an exact-head snapshot. It must not be presented as CI evidence for a later commit until checks run against that later exact head.

## 4. Remaining evidence gaps and safe disposition

### E-01 — External commit-tree and path/blob identity

**Status: VERIFIED for the 15 pinned external sources in the manifest.**

The verifier acquires the exact external commit, resolves its tree, resolves each repository-relative path to a Git object, confirms the object is a blob, and compares the actual blob SHA with the pinned SHA. The current exact-head CI run passed all 15 bindings.

**Residual:** This result is bounded to the 15 manifest entries. It does not imply that every historical source or every SCR lifecycle fact is verified.

### E-02 — Signer trust roots and fingerprint allowlist

**Status: BLOCKED — no trusted signer is currently configured.**

The trust store currently contains an empty `trusted_signer_fingerprints` array. The validator deliberately treats an empty trust store as trusting no signers. Tests confirm that behavior and reject malformed fingerprints.

No signer fingerprint, Owner identity, trust root, or rotation/revocation authority is inferred from a commit author name, GitHub account, unsigned commit, or a valid signature alone.

**Required evidence to close:** an attributable, authorized trust-root decision identifying the accepted signer fingerprint(s), the authority scope, validity/rotation policy, and revocation procedure. Until then, the empty allowlist is the correct fail-closed state.

### E-03 — Cross-SCR relationship graph and cycle semantics

**Status: RESIDUAL — local source relationships exist; graph-wide model is not established.**

The registry supports per-entry `related_sources[]` records with typed relationships and an explicit scope. The current schema does not define a graph-wide target-SCR edge model, authoritative cardinality, or cycle semantics across SCR entries.

Adding edges or declaring cycles invalid without an approved relationship vocabulary and directionality would invent governance semantics. No such edges or rules are asserted in this report.

**Required evidence to close:** an authoritative relationship vocabulary, edge directionality, cardinality constraints, and a decision on which relationship classes must be acyclic. Implementation can then validate endpoints, duplicates, and cycles without changing SCR allocation or lifecycle.

### E-04 — Unresolved historical identities and lifecycle evidence

**Status: RESIDUAL — 31 entries remain unresolved.**

The registry validator reports 140 entries, including 31 unresolved entries, and no unresolved numeric ranges. Technical source identity derivation is not equivalent to allocation authority, Owner approval, implementation acceptance, or lifecycle closure.

The current state must remain fail-closed. No entry is promoted to ACCEPTED, REJECTED, CLOSED, OBSOLETE, SUPERSEDED, or FREE without attributable evidence and the applicable authority.

### E-05 — Status and scope contradictions

**Status: RESIDUAL — contradictions are surfaced; formal adjudication is not supplied by technical validation.**

- ATC-STD-041 has an effectiveness inconsistency: frontmatter says `status: approved` and `normative: true`, while `effective_date` is null and the body says effectiveness is deferred until the required release.
- SCR-0095 has evidence for at least two scopes: Automated Repository Assurance and the Hub repository-file sweep. The evidence does not decide whether these were one umbrella SCR or misattributed/split work.
- SCR-0096 has evidence for both scanner badge correction and Standards Family ID architecture. The evidence does not decide whether both scopes intentionally belong to one SCR.
- SCR-0139's `status: approved` and `normative: false` are separate dimensions and may be consistent. No normative promotion is inferred.

The validator's contradiction tests are useful technical controls; they do not substitute for an Owner decision.

## 5. Governance and change boundaries

This report is evidence documentation only. It does not:
- allocate, recycle, or automatically assign an SCR identifier;
- change an SCR allocation, lifecycle, decision, owner, or normative status;
- create an Owner approval or trust-root decision;
- alter approved standards or product implementation;
- rewrite Git history;
- create another pull request;
- mark PR #120 ready, merge it, or initiate a release.

PR #120 remains the sole workstream. The unresolved items above remain explicitly RESIDUAL or BLOCKED until the required evidence exists.
