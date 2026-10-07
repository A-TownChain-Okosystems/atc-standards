---
standard:
  id: ATC-STD-644
  title: "Function & Change Evidence Standard"
  version: "0.1.0"
  status: draft
  category: audit
  authority: A-TownChain-Okosystems
  owner: "Standards Governance"
  created: "2026-09-27"
  updated: "2026-09-27"
  normative: false
  effective_date: null
  review_date: null
  classification: PUBLIC
  language: en-US
  supersedes: null
  superseded_by: null
  dependencies:
    - ATC-STD-000
    - ATC-STD-561
    - ATC-STD-CHANGE-001
    - ATC-STD-999
  related_standards:
    - ATC-STD-AUDIT-001
    - ATC-STD-VERSION-001
    - ATC-STD-COMPAT-001
  license: "Copyright (c) 2026 A-TownChain-Okosystems"
  applies_to: "Alle ATC-Repositories"
---

# ATC-STD-644 — Function & Change Evidence Standard

> **Status:** DRAFT / CANDIDATE (v0.1.0) — SCR-0130. Nicht APPROVED und nicht normativ.

## Abstract

ATC-STD-644 defines the machine-checkable evidence model connecting requirements, specifications, components, functions, implementations, changes, tests, CI, E2E verification, audits and releases.

The standard operationalizes **No Evidence, No Trust** at function and change granularity.

## §1 Core Rule

> **No claim without evidence. No evidence without identity. No verification without exact source binding. No release status without complete required traceability.**

## §2 Canonical Evidence Graph

```text
REQUIREMENT
    ↓
SPECIFICATION
    ↓
COMPONENT
    ↓
FUNCTION
    ↓
IMPLEMENTATION
    ↓
CHANGE
    ├── DOCUMENTATION
    └── TEST
          ↓
         CI
          ↓
         E2E
          ↓
        AUDIT
          ↓
       RELEASE
```

The graph MUST support reverse traversal:

- Requirement → implementation
- Source symbol → function → specification → requirement
- Change → affected functions/components → documentation/tests/evidence

## §3 Canonical Identifiers

| Object | Identifier |
|---|---|
| Requirement | `ATC-REQ-*` |
| Specification | `ATC-SPEC-*` |
| Component | `ATC-COMP-*` |
| Function | `ATC-FUNC-*` |
| Implementation | `ATC-IMPL-*` |
| Change | `ATC-CHANGE-*` |
| Documentation | `ATC-DOC-*` |
| Test | `ATC-TEST-*` |
| CI Evidence | `ATC-CI-*` |
| E2E Evidence | `ATC-E2E-*` |
| Audit | `ATC-AUDIT-*` |
| Release | `ATC-REL-*` |

Identifiers MUST be stable within their lifecycle. A Function ID MUST NOT change merely because its implementation commit changes.

## §4 Function Identity

Every auditable function MUST have:

- Function ID
- purpose
- inputs
- outputs
- errors
- invariants
- security/capability requirements where applicable
- specification reference
- documentation reference
- component reference
- implementation reference
- test references

Example:

```yaml
function_id: ATC-FUNC-GENESIS-RUNTIME-001
name: GenesisRuntime::replicate
purpose: Replicate authoritative runtime state.
specification:
  id: ATC-SPEC-...
  version: "1.0"
documentation:
  id: ATC-DOC-...
  version: "1.0"
component:
  id: ATC-COMP-GENESIS-RUNTIME
```

## §5 Implementation Evidence

An implementation record MUST identify repository, path, module/symbol and exact commit SHA:

```yaml
implementation:
  id: ATC-IMPL-...
  repository: A-TownChain-Okosystems/genesis-engine
  path: modules/atc-genesis-runtime/src/lib.rs
  module: atc_genesis_runtime
  symbol: GenesisRuntime::replicate
  commit_sha: "EXACT_SHA"
```

A file's existence alone MUST NOT establish implementation status.

## §6 Change Evidence

Every relevant change MUST be traceable by:

```yaml
change:
  id: ATC-CHANGE-...
  base_sha: "EXACT_BASE_SHA"
  head_sha: "EXACT_HEAD_SHA"
  classification:
    - BUGFIX
  affected_components: []
  affected_functions: []
  files: []
```

Allowed classifications:

