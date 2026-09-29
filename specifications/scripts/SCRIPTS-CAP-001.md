---
artifact:
  id: SCRIPTS-CAP-001
  title: "Scripts-KI Capability and Authorization Model"
  version: "0.1.0"
  status: candidate
  artifact_class: SPEC
  normative: false
  owner: A-TownChain-Okosystems
  proposed_standard_family: SCRIPT
  proposed_standard_id: ATC-STD-SCRIPT-CAP-001
  dependencies: [ATC-STD-000, ATC-STD-002, ATC-AI-GOV-CAPABILITY-001]
  related: [SCRIPTS-IR-001, atc-shivacore capability model, globus-os IPC/security boundaries]
---

# SCRIPTS-CAP-001 — Capability and Authorization Model

> Status: CANDIDATE / architecture contract only.
> This artifact is not an approved ATC Standard and does not establish implementation evidence.

## 1. Purpose

Defines the authority model used by Scripts-KI-generated and authored scripts.

It complements, but does not replace, ATC-AI-GOV-CAPABILITY-001.

Agent capability answers what an AI agent may do in the engineering system.
Script capability answers what an executing script may request from a game, runtime, service, blockchain or OS boundary.

Neither class is inherited implicitly from the other.

## 2. Security invariants

1. Default deny.
2. No ambient authority.
3. Least privilege.
4. Explicit scope.
5. READ/WRITE/EXECUTE separation.
6. Fail closed for malformed, expired or unknown grants.
7. Capability decisions are auditable.
8. Delegation is explicit.
9. Declaration alone is never runtime enforcement evidence.

## 3. Capability identity

Candidate identifier form:

domain.resource.operation

Examples:
- world.read
- world.write
- player.read
- player.write
- inventory.read
- inventory.write
- network.connect
- blockchain.read
- blockchain.write
- filesystem.read
- filesystem.write
- system.execute

These IDs remain candidates until normative allocation and registry approval.

## 4. Permission classes

| Class | Meaning |
|---|---|
| READ | observe/query |
| WRITE | mutate authorized state |
| EXECUTE | invoke an executable operation |
| DELEGATE | grant a subset of authority |
| ADMIN | modify policy/capability configuration |

DELEGATE and ADMIN MUST NOT be inferred from other classes.

## 5. Scope

Every runtime grant MUST define scope.

Possible dimensions:
- script/module
- actor/entity
- player/session
- world/scene
- resource
- namespace
- network destination
- blockchain contract/address
- time/epoch
- execution environment

Unrestricted wildcard scope is high risk and requires explicit approval.

## 6. Capability grant

A grant conceptually contains:
- capability_id
- effect (allow/deny)
- scope
- issuer
- subject
- validity
- resource_limits
- delegation_policy
- approval_reference
- policy_version

Conflicting rules default to deny unless a future normative policy defines deterministic precedence.

## 7. Resource limits

Limits SHOULD cover maximum calls, bytes, entities affected, storage mutation, network requests, compute budget, execution quanta and value transfer where relevant.

Exceeding a limit MUST deny or terminate in a controlled manner.

## 8. Approval and delegation

High-risk capabilities SHOULD require an explicit approval record.

Initial high-risk examples:
- system.execute
- unrestricted filesystem writes
- unrestricted network access
- blockchain writes
- economy/asset mutation
- capability delegation
- policy administration

Delegation MUST satisfy:
delegated scope is a subset of issuer scope
and
delegated capabilities are a subset of issuer capabilities

Scripts MUST NOT self-escalate.

## 9. Sandbox boundary

Execution follows:

Script -> Policy -> Capability Check -> Sandbox/Adapter -> Host Resource

Direct host access from script semantics is prohibited.

The boundary MUST be independently enforceable from AI-generated text.

## 10. ShivaCore / Globus OS mapping

Mapping is adapter-based.

| Script capability | Platform boundary |
|---|---|
| world.* | game/world service |
| player.* | player/session service |
| inventory.* | item/inventory service |
| network.* | network policy/service |
| filesystem.* | sandboxed storage service |
| blockchain.* | L1/contract adapter |
| system.execute | privileged OS service boundary |

Scripts-KI MUST NOT directly depend on kernel internals.

ShivaCore/Globus OS remains the authority boundary; adapters expose only explicitly granted capabilities.

## 11. Audit events

Capability decisions SHOULD emit structured events containing script/module identity, capability ID, requested operation, scope, decision, policy version, approval reference, resource usage and denial reason.

Security-sensitive audit storage follows the applicable platform audit standard.

## 12. Lifecycle

DECLARE -> RESOLVE -> APPROVE (if required) -> GRANT -> CHECK -> USE -> AUDIT -> REVOKE/EXPIRE

Unknown capabilities fail at RESOLVE.
Expired or revoked grants fail at CHECK.

## 13. IR integration

SCRIPTS-IR-001 records requested capabilities but never grants them.

The verifier MUST establish that every effectful IR node has a resolvable capability requirement.

The runtime MUST enforce the effective grant independently.

Therefore:

REQUESTED != AUTHORIZED != ENFORCED

A declaration alone is never evidence of authorization or enforcement.

## 14. Threat model

The model covers prompt-generated privilege escalation, confused deputy attacks, capability laundering through adapters, wildcard abuse, stale grants, approval replay, cross-world/resource access, unauthorized blockchain/economy mutation, sandbox escape and agent/script capability confusion.

## 15. Implementation status

| Layer | Status |
|---|---|
| Capability architecture | DESIGNED |
| Normative approval | NOT APPROVED |
| Schema | NOT IMPLEMENTED |
| Policy evaluator | NOT IMPLEMENTED |
| Runtime enforcement | NOT IMPLEMENTED |
| Sandbox integration | NOT IMPLEMENTED |
| Audit implementation | NOT IMPLEMENTED |
| CI evidence | NOT ESTABLISHED |
| E2E evidence | NOT ESTABLISHED |

## 16. Promotion criteria

Promotion requires owner-approved SCR, registry allocation, security review, machine-readable schema, positive and negative authorization vectors, scope/delegation tests, fail-closed tests, platform mapping review and applicable CI/security evidence.

## Changelog

### 0.1.0 — 2026-09-27
Initial candidate specification for Scripts-KI capability and authorization semantics.
