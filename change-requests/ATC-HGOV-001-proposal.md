---
proposal:
  key: ATC-HGOV-001
  proposed_standard_id: ATC-STD-608
  title: "Hybrid Governance Specification"
  proposed_version: "0.1.0"
  status: candidate
  normative: false
  category: blockchain
  authority: "A-TownChain-Okosystems"
  owner: "Pending Owner validation"
  created: "2026-11-01"
  updated: "2026-11-01"
  change_request: SCR-0143
  allocation_status: pending
  approval_status: pending
---

# ATC-HGOV-001 — Hybrid Governance Specification

> **Proposal only.** This document is a non-normative candidate for the proposed canonical standard
> `ATC-STD-608`. Neither the standard identifier nor SCR-0143 is asserted as formally allocated.
> No requirement in this document overrides an existing approved standard. Normative effect
> requires confirmed identifier allocation, Owner decision, required technical/security/architecture
> reviews, registry registration, and the approval process in ATC-STD-000.

## 1. Purpose

This proposal defines the governance and control boundaries for the A-TownChain hybrid model:
development is centrally coordinated by the A-TownChain development organization, while consensus,
block production, transaction validation and network operation are performed by independently
operated participants under deterministic protocol rules.

The model is intended to support ATC as the native, freely market-priced asset of its own public
blockchain. This document does not classify ATC legally, authorize a public offering, authorize
exchange admission, or establish that any regulatory obligation has been discharged.

## 2. Scope

The proposed standard applies to:
- A-TownChain protocol governance and protocol upgrades;
- validator admission, operation, staking, consensus participation and exit;
- monetary issuance, supply limits, fees and protocol-defined rewards;
- emergency response and network recovery;
- governance transparency, decentralization measurement and evidence.

It does not define or replace the consensus algorithm, transaction encoding, cryptographic
primitives, validator implementation, wallet implementation, token economics formula, or legal
classification. Those remain owned by their existing normative sources and implementation
repositories.

## 3. Normative language and status

If and when approved, MUST, MUST NOT, SHOULD, SHOULD NOT and MAY shall be interpreted according
to ATC-STD-000. At this candidate stage, these clauses are proposed requirements, not effective
normative obligations.

Each requirement has a stable identifier, proposed level, rationale, applicability, validation
method, evidence expectation and known residual risk. Requirement identifiers in this proposal
must be checked against the canonical requirement registry before approval.

## 4. Governance authority model

### REQ-608-001 — Separation of development and consensus authority
**Proposed level:** MUST  
**Rationale:** Development coordination must not confer unilateral control over the live network.  
**Applicability:** Development organization, node software, validators, release engineering.  
**Requirement:** The development organization MUST NOT possess an administrative protocol
capability that independently changes canonical chain state, forges validator decisions, rewrites
confirmed balances, or unilaterally determines canonical block history.  
**Validation:** Architecture review; privileged-interface inventory; adversarial integration tests.  
**Acceptance:** No organization-only key, API, RPC method, upgrade endpoint or deployment role can
perform any prohibited state or consensus action.  
**Evidence:** Exact source commit, privileged-symbol inventory, negative authorization tests, CI
run/job/step links, logs and SHA-256 artifact manifest.  
**Residual risk:** Undiscovered privileged paths and social coordination pressure.

### REQ-608-002 — Public authority and responsibility register
**Proposed level:** MUST  
**Requirement:** Governance roles, decision scope, appointment/removal process, conflict-of-interest
rules and authority limitations MUST be publicly documented. A role MUST NOT imply powers beyond
its explicitly defined scope.  
**Validation:** Schema validation and review against deployed authority configuration.  
**Acceptance:** Every active role maps to a published authority record and an enforceable permission
boundary.  
**Evidence:** Registry snapshot, schema, validator output, exact commit and artifact hashes.  
**Residual risk:** Off-chain influence may exceed formally declared authority.