- ADD
- MODIFY
- REMOVE
- REFACTOR
- SECURITY
- BUGFIX
- API_CHANGE
- ABI_CHANGE
- DEPENDENCY_CHANGE
- CONFIG_CHANGE
- DOCUMENTATION_ONLY
- TEST_ONLY

A DOCUMENTATION_ONLY or TEST_ONLY change MUST NOT be represented as an implementation change.

## §7 Change Impact Gate

For every change:

```text
CHANGE
 ├── Source changed? → Implementation impact
 ├── Behavior changed? → Specification / Documentation / Test impact
 ├── API changed? → API evidence
 ├── ABI changed? → ABI evidence
 ├── Security boundary changed? → Security review
 └── Dependency changed? → Dependency evidence
```

A required impact record MUST exist before the corresponding verification status can be claimed.

## §8 Test Evidence

Tests SHOULD be classified:

- positive
- negative
- boundary
- regression

A test record MUST resolve to a concrete implementation/function and MUST identify the tested source state where relevant.

## §9 CI Evidence and Exact SHA Binding

CI verification MUST be bound to the exact implementation commit:

```text
CI.commit_sha == Implementation.commit_sha
```

A CI evidence record MUST contain:

```yaml
ci_evidence:
  id: ATC-CI-...
  commit_sha: "EXACT_SHA"
  run_id: "RUN_ID"
  job_id: "JOB_ID"
  step: "STEP"
  result: PASS|FAIL|SKIPPED
```

A CI run that executes a PR merge ref or another synthetic integration commit MUST NOT be represented as exact source-commit CI evidence unless the evidence record also identifies the executed commit and the policy explicitly permits that verification class.

Historical CI success MUST NOT be substituted for current-SHA evidence.

## §10 E2E, Audit and Release Evidence

E2E, audit and release records MUST reference the implementation/change evidence they validate.

Absence of required evidence MUST be represented as NOT_PROVEN, not inferred as PASS.

## §11 Status Model

```text
PRESENT
  ↓
SPECIFIED
  ↓
DOCUMENTED
  ↓
IMPLEMENTED
  ↓
TESTED
  ↓
CI-VERIFIED
  ↓
E2E-VERIFIED
  ↓
AUDITED
  ↓
RELEASE-READY
```

A status MUST NOT be promoted solely because a lower-level artifact exists.

## §12 Traceability Model

Traceability is a separate dimension:

- COMPLETE
- PARTIAL
- INCOMPLETE
- BROKEN

Example:

```text
Status: CI-VERIFIED
Traceability: INCOMPLETE
```

This means the exact implementation passed the required CI evidence, but the full requirement/documentation/change chain is not closed.

## §13 Function Consistency Gate

The following MUST be machine-checkable:

- every implemented Function ID has a specification where required
- every implemented Function ID has documentation where required
- every implementation maps to a source symbol
- behavior-changing changes have tests
- API changes update applicable specification/documentation
- ABI changes update applicable specification/documentation
- removed functions are removed/deprecated in applicable documentation
- tests reference valid Function IDs where the repository adopts Function IDs
- CI evidence references the exact implementation SHA
- required E2E evidence references the exact implementation/change SHA

## §14 Change Completeness Gate

```text
BASE SHA
   ↓
DIFF
   ↓
HEAD SHA
   ↓
IMPACT ANALYSIS
   ↓
SPEC / DOC / TEST
   ↓
CI
   ↓
RESULT
```

An incomplete required chain MUST result in TRACEABILITY=INCOMPLETE or BROKEN and MUST NOT support RELEASE-READY.

## §15 Canonical Function Record

```yaml
function_id: ATC-FUNC-GENESIS-RUNTIME-001

requirement:
  id: ATC-REQ-...
  version: "1.0"

specification:
  id: ATC-SPEC-...
  version: "1.0"

documentation:
  id: ATC-DOC-...
  version: "1.0"

component:
  id: ATC-COMP-GENESIS-RUNTIME

implementation:
  id: ATC-IMPL-...
  repository: A-TownChain-Okosystems/genesis-engine
  path: modules/atc-genesis-runtime/src/lib.rs
  module: atc_genesis_runtime
  symbol: GenesisRuntime::replicate
  commit_sha: "..."

change:
  id: ATC-CHANGE-...
  base_sha: "..."
  head_sha: "..."
  classification: [BUGFIX]

tests:
  - id: ATC-TEST-...
    type: regression

ci_evidence:
  id: ATC-CI-...
  commit_sha: "..."
  run_id: "..."
  job_id: "..."
  step: "..."
  result: PASS

e2e_evidence:
  id: ATC-E2E-...
  status: NOT_PROVEN

audit:
  id: ATC-AUDIT-...
  status: NOT_PROVEN

release:
  id: ATC-REL-...
  status: NOT_READY
```

