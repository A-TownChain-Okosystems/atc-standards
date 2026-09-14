---
standard:
  id: ATC-STD-MAINT-000
  title: "Maintenance Governance & Specification Standard"
  version: "1.0.0"
  status: draft
  category: maint
  family: MAINT
  authority: A-TownChain Ecosystems
  owner: ShivaCoreDev
  created: "2026-09-13"
  updated: "2026-09-14"
  normative: true
  supersedes: []
  superseded_by: null
  effective_date: null
  review_date: null
  license: "Copyright (c) 2026 Michael Wroblewski"
---

# ATC-STD-MAINT-000 — Maintenance Governance & Specification Standard

> **Maintenance Capability is a Release Requirement.**
>
> *A system MUST NOT be released to a lifecycle state requiring operational support unless its
> required maintenance capabilities are implemented, validated, documented, and evidenced.*

## 1. Purpose

ATC-STD-MAINT-000 defines the normative governance and specification model for maintenance across
the A-TownChain Ecosystem.

The standard establishes a common maintenance framework for:

- KAI-OS
- GlobusOS
- ShivaCore
- A-TownChain
- ATC-VM
- ATCLang
- Aurora AI
- infrastructure
- repositories
- standards
- documentation
- applications
- ecosystem integrations

The purpose is to ensure that systems remain secure, maintainable, compatible, observable,
recoverable, and operational throughout their complete lifecycle.

Maintenance MUST be treated as a lifecycle capability and MUST NOT be treated solely as a
post-release activity.

## 2. Scope

This standard applies to all normative ATC systems, repositories, services, platforms, protocols,
runtimes, infrastructure components, and production-bound artifacts that require maintenance.

The standard covers:

- preventive maintenance
- corrective maintenance
- adaptive maintenance
- security maintenance
- operational maintenance
- emergency maintenance
- upgrade and migration
- compatibility management
- rollback and recovery
- end-of-life and retirement
- maintenance automation
- maintenance evidence

The following maintenance classes are defined:

| Class | Name | General Meaning |
|---|---|---|
| M0 | Routine | Normal, planned maintenance |
| M1 | Operational | Operationally significant maintenance |
| M2 | Security | Security-relevant maintenance |
| M3 | Critical | System-critical or emergency maintenance |

## 3. Normative Authority

ATC-STD-MAINT-000 is the parent standard for the "ATC-STD-MAINT-*" family.

It MUST conform to "ATC-STD-000".

Specialized Maintenance Standards MUST inherit the governance baseline defined by this standard.

The relationship is:

```
ATC-STD-000
      │
      ▼
ATC-STD-MAINT-000
      │
      ├── MAINT-001 Classification
      ├── MAINT-002 Lifecycle
      ├── MAINT-003 Code
      ├── MAINT-004 Dependencies
      ├── MAINT-005 Security
      ├── MAINT-006 Infrastructure
      ├── MAINT-007 OS
      ├── MAINT-008 Blockchain
      ├── MAINT-009 VM & Runtime
      ├── MAINT-010 AI
      ├── MAINT-011 Repository
      ├── MAINT-012 Standards
      ├── MAINT-013 Documentation
      ├── MAINT-014 Performance
      ├── MAINT-015 Reliability
      ├── MAINT-016 Compatibility
      ├── MAINT-017 Upgrade & Migration
      ├── MAINT-018 Rollback & Recovery
      ├── MAINT-019 Evidence
      ├── MAINT-020 Automation
      ├── MAINT-021 Emergency
      ├── MAINT-022 End-of-Life
      ├── MAINT-023 Vendor & Supply-Chain
      └── MAINT-024 Cross-Ecosystem
```

A specialized Maintenance Standard MUST NOT weaken a requirement established by this standard
unless an explicitly governed exception exists.

## 4. Normative Language

The following terms are normative:

| Keyword | Meaning |
|---|---|
| MUST | Mandatory requirement |
| MUST NOT | Prohibited behavior |
| REQUIRED | Mandatory |
| SHOULD | Strong recommendation |
| SHOULD NOT | Strong recommendation against |
| MAY | Optional |

Normative requirements MUST be unambiguous and machine-identifiable.

## 5. Maintenance Principles

### 5.1 Lifecycle Principle

Maintenance MUST exist throughout the complete lifecycle of a system.

### 5.2 Evidence Principle

Maintenance actions MUST produce sufficient evidence to establish what changed, why it changed,
who or what performed the action, and whether the resulting state was validated.