### REQ-608-003 — No unilateral emergency sovereignty
**Proposed level:** MUST NOT  
**Requirement:** No single person, organization, multisignature group, administrator or validator
MUST be able to unilaterally confiscate user funds, mint ATC outside issuance rules, rewrite finalized
state, or permanently censor an account.  
**Validation:** Threat model, key/permission graph, negative tests and independent security review.  
**Acceptance:** All prohibited actions are unreachable through supported interfaces and privileged
keys.  
**Evidence:** Capability matrix, key inventory, test vectors, review record and exact-SHA CI evidence.  
**Residual risk:** A coordinated majority attack or client monoculture may still affect liveness.

## 5. Validator independence and network operation

### REQ-608-004 — Independent validator operation
**Proposed level:** MUST  
**Requirement:** The protocol MUST permit validators to be operated by independent legal or natural
persons using independently controlled infrastructure and keys. No single development entity may
be a mandatory validator operator or sole source of validator authorization.  
**Validation:** Reproducible node deployment; operator onboarding and exit tests; infrastructure audit.  
**Acceptance:** An independent operator can synchronize, validate, produce blocks when selected,
and exit using public documentation without privileged organizational access.  
**Evidence:** Reproducible build and deployment records, public protocol docs, testnet traces and
operator independence attestations.  
**Residual risk:** Nominally separate operators may share beneficial ownership or infrastructure.

### REQ-608-005 — Validator key separation
**Proposed level:** MUST  
**Requirement:** Validator consensus keys MUST be distinct from development, release-signing,
treasury, wallet and emergency-coordination keys. Consensus keys MUST NOT be held in a shared
administrative trust domain with release credentials.  
**Validation:** Key-role inventory, configuration linting, signing-policy tests and security review.  
**Acceptance:** Key reuse and cross-role signing are rejected by automated checks.  
**Evidence:** Redacted key architecture, policy configuration, negative tests and CI artifacts.  
**Residual risk:** Operational compromise of an individual validator remains possible.

### REQ-608-006 — Stake and operator concentration transparency
**Proposed level:** MUST  
**Requirement:** The network MUST expose enough verifiable data to calculate stake concentration,
validator voting/consensus weight, active-operator count, operator concentration and relevant
infrastructure concentration. Operator identity claims MUST be distinguished from cryptographically
verifiable on-chain facts.  
**Validation:** Independent calculation from canonical chain data; cross-check against published
network telemetry.  
**Acceptance:** Metrics are reproducible from documented inputs and disclose data limitations.  
**Evidence:** Snapshot block hash, calculation code/version, raw input hashes and report artifact.  
**Residual risk:** Common ownership and infrastructure dependencies may be hidden or misreported.

### REQ-608-007 — Decentralization thresholds require explicit approval
**Proposed level:** MUST  
**Requirement:** Numerical limits for maximum stake share, minimum independent operators, geographic
or hosting diversity, and concentration alarms MUST be specified in a separately approved
decentralization profile before mainnet readiness is claimed. Thresholds MUST NOT be invented or
silently inferred from monitoring dashboards.  
**Validation:** Profile schema and policy tests.  
**Acceptance:** Each metric has a definition, observation window, threshold, exception process and
failure action.  
**Evidence:** Approved profile version, test vectors, monitoring output and signed review record.  
**Residual risk:** Thresholds can become stale as the network grows.

### REQ-608-008 — Validator entry, exit and sanctions
**Proposed level:** MUST  
**Requirement:** Validator admission, key rotation, voluntary exit, downtime handling, slashing and
appeals MUST be deterministic, documented and enforced by protocol rules. No off-chain authority
may apply discretionary slashing or confiscation.  
**Validation:** State-machine tests, boundary tests, fault injection and replay determinism.  
**Acceptance:** Identical valid chain inputs produce identical validator-set and penalty outcomes.  
**Evidence:** Golden vectors, test logs, state transition traces and artifact hashes.  
**Residual risk:** Economic parameters may create unintended centralization incentives.

## 6. Consensus and protocol upgrades

### REQ-608-009 — Consensus authority
**Proposed level:** MUST  
**Requirement:** Canonical block acceptance MUST be determined by the published consensus protocol
and its validator rules. A development organization release, announcement or signature MUST NOT
alone constitute consensus approval or force nodes to accept a new chain history.  
**Validation:** Multi-node adversarial tests and protocol conformance tests.  
**Acceptance:** Nodes reject invalid consensus transitions even when a release is organization-signed.  
**Evidence:** Multi-node traces, negative vectors, exact source bindings and CI artifacts.  
**Residual risk:** Social coordination can still influence which software participants choose to run.

