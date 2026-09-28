---
standard:
  id: ATC-STD-IDENTITY-001
  title: "Canonical Identity and Trust Contract"
  version: "0.1.0"
  status: draft
  category: system
  normative: false
  applies_to: "All identity-bearing ATC actors and services"
---

# ATC-STD-IDENTITY-001 — Canonical Identity & Trust Contract

**Status:** DRAFT / CONTRACT CANDIDATE  
**Purpose:** Establish one canonical identity/trust model for MASTER-ARCH-001.

## 1. Canonical identity object

Every identity MUST have:

identity_id, identity_type, status, version, owner, credential_bindings, capability_bindings, created_at, updated_at, revocation_state and audit_reference.

Supported identity types include human, account, wallet, device, node, validator, service, agent, model, game, npc, world and organization.

New identity types require governance approval and schema/version registration.

## 2. Trust chain

    Identity
     → Credential
     → Key Binding
     → Capability
     → Policy
     → Authorization
     → Execution
     → Audit

Identity alone MUST NOT grant authority.

## 3. Credential binding

Credentials MUST be explicitly bound to an identity and MUST define credential_id, credential_type, verifier key binding, issuer, validity interval, status, revocation reference and proof/signature metadata.

## 4. Key lifecycle

The canonical lifecycle is:

    CREATE → BIND → ACTIVATE → ROTATE → REVOKE → RETIRE

Rotation MUST preserve an auditable relationship between predecessor and successor credentials where policy requires continuity.

## 5. Revocation

Revocation MUST be authoritative, versioned and auditable. A revoked credential MUST fail authorization after the applicable revocation boundary.

## 6. Capability and policy separation

Capabilities express what an identity MAY request. Policies determine whether the request is permitted in context. Authorization is the evaluated decision.

    Capability ≠ Policy ≠ Authorization

## 7. Single-SSOT rule

There MUST be one canonical Identity SSOT for the ecosystem. Domain repositories MAY cache, reference or project identity data, but MUST NOT create a competing authoritative identity namespace.

## 8. Audit requirements

Identity lifecycle operations MUST produce auditable evidence for creation, binding, authorization, rotation, revocation and retirement.

## 9. Evidence boundary

This contract does not claim that an identity implementation exists. Implementation, tests, exact-SHA CI and E2E require separate evidence.
