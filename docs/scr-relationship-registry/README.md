# SCR Relationship Registry — Module Contract (Design Draft)

**Module:** SCR Relationship Registry  
**Module ID:** `scr-relationship-registry`  
**Contract version:** `1.0.0-draft.1`  
**Status:** NON-NORMATIVE DESIGN / PARTIALLY IMPLEMENTED  
**Parent work:** PR #120 — SCR-0142  
**Decision:** Independent, versioned module

> This document records an architectural design decision and a proposed technical contract. It does not establish Owner approval, normative relation semantics, SCR allocation, or any SCR lifecycle transition.

## 1. Purpose and responsibility

The SCR Relationship Registry stores explicit relationships between two SCR identities. It is a separate data and validation boundary from the existing SCR identity registry.

Its responsibility is limited to:

- representing directed or non-directed SCR-to-SCR relationships as explicitly typed records;
- binding each relationship to its scope and supporting evidence references;
- validating relationship-record structure and endpoint identity;
- applying graph constraints only where the corresponding relation semantics have been explicitly approved;
- versioning its own data format and migration process.

It does **not** own SCR identity, allocation, metadata reconciliation, Owner authority, approval, normative status, or SCR lifecycle.

## 2. System boundaries and source of truth

| Concern | Authoritative component | Relationship module behavior |
|---|---|---|
| SCR identity and existence | `registry/scr-registry.yaml` | Read-only endpoint lookup |
| Allocation and reservation | SCR identity registry and its governance process | No allocation, reservation, reuse, or number generation |
| SCR lifecycle and decision | SCR identity registry and authorized governance evidence | No lifecycle writes or inferred transitions |
| Source/evidence identity | Existing source-binding model and source verifier | Reference evidence; do not redefine source verification |
| SCR-to-SCR relationship | This module | Sole owner of relationship records and graph-specific validation |
| Normative relation semantics | Applicable Owner/governance decision | Consume only approved semantics; proposals remain non-normative |

The existing `related_sources[]` field remains a source-evidence association attached to an SCR entry. It is **not** a substitute for a graph edge and must not be reinterpreted as one. The new module must not copy or silently migrate `related_sources[]` into SCR-to-SCR edges.

## 3. Proposed repository layout

The following layout is present for the initial v1 schema, manifest, empty registry snapshot, validator and regression suite. Dedicated CI wiring remains a separate gate:

```text
registry/
  scr-relationships/
    v1/
      relationships.yaml
schemas/
  scr-relationships/
    v1/
      relationships.schema.json
tools/
  scr-relationship-validator/
    validate_scr_relationships.py
    tests/
docs/
  scr-relationship-registry/
    README.md
```

The versioned directory is the compatibility boundary. A future incompatible format is introduced under `v2/`; it must not overwrite or reinterpret v1 data in place.

## 4. Data contract — proposed v1 shape

The initial document is proposed to contain:

- `relationship_registry_version`: integer schema version; exactly `1` for this format;
- `repository`: canonical repository identifier;
- `scr_registry_ref`: the ref of the exact SCR identity registry snapshot used for endpoint and evidence resolution;
- `scr_registry_commit`: exact 40-character commit SHA of the SCR identity registry snapshot used for validation;
- `relationships`: explicit relationship records.

Each relationship record is proposed to contain:

| Field | Requirement | Meaning |
|---|---|---|
| `relationship_id` | Required, unique within this document | Stable record identifier; never auto-generated during validation |
| `from_scr` | Required | Source endpoint, format `SCR-NNNN` |
| `to_scr` | Required | Target endpoint, format `SCR-NNNN` |
| `relation_type` | Required | Typed relation token from the separately governed vocabulary |
| `scope` | Required | Bounded explanation of what the relationship asserts |
| `evidence_refs` | Required, non-empty | References to existing immutable source identities supporting the edge |
| `notes` | Optional | Additional non-authoritative context |

Unknown fields must be rejected by the v1 schema (`additionalProperties: false`). Unknown relation tokens must fail closed; validators must not silently coerce them to a generic relationship.

### 4.1 Endpoint rules

- Both endpoints must match the SCR identifier syntax.
- Both endpoints must resolve to entries in the exact SCR registry snapshot selected for validation.
- An unresolved, reserved-only, or otherwise non-canonical endpoint must not be treated as an established SCR merely because its identifier string is syntactically valid. The validator must distinguish syntax from registry resolution and report the precise unresolved condition.
- A relationship record must not create, reserve, allocate, rename, merge, split, close, approve, reject, or supersede an SCR.
- Self-edges are rejected by default for directed relation types unless an approved semantic definition explicitly permits them. The default is a technical safeguard, not a final normative relation rule.

### 4.2 Evidence references

Evidence references must point to immutable source identities already represented by the SCR source-binding model. At minimum, a reference must identify the source using its canonical identity digest and enough registry coordinates to resolve it unambiguously.

