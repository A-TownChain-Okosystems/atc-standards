# Proof-of-System Conformance Contract v1 — PROPOSED

Status: **PROPOSED / NOT NORMATIVE**. This contract makes the requested cases machine-addressable. It does not freeze protocol parameters or claim that any case has been implemented or executed. Every case remains `BLOCKED` until its prerequisite decisions, independent oracle, fixtures, and exact-SHA evidence exist.

## Contract

- Contract ID: `ATC-POS-CONFORMANCE-001`
- Chain ID: `658467`
- Machine-readable case catalogue: [`fixtures/vectors.json`](fixtures/vectors.json)
- JSON Schema: [`fixtures/ATC-POS-CONFORMANCE-001.schema.json`](fixtures/ATC-POS-CONFORMANCE-001.schema.json)
- Contract-only validator: [`tools/atc-pos-conformance/check_vectors.py`](../../tools/atc-pos-conformance/check_vectors.py)
- Reproducible command from repository root: `python3 tools/atc-pos-conformance/check_vectors.py`
- Format: UTF-8 JSON input; canonical protocol serialization remains **BLOCKED** pending protocol freeze.
- Harness output contract: `case_id`, `input_sha256`, `oracle_version`, `actual_decision`, `actual_error_code`, `exit_code`, `evidence_refs`.
- Decision vocabulary: `ACCEPT`, `REJECT`, `FINALIZE`, `NOT_FINALIZED`, `SECURITY_STOP`, `BLOCKED`.
- Error codes are **provisional harness identifiers**, not normative wire-protocol error codes.
- Fixture names are stable references that must resolve to checked-in, hashed fixture files before protocol execution. No placeholder fixture may be silently substituted.
- Golden expected outputs must be authored/reviewed independently of the production implementation.

### Validator scope boundary

`check_vectors.py` checks the completeness and guardrails of the contract records only: 19 unique IDs, expected ordering, envelope constants, parameter blockers, and explicit `BLOCKED`/non-normative markers. A successful result means **contract metadata validation only**. It does not run consensus logic, cryptographic checks, finality, fork choice, multi-node, partition or recovery tests, and must not be reported as `TESTED`, `CI_VERIFIED` for protocol behavior, `E2E_VERIFIED` or `VERIFIED`.

## Shared JSON input envelope

Each vector uses this envelope; case-specific data is in `scenario`.

```json
{
  "contract_id": "ATC-POS-CONFORMANCE-001",
  "case_id": "POS-V-001",
  "chain_id": 658467,
  "protocol_version": "UNFROZEN",
  "epoch": "FIXTURE:epoch_0",
  "height": "FIXTURE:height_1",
  "round": "FIXTURE:round_0",
  "validator_set_hash": "FIXTURE:validator_set_hash_0",
  "parent_block_id": "FIXTURE:parent_A",
  "scenario": {},
  "expected": {
    "decision": "BLOCKED",
    "error_code": "SPEC_NOT_FROZEN"
  }
}
```

`UNFROZEN` and `FIXTURE:*` are contract placeholders, not valid production wire values. Until placeholders are resolved to exact bytes/numbers with hashes and the relevant parameters are frozen, expected harness status is `BLOCKED / SPEC_NOT_FROZEN`, not a pass.

## Positive vectors

### POS-V-001 — Valid proposal
Input scenario: proposal, eligible proposer, signature, parent and body fixture references.
Expected protocol behavior: `ACCEPT`; provisional failure code: `E_PROPOSAL_INVALID`.
Preconditions: leader-selection and proposal-encoding rules frozen; signature fixture independently verified.
Status: **BLOCKED** pending protocol version, leader rule, encoding and fixture hashes.

### POS-V-002 — Valid vote scope
Input scenario: signed vote with chain/version/epoch/height/round/block/validator-set scope.
Expected protocol behavior: `ACCEPT`; provisional failure code: `E_VOTE_SCOPE_INVALID`.
Status: **BLOCKED** pending vote schema, signature domain and validator-snapshot freeze.

