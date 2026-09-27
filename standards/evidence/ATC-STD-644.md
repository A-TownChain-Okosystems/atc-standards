# ATC-STD-644 — Function & Change Evidence Standard

**Version:** 0.1.0  
**Status:** draft  
**Category:** evidence / development  
**Normative:** candidate only  
**Authority:** A-TownChain-Okosystems  
**Owner:** Standards Governance  
**SCR:** SCR-0130

## 1. Purpose

ATC-STD-644 defines the machine-checkable evidence model connecting requirements, specifications, components, functions, implementations, changes, tests, CI, E2E verification, audits and releases.

The standard operationalizes **No Evidence, No Trust** at function and change granularity.

## 2. Core rule

> No claim without evidence. No evidence without identity. No verification without exact source binding. No release status without complete required traceability.

## 3. Canonical evidence graph

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

## 4. Canonical identifiers

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

## 5. Function identity

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

## 6. Implementation evidence

An implementation record MUST identify:

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

## 7. Change evidence

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

Allowed classifications include:

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

## 8. Change-impact gate

For every change:

```text
CHANGE
 ├── Source changed? → Implementation impact
 ├── Behavior changed? → Spec / Documentation / Test impact
 ├── API changed? → API evidence
 ├── ABI changed? → ABI evidence
 ├── Security boundary changed? → Security review
 └── Dependency changed? → Dependency evidence
```

A required impact record MUST exist before the corresponding verification status can be claimed.

## 9. Test evidence

Tests SHOULD be classified as:

- positive
- negative
- boundary
- regression

A test record MUST resolve to a concrete implementation/function and MUST identify the tested source state where relevant.

## 10. CI evidence

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

If the SHA does not match, the evidence MUST NOT establish CI-VERIFIED for that implementation.

Historical CI success MUST NOT be substituted for current-SHA evidence.

## 11. E2E, audit and release evidence

E2E, audit and release records MUST reference the implementation/change evidence they validate.

Absence of required evidence MUST be represented as NOT_PROVEN, not inferred as PASS.

## 12. Status model

Status is monotonic only when the required evidence for the next state exists:

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

## 13. Traceability model

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

## 14. Function consistency gate

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

## 15. Change completeness gate

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

## 16. Canonical function record

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

## 17. Compliance principle

The standard distinguishes:

```text
EXISTS
≠ IMPLEMENTED
≠ VERIFIED
≠ TRACEABLE
≠ RELEASE-READY
```

The following claim is prohibited without its corresponding evidence:

```text
"implemented"
"tested"
"CI-verified"
"E2E-verified"
"audited"
"release-ready"
```

## 18. Relationship to existing standards

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

## 19. Candidate status

Version 0.1.0 is a candidate specification. It is NOT APPROVED and MUST NOT be represented as an approved normative standard until the required governance/review process is completed.