### REQ-608-010 — Public upgrade proposal
**Proposed level:** MUST  
**Requirement:** Every consensus-affecting upgrade MUST have a public proposal containing motivation,
specification diff, affected components, compatibility analysis, threat model, state-migration plan,
activation method, rollback/failure behavior and test evidence before signaling or activation.  
**Validation:** Required-field schema and release-gate checks.  
**Acceptance:** Missing or unresolved mandatory fields block progression.  
**Evidence:** Immutable proposal revision, review records, testnet evidence and release manifest.  
**Residual risk:** Public review may not identify every latent protocol defect.

### REQ-608-011 — Independent review and testnet proof
**Proposed level:** MUST  
**Requirement:** Consensus, cryptography, monetary policy, validator-set, state migration and
authorization changes MUST receive the applicable independent technical and security reviews and
must be exercised on testnet before mainnet activation.  
**Validation:** Review completeness gate, deterministic migration tests, multi-client or
cross-implementation tests where applicable.  
**Acceptance:** All required reviews and test evidence bind to the exact proposed release commit.  
**Evidence:** Reviewer decisions, testnet block range, client versions, logs and SHA-256 artifacts.  
**Residual risk:** Testnet may not reproduce all mainnet conditions.

### REQ-608-012 — No unilateral upgrade activation
**Proposed level:** MUST NOT  
**Requirement:** The development organization MUST NOT unilaterally activate a consensus-breaking
upgrade on mainnet. Activation MUST follow the approved proposal, signaling, coordination and
protocol-defined activation procedure.  
**Validation:** Upgrade state-machine tests and unauthorized-activation tests.  
**Acceptance:** An organization-controlled release key alone cannot trigger activation.  
**Evidence:** Activation test vectors, validator signaling traces and CI records.  
**Residual risk:** A coordinated supermajority or ecosystem-wide client adoption can still create a
de facto upgrade.

### REQ-608-013 — Existing upgrade-standard compatibility
**Proposed level:** MUST  
**Requirement:** This proposal does not supersede or silently reinterpret ATC-STD-NET-006. Its
existing upgrade sequence and the stated 80% active-staking-power signaling threshold remain
unchanged unless a separately approved change resolves their exact semantics and compatibility
with independent validator governance.  
**Validation:** Cross-standard conflict review and requirement traceability.  
**Acceptance:** No implementation uses conflicting or ambiguous activation thresholds.  
**Evidence:** Compatibility matrix, approved SCR, exact versions and tests.  
**Residual risk:** The current meaning of "governance approval" and signaling power may require
clarification before deployment.

## 7. Monetary policy, issuance and ATC supply

### REQ-608-014 — Maximum supply invariant
**Proposed level:** MUST  
**Requirement:** The protocol MUST enforce a maximum aggregate ATC supply of 360,000,000 ATC
(360,000,000 × 10^18 base units if the established 18-decimal denomination remains authoritative).
No privileged administrative minting path may bypass this invariant.  
**Validation:** Arithmetic boundary tests, state-transition tests, supply invariant checks and
independent replay.  
**Acceptance:** Every reachable state satisfies total issued supply less than or equal to the
canonical maximum; unauthorized mint attempts fail closed.  
**Evidence:** Golden vectors, property tests, chain replay output, exact source commit and artifact
hashes.  
**Residual risk:** Existing issuance semantics and historical allocations must be reconciled with
the canonical implementation.

### REQ-608-015 — Deterministic issuance schedule
**Proposed level:** MUST  
**Requirement:** Block rewards, AI-compute mining rewards, validator rewards, halvings, genesis
allocations, burns and any other supply-changing events MUST be completely specified as deterministic
protocol rules. No discretionary operator may alter an individual reward.  
**Validation:** Reference implementation comparison, reward vectors and long-horizon simulation.  
**Acceptance:** Independent implementations calculate identical issuance and supply totals for the
same chain history.  
**Evidence:** Formula specification, vectors, simulation inputs/outputs and source-bound test logs.  
**Residual risk:** The current relationship between AI-compute rewards and PoS validator rewards
requires a complete supply-budget reconciliation.