## §16 Compliance Principle

```text
EXISTS
≠ IMPLEMENTED
≠ VERIFIED
≠ TRACEABLE
≠ RELEASE-READY
```

The claims "implemented", "tested", "CI-verified", "E2E-verified", "audited" and "release-ready" MUST NOT be asserted without the corresponding evidence.

## §17 Relationship to Existing Standards

ATC-STD-644 complements and does not replace:

- ATC-STD-000 — Standards Governance
- ATC-STD-300 — Development & Project Management
- ATC-STD-561 — Functional Requirements
- ATC-STD-CHANGE-001 — Change Governance
- ATC-STD-999 — Master-Audit
- ATC-STD-AUDIT-001 — Audit procedure
- ATC-STD-VERSION-001 — Versioning
- ATC-STD-COMPAT-001 — Compatibility

Where another standard is authoritative for a specific lifecycle or governance decision, that standard remains authoritative.


## §19 Required Machine-Checkable Function Set

The following functions define the minimum machine-checkable functional surface of ATC-STD-644.

### P0 — Core Evidence Graph

| Function ID | Function | Purpose |
|---|---|---|
| ATC-FUNC-EVIDENCE-001 | Requirement Resolver | Resolve Requirement → Specification relationships. |
| ATC-FUNC-EVIDENCE-002 | Component Resolver | Resolve Specification → Component relationships. |
| ATC-FUNC-EVIDENCE-003 | Function Registry | Register, resolve and enforce uniqueness of ATC-FUNC-* identities. |
| ATC-FUNC-EVIDENCE-004 | Implementation Resolver | Resolve Function → repository/path/module/symbol/commit SHA. |
| ATC-FUNC-EVIDENCE-005 | Change Resolver | Resolve Function/Component → Change/Base SHA/Head SHA/impact. |
| ATC-FUNC-EVIDENCE-006 | Test Resolver | Resolve Function/Implementation → applicable tests and test state. |
| ATC-FUNC-EVIDENCE-007 | CI Evidence Resolver | Resolve Implementation SHA → Run/Job/Step/Log evidence. |
| ATC-FUNC-EVIDENCE-011 | Function Consistency Validator | Validate Function ↔ Specification ↔ Documentation ↔ Implementation consistency. |
| ATC-FUNC-EVIDENCE-012 | Implementation Validator | Validate repository/path/module/symbol and exact implementation SHA identity. |
| ATC-FUNC-EVIDENCE-013 | Change Completeness Validator | Validate Base SHA → Diff → Head SHA → Impact completeness. |
| ATC-FUNC-EVIDENCE-014 | Test Coverage Validator | Validate required Function/Implementation → Test bindings. |
| ATC-FUNC-EVIDENCE-015 | Exact-SHA CI Validator | Require CI.commit_sha == Implementation.commit_sha for exact-SHA CI verification. |
| ATC-FUNC-EVIDENCE-017 | Traceability Validator | Validate the complete required evidence graph and reverse traversal. |
| ATC-FUNC-EVIDENCE-018 | Status Validator | Prevent status promotion without the evidence required for that status. |
| ATC-FUNC-EVIDENCE-019 | Evidence Identity Validator | Require unique, stable identities for evidence records. |

### P0 — Previously missing graph function

| Function ID | Function | Purpose |
|---|---|---|
| ATC-FUNC-EVIDENCE-021 | Documentation Resolver | Resolve Function/Change → applicable Documentation records and validate documentation coverage for behavior, API and ABI changes. |

ATC-FUNC-EVIDENCE-021 is mandatory because Documentation is an explicit node of the canonical evidence graph. A Change Resolver or Function Consistency Validator MUST NOT be considered a substitute for the ability to resolve documentation evidence independently.