The relationship module does not independently assert signer authority. Cryptographic signature verification, trust-root membership, signer authorization, and Owner authority remain separate evidence dimensions and are delegated to their respective controls.

A source reference can establish provenance for a relationship proposal; it cannot by itself establish Owner approval or SCR lifecycle closure.

## 5. Relation vocabulary and graph semantics

The relation vocabulary is **not approved by this design draft**. The following tokens are candidate examples for governance review only:

| Candidate token | Candidate interpretation | Candidate graph constraint |
|---|---|---|
| `DEPENDS_ON` | One SCR depends on another | Potentially acyclic |
| `SUPERSEDES` | One SCR supersedes another | Potentially acyclic |
| `SPLIT_FROM` | One SCR derives from a prior SCR split | Lineage constraint to be defined |
| `MERGED_INTO` | One SCR was consolidated into another | Lineage constraint to be defined |
| `RELATED_TO` | General association | Cycles may be permitted |

No candidate token is enabled merely because it appears in this document. Before implementation, the applicable governance authority must decide:

1. canonical token and definition;
2. edge direction and endpoint interpretation;
3. cardinality constraints, if any;
4. whether self-edges are permitted;
5. whether cycles are permitted;
6. whether the relation is symmetric, asymmetric, or inverse-paired;
7. required evidence and authority threshold;
8. whether historical/backfilled edges are allowed and how they are labelled.

Cycle detection must be relation-specific. The implementation must **not** impose a global DAG rule across all relationship types. Only relation types explicitly approved as acyclic are included in cycle checks. If semantics are unknown or unapproved, the corresponding relation is BLOCKED from normative use; it must not be guessed by the validator.

## 6. Versioning and migration contract

The relationship module has an independent schema version and release lifecycle. It does not inherit the SCR identity registry's `registry_version`.

- v1 schema changes that alter required fields, token meaning, endpoint semantics, evidence interpretation, or validation outcomes are breaking changes and require a new major schema directory.
- Additive optional fields may be considered within a compatible minor contract revision only when the v1 schema explicitly supports them and strict validation remains deterministic.
- Patch revisions may correct documentation or validator defects without changing the accepted data model or semantics.
- Every migration must identify source version, target version, deterministic transformation, preconditions, postconditions, and a reproducible migration report.
- Migration is explicit and reviewable. No automatic in-place rewrite, silent normalization, ID allocation, relationship invention, or lifecycle mutation is permitted.
- The original input and its commit/blob identity must remain recoverable.
- A validator must reject unsupported schema versions rather than attempting best-effort interpretation.
- A v1-to-v2 migration must preserve relationship IDs and evidence references where valid; any dropped or transformed record must be reported with a machine-readable reason and remain subject to review.

## 7. Validator contract

The validator is read-only and fail-closed. Its input set must be explicit:

1. relationship document;
2. relationship schema for the declared version;
3. exact SCR identity registry snapshot;
4. source/evidence identity index or resolver;
5. approved relation-semantics manifest for the validation context.

Minimum validation stages:

- parse safely and reject duplicate YAML keys;
- validate document and record schema;
- reject duplicate relationship IDs;
- validate endpoint syntax and resolve both endpoints against the exact SCR registry snapshot;
- reject missing, ambiguous, or invalid evidence references;
- reject unknown or unapproved relation tokens for any normative validation mode;
- validate relation-specific self-edge, direction, cardinality, inverse and cycle constraints only when approved semantics define them;
- produce deterministic diagnostics with stable error codes and source locations;
- never write back to either registry or modify source files.

A syntactically valid relationship document with unresolved endpoints, missing evidence, or unapproved semantics is not VERIFIED. Unknown conditions are BLOCKED, not silently accepted.

## 8. CI and evidence requirements

The module must have its own focused test suite and CI gate. Integration into broader registry workflows occurs only after the standalone gate is deterministic and independently runnable.

Required evidence for a verified implementation:

- exact tested commit SHA;
- exact schema, validator, test, and fixture paths;
- blob SHA for each relevant source file;
- Actions workflow Run → Job → Step identifiers and relevant log excerpts;
- test totals, including negative and mutation-oriented cases;
- artifact identifier and SHA-256 where an artifact is produced;
- explicit separation of schema conformance, graph-semantic validation, source verification, and governance authorization.

Green CI alone does not establish Owner authority, normative approval, or lifecycle closure.

## 9. Security and governance invariants

The implementation must preserve all of the following:

- read-only access to the SCR identity registry;
- no SCR ID allocation, reuse, reservation, or renumbering;
- no lifecycle, decision, approval, or normative-status mutation;
- no inference of Owner authority from usernames, commit authors, unsigned provenance, or GitHub merge state;
- no promotion of source-evidence associations into graph edges without an explicit relationship record;
- no global cycle rule across semantically different relation types;
- fail-closed behavior for unknown schema versions, relation tokens, endpoints, and evidence identities;
- deterministic validation and migration output.