### REQ-608-016 — Monetary parameter changes
**Proposed level:** MUST  
**Requirement:** Monetary parameters MUST NOT be changed by a routine software release or private
administrative configuration. Any proposed change MUST undergo explicit public governance, economic
impact analysis, security review and the applicable network upgrade process.  
**Validation:** Configuration and code-path audit; upgrade tests.  
**Acceptance:** Monetary changes are impossible without the approved protocol transition.  
**Evidence:** Parameter diff, SCR, approval records, simulation report and exact-SHA test evidence.  
**Residual risk:** A sufficiently broad consensus change could intentionally change monetary policy;
immutability is therefore a governance and social-consensus commitment, not a mathematical guarantee
against all future forks.

## 8. Staking, fees and reward accounting

### REQ-608-017 — Protocol-defined staking
**Proposed level:** MUST  
**Requirement:** Staking eligibility, delegation, validator selection, reward accrual, unbonding,
slashing, withdrawal and reward claiming MUST be deterministic and publicly specified. Wallet
display balances MUST distinguish liquid, bonded, unbonding and claimable amounts.  
**Validation:** State-machine and wallet-accounting tests.  
**Acceptance:** Displayed balances reconcile exactly with canonical on-chain state.  
**Evidence:** State vectors, wallet integration tests and replay logs.  
**Residual risk:** The intended relationship between liquid ATC and automatically participating
staking balances remains an open economic design decision.

### REQ-608-018 — No undisclosed encumbrance of self-custodied funds
**Proposed level:** MUST NOT  
**Requirement:** A wallet MUST NOT represent funds as freely spendable while protocol rules
simultaneously make those same units unavailable, slashable or subject to an undisclosed lock.
Any automatic reward participation MUST have explicit, auditable semantics and must not imply
custody or transfer of the user's signing authority.  
**Validation:** Wallet/protocol consistency tests and user-visible balance-state tests.  
**Acceptance:** Spendability, bonded status, slashing exposure and withdrawal conditions are
accurately represented.  
**Evidence:** Wallet test vectors, protocol state traces and UI/API conformance reports.  
**Residual risk:** Users may misunderstand complex staking or reward mechanics.

### REQ-608-019 — Fee determinism and transparency
**Proposed level:** MUST  
**Requirement:** Fee calculation, fee caps/floors, congestion adjustment, rounding, fee destination,
burning and reward allocation MUST be deterministic, documented and reproducible by independent
clients. No administrator may selectively alter an individual user's protocol fee.  
**Validation:** Fee vectors, congestion simulations, arithmetic boundary tests and replay.  
**Acceptance:** Independent implementations compute identical fees and accounting outcomes.  
**Evidence:** Vectors, simulation report, source commit and CI artifacts.  
**Residual risk:** Poorly calibrated fee parameters may impair access or network sustainability.

### REQ-608-020 — Same-block accounting semantics
**Proposed level:** MUST  
**Requirement:** The protocol MUST specify whether transaction fees and staking/validator rewards
are accounted for in the transaction block, a subsequent block, or a separately defined epoch.
The ordering MUST be deterministic and safe against double spending, reward amplification and
intra-block reordering.  
**Validation:** Block execution vectors, adversarial ordering tests and supply accounting tests.  
**Acceptance:** Every fee unit and reward unit has exactly one canonical accounting outcome.  
**Evidence:** Transaction/block vectors, accounting invariants and replay results.  
**Residual risk:** The preferred same-block reward behavior has not yet been reconciled with the
existing transaction and consensus specifications.

## 9. Security, emergency response and recovery

### REQ-608-021 — No unilateral pause or rollback
**Proposed level:** MUST NOT  
**Requirement:** No organization-controlled emergency key or operator endpoint may unilaterally
pause the canonical network, reverse finalized transactions, rewrite balances or select an
alternative chain history.  
**Validation:** Privilege audit, fault-injection and unauthorized-control tests.  
**Acceptance:** No single administrative credential can perform these actions.  
**Evidence:** Threat model, key inventory, negative tests and exact-SHA CI evidence.  
**Residual risk:** Protocol-level safety halts or loss of liveness may still occur under defined
consensus failure conditions.