### P1 — Verification and Release Lifecycle

| Function ID | Function | Purpose |
|---|---|---|
| ATC-FUNC-EVIDENCE-008 | E2E Evidence Resolver | Resolve Change/Implementation → E2E evidence. |
| ATC-FUNC-EVIDENCE-009 | Audit Evidence Resolver | Resolve required evidence → Audit records and findings. |
| ATC-FUNC-EVIDENCE-010 | Release Evidence Resolver | Resolve Audit/Traceability → Release evidence. |
| ATC-FUNC-EVIDENCE-016 | E2E Binding Validator | Validate E2E evidence against the exact implementation/change evidence. |
| ATC-FUNC-EVIDENCE-020 | Release Readiness Validator | Permit RELEASE-READY only when all required evidence and traceability conditions are satisfied. |

### Function invariants

1. Function IDs MUST remain stable when implementation commits change.
2. Resolver output MUST identify the referenced evidence object by its canonical ID.
3. A resolver MUST NOT infer missing evidence as PASS.
4. A validator MUST distinguish NOT_PROVEN, FAIL, INCOMPLETE and BROKEN where applicable.
5. Exact-SHA CI verification MUST use the implementation commit SHA as the binding identity.
6. Documentation coverage MUST be independently resolvable for changes where §7 requires documentation impact.
7. The function set is a minimum surface; repository-specific standards MAY define additional functions.

## §20 Candidate Functional Requirements

Before ATC-STD-644 can become normative, each function in §19 MUST have a corresponding ATC-REQ-* requirement and ATC-SPEC-* machine-checkable specification covering at minimum:

- input schema
- output schema
- preconditions
- postconditions
- invariants
- failure conditions
- required evidence
- testability
- traceability
- priority

Positive and negative test vectors MUST be defined before implementation of the corresponding validator is considered complete.



## §22 Machine-Readable System Artifacts

The candidate MUST provide the following machine-readable artifacts:

- `schemas/evidence/record.schema.json` — canonical evidence object shape and identifier constraints.
- `schemas/evidence/traceability.schema.json` — canonical traceability edge model.
- `tests/evidence/reference-system.json` — positive and negative system vectors.
- `tools/validate_evidence_system.py` — fail-closed reference validator for identity, graph, exact-SHA and status gates.

The artifacts form one system and MUST be evaluated together. A schema-valid object with a broken reference, an unbound CI SHA, or an unjustified status MUST NOT be considered valid system evidence.

## §23 System Integrity Test

The reference system test is `ATC-TEST-EVIDENCE-SYSTEM-001`.

The positive vector MUST demonstrate:

`Implementation SHA == CI SHA`
→ `CI-VERIFIED`
→ `Traceability=COMPLETE`.

The negative vector MUST demonstrate:

`Implementation SHA != CI SHA`
→ `CI-VERIFIED=NOT_PROVEN`
→ `Traceability=INCOMPLETE`
→ `Release=BLOCKED`.

The test MUST fail closed. It MUST NOT convert missing, invalid, or mismatched evidence into PASS.

A future normative implementation MUST extend this reference test from the synthetic vectors to repository-backed evidence records while preserving these invariants.

## §24 System Definition of Done

ATC-STD-644 functional system implementation is not complete until all of the following are machine-verified:

1. Canonical IDs conform to the identifier grammar.
2. Evidence records conform to the applicable schema.
3. Traceability edges resolve to existing evidence objects.
4. Forward traversal REQ → RELEASE is closed where required.
5. Reverse traversal SOURCE → FUNCTION → SPECIFICATION → REQUIREMENT is available where required.
6. Implementation identity contains an exact source commit SHA.
7. CI evidence contains Run, Job, Step and Result identity.
8. Exact-SHA validation proves `CI.commit_sha == Implementation.commit_sha`.
9. Status promotion is blocked when required evidence is missing or mismatched.
10. The negative exact-SHA vector proves that false verification is rejected.
11. Release readiness is blocked while required traceability is incomplete.
12. The complete system test itself is executed by CI on the exact candidate commit.

## §25 Candidate Status

The machine-readable artifacts and system test are part of the ATC-STD-644 candidate specification. They do not make the standard approved or normative. Approval remains subject to the ATC-STD-000 governance lifecycle.