### 5.3 No Evidence, No Trust

A maintenance action MUST NOT be considered successfully completed solely because an
implementation claims that it succeeded.

The resulting state MUST be supported by verifiable evidence.

### 5.4 Fail-Closed Principle

A required maintenance gate MUST fail closed.

If required evidence, validation, approval, or safety information is missing, the affected release
or maintenance operation MUST be blocked.

### 5.5 Least-Privilege Principle

Maintenance automation MUST operate with the minimum permissions required for its assigned task.

### 5.6 Separation of Duties

For M2 and M3 maintenance:

```
Implementer != Validator != Auditor
```

For critical release operations:

```
Release Authority != Implementer
```

Exceptions MUST be explicitly authorized and evidenced.

### 5.7 Reproducibility

Maintenance operations SHOULD be reproducible.

Automated maintenance SHOULD use deterministic configuration, version-pinned tooling, and
machine-readable inputs wherever practical.

## 6. Maintenance Capability

A system requiring operational support MUST define its required maintenance capabilities before
release.

At minimum, applicable systems MUST define:

- maintenance ownership
- maintenance documentation
- dependency inventory
- security maintenance process
- test strategy
- compatibility strategy
- rollback strategy
- recovery strategy
- monitoring
- evidence collection
- lifecycle status

The required capability set MAY be extended according to system risk.

## 7. Maintenance Readiness Gate

A release MUST pass the Maintenance Readiness Gate when the target lifecycle state requires
operational support.

```
RELEASE CANDIDATE
        │
        ▼
MAINTENANCE READINESS GATE
        │
   ┌────┴────┐
   │         │
 FAIL       PASS
   │         │
   ▼         ▼
 BLOCK     RELEASE
             │
             ▼
          OBSERVE
             │
             ▼
          EVIDENCE
             │
             ▼
       VERIFIED STATE
```

The gate MUST verify, at minimum:

```yaml
maintenance_readiness:
  maintenance_owner: required
  maintenance_documentation: required
  dependency_inventory: required
  security_process: required
  test_suite: required
  rollback_strategy: required
  compatibility_strategy: required
  monitoring: required
  evidence_collection: required
  lifecycle_status: required
```

A failed mandatory check MUST block release.

## 8. Maintenance Classification

Every maintenance activity MUST receive a maintenance classification.

### 8.1 M0 — Routine

M0 covers normal, low-risk, planned maintenance.

Examples:

- documentation updates
- dependency updates without material security impact
- small refactorings
- CI optimization
- logging improvements
- metrics improvements
- non-critical performance optimization

M0 maintenance MAY be automated when the applicable controls are satisfied.

### 8.2 M1 — Operational

M1 covers operationally significant maintenance.

Examples:

- build failures
- release pipeline instability
- service instability
- storage problems
- node problems
- performance regressions
- recovery exercises

M1 maintenance MUST receive operational review appropriate to its risk.

### 8.3 M2 — Security

M2 covers security-relevant maintenance.

Examples:

- CVEs
- vulnerable dependencies
- supply-chain compromise
- secret exposure
- key rotation
- sandbox weaknesses
- permission bypasses
- security hardening

M2 maintenance MAY bypass normal release scheduling when required to reduce security exposure.

Security review MUST be performed when required by the affected security boundary.

### 8.4 M3 — Critical

M3 covers events that can materially compromise system integrity, availability, confidentiality,
or consensus.

Examples:

- consensus defects
- kernel security-boundary compromise
- critical ATC-VM incompatibility
- chain-state corruption
- confirmed data loss
- critical remote code execution
- cryptographic trust failure

M3 maintenance MUST use the Emergency Maintenance process.

M3 maintenance MAY temporarily override ordinary maintenance scheduling, but MUST NOT eliminate
evidence, validation, or post-event accountability.

## 9. Maintenance Lifecycle

All controlled maintenance MUST follow the applicable lifecycle:

```
DETECT
  ↓
ASSESS
  ↓
CLASSIFY
  ↓
PLAN
  ↓
APPROVE
  ↓
IMPLEMENT
  ↓
TEST
  ↓
VALIDATE
  ↓
DEPLOY
  ↓
MONITOR
  ↓
EVIDENCE
  ↓
CLOSE
```

Not every lifecycle stage must require a separate human action, but required controls MUST be
demonstrably satisfied.

### 9.1 Detect

