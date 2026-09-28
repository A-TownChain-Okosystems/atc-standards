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
**Purpose:** Define the machine-readable authority boundary required by MASTER-ARCH-001.

This document is a contract candidate. It does not assert implementation or CI/E2E verification.

## 1. Mandatory authority record

Every authoritative state domain MUST have a record containing:

| Field | Required |
|---|---|
| domain_id | MUST |
| owner_id | MUST |
| source_of_truth | MUST |
| read_authorities | MUST |
| write_authority | MUST |
| direct_mutation_policy | MUST |
| required_capabilities | MUST |
| policy_id | MUST |
| approval_policy | MUST |
| audit_policy | MUST |
| api_id | MUST |
| state_id | MUST |
| version | MUST |

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

A caller MUST NOT mutate authoritative state by bypassing the canonical Domain API and its authorization path.

## 3. Initial domain authority registry

| domain_id | owner_id | write_authority | direct_mutation | Aurora |
|---|---|---|---|---|
| consensus_state | a-townchain | consensus/state-transition authority | DENY | query/propose/authorized transaction |
| vm_state | atc-vm | VM runtime | DENY | query/authorized execution |
| node_state | atc-node | node runtime | DENY | policy-gated node API |
| identity_state | identity | identity authority | DENY | authorized identity API |
| os_state | globus-os | OS-authorized services/kernel boundary | DENY | policy-gated OS API |
| kernel_state | shivacore | kernel | DENY | no direct mutation |
| ai_state | aurora-ai | Aurora runtime | ALLOW within Aurora authority | Aurora-owned |
| memory_state | memory | authorized memory runtime | DENY | capability/policy-gated |
| world_state | genesis-engine | Genesis runtime | DENY | Genesis API only |
| player_state | genesis/application | authorized game runtime | DENY | Genesis API only |
| lore_state | lore | canonical lore authority | DENY | read/propose via validated API |
| economy_state | economic domain | domain economic authority | DENY | policy/capability-gated |

This registry is an architecture contract, not evidence that each authority is already implemented.

## 4. Aurora boundary

Aurora MAY READ, QUERY, PLAN and PROPOSE. Aurora MAY EXECUTE only after capability and policy authorization.

Aurora MUST NOT directly mutate consensus, VM, Genesis, OS, kernel, governance or federated-memory state.

## 5. Enforcement requirements

The reference implementation MUST make unauthorized direct mutation fail closed and produce auditable evidence containing at least actor, identity, capability, policy, target domain, operation, decision and result.

## 6. Evidence boundary

PRESENT, SPECIFIED, IMPLEMENTED, TESTED, CI-VERIFIED and E2E-VERIFIED are independent states. Documentation alone MUST NOT advance a domain beyond PRESENT/SPECIFIED.
