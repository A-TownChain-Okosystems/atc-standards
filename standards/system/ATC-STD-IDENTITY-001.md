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

This contract establishes the ecosystem identity/trust model. It MUST integrate with existing identity standards and MUST NOT create a competing identity namespace or protocol.

## 1. Canonical identity object

Every identity MUST have:

identity_id, identity_type, status, version, owner, credential_bindings, capability_bindings, created_at, updated_at, revocation_state, audit_reference.

Supported identity types include human, account, wallet, device, node, validator, service, agent, model, game, npc, world and organization.

New identity types require governance approval and schema/version registration.

## 2. Existing identity relationship

ATC-STD-IDENTITY-001 is the ecosystem-level identity/trust contract.

It MUST reference rather than duplicate:

- ATC-03 — Decentralized Identity (DID) & Zero-Trust IAM
- ATC-PROTO-IDENTITY-001 — protocol/wire semantics
- independently verified DID/Ed25519/RCT implementation evidence

K6/K6b implementation evidence MUST NOT by itself establish global Identity State ownership.

## 3. Trust chain

    Identity
     → Credential
     → Key Binding
     → Capability
     → Policy
     → Authorization
     → Execution
     → Audit

Identity alone MUST NOT grant authority.

## 4. Credential binding

Credentials MUST be explicitly bound to an identity and define credential ID, credential type, verifier key binding, issuer, validity interval, status, revocation reference and proof/signature metadata.

## 5. Key lifecycle and revocation

    CREATE → BIND → ACTIVATE → ROTATE → REVOKE → RETIRE

Rotation MUST preserve an auditable predecessor/successor relationship where policy requires continuity. Revocation MUST be authoritative, versioned and auditable, and revoked credentials MUST fail authorization after the applicable revocation boundary.

## 6. Capability and policy separation

Capability ≠ Policy ≠ Authorization.

Capabilities express what an identity MAY request; policy determines whether the request is permitted; authorization is the evaluated decision.

## 7. Single SSOT

There MUST be one canonical Identity SSOT. Domain repositories MAY cache, reference or project identity data but MUST NOT create a competing authoritative identity namespace.

The repository, canonical path, schema ID, runtime owner, write authority, API ID, version and evidence location are bound in registry/p0-contract-registry.yaml.

Unresolved ownership MUST remain UNRESOLVED until evidence establishes it.

## 8. Audit and evidence

Identity creation, binding, authorization, rotation, revocation and retirement MUST be auditable.

This contract does not claim implementation, tests, exact-SHA CI or E2E verification.
