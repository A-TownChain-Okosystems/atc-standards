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
**Purpose:** Define deterministic, authorized and auditable memory federation without making memory an authority plane.

## 1. State boundary

    Memory State ≠ Consensus State
    Memory State ≠ World State
    Memory State ≠ AI Authority
    Memory State ≠ Governance Authority

Memory may provide context. It MUST NOT acquire authority merely because an AI agent can read or write a memory record.

## 2. Canonical memory record

Every record MUST define:

record_id, schema_version, namespace, owner_id, subject_id, content, content_hash, serialization_version, provenance, authorization, created_at, updated_at, retention_policy, revocation_state, record_version and audit_reference.

## 3. Canonical processing pipeline

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

A record MUST NOT be accepted into authoritative memory state unless serialization and integrity verification succeed.

## 4. Deterministic serialization

The canonical serialization algorithm MUST be versioned and deterministic. Equivalent records MUST serialize to identical bytes before hashing.

The content hash MUST be computed over the canonical serialized representation, excluding fields explicitly designated as non-canonical metadata by the schema.

## 5. Provenance and ownership

Every record MUST identify its provenance and owner. Provenance MUST be preserved across replication and federation.

Ownership does not by itself authorize mutation. Authorization MUST be evaluated independently.

## 6. Federation handshake

A federation peer MUST establish:

    IDENTITY
     → PROTOCOL VERSION
     → CAPABILITIES
     → AUTHENTICATION
     → AUTHORIZATION
     → MEMORY SCHEMA VERSION
     → SESSION

Unsupported schema versions MUST fail closed or enter an explicitly defined compatibility path.

## 7. Replication and conflict resolution

Replication MUST define replication policy, consistency model, ordering/causality, duplicate detection, conflict detection, deterministic conflict resolution and failure/retry behavior.

No conflict-resolution rule may silently overwrite a record without auditable provenance.

## 8. Retention and revocation

Retention MUST be policy-controlled. Revocation MUST be versioned, authenticated and auditable. A revoked record MUST NOT be silently resurrected through replication.

## 9. Authorization boundary

Only an authorized Memory Runtime MAY mutate federated memory state. Aurora or another agent MUST use the canonical Memory API and required capabilities.

## 10. Evidence boundary

This contract establishes specification only. Implementation, tests, exact-SHA CI and E2E require independent evidence.