The maintenance requirement MUST be identified through one or more valid sources, such as:

- monitoring
- automated scanners
- vulnerability databases
- tests
- audits
- incident reports
- lifecycle schedules
- user reports
- engineering analysis

### 9.2 Assess

The impact, scope, affected components, dependencies, risks, and urgency MUST be assessed.

### 9.3 Classify

The activity MUST be assigned M0, M1, M2, or M3.

### 9.4 Plan

The implementation, testing, deployment, rollback, and evidence strategy MUST be defined according
to risk.

### 9.5 Approve

Required approvals MUST be obtained before implementation or deployment.

### 9.6 Implement

The approved change MUST be implemented within the authorized scope.

### 9.7 Test

Required automated and manual tests MUST be executed.

### 9.8 Validate

Validation MUST establish that the intended result was achieved and that unacceptable regressions
were not introduced.

### 9.9 Deploy

Deployment MUST follow applicable release and change-control requirements.

### 9.10 Monitor

The resulting system state MUST be monitored for the required observation period.

### 9.11 Evidence

Required evidence MUST be recorded.

### 9.12 Close

A maintenance record MUST NOT be closed until all mandatory acceptance conditions are satisfied.

## 10. Maintenance Governance Roles

The following roles SHOULD be used:

| Role | Responsibility |
|---|---|
| Maintenance Owner | Accountable for maintenance capability |
| Implementer | Performs approved changes |
| Validator | Independently validates results |
| Auditor | Reviews evidence and compliance |
| Security Reviewer | Reviews security impact |
| Release Authority | Authorizes release |
| System Owner | Accountable for system lifecycle |
| Automation Agent | Performs authorized automated maintenance |

Roles MAY be combined for low-risk M0 activities where permitted by the applicable governance
rules.

Roles MUST NOT be combined where separation is explicitly required.

## 11. Maintenance Evidence

Each controlled maintenance activity MUST have a machine-readable maintenance record.

Minimum structure:

```yaml
maintenance:
  id: MAINT-2026-0001
  classification: M1
  component: atc-node
  detected: "2026-09-13"
  reason: dependency_update

  change:
    before: "x.y.z"
    after: "x.y.z+1"

  validation:
    unit_tests: PASS
    integration_tests: PASS
    security_scan: PASS
    compatibility: PASS
    performance: PASS

  rollback:
    available: true
    tested: true

  evidence:
    commit: "..."
    pull_request: "..."
    test_report: "..."
    audit_report: "..."

  status: CLOSED
```

The actual schema MUST be defined by the applicable machine-readable Maintenance schema.

## 12. Evidence Requirements

Evidence SHOULD establish:

- maintenance identifier
- classification
- affected component
- reason
- scope
- before-state
- after-state
- actor
- timestamp
- implementation reference
- validation results
- security results
- compatibility results
- rollback status
- approval
- deployment status
- monitoring result
- closure decision

Evidence MUST be tamper-evident or traceable to an authoritative source where the risk level
requires it.

## 13. M2/M3 Additional Controls

For M2 and M3 activities, the following controls are REQUIRED unless a documented emergency
exception applies:

```yaml
critical_maintenance:
  independent_validation: required
  security_review: required
  rollback_test: required
  incident_record: required
  audit_evidence: required
```

Emergency exceptions MUST be documented and reviewed retrospectively.

## 14. Maintenance Dependencies

Maintenance MUST account for dependencies between affected components.

For KAI-OS and other layered systems, changes crossing architectural boundaries MUST validate the
affected interfaces.

For example:

```
ATCLang
   ↓
ATC-VM
   ↓
Contract Execution
   ↓
State Transition
   ↓
Consensus
   ↓
Node
   ↓
Network
```

An ATC-VM maintenance operation MUST NOT be treated as an isolated package update when it can
affect contract execution, state transitions, consensus, or network compatibility.

## 15. Compatibility

Maintenance MUST preserve defined compatibility guarantees.

Where compatibility is intentionally broken:

- the break MUST be identified,
- migration requirements MUST be documented,
- affected consumers MUST be identified,
- the new compatibility boundary MUST be validated,
- rollback or recovery MUST be evaluated.

Compatibility requirements are further specified by "ATC-STD-MAINT-016".

## 16. Upgrade and Migration

Production-bound upgrades MUST define:

- source version
- target version
- migration mechanism
- migration validation
- rollback strategy
- data/schema impact
- compatibility impact
- operational impact