## 10. Implementation phases and acceptance gates

| Phase | Deliverable | Exit criteria |
|---|---|---|
| A — Contract | This design, reviewed against current registry and validator | Boundaries and versioning model accepted |
| B — Governance semantics | Candidate vocabulary and explicit approval manifest | Candidates remain non-normative; approved list is empty until attributable decision |
| C — Schema | Versioned v1 JSON Schema, empty registry snapshot and regression fixtures | Structural schema and regression tests pass in exact-head CI |
| D — Validator | Standalone read-only validator | Endpoint, evidence, duplicate, and approved graph rules tested |
| E — CI/evidence | Dedicated workflow and reproducible artifacts | Exact-head evidence complete |
| F — Integration | Optional read-only integration into registry consistency gates | No lifecycle coupling; no regression in existing SCR gate |

Phase A is represented by the original contract. Phases B and C now have an initial technical implementation: the v1 schema, a non-normative candidate manifest, an empty v1 relationship snapshot, a read-only validator, and positive/negative regression tests. Phase D is partially represented by the validator implementation but remains subject to exact-head test execution and review. No relation type has been governance-approved; no CI integration, normative approval, or lifecycle transition is claimed.

## 11. Open decisions — explicit blockers

The following decisions remain open and must not be filled by implementation guesswork:

- final relation vocabulary and normative definitions;
- directionality and inverse relation rules;
- per-type cycle and cardinality constraints;
- evidence-reference minimum shape and resolution contract;
- policy for unresolved or reserved SCR endpoints;
- governance authority and approval evidence required to publish an edge;
- version compatibility and deprecation window for future schema versions.

Until these are resolved, E-03 remains **RESIDUAL**. The module contract is a design artifact, not a verified relationship registry.


## 12. Phase B/C implementation addendum — 2026-11-01

### Added technical assets

- `schemas/scr-relationships/v1/relationships.schema.json`: independent JSON Schema Draft 2020-12; strict object fields; version pinned to 1; SCR endpoint syntax; relationship record and evidence-reference structure.
- `registry/scr-relationships/v1/semantics.yaml`: non-normative candidate vocabulary. `approved_relation_types` and `acyclic_relation_types` are intentionally empty. Candidate definitions do not create normative semantics.
- `registry/scr-relationships/v1/relationships.yaml`: empty initial registry snapshot. No historical `related_sources[]` values were converted into graph edges.
- `tools/scr-relationship-validator/validate_scr_relationships.py`: read-only validator with structural and normative modes; duplicate YAML key rejection; endpoint resolution against ASSIGNED SCR entries; evidence identity resolution against existing SCR source bindings; duplicate ID/edge and self-edge checks; relation-specific cycle checks only for explicitly approved acyclic types.
- `tools/scr-relationship-validator/tests/test_validate_scr_relationships.py`: 18 positive and negative regression cases for the initial contract; committed but not yet executed by a dedicated CI step.

### Governance behavior

The semantics manifest is deliberately marked `NON_NORMATIVE`. The candidate tokens are `DEPENDS_ON`, `SUPERSEDES`, `SPLIT_FROM`, `MERGED_INTO`, and `RELATED_TO`. None is approved. Structural mode permits known candidates as proposals; normative mode blocks every candidate until an attributable governance decision is recorded and the approved list is updated through a separately reviewed change. Unknown tokens always fail closed.

The schema's `governance_status` field is record metadata only. It does not represent Owner identity, Owner authority, or SCR lifecycle. A future `GOVERNANCE_APPROVED` semantics manifest must carry a decision ID and evidence references that resolve to immutable source identities. This is traceability, not cryptographic signer or Owner-authority verification; that remains a separate governance control. The validator does not mutate the SCR identity registry.

### Current limitations and remaining gates

- The validator and tests have been committed. Ruff lint and format passed on code head `c2d6f2ab504fff942373fade2d7c766e39f239fa` (Run `41327325133`, Job `124909894165`). The existing SCR Registry Gate passed on the same code head (Run `41327324664`, Job `124909892943`); it did not execute the new relationship validator/tests. The relationship suite remains pending dedicated CI integration. The new relationship validator/test suite has not yet been executed by GitHub Actions; the existing SCR Registry Gate currently executes only the original SCR identity-registry suite.
- The relationship validator is not yet integrated into the existing SCR Registry Gate; that is a separate CI integration phase.
- No populated relationship edge is asserted.
- Relation direction, inverse rules, cardinality, self-edge exceptions, cycle policy and authority thresholds remain governance decisions.
- E-03 remains RESIDUAL until governance decisions, complete validator verification, CI evidence and integration gates are satisfied.