### REQ-608-022 — Emergency response transparency
**Proposed level:** MUST  
**Requirement:** Emergency coordination MUST publish the incident scope, affected versions,
evidence, proposed mitigation, authority basis, risks and expiry/review condition. Emergency
coordination MUST NOT silently create permanent privileged authority.  
**Validation:** Incident record schema and post-incident review.  
**Acceptance:** Every emergency action is attributable, time-bounded where applicable and
independently reviewable.  
**Evidence:** Incident timeline, signed records, release diff, approvals and postmortem.  
**Residual risk:** Disclosure timing may be constrained by active exploitation.

### REQ-608-023 — Recovery without trusted state substitution
**Proposed level:** MUST  
**Requirement:** Recovery MUST use verifiable canonical chain data and deterministic replay under
the applicable network recovery standard. An operator-provided snapshot MUST NOT be trusted solely
because it was published by the development organization.  
**Validation:** Snapshot verification, replay comparison, partition/rejoin and recovery tests.  
**Acceptance:** Recovered state matches independently verified canonical state roots.  
**Evidence:** Snapshot hashes, block ranges, state-root comparisons and test logs.  
**Residual risk:** Correlated software defects can affect multiple implementations.

## 10. Decentralization, disclosure and evidence

### REQ-608-024 — Decentralization reporting
**Proposed level:** MUST  
**Requirement:** Mainnet governance reporting MUST distinguish protocol decentralization, validator
operator independence, stake distribution, client diversity, infrastructure diversity and
organizational influence. A single composite score MUST NOT conceal a critical concentration.  
**Validation:** Reproducible report generation and independent review.  
**Acceptance:** Each dimension is reported separately with source data, methodology and limitations.  
**Evidence:** Data snapshot, report code/version, calculations and artifact hashes.  
**Residual risk:** Off-chain ownership and influence data may be incomplete.

### REQ-608-025 — Open protocol and reproducible releases
**Proposed level:** MUST  
**Requirement:** Protocol specifications, upgrade proposals and release source must be publicly
reviewable, subject to applicable security disclosure windows. Production releases MUST be
reproducible or have a documented, independently reviewed exception.  
**Validation:** Reproducible-build checks and source-to-binary provenance verification.  
**Acceptance:** Release artifacts bind to exact source commits and immutable checksums.  
**Evidence:** Build logs, provenance attestations, artifact SHA-256 and release manifest.  
**Residual risk:** Build environment compromise and dependency supply-chain risks.

### REQ-608-026 — Evidence completeness and status discipline
**Proposed level:** MUST  
**Requirement:** Every governance requirement MUST map to its implementation owner, test or review
method, evidence source and status. Evidence MUST identify exact repository, commit, path, symbol
or blob SHA, Actions run, job, step/log and artifact SHA-256 where applicable. Missing or ambiguous
evidence MUST remain BLOCKED or UNKNOWN; it MUST NOT be inferred as PASS.  
**Validation:** Schema validation, evidence-link resolution, exact-head CI verification and
negative tests for missing/mismatched evidence.  
**Acceptance:** No requirement is marked VERIFIED without complete, exact-source evidence and all
required gates.  
**Evidence:** Machine-readable traceability manifest, validator output and immutable artifacts.  
**Residual risk:** Evidence can be complete yet fail to represent production behavior.

## 11. Cross-standard dependencies and unresolved compatibility

This proposal is intended to complement, not silently replace, at least the following existing
sources:
- ATC-STD-000 — Standards Governance & Specification Standard;
- ATC-STD-002 — Standards Family ID & Artifact Identifier Architecture;
- ATC-STD-600 — Chain Identity & Network Identification;
- ATC-STD-NET-003 — Mainnet Standard;
- ATC-STD-NET-005 — Network Genesis Standard;
- ATC-STD-NET-006 — Network Upgrade Standard;
- ATC-STD-NET-007 — Network Security Standard;
- ATC-STD-NET-008 — Network Recovery Standard;
- applicable consensus, staking, transaction-domain and monetary-policy specifications in the
  implementation-owning repositories.