Irreversible migrations MUST receive additional review proportional to their risk.

## 17. Rollback and Recovery

Production systems MUST define a rollback or recovery strategy appropriate to their architecture.

For critical systems:

- rollback SHOULD be tested before production deployment;
- recovery procedures MUST be documented;
- recovery evidence MUST be retained;
- recovery assumptions MUST be periodically validated.

A rollback strategy that has never been validated MUST NOT be represented as tested.

## 18. Automation

Maintenance automation MAY perform:

- dependency detection
- vulnerability detection
- SBOM generation
- static analysis
- test execution
- maintenance record creation
- low-risk updates
- evidence collection
- escalation

Automation MUST operate within explicit authorization boundaries.

Automated maintenance MUST NOT bypass mandatory governance gates.

An AI agent MUST NOT independently authorize a maintenance action requiring human approval unless
an applicable governance standard explicitly grants that authority.

## 19. Repository Requirements

Production repositories governed by this standard SHOULD contain:

- MAINTENANCE.md
- SECURITY.md
- CHANGELOG.md
- STATUS.md
- ROADMAP.md

Critical repositories SHOULD additionally maintain:

```
docs/
└── maintenance/
    ├── procedures/
    ├── runbooks/
    ├── recovery/
    └── evidence/
```

The applicable repository standard MAY define stricter requirements.

## 20. Machine-Readable Conformance

The Maintenance framework MUST support machine-readable validation.

The canonical implementation SHOULD contain:

```
schemas/
└── maintenance/
    ├── maintenance-record.schema.json
    ├── maintenance-readiness.schema.json
    └── maintenance-evidence.schema.json
```

The schemas MUST use explicit types and MUST reject unknown properties where strict validation is
required.

CI SHOULD validate:

- maintenance metadata
- classification
- required evidence
- maintenance readiness
- lifecycle state
- required documentation
- dependency inventory
- security controls
- rollback declaration
- compatibility declaration

## 21. CI Maintenance Conformance

A repository implementing this standard SHOULD provide automated conformance checks.

Example:

```
Repository
    │
    ├── Dependency Scanner
    ├── Vulnerability Scanner
    ├── SBOM Generator
    ├── License Scanner
    ├── Static Analysis
    ├── Test Suite
    ├── Performance Tests
    ├── Compatibility Tests
    └── Repository Governance
              │
              ▼
      Maintenance Conformance
              │
       ┌──────┼──────┐
       ▼      ▼      ▼
      M0     M1    M2/M3
       │      │      │
       ▼      ▼      ▼
    Automate Review Escalate
```

A mandatory conformance failure MUST block the applicable gate.

## 22. Maintenance Metrics

Organizations implementing this standard SHOULD track:

| Metric | Description |
|---|---|
| MTTD | Mean Time to Detect |
| MTTA | Mean Time to Acknowledge |
| MTTR | Mean Time to Recovery/Repair |
| MTBF | Mean Time Between Failures |
| Patch Latency | Time from vulnerability identification to remediation |
| Dependency Freshness | Currency of dependencies |
| Technical Debt | Outstanding maintenance debt |
| Maintenance Backlog | Outstanding maintenance work |
| Rollback Success Rate | Successful rollback ratio |
| Regression Rate | Maintenance-induced regression ratio |
| Evidence Completeness | Percentage of complete evidence records |
| Recovery Readiness | Validated recovery capability |

Metrics MUST NOT be used to conceal individual critical failures.

## 23. Compliance

A system conforms to ATC-STD-MAINT-000 when:

1. applicable maintenance requirements are identified;
2. required maintenance capabilities exist;
3. applicable maintenance classifications are used;
4. required lifecycle controls are implemented;
5. required gates are enforced;
6. required evidence is generated;
7. required security and compatibility controls are satisfied;
8. applicable rollback/recovery requirements are satisfied;
9. machine-readable conformance requirements are satisfied where applicable.

A system MUST NOT be declared compliant solely from documentation claims.

Compliance MUST be supported by evidence.

## 24. Exceptions

Exceptions MUST:

- identify the affected requirement;
- document the reason;
- identify the affected system;
- assess the risk;
- define compensating controls;
- identify an owner;
- define an expiration or review date;
- be approved by the applicable authority;
- be recorded as evidence.

Permanent exceptions SHOULD NOT be used to bypass fundamental security or integrity requirements.

M3 emergency exceptions MUST receive retrospective review.

