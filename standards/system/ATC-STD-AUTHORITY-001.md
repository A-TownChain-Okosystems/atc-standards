---
standard:
  id: ATC-STD-AUTHORITY-001
  title: "System Authority and Write Boundary Contract"
  version: "0.1.0"
  status: draft
  category: system
  normative: false
  applies_to: "All A-TownChain system domains"
---

# ATC-STD-AUTHORITY-001 — System Authority & Write Boundary Contract

**Status:** DRAFT / CONTRACT CANDIDATE

This contract defines authority boundaries without inventing unresolved ownership. It does not assert implementation or CI/E2E verification.

## 1. Mandatory authority record

Every authoritative state domain MUST define:

domain_id, owner_id, source_of_truth, read_authorities, write_authority, direct_mutation_policy, required_capabilities, policy_id, approval_policy, audit_policy, api_id, state_id, version.

Concrete cross-repository bindings are maintained in registry/p0-contract-registry.yaml. Unknown ownership MUST remain explicitly UNRESOLVED until repository/code evidence establishes it.

## 2. Canonical authorization path

    Actor
     → Identity
     → Credential
     → Capability
     → Policy
     → Authorization
     → Domain API
     → Domain Authority
     → State Mutation
     → Audit Evidence

A caller MUST NOT mutate authoritative state by bypassing the canonical Domain API and authorization path.

## 3. Domain authority registry

| domain_id | owner_id | write_authority | direct_mutation | resolution |
|---|---|---|---|---|
| consensus_state | a-townchain | consensus/state-transition authority | DENY | repository identified; runtime/API evidence required |
| vm_state | atc-vm | VM runtime | DENY | repository identified; runtime/API evidence required |
| node_state | atc-node | node runtime | DENY | repository identified; runtime/API evidence required |
| identity_state | UNRESOLVED:IDENTITY-STATE-OWNER | UNRESOLVED:IDENTITY-WRITE-AUTHORITY | DENY | P0 unresolved |
| os_state | globus-os | OS-authorized services/kernel boundary | DENY | exact write authority evidence required |
| kernel_state | atc-shivacore | kernel | DENY | integrated source ownership evidence required |
| ai_state | aurora-ai | Aurora runtime | ALLOW within Aurora authority | Aurora-owned domain state only |
| memory_state | UNRESOLVED:MEMORY-STATE-OWNER | UNRESOLVED:MEMORY-WRITE-AUTHORITY | DENY | P0 unresolved |
| world_state | genesis-engine | Genesis runtime | DENY | repository identified; runtime/API evidence required |
| player_state | UNRESOLVED:PLAYER-STATE-OWNER | UNRESOLVED:PLAYER-WRITE-AUTHORITY | DENY | unresolved |
| lore_state | UNRESOLVED:LORE-STATE-OWNER | UNRESOLVED:LORE-WRITE-AUTHORITY | DENY | unresolved |
| economy_state | UNRESOLVED:ECONOMY-STATE-OWNER | UNRESOLVED:ECONOMY-WRITE-AUTHORITY | DENY | unresolved |

These entries are architecture contracts, not implementation evidence.

## 4. Governance authority versus domain authority

The existing governance/authority/authority-matrix.yaml is the governance decision-rights SSOT. It MUST NOT be interpreted as proof that a domain runtime owns state.

Governance Authority ≠ Domain Write Authority ≠ Capability ≠ Policy ≠ Authorization.

## 5. Aurora boundary

Aurora MAY READ, QUERY, PLAN and PROPOSE. Aurora MAY EXECUTE only after capability and policy authorization.

Aurora MUST NOT directly mutate consensus, VM, Genesis, OS, kernel, governance or federated-memory state.

## 6. Enforcement

Unauthorized direct mutation MUST fail closed and produce auditable evidence containing actor, identity, capability, policy, target domain, operation, decision and result.

## 7. Evidence boundary

PRESENT, SPECIFIED, IMPLEMENTED, TESTED, CI-VERIFIED and E2E-VERIFIED are independent states. Documentation alone MUST NOT advance a domain beyond PRESENT/SPECIFIED.