### POS-V-003 — Quorum finalizes
Input scenario: vote set exactly at the subsequently approved threshold.
Expected protocol behavior: `FINALIZE`; provisional failure code: `E_QUORUM_INSUFFICIENT`.
Status: **BLOCKED** until the owner decides >2/3 versus >=2/3, eligible stake, integer width, rounding and duplicate handling. Fixture generation must follow that decision.

### POS-V-004 — Deterministic fork choice
Input scenario: same valid candidate set delivered in orders A→B and B→A.
Expected protocol behavior: both independent executions return identical selected block and state hash; provisional mismatch code: `E_FORK_CHOICE_NONDETERMINISTIC`.
Status: **BLOCKED** pending fork ranking, tie-break, serialization and independent oracle.

### POS-V-005 — Validator snapshot transition
Input scenario: state before epoch boundary, stake changes and approved activation boundary.
Expected protocol behavior: exact approved validator-set hash and eligibility; provisional mismatch code: `E_VALIDATOR_SNAPSHOT_MISMATCH`.
Status: **BLOCKED** pending epoch boundary, unbonding/slashing interaction, activation delay and integer rules.

### POS-V-006 — Valid round change
Input scenario: authenticated round-change message, highest valid QC and signer set.
Expected protocol behavior: deterministic next-round state; provisional failure code: `E_ROUND_CHANGE_INVALID`.
Status: **BLOCKED** pending round-change state machine, timeout semantics and QC/vote encoding.

### POS-V-007 — Recovery without finality regression
Input scenario: pre-partition finalized block, partition/rejoin messages and valid certificate.
Expected protocol behavior: deterministic recovery while preserving prior finality; provisional failure code: `E_FINALITY_REGRESSION`.
Status: **BLOCKED** pending certificate, recovery protocol and network/liveness assumptions.

## Negative vectors

### POS-N-001 — Wrong domain / replay
Input scenario: valid vote mutated to a previous epoch.
Expected protocol behavior: `REJECT`; provisional code: `E_DOMAIN_MISMATCH`.
Status: **BLOCKED** pending canonical signed fields and replay-window rules.

### POS-N-002 — Equivocation
Input scenario: two individually valid incompatible votes from one signer in the same approved scope.
Expected protocol behavior: reject incompatible second vote, emit evidence, no second finality; provisional code: `E_EQUIVOCATION`.
Status: **BLOCKED** pending conflict scope, evidence encoding, retention and slashing policy.

### POS-N-003 — Quorum below threshold
Input scenario: vote set one smallest stake unit below the approved threshold.
Expected protocol behavior: `NOT_FINALIZED`; provisional code: `E_QUORUM_INSUFFICIENT`.
Status: **BLOCKED** pending quorum threshold and smallest stake unit.

### POS-N-004 — Duplicate signer / noncanonical vote set
Input scenario: duplicate validator vote or noncanonical vote-set ordering.
Expected protocol behavior: `REJECT`; provisional code: `E_DUPLICATE_OR_NONCANONICAL_VOTE`.
Status: **BLOCKED** pending canonical sort key, duplicate policy and vote-set encoding.

### POS-N-005 — Invalid parent / noncanonical bytes
Input scenario: unknown parent and/or noncanonical proposal encoding.
Expected protocol behavior: `REJECT`; provisional code: `E_PARENT_OR_ENCODING_INVALID`.
Status: **BLOCKED** pending serialization, parent-validity and validation-order rules.

### POS-N-006 — Conflicting finality certificates
Input scenario: two conflicting certificates at the same height and domain.
Expected protocol behavior: security stop, no rollback or silent overwrite, emit incident evidence; provisional code: `E_CONFLICTING_FINALITY_CERTIFICATES`.
Status: **BLOCKED** pending certificate semantics and operator response.

### POS-N-007 — Stake arithmetic overflow
Input scenario: maximum allowed weight plus one unit.
Expected protocol behavior: `REJECT`; provisional code: `E_STAKE_ARITHMETIC_OVERFLOW`; wraparound forbidden.
Status: **BLOCKED** pending integer width and maximum valid stake.

### POS-N-008 — Invalid signature / unauthorized leader
Input scenario: invalid signature and/or ineligible proposer.
Expected protocol behavior: `REJECT`; provisional code: `E_SIGNATURE_OR_LEADER_INVALID`.
Status: **BLOCKED** pending signature scheme, leader eligibility and validation order.

