# SCR-AURORA-AICP-001 — Aurora AI Compute Platform

**Status:** CHANGE_REQUEST  
**Repository:** `atc-standards`  
**Target:** Canonical AI / Hardware / Security architecture contracts

## Decision Requested

Establish the following canonical concepts for the A-TownChain ecosystem:

- Aurora AI
- Aurora Authority Plane
- Aurora Runtime
- ATC AI Runtime
- ATC Model ABI
- ATC CPU HAL
- ATC GPU HAL
- ATC NPU HAL
- ATC Security HAL
- ATC AI Compute Platform

## Architectural Rules

1. Aurora is the intelligent system and is not part of the ShivaCore TCB.
2. Aurora Runtime is distinct from the ATC AI Runtime.
3. AI services do not receive implicit kernel privileges.
4. NPU, GPU and CPU are compute resources exposed through explicit hardware contracts.
5. NPU is not a trust domain by default.
6. TPM, secure processor and TEE are distinct security capabilities.
7. Secure Boot and Measured Boot are separate from runtime authorization.
8. Hardware architecture is manufacturer- and product-neutral.
9. External platform AI runtimes are not normative dependencies of Aurora, GlobusOS or ShivaCore.
10. Implementation status requires evidence and must not be inferred from architecture text or hardware presence.

## Canonical Execution Contract

```
Aurora Agent
  -> Capability Request
  -> Aurora Authority Plane
  -> ATC Model ABI
  -> Model Verification
  -> ATC AI Runtime
  -> Execution Planner
  -> CPU / GPU / NPU
  -> Verified Execution
  -> Result Validation
  -> Aurora
```

## Evidence Model

```
ARCHITECTURE_ONLY
-> SPECIFIED
-> IMPLEMENTED
-> TESTED
-> CI_VERIFIED
-> INTEGRATED
-> E2E_VERIFIED
```

No status transition is valid without its required evidence.

## Repository Responsibilities

- `atc-standards`: normative contracts, schemas and conformance rules.
- `aurora-ai`: Aurora implementation.
- `a-townchain-os`: GlobusOS integration and AI services.
- `atc-shivacore`: kernel/TCB and HAL/security boundary contracts.
- `globus-os`: active canonical ShivaCore kernel implementation.
- `a-townchain-ecosystem`: master architecture and cross-repository evidence.

## Governance

This is a proposal only. It must follow the repository's canonical SCR/registry/approval process before any proposed contract becomes APPROVED or normative.

**No implementation status is claimed by this SCR.**
