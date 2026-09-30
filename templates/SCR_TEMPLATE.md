# SCR-<NNNN> — <Change Contract Title>

> **Schema:** v2 (SCR-0129)
> **Governance state:** PROPOSED / PENDING until the applicable Owner / §9 gate is satisfied.
> **Important:** APPROVED ≠ IMPLEMENTED ≠ VERIFIED ≠ CLOSED.

## Machine-readable Change Contract

```yaml
schema_version: 2
id: SCR-<NNNN>
affected_standard: ATC-STD-<XXX>
proposed_change: "<...>"
motivation: "<...>"
compatibility_impact: "<...>"
security_impact: "<...>"
migration_impact: "<...>"
decision: PENDING
date: YYYY-MM-DD

purpose:
  objective: "<...>"
  problem_solved: "<...>"
  system_benefit: "<...>"
  user_consumer_benefit: "<...>"
  technical_operational_benefit: "<...>"
  expected_measurable_outcome: "<...>"

necessity:
  required: true
  classification: REQUIRED
  requirement_source: "<REQ/STD/contract>"
  blocking_consequence: "<...>"
  affected_invariants: []
  reason: "<...>"

rationale:
  why: "<...>"
  why_now: "<...>"
  root_cause: "<...>"
  requirement_contract_reference: "<...>"
  consequence_without_change: "<...>"
  technical_rationale: "<...>"

improvement:
  before: "<observable current state>"
  after: "<expected target state>"
  dimensions: {}
  evidence: []

safety_security:
  safe: false
  security_impact: "<...>"
  safety_impact: "<...>"
  attack_surface_change: "<...>"
  authorization_capability_impact: "<...>"
  cryptography_impact: "<...>"
  secrets_credentials_impact: "<...>"
  data_integrity: "<...>"
  availability_reliability: "<...>"
  compatibility_breaking_change: "<...>"
  new_failure_modes: "<...>"
  rollback_recovery: "<...>"
  residual_risk: "<...>"
  evidence: []

completeness:
  matrix: []
  residual_risk: "<...>"

evidence_separation:
  error_evidence: []
  finding_evidence: []
  verification_evidence: []
  exact_sha: ""

lifecycle:
  status: ANALYZED
  implementation_state: NOT_STARTED
  verification_state: NOT_VERIFIED
  closure_assessment: OPEN
  closure_decision: OPEN

existing_first:
  performed: true
  ssot: "<canonical SSOT>"
  existing_artifacts: []
  reuse_extend_consolidate_decision: "<reuse | extend | consolidate | new>"
```

## 1. Purpose

### Objective
<...>

### Problem solved
<...>

### System benefit
<...>

### Expected measurable outcome
<...>

## 2. Necessity

- **Required:** true / false
- **Classification:** MANDATORY / REQUIRED / CONDITIONAL / OPTIONAL / REJECTED
- **Requirement source:** <...>
- **Blocking consequence:** <...>
- **Affected invariants:** <...>
- **Reason:** <...>

## 3. Rationale

- **Why:** <...>
- **Why now:** <...>
- **Root cause:** <...>
- **Requirement / contract:** <...>
- **Consequence without change:** <...>
- **Technical rationale:** <...>

Canonical chain: `Requirement → Problem → Root Cause → Consequence → Required Change`

## 4. Improvement — Before / After

| Dimension | Before | After | Evidence |
|---|---|---|---|
| Correctness | | | |
| Security | | | |
| Reliability | | | |
| Performance | | | |
| Maintainability | | | |
| Interoperability | | | |
| Determinism | | | |
| Observability | | | |
| Operability | | | |
| Compatibility | | | |

Only evidence-backed improvements are claims. Non-applicable dimensions are **N/A**, not PASS.

## 5. Safety & Security

Document security/safety impact, attack-surface changes, authorization/capability effects, cryptography, secrets, data integrity, availability/reliability, compatibility, new failure modes, rollback/recovery and residual risk.

> `safe: true` without supporting evidence is not a valid safety/security verification.

## 6. Completeness Matrix

The matrix is authoritative for closure assessment. Every required area must be `DONE`; non-required areas must be explicitly `N/A`.

| Area | Required | Status | Evidence |
|---|---:|---|---|
| Architecture / SSOT | | | |
| Specification / Contract | | | |
| Source Code | | | |
| API | | | |
| ABI / Wire Format | | | |
| State / Storage | | | |
| Security | | | |
| Tests | | | |
| Integration | | | |
| CI/CD | | | |
| Documentation | | | |
| Migration | | | |
| Compatibility | | | |
| Release | | | |
| Audit | | | |

## 7. Evidence Separation

**Error Evidence ≠ Finding Evidence ≠ Verification Evidence.**

- Error Evidence: raw failure/log/observed error.
- Finding Evidence: evidence establishing a governed finding and its scope.
- Verification Evidence: independent evidence that the claimed fix/requirement is satisfied.

For CI-relevant changes, Verification Evidence MUST reference the exact verified SHA.

## 8. Lifecycle / Closure

`UNANALYZED → ANALYZED → PLANNED → IMPLEMENTING → FIXED → RERUNNING → VERIFIED → CLOSED`

Alternative states: `REJECTED`, `FAILED`, `RESIDUAL`.

Rules:
- `FIXED ≠ VERIFIED`
- `PASS ≠ VERIFIED`
- `IMPLEMENTED ≠ COMPLETE`
- CI-relevant `VERIFIED` requires Exact-SHA Evidence.
- `CLOSED` requires a completed Completeness Assessment.
- `APPROVED ≠ IMPLEMENTED ≠ VERIFIED ≠ CLOSED`.

## 9. Existing-First

Record existing equivalent, SSOT, dependencies, reuse/extend/consolidate decision, and why a new artifact is necessary if applicable.

## 10. Acceptance / Closure Gate

A SCR is closable only when Purpose, Necessity, Rationale, Impact, Improvement, Safety/Security, required Implementation, Tests, separated Evidence, Completeness, SSOT/Documentation sync, Residual Risk and required Human/Audit Gates are satisfied.

## 11. Governance Decision

- Decision: `PENDING / ACCEPTED / REJECTED`
- Owner / §9 reference: `<required for normative approval>`
- Verification reference: `<Exact-SHA / audit evidence>`