### POS-N-009 — Partition without quorum
Input scenario: each isolated partition has less than the approved quorum and no cross-partition messages.
Expected protocol behavior: neither partition finalizes; recovery only follows approved deterministic rules; provisional code: `E_QUORUM_INSUFFICIENT`.
Status: **BLOCKED** pending quorum and recovery/liveness rules.

### POS-N-010 — Arrival-order invariance
Input scenario: identical candidate set replayed in two delivery orders.
Expected protocol behavior: `ACCEPT` if both executions select the same block/state hash; differing results fail with `E_FORK_CHOICE_NONDETERMINISTIC`.
Status: **BLOCKED** pending fork-choice rule and independent oracle.

### POS-N-011 — Mining/PoH proof presented as finality
Input scenario: valid work/PoH proofs but no validator votes, with finalization requested.
Expected protocol behavior: `REJECT`; provisional code: `E_FINALITY_REQUIRES_VALIDATOR_QUORUM`.
Status: **BLOCKED** pending separation of work proofs and finality schema.

### POS-N-012 — Finality regression attempt
Input scenario: conflicting certificate after an existing finalized block.
Expected protocol behavior: approved security-stop/reject response; never overwrite finalized state; provisional code: `E_FINALITY_REGRESSION`.
Status: **BLOCKED** pending conflict-response semantics and incident-evidence format.

## Parameter decision register

No defaults are implied. Every row requires an accountable owner decision, exact normative value/formula, versioning rule, independent review and boundary vectors.

| ID | Open decision | Current status |
|---|---|---|
| PARAM-01 | Effective stake formula, self/delegated stake, caps, minimum stake, integer width | BLOCKED |
| PARAM-02 | Validator snapshot height/epoch, activation delay, unbonding/slashing transition | BLOCKED |
| PARAM-03 | Cryptographic hash, domain separation, seed byte order, weighted-sampling method and bias bound | BLOCKED |
| PARAM-04 | Hybrid weights `W_S`/`W_W`, normalization, difficulty and reward coupling | BLOCKED |
| PARAM-05 | Quorum threshold: strictly greater than 2/3 or at least 2/3; eligible stake and exact comparison arithmetic | BLOCKED |
| PARAM-06 | Per-formula integer widths, rounding direction, overflow/underflow behavior | BLOCKED |
| PARAM-07 | Vote/round-change wire schema, timeout escalation and state transitions | BLOCKED |
| PARAM-08 | Finality-certificate format, signature/aggregation scheme, canonical ordering and certificate ID | BLOCKED |
| PARAM-09 | Equivocation scope, evidence serialization, slashing amount/timing and appeal policy | BLOCKED |
| PARAM-10 | Fork-choice precedence, QC/round/height ordering, deterministic tie-break | BLOCKED |
| PARAM-11 | Partition assumptions, liveness conditions, rejoin/state-sync and operator incident response | BLOCKED |

## Evidence manifest required for every protocol run

```json
{
  "case_id": "POS-N-001",
  "repository": "A-TownChain-Okosystems/a-townchain",
  "implementation_commit_sha": "REQUIRED_FULL_SHA",
  "source_path_and_symbol": "REQUIRED",
  "source_blob_sha": "REQUIRED",
  "fixture_path": "REQUIRED",
  "fixture_sha256": "REQUIRED",
  "oracle_repository_commit_sha": "REQUIRED_FULL_SHA",
  "runner_command": "REQUIRED",
  "toolchain_and_platform": "REQUIRED",
  "workflow_run_id_url": "REQUIRED",
  "job_step_exit_code": "REQUIRED",
  "log_reference_sha256": "REQUIRED",
  "output_sha256": "REQUIRED",
  "artifact_sha256": "REQUIRED",
  "independent_reviewer": "REQUIRED",
  "status": "BLOCKED"
}
```

A successful contract validator, documentation build or generic CI workflow does not satisfy protocol-vector, negative-test, multi-node, partition/recovery, cryptographic-review or production-readiness gates.