Before approval, a source-to-requirement compatibility matrix MUST establish exact versions and
identify conflicting or missing normative rules. In particular:
1. The existing 80% active-staking-power upgrade signal in NET-006 must be reconciled with the
   proposed governance and validator-independence model; this proposal does not change it.
2. The exact boundary between AI-compute mining rewards and PoS validator rewards must be reconciled
   with the 360,000,000 ATC maximum supply.
3. The liquid-balance / automatic-staking design must be specified without misrepresenting
   spendability, custody or slashing exposure.
4. Same-block versus next-block fee/reward accounting must be defined in the transaction and
   consensus specifications.
5. Any claim of decentralization must be supported by measured operator and infrastructure
   independence, not merely by validator count.

Unresolved conflicts MUST block normative approval or the affected implementation gate.

## 12. Implementation ownership and repository boundaries

| Concern | Authoritative location |
|---|---|
| Normative governance standard and registry | `atc-standards` |
| Blockchain, VM, algorithm and wallet implementation | `a-townchain/components/{vm,algorithm,wallet}` |
| Consensus implementation | Existing consensus-owning source repository; exact path to be bound by compatibility review |
| SDK integration | `atc-sdk` |
| Ecosystem integration, compliance and evidence control | `a-townchain-ecosystem` |

This proposal MUST NOT create a second implementation of consensus, monetary policy, wallet
accounting or validator logic in the standards repository. The standards repository defines
requirements and validation contracts; implementation remains in its owning source repository.

## 13. Proposed validation and release gates

| Gate | Proposed check | Failure result |
|---|---|---|
| GATE-608-001 | Metadata, ID and requirement uniqueness | BLOCKED |
| GATE-608-002 | Cross-standard compatibility matrix | BLOCKED |
| GATE-608-003 | Authority and privilege boundary tests | BLOCKED |
| GATE-608-004 | Validator independence and concentration report | BLOCKED |
| GATE-608-005 | Consensus and upgrade conformance | BLOCKED |
| GATE-608-006 | Monetary supply and issuance invariants | BLOCKED |
| GATE-608-007 | Staking, fee and reward accounting | BLOCKED |
| GATE-608-008 | Emergency and recovery security tests | BLOCKED |
| GATE-608-009 | Exact-source evidence completeness | BLOCKED |
| GATE-608-010 | Required Owner and specialist approvals | BLOCKED |

A green CI result alone MUST NOT imply normative approval, implementation completeness, or mainnet
readiness.

## 14. Required evidence model

Each requirement record should expose at least:
- requirement_id;
- normative_level;
- implementation_owner;
- source_repository;
- source_commit;
- source_path;
- source_symbol_or_blob_sha;
- validation_method;
- test_case_ids;
- actions_run_id;
- actions_job_id;
- actions_step_and_log_reference;
- artifact_sha256;
- reviewer_identity_and_scope;
- status;
- residual_risk.

Evidence must be immutable or content-addressed. A reference to a branch name, mutable URL or
unbound CI run is insufficient to prove exact-source verification.

## 15. Approval, versioning and change control

This proposal remains candidate v0.1.0 and non-normative. Promotion to v1.0.0 requires:
1. confirmed allocation of the canonical standard identifier through the Standards Registry;
2. validated SCR identity and lifecycle state;
3. Owner decision under ATC-STD-000;
4. completed technical, security and architecture reviews;
5. resolved cross-standard conflicts or explicitly scoped, approved exceptions;
6. schema and validator support where required;
7. exact-commit CI and evidence verification;
8. registry update and generated-view consistency checks.

No approval, effective date, normative force, implementation status or mainnet readiness is implied
by this proposal or its pull request.

## 16. Changelog

- 0.1.0 — Initial hybrid-governance proposal. Defines authority separation, validator independence,
  consensus upgrades, monetary controls, staking/fee accounting, emergency constraints and evidence
  requirements. Candidate only; not approved.
