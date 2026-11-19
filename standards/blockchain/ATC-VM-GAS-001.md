---
standard:
  id: ATC-VM-GAS-001
  title: "ATC-VM Deterministic Gas Schedule"
  version: "1.0.0"
  status: draft
  lifecycle: conformance
  role: "Normative Execution Contract"
  category: blockchain
  authority: A-TownChain-Okosystems
  owner: "Standards Governance"
  normative: true
---

# ATC-VM-GAS-001 — Deterministic Gas Schedule

This standard freezes the baseline opcode gas schedule used by the production ATC-VM.
Changing a value is consensus-visible and requires a governed version change plus
cross-language conformance evidence.

## Canonical schedule

| Opcode | Gas |
|---|---:|
| PUSH | 3 |
| ADD | 5 |
| SUB | 5 |
| MUL | 5 |
| DIV | 10 |
| DUP | 2 |
| SWAP | 2 |
| CALLER | 2 |
| EQ | 3 |
| LT | 3 |
| JUMP | 8 |
| JUMP_IF_NOT_ZERO | 8 |
| JUMP_IF_ZERO | 8 |
| LOAD | 200 |
| STORE | 5000 |
| HALT | 0 |

## Enforcement

1. Every opcode MUST have a defined gas cost.
2. Gas MUST be checked before the opcode effect.
3. Insufficient gas MUST return the OutOfGas error with required and remaining values.
4. An opcode that fails its gas check MUST have no effect.
5. A failed state transition MUST roll back state effects.
6. Gas accounting MUST be deterministic and overflow-safe.
7. Consensus execution MUST use this schedule exactly; local alternative schedules are non-conformant.
8. Exact-SHA CI evidence is required before a schedule implementation can be VERIFIED.

## Conformance vectors

Required tests include:
- exact cost per opcode;
- exact-budget success;
- one-unit-under-budget failure;
- no-effect on failed charge;
- rollback after later runtime failure;
- gas overflow/underflow boundaries;
- deterministic consumed and remaining gas.

Status remains CI_PENDING until the production VM implementation is verified against this contract.
