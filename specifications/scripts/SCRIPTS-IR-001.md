---
artifact:
  id: SCRIPTS-IR-001
  title: "Scripts-KI Semantic Script IR"
  version: "0.1.0"
  status: candidate
  artifact_class: SPEC
  normative: false
  owner: A-TownChain-Okosystems
  proposed_standard_family: SCRIPT
  proposed_standard_id: ATC-STD-SCRIPT-IR-001
  dependencies: [ATC-STD-000, ATC-STD-002, ATC-STD-VERSION-001]
  related: [SCRIPTS-CAP-001, atclang ATC-IR]
---

# SCRIPTS-IR-001 — Semantic Script IR

> Status: CANDIDATE / architecture contract only.
> This artifact is not an approved ATC Standard and does not establish implementation evidence.

## 1. Purpose

Defines the canonical semantic intermediate representation for Scripts-KI.

The IR is the semantic boundary between source representations (natural language, visual scripts and supported programming languages) and verified executable targets. Source syntax and target bytecode are representations of the IR, not substitutes for it.

## 2. Design invariants

1. Deterministic semantics: equal canonical IR inputs produce equal canonical serialization.
2. Explicit authority: every operation requiring authority declares required capabilities.
3. No ambient authority.
4. Versioned evolution with explicit compatibility classification.
5. Fail-closed validation.
6. Target independence.
7. Stable node identity for diagnostics, verification and audit evidence.

## 3. Top-level IR document

A canonical document MUST contain:

- ir_version
- script_id
- module
- metadata
- imports
- types
- constants
- variables
- functions
- events
- capabilities
- resource_limits
- target_constraints
- source_map

Unknown mandatory-domain fields MUST NOT be silently ignored.

## 4. Semantic node model

Expressions:
- Literal
- VariableRef
- BinaryOp
- UnaryOp
- Call
- Index
- FieldAccess
- Cast
- Await, only for explicitly asynchronous targets

Statements/actions:
- Let
- Assign
- Block
- If
- While
- ForEach
- Return
- EmitEvent
- CallAction
- Throw

Domain actions are typed operations resolved through explicit adapters, including World, Character, Quest, Creature, Item, Weapon, Player, Economy, Network and Blockchain operations.

A domain action is invalid unless its adapter, semantic signature and required capability set are known.

## 5. Types

Initial types:
- boolean
- signed/unsigned integers with explicit width
- floating point only where target determinism permits
- string
- bytes
- entity/reference handles
- arrays/lists
- maps
- tuples/records
- option/nullable values
- domain-defined opaque handles

Implicit numeric narrowing MUST be rejected unless an explicit checked conversion exists.

## 6. State

State MUST distinguish immutable constants, local function state, script-instance state, world/game state references and externally owned state.

Externally owned state MUST be accessed through declared interfaces and capabilities.

## 7. Functions and events

Functions declare stable identifier, parameters, return type, effects/capabilities, body and optional resource budget.

Events declare stable identifier, payload schema, producer/consumer contract and ordering requirements where applicable.

## 8. Imports and dependencies

Imports MUST be explicit and canonicalized. Each dependency identifies module, version constraint, exported symbols used and required capabilities.

Circular dependencies are rejected unless a future version explicitly defines a safe cycle model.

## 9. Capability requirements

Each IR document and effectful node MAY declare required capabilities.

Capability identifiers are resolved through SCRIPTS-CAP-001. Unresolved identifiers are validation failures.

The IR records requested authority; it does not grant authority.

## 10. Resource limits

IR MAY declare limits for operation count, recursion/call depth, memory, storage, event emissions, network operations and deterministic execution quanta.

Runtime policy MAY impose stricter limits.

## 11. Canonical serialization

The first normative version MUST define field ordering, identifier encoding, numeric encoding, string/byte encoding, absent-vs-null semantics, map ordering, enum representation and hash/digest domain if hashes are introduced.

A non-canonical serializer MUST NOT be used as consensus evidence.

## 12. Source mapping and diagnostics

Every semantic node SHOULD expose a stable node identifier and MAY contain source spans.

Diagnostics MUST support:
source -> IR node -> verification finding -> target artifact/runtime location

Diagnostics MUST NOT alter execution.

## 13. Validation model

Validation is staged:

1. envelope/schema
2. identifier
3. type
4. dependency resolution
5. control-flow
6. effect/capability
7. resource
8. target constraints

Failure of any mandatory stage rejects the IR.

## 14. Versioning

ir_version follows semantic-versioning semantics:
- MAJOR: incompatible semantic/schema change
- MINOR: backward-compatible semantic addition
- PATCH: clarification or non-semantic correction

Consumers MUST reject unsupported major versions.

## 15. Security boundary

This specification does not authorize filesystem access, process execution, arbitrary native calls, network access, blockchain mutation or kernel/OS operations. Such actions require capabilities and runtime enforcement.

## 16. Implementation status

| Layer | Status |
|---|---|
| IR architecture | DESIGNED |
| Normative approval | NOT APPROVED |
| Schema implementation | NOT IMPLEMENTED |
| Parser | NOT IMPLEMENTED |
| Verifier | NOT IMPLEMENTED |
| Runtime | NOT IMPLEMENTED |
| CI evidence | NOT ESTABLISHED |
| E2E evidence | NOT ESTABLISHED |

## 17. Promotion criteria

Promotion requires owner-approved SCR, registry allocation, normative review, machine-readable schema, reference examples, negative validation cases, conformance tests, compatibility tests and applicable CI evidence.

## Changelog

### 0.1.0 — 2026-09-27
Initial candidate specification for Scripts-KI semantic IR.