## 25. Lifecycle and Status

This standard follows the lifecycle defined by "ATC-STD-000":

```
IDEA
  ↓
PROPOSED
  ↓
DRAFT
  ↓
REVIEW
  ↓
CANDIDATE
  ↓
APPROVED
  ↓
STABLE
  ↓
DEPRECATED
  ↓
RETIRED
```

The identifier "ATC-STD-MAINT-000" MUST remain immutable throughout its lifecycle.

Version changes MUST NOT change the standard identifier.

## 26. Relationship to GSEPF

ATC-STD-MAINT-000 defines the normative Maintenance Governance layer.

GSEPF provides the governed execution framework.

The conceptual relationship is:

```
ATC Standards
      │
      ▼
     GSEPF
      │
      ├── Development Governance
      ├── Security Governance
      ├── Release Governance
      └── Maintenance Governance
                         │
                         ▼
                Maintenance Engine
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
             M0         M1        M2/M3
              │          │          │
              ▼          ▼          ▼
           Automate    Review     Escalate
                         │
                         ▼
                    Evidence
                         │
                         ▼
                  VERIFIED STATE
```

GSEPF MUST NOT weaken the normative requirements of ATC-STD-MAINT-000.

## 27. Relationship to KAI-OS

KAI-OS maintenance MUST respect the architectural boundaries of its constituent systems.

Relevant maintenance domains include:

- ATCLang
- ShivaCore
- A-TownChain
- ATC-VM
- Aurora AI
- GlobusOS
- hardware and firmware interfaces

Maintenance crossing these boundaries MUST evaluate interface and compatibility impact.

Particularly critical boundaries include:

- ShivaCore ↔ GlobusOS
- GlobusOS ↔ Aurora AI
- ATCLang ↔ ATC-VM
- ATC-VM ↔ A-TownChain
- A-TownChain ↔ Node/Network
- Node ↔ Infrastructure

## 28. Maintenance Family

The following standards are assigned to the "ATC-STD-MAINT-*" family:

| ID | Standard |
|---|---|
| ATC-STD-MAINT-000 | Maintenance Governance |
| ATC-STD-MAINT-001 | Maintenance Classification |
| ATC-STD-MAINT-002 | Maintenance Lifecycle |
| ATC-STD-MAINT-003 | Code Maintenance |
| ATC-STD-MAINT-004 | Dependency Maintenance |
| ATC-STD-MAINT-005 | Security Maintenance |
| ATC-STD-MAINT-006 | Infrastructure Maintenance |
| ATC-STD-MAINT-007 | OS Maintenance |
| ATC-STD-MAINT-008 | Blockchain Maintenance |
| ATC-STD-MAINT-009 | VM & Runtime Maintenance |
| ATC-STD-MAINT-010 | AI Maintenance |
| ATC-STD-MAINT-011 | Repository Maintenance |
| ATC-STD-MAINT-012 | Standards Maintenance |
| ATC-STD-MAINT-013 | Documentation Maintenance |
| ATC-STD-MAINT-014 | Performance Maintenance |
| ATC-STD-MAINT-015 | Reliability Maintenance |
| ATC-STD-MAINT-016 | Compatibility Maintenance |
| ATC-STD-MAINT-017 | Upgrade & Migration |
| ATC-STD-MAINT-018 | Rollback & Recovery |
| ATC-STD-MAINT-019 | Maintenance Evidence |
| ATC-STD-MAINT-020 | Maintenance Automation |
| ATC-STD-MAINT-021 | Emergency Maintenance |
| ATC-STD-MAINT-022 | End-of-Life / Retirement |
| ATC-STD-MAINT-023 | Vendor & Supply-Chain Maintenance |
| ATC-STD-MAINT-024 | Cross-Ecosystem Maintenance |

Reserved identifiers MUST NOT be assigned to unrelated standards.

## 29. Minimum Release Requirement

The following rule is normative:

> *A system MUST NOT be released to a lifecycle state requiring operational support unless its
> required maintenance capabilities are implemented, validated, documented, and evidenced.*

At minimum, the release decision MUST consider:

```
Maintenance Owner
       +
Maintenance Documentation
       +
Dependency Inventory
       +
Security Process
       +
Testing
       +
Compatibility
       +
Rollback
       +
Recovery
       +
Monitoring
       +
Evidence
       =
MAINTENANCE READY
```

If a mandatory capability is absent:

```
MAINTENANCE READY = FALSE
RELEASE = BLOCKED
```

