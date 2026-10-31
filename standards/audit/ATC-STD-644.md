---
standard:
  id: ATC-STD-644
  title: "Function & Change Evidence Standard"
  version: "0.1.0"
  status: candidate
  category: audit
  authority: A-TownChain-Okosystems
  owner: "Standards Governance"
  created: "2026-09-27"
  updated: "2026-10-31"
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
  applies_to: "ATC repositories publishing or consuming auditable function and change evidence"
  not_applies_to:
    - "External repositories outside ATC governance"
    - "Exploratory notes that make no implementation or verification claim"
---

# ATC-STD-644 — Function & Change Evidence Standard

> **Status:** DRAFT / CANDIDATE (v0.1.0) — SCR-0130. Nicht APPROVED und nicht normativ.

## Abstract

ATC-STD-644 defines the machine-checkable evidence model connecting requirements, specifications, components, functions, implementations, changes, tests, CI, E2E verification, audits and releases.

The standard operationalizes **No Evidence, No Trust** at function and change granularity.

## Scope

**Applies to:** ATC repositories that publish, consume, or audit function-level and change-level evidence, including implementation identity, tests, CI, E2E, audit, and release traceability.

**Does not apply to:** external repositories outside ATC governance, personal or exploratory notes that make no implementation claim, and generated artifacts that are not authoritative evidence records.

A repository may adopt a narrower operational profile only when the applicable governance authority records that scope. Scope exclusions MUST NOT be used to bypass a required security, governance, or release gate.

## §1 Core Rule

> **No claim without evidence. No evidence without identity. No verification without exact source binding. No release status without complete required traceability.**

## §2 Canonical Evidence Graph

```text
REQUIREMENT → SPECIFICATION → COMPONENT → FUNCTION → IMPLEMENTATION → CHANGE
                                                        ├── DOCUMENTATION
                                                        └── TEST → CI → E2E → AUDIT → RELEASE
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

Every auditable function MUST have a stable Function ID, purpose, inputs, outputs, errors, invariants, applicable security/capability requirements, specification reference, documentation reference, component reference, implementation reference, and test references.

## §5 Implementation Evidence

An implementation record MUST identify repository, path, module/symbol and exact 40-character source commit SHA. A file's existence alone MUST NOT establish implementation status.

## §6 Change Evidence

Every relevant change MUST identify base SHA, head SHA, classification, affected components, affected functions and changed files. Documentation-only or test-only changes MUST NOT be represented as implementation changes.

Allowed classifications: ADD, MODIFY, REMOVE, REFACTOR, SECURITY, BUGFIX, API_CHANGE, ABI_CHANGE, DEPENDENCY_CHANGE, CONFIG_CHANGE, DOCUMENTATION_ONLY, TEST_ONLY.

## §7 Change Impact Gate

For every change, evaluate source, behavior, API, ABI, security-boundary and dependency impact. Required specification, documentation, test, API/ABI and security evidence MUST exist before the corresponding verification status can be claimed.

## §8 Test Evidence

Tests SHOULD be classified as positive, negative, boundary or regression. A test record MUST resolve to a concrete implementation/function and identify the tested source state where relevant.

## §9 CI Evidence and Exact SHA Binding

CI verification MUST be bound to the exact implementation commit:

```text
CI.commit_sha == Implementation.commit_sha
```

A CI evidence record MUST identify the commit SHA, workflow run ID, job ID, step name/number and result. A PR merge-ref or synthetic integration commit MUST NOT be represented as exact source-commit evidence. Historical CI success MUST NOT be substituted for current-SHA evidence.

## §10 E2E, Audit and Release Evidence

E2E, audit and release records MUST reference the implementation/change evidence they validate. Missing required evidence MUST be represented as NOT_PROVEN, not inferred as PASS.

## §11 Status Model

```text
PRESENT → SPECIFIED → DOCUMENTED → IMPLEMENTED → TESTED
        → CI-VERIFIED → E2E-VERIFIED → AUDITED → RELEASE-READY
