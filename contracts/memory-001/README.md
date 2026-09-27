# MEMORY-001 — Machine-Readable Contract Package

Status: DRAFT / NOT NORMATIVE.

This package is the machine-readable contract candidate for decentralized Memory federation.

Canonical ownership:
- Architecture: a-townchain-ecosystem/ARCHITECTURE.md
- Normative governance: atc-standards
- Runtime implementation: domain repositories
- Evidence: exact commit SHA plus CI/E2E/federation records

Contract package:
- JSON Schemas define record, identity, authorization, handshake, exchange, evidence, and federation session shape.
- protocol.yaml defines version negotiation, capability negotiation, session state, replay window, and close rules.
- serialization.yaml defines RFC8785 canonical bytes, hashing, identity, and signing.
- replication.yaml defines deterministic conflict ordering.
- invariants.yaml defines contract invariants.
- determinism.json contains golden canonical-byte, SHA-256, and Ed25519 vectors.
- negative.json contains rejection vectors.
- conflict.json contains replication ordering vectors.
- tools/memory_001_reference.py is an independent contract verifier, not a runtime implementation.

No file in this package claims implementation, CI verification, E2E verification, or federation verification.

Next gate:
1. execute schema validation in CI
2. execute the reference verifier against the golden vectors
3. add cross-implementation serializer tests
4. execute rejection and conflict vectors in CI
5. promote through ATC standards governance
6. only then begin runtime implementation
