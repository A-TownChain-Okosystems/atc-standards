---
standard:
  id: ATC-STD-MEMORY-001
  title: "Canonical Federated Memory Contract"
  version: "0.1.0"
  status: draft
  category: system
  normative: false
  applies_to: "Federated memory records and authorized memory runtimes"
---

# ATC-STD-MEMORY-001 — Canonical Federated Memory Contract

**Status:** DRAFT / CONTRACT CANDIDATE

This is the system-level Memory contract. The existing machine-readable MEMORY-001 package MUST remain the single schema/protocol/vector candidate; this document MUST NOT create a competing definition.

## 1. State boundary

    Memory State ≠ Consensus State
    Memory State ≠ World State
    Memory State ≠ AI Authority
    Memory State ≠ Governance Authority

Memory may provide context but MUST NOT acquire authority because an AI agent can read or write a memory record.

## 2. Existing machine-readable package

The current candidate package is registered as:

- protocol: MEMORY-001/1.0.0
- schema root: https://atc.ecosystem/schemas/memory-001/
- path: schemas/memory-001/
- serialization: MEMORY-001-CANONICAL-SERIALIZATION
- verifier: tools/memory_001_reference.py
- schema validation: tools/validate_memory_001.py
- vectors: test-vectors/memory-001/

This is contract evidence only, not runtime implementation evidence. The package and this system contract MUST be reconciled before schema freeze.

## 3. Canonical memory record

The system model requires:

record_id, schema_version, namespace, owner_id, subject_id, content, content_hash, serialization_version, provenance, authorization, created_at, updated_at, retention_policy, revocation_state, record_version, audit_reference.

The machine-readable package MUST define the exact serialized representation and hash input before freeze. A field-model mismatch is a P0 consistency failure.

## 4. Processing pipeline

    Memory Record
     → Canonical Serialization
     → Content Hash
     → Provenance
     → Ownership
     → Authorization
     → Replication
     → Federation Handshake
     → Verification
     → Persistence
     → Audit

A record MUST NOT enter authoritative memory state unless serialization and integrity verification succeed.

## 5. Determinism

Canonical serialization MUST be versioned and deterministic. Equivalent records MUST produce identical bytes.

The exact hash input and signing preimage MUST come from the machine-readable serialization contract. Implementations MUST NOT introduce a second hash/signing rule.

## 6. Provenance and ownership

Provenance MUST survive replication and federation. Ownership does not itself authorize mutation; authorization MUST be evaluated independently.

## 7. Federation

    IDENTITY
     → PROTOCOL VERSION
     → CAPABILITIES
     → AUTHENTICATION
     → AUTHORIZATION
     → MEMORY SCHEMA VERSION
     → SESSION

Unsupported versions MUST fail closed or use an explicit compatibility path.

## 8. Replication and conflicts

Replication MUST define policy, consistency, ordering/causality, duplicate detection, conflict detection, deterministic conflict resolution and failure/retry.

The existing machine-readable replication rules/vectors are the canonical candidate. A second ordering algorithm MUST NOT be introduced here.

## 9. Retention and revocation

Retention MUST be policy-controlled. Revocation MUST be versioned, authenticated and auditable. Revoked records MUST NOT be silently resurrected through replication.

## 10. Authorization boundary

Only an authorized Memory Runtime MAY mutate federated memory state. Aurora and other agents MUST use the canonical Memory API and required capabilities.

Aurora Memory is not automatically the ecosystem Memory Authority. Runtime owner and write authority remain UNRESOLVED until repository/code evidence establishes them.

## 11. Cross-contract binding

Concrete Memory SSOT ownership is registered in registry/p0-contract-registry.yaml.

The registry distinguishes standards SSOT, machine-readable contract package and runtime/evidence repositories.

## 12. Evidence boundary

This contract is specification only. Implementation, tests, exact-SHA CI and E2E require independent evidence.