```

A status MUST NOT be promoted solely because a lower-level artifact exists.

## §12 Traceability Model

Traceability is a separate dimension: COMPLETE, PARTIAL, INCOMPLETE or BROKEN. A function may be CI-VERIFIED while overall traceability remains INCOMPLETE; that state MUST NOT support RELEASE-READY.

## §13 Function Consistency Gate

Machine checks MUST verify applicable specification/documentation links, source symbol identity, behavior-change tests, API/ABI updates, removed-function documentation, Function ID references, exact-SHA CI evidence and required E2E bindings.

## §14 Change Completeness Gate

```text
BASE SHA → DIFF → HEAD SHA → IMPACT ANALYSIS → SPEC / DOC / TEST → CI → RESULT
```

An incomplete required chain MUST result in TRACEABILITY=INCOMPLETE or BROKEN and MUST NOT support RELEASE-READY.

## §15 Canonical Function Record

A canonical record MUST link requirement, specification, documentation, component, implementation, change, tests, CI evidence, E2E evidence, audit and release records through stable IDs and exact source identities.

## §16 Compliance Principle

```text
EXISTS ≠ IMPLEMENTED ≠ VERIFIED ≠ TRACEABLE ≠ RELEASE-READY
```

The claims implemented, tested, CI-verified, E2E-verified, audited and release-ready MUST NOT be asserted without corresponding evidence.

## §17 Relationship to Existing Standards

ATC-STD-644 complements and does not replace ATC-STD-000, ATC-STD-300, ATC-STD-561, ATC-STD-CHANGE-001, ATC-STD-999, ATC-STD-AUDIT-001, ATC-STD-VERSION-001 or ATC-STD-COMPAT-001. The authoritative existing standard remains authoritative for its lifecycle/governance decision.

## §18 Candidate Governance Boundary

ATC-STD-644 remains a candidate under SCR-0130. This document and its reference validator do not approve the standard, amend ATC-STD-000, grant an exception, or make the candidate normative. Adoption and approval remain subject to the existing ATC-STD-000 authority and review lifecycle.

Until approval, this candidate MUST NOT be used to assert that a repository, function, change or release is VERIFIED solely because it conforms to reference examples.

## §19 Required Machine-Checkable Function Set

The minimum functional surface includes requirement, component, function, implementation, change, test, CI, E2E, audit, release and documentation resolvers; function consistency, implementation, change completeness, test coverage, exact-SHA, E2E binding, traceability, status, evidence identity and release-readiness validators.

The required function identifiers are ATC-FUNC-EVIDENCE-001 through ATC-FUNC-EVIDENCE-021, with ATC-FUNC-EVIDENCE-021 reserved for independent documentation resolution.

## §20 Candidate Functional Requirements

Before ATC-STD-644 can become normative, each function in §19 MUST have an ATC-REQ-* requirement and ATC-SPEC-* machine-checkable specification covering inputs, outputs, preconditions, postconditions, invariants, failure conditions, required evidence, testability, traceability and priority. Positive and negative test vectors MUST be defined.

## §21 Conformance and Evidence Boundary

Reference graphs and test vectors are conformance fixtures, not production attestations. Their identifiers, SHA values and CI run/job/step values MUST NOT be copied into live implementation records.

Repository-backed verification MUST independently resolve the exact checked-out source commit, GitHub Actions workflow run, completed validation job, named successful validation step and result associated with that source commit.

Missing API responses, permissions, jobs, steps, SHA matches or identities MUST remain NOT_PROVEN/BLOCKED. They MUST NOT be converted into PASS by fallback logic.

## §22 Machine-Readable System Artifacts

The candidate provides `schemas/evidence/record.schema.json`, `schemas/evidence/traceability.schema.json`, `tests/evidence/reference-system.json` and `tools/validate_evidence_system.py`. These artifacts MUST be evaluated together.

## §23 System Integrity Test

The positive vector MUST demonstrate a closed graph and exact-SHA binding. The negative vector MUST demonstrate that a mismatched implementation/CI SHA produces NOT_PROVEN, INCOMPLETE traceability and BLOCKED release. Synthetic vectors are limited to conformance testing and MUST NOT substitute for live CI evidence.

## §24 System Definition of Done

1. Canonical IDs conform to the identifier grammar.
2. Evidence records conform to the applicable JSON Schema.
3. Traceability edges resolve to existing evidence objects.
4. Forward and reverse traversal are available where required.
5. Implementation identity contains an exact source commit SHA.
6. CI evidence resolves Run, Job, Step and Result identities.
7. Exact-SHA validation proves CI.commit_sha == Implementation.commit_sha.
8. Status promotion is blocked when required evidence is missing or mismatched.
9. Negative vectors reject false verification.
10. Release readiness is blocked while required traceability is incomplete.
11. CI explicitly checks out and verifies the exact candidate head SHA.
12. CI resolves the completed validation job and successful named step through the GitHub Actions API.

## §25 Candidate Status

The machine-readable artifacts and tests do not make ATC-STD-644 approved or normative. Approval remains subject to ATC-STD-000 governance.
