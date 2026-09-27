# MEMORY-001 — Machine-Readable Contract Package

Status: DRAFT / NOT NORMATIVE.

This package is the machine-readable contract candidate for decentralized Memory federation.

Canonical ownership:
- Architecture: a-townchain-ecosystem/ARCHITECTURE.md
- Normative governance: atc-standards
- Runtime implementation: domain repositories (Aurora/GlobusOS)
- Evidence: exact commit SHA + CI/E2E/federation records

Contract package:
- JSON Schemas define wire/data shape.
- serialization.yaml defines canonical bytes, hashing and signing.
- invariants.yaml defines deterministic validation rules.
- determinism.json contains positive/negative vector scaffolding.
- error codes are defined in exchange-message.schema.json.

No file in this package claims implementation, CI verification, E2E verification, or federation verification.

Next gate:
1. validate schemas
2. complete golden canonical-byte/hash/signature vectors
3. add negative authorization/replay/conflict vectors
4. implement independent reference serializers
5. run deterministic cross-implementation tests
6. promote through ATC standards governance
