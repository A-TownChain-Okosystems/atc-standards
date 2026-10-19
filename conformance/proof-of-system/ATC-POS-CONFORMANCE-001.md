# Proof-of-System Conformance Contract v1 — PROPOSED

Status: **PROPOSED / NOT NORMATIVE**. This contract makes the requested cases machine-addressable. It does not freeze protocol parameters or claim that any case has been implemented or executed. Every case remains `BLOCKED` until its prerequisite decisions, independent oracle, fixtures, and exact-SHA evidence exist.

## Contract

- Contract ID: `ATC-POS-CONFORMANCE-001`
- Chain ID: `658467`
- Format: UTF-8 JSON input; canonical serialization rules remain **BLOCKED** pending protocol freeze.
- Test runner output: JSON object with `case_id`, `input_sha256`, `oracle_version`, `actual_decision`, `actual_error_code`, `exit_code`, `evidence_refs`.
- Decision vocabulary: `ACCEPT`, `REJECT`, `FINALIZE`, `NOT_FINALIZED`, `SECURITY_STOP`, `BLOCKED`.
- Error codes below are **provisional harness identifiers**, not normative wire-protocol error codes.
- Fixture names are stable references that must resolve to checked-in, hashed fixture files before execution. No placeholder fixture may be silently substituted.
- A vector is reproducible only when input bytes, fixture manifest, oracle version, implementation commit, runner/toolchain, command, output, and artifact SHA-256 are recorded.
- Golden expected outputs must be authored/reviewed independently of the production implementation.

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

`UNFROZEN` and `FIXTURE:* ` are contract placeholders, not valid production wire values. A runnable vector must resolve them to exact bytes/numbers from the fixture manifest. While any required value is unresolved, expected harness result is `BLOCKED / SPEC_NOT_FROZEN`, not a pass.

## Positive vectors

### POS-V-001 — Valid proposal
Input: shared envelope with `scenario = {"proposal":"FIXTURE:valid_proposal_A","proposer":"FIXTURE:eligible_leader_A","signature":"FIXTURE:valid_proposal_signature_A","parent":"FIXTURE:parent_A","body":"FIXTURE:valid_body_A"}`.
Expected: `ACCEPT`; provisional failure code if rejected: `E_PROPOSAL_INVALID`.
Preconditions: leader-selection and proposal-encoding rules frozen; proposal signature fixture independently verified.
Status: **BLOCKED** pending protocol version, leader rule, encoding, and fixture hashes.

### POS-V-002 — Valid vote scope
Input: `scenario = {"vote":"FIXTURE:valid_vote_A","vote_type":"PREVOTE","signer":"FIXTURE:validator_A","signature":"FIXTURE:valid_vote_signature_A"}`; vote binds chain/version/epoch/height/round/block/set hash.
Expected: `ACCEPT`; provisional failure code: `E_VOTE_SCOPE_INVALID`.
Status: **BLOCKED** pending vote schema, signature domain and validator-snapshot freeze.

### POS-V-003 — Quorum finalizes
Input: `scenario = {"votes":"FIXTURE:quorum_exactly_at_approved_threshold","target_block":"FIXTURE:block_A","validator_set":"FIXTURE:validator_set_0"}`.
Expected: `FINALIZE`; provisional failure code: `E_QUORUM_INSUFFICIENT`.
Status: **BLOCKED** until owner chooses the threshold (including >2/3 versus >=2/3), integer width, eligible voting stake, rounding and duplicate handling. The fixture must be generated only after that decision.

### POS-V-004 — Deterministic fork choice
Input: `scenario = {"valid_candidates":["FIXTURE:block_A","FIXTURE:block_B"],"delivery_order":"FIXTURE:order_AB","oracle_replay_order":"FIXTURE:order_BA"}`.
Expected: both independent oracle executions return identical selected block and state hash; decision `ACCEPT`; provisional mismatch code: `E_FORK_CHOICE_NONDETERMINISTIC`.
Status: **BLOCKED** pending fork ranking, tie-break, serialization and independent oracle.

### POS-V-005 — Validator snapshot transition
Input: `scenario = {"state_before":"FIXTURE:state_epoch_0","stake_changes":"FIXTURE:stake_delta_epoch_1","activation_boundary":"FIXTURE:approved_epoch_boundary"}`.
Expected: exact approved validator-set hash and eligibility result; decision `ACCEPT`; provisional mismatch code: `E_VALIDATOR_SNAPSHOT_MISMATCH`.
Status: **BLOCKED** pending epoch boundary, unbonding/slashing interaction, activation delay and integer rules.

### POS-V-006 — Valid round change
Input: `scenario = {"round_change":"FIXTURE:valid_round_change_A","highest_qc":"FIXTURE:valid_qc_A","signers":"FIXTURE:round_change_quorum_signers"}`.
Expected: deterministic next-round state; decision `ACCEPT`; provisional failure code: `E_ROUND_CHANGE_INVALID`.
Status: **BLOCKED** pending round-change state machine, timeout semantics and QC/vote encoding.

### POS-V-007 — Recovery without finality regression
Input: `scenario = {"pre_partition_finality":"FIXTURE:finalized_block_A","partition_messages":"FIXTURE:partition_messages_valid","rejoin_messages":"FIXTURE:rejoin_messages_valid","certificate":"FIXTURE:valid_finality_certificate_A"}`.
Expected: recovery reaches the deterministic valid state; finalized block A remains finalized; decision `ACCEPT`; provisional failure code: `E_FINALITY_REGRESSION`.
Status: **BLOCKED** pending finality certificate, recovery protocol and network/liveness assumptions.

## Negative vectors