## 30. Validation

Conformance validation SHOULD include:

- schema validation
- metadata validation
- lifecycle validation
- dependency validation
- security scanning
- test execution
- compatibility testing
- rollback verification
- evidence validation
- repository governance validation

The validator MUST fail closed for mandatory requirements.

## 31. References

Normative:

- "ATC-STD-000" — Standards Governance & Specification Standard
- applicable "ATC-STD-MAINT-*" specialized standards
- applicable GSEPF specifications
- applicable repository, security, OS, blockchain, AI, and architecture standards

## 32. Changelog

v1.0.0 — Draft — 2026-09-13

- Initial normative Maintenance Governance framework.
- Established "ATC-STD-MAINT-*" as a dedicated standard family.
- Established M0–M3 classification.
- Established Maintenance Lifecycle.
- Established Maintenance Readiness Gate.
- Established Maintenance Capability as a release prerequisite.
- Established Maintenance Evidence requirements.
- Established M2/M3 Separation of Duties.
- Established machine-readable conformance requirements.
- Established GSEPF integration.
- Established KAI-OS cross-layer maintenance requirements.
- Included MAINT-021 through MAINT-024 as committed family members (Emergency, End-of-Life,
  Vendor & Supply-Chain, Cross-Ecosystem).

## Anhang A — REQ-Matrix (machine-identifiable, §4)

| REQ | Anforderung (Quelle) | Pflicht |
|---|---|---|
| REQ-MAINT-000-001 | Specialized Maintenance Standards inherit the governance baseline; MUST NOT weaken a requirement without an explicitly governed exception (§3) | MUST |
| REQ-MAINT-000-002 | Maintenance MUST be treated as a lifecycle capability, not solely post-release (§1, §5.1) | MUST |
| REQ-MAINT-000-003 | A system MUST NOT be released to a lifecycle state requiring operational support unless its required maintenance capabilities are implemented, validated, documented, and evidenced (§7, §29) | MUST |
| REQ-MAINT-000-004 | Required maintenance gates MUST fail closed; missing evidence/validation/approval blocks the release or operation (§5.4) | MUST |
| REQ-MAINT-000-005 | SoD for M2/M3 (Implementer != Validator != Auditor) and for critical release operations (Release Authority != Implementer); exceptions explicitly authorized and evidenced (§5.6) | MUST |
| REQ-MAINT-000-006 | No Evidence, No Trust: completion requires verifiable evidence, not implementation claims (§5.2, §5.3) | MUST |
| REQ-MAINT-000-007 | Every maintenance activity MUST receive an M0-M3 classification (§8) | MUST |
| REQ-MAINT-000-008 | Required lifecycle controls MUST be demonstrably satisfied; a record MUST NOT close before all mandatory acceptance conditions hold (§9, §9.12) | MUST |
| REQ-MAINT-000-009 | M2/M3 controls (independent_validation, security_review, rollback_test, incident_record, audit_evidence) REQUIRED unless documented emergency exception; retrospective review mandatory (§13, §24) | MUST |
| REQ-MAINT-000-010 | Changes crossing architectural boundaries MUST validate affected interfaces; ATC-VM maintenance MUST NOT be treated as an isolated package update (§14, §27) | MUST |
| REQ-MAINT-000-011 | Intentional compatibility breaks MUST be identified, documented, consumer-checked, validated, and rollback-evaluated (§15) | MUST |
| REQ-MAINT-000-012 | A rollback strategy that has never been validated MUST NOT be represented as tested (§17) | MUST |
| REQ-MAINT-000-013 | Automation MUST operate within explicit authorization boundaries, MUST NOT bypass mandatory gates; an AI agent MUST NOT independently authorize human-approval actions (§18, §5.5) | MUST |
| REQ-MAINT-000-014 | The framework MUST support machine-readable validation; schemas use explicit types and reject unknown properties where strict validation is required (§20) | MUST |
| REQ-MAINT-000-015 | A system MUST NOT be declared compliant solely from documentation claims; compliance MUST be evidence-supported (§23) | MUST |
| REQ-MAINT-000-016 | Exceptions MUST identify requirement/reason/system/risk/compensating controls/owner/expiration, be approved, and be recorded as evidence (§24) | MUST |
| REQ-MAINT-000-017 | Family membership per §28 is fixed; reserved identifiers MUST NOT be assigned to unrelated standards (§28) | MUST |