### POS-N-001 — Wrong domain / replay
Input: `scenario = {"message":"FIXTURE:valid_vote_A","mutation":{"field":"epoch","value":"FIXTURE:previous_epoch"}}`.
Expected: `REJECT`; provisional code: `E_DOMAIN_MISMATCH`.
Status: **BLOCKED** pending canonical signed fields and replay-window rules.

### POS-N-002 — Equivocation
Input: `scenario = {"vote_A":"FIXTURE:valid_vote_block_A","vote_B":"FIXTURE:valid_vote_block_B","same_signer":"FIXTURE:validator_A","same_scope":true,"blocks_conflict":true}`.
Expected: both signatures individually verify; second incompatible vote is rejected and evidence emitted; no second finality; decision `REJECT`; provisional code: `E_EQUIVOCATION`.
Status: **BLOCKED** pending exact conflict scope, evidence encoding, retention and slashing policy.

### POS-N-003 — Quorum below threshold
Input: `scenario = {"votes":"FIXTURE:quorum_one_unit_below_approved_threshold","target_block":"FIXTURE:block_A"}`.
Expected: `NOT_FINALIZED`; provisional code: `E_QUORUM_INSUFFICIENT`.
Status: **BLOCKED** pending quorum threshold and smallest stake unit definition.

### POS-N-004 — Duplicate signer / noncanonical vote set
Input: `scenario = {"votes":["FIXTURE:vote_validator_A","FIXTURE:vote_validator_A_duplicate"],"encoding":"FIXTURE:noncanonical_vote_order"}`.
Expected: `REJECT`; provisional code: `E_DUPLICATE_OR_NONCANONICAL_VOTE`.
Status: **BLOCKED** pending canonical sort key, duplicate policy and vote-set encoding.

### POS-N-005 — Invalid parent / noncanonical bytes
Input: `scenario = {"proposal":"FIXTURE:proposal_A","parent":"FIXTURE:unknown_parent","encoding":"FIXTURE:noncanonical_proposal_bytes"}`.
Expected: `REJECT`; provisional code: `E_PARENT_OR_ENCODING_INVALID`.
Status: **BLOCKED** pending block serialization, parent-validity and validation-order rules.

### POS-N-006 — Conflicting finality certificates
Input: `scenario = {"certificate_A":"FIXTURE:valid_certificate_block_A","certificate_B":"FIXTURE:valid_certificate_conflicting_block_B","same_height":true,"same_domain":true}`.
Expected: `SECURITY_STOP`; provisional code: `E_CONFLICTING_FINALITY_CERTIFICATES`; no state rollback or silent overwrite; emit incident evidence.
Status: **BLOCKED** pending finality certificate semantics and mandated node/operator response.

### POS-N-007 — Stake arithmetic overflow
Input: `scenario = {"weights":["FIXTURE:weight_max","FIXTURE:weight_one"],"operation":"SUM_EFFECTIVE_VOTING_STAKE"}`.
Expected: `REJECT`; provisional code: `E_STAKE_ARITHMETIC_OVERFLOW`; wraparound forbidden.
Status: **BLOCKED** pending exact integer width and maximum valid stake.

### POS-N-008 — Invalid signature / unauthorized leader
Input: `scenario = {"proposal":"FIXTURE:proposal_A","signature":"FIXTURE:invalid_signature_A","proposer":"FIXTURE:not_eligible_validator"}`.
Expected: `REJECT`; provisional code: `E_SIGNATURE_OR_LEADER_INVALID`.
Status: **BLOCKED** pending signature scheme, leader eligibility and validation order.

### POS-N-009 — Partition without quorum
Input: `scenario = {"partition_A":"FIXTURE:validators_A_below_quorum","partition_B":"FIXTURE:validators_B_below_quorum","cross_partition_messages":false}`.
Expected: neither partition finalizes; after rejoin, only approved deterministic recovery may proceed; provisional code for attempted finalization: `E_QUORUM_INSUFFICIENT`.
Status: **BLOCKED** pending quorum and recovery/liveness rules.

### POS-N-010 — Arrival-order influence
Input: `scenario = {"candidate_set":"FIXTURE:same_valid_candidate_set","delivery_orders":["FIXTURE:order_AB","FIXTURE:order_BA"]}`.
Expected: selected block and resulting state hash are identical for both delivery orders; differing outputs fail with `E_FORK_CHOICE_NONDETERMINISTIC`.
Status: **BLOCKED** pending fork-choice rule and independent oracle.

### POS-N-011 — Mining/PoH proof presented as finality
Input: `scenario = {"work_proof":"FIXTURE:valid_work_proof_A","poh_proof":"FIXTURE:valid_poh_proof_A","validator_votes":[],"requested_action":"FINALIZE"}`.
Expected: `REJECT`; provisional code: `E_FINALITY_REQUIRES_VALIDATOR_QUORUM`.
Status: **BLOCKED** pending separation of work proofs and finality message schema; intended invariant is that work/PoH alone cannot finalize.

### POS-N-012 — Finality regression attempt
Input: `scenario = {"existing_finalized":"FIXTURE:block_A","new_certificate":"FIXTURE:certificate_block_B_same_height","same_domain":true}`.
Expected: `SECURITY_STOP` or deterministic rejection per approved operator-response policy; never overwrite block A; provisional code: `E_FINALITY_REGRESSION`.
Status: **BLOCKED** pending conflict-response semantics and incident-evidence format.

## Parameter decision register

No defaults are implied. Each row needs an owner decision, exact normative value/formula, versioning rule, independent review, and boundary vectors.

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

## Evidence manifest required for every run

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

A successful documentation/build workflow does not satisfy any protocol-vector, negative-test, multi-node, partition/recovery, cryptographic-review or production-readiness gate.
