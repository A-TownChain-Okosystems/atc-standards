# AGENT_MANIFEST.md

> **Generated-state declaration:** This manifest is a governance pointer, not a second standards registry. The authoritative standards SSOT is `registry/standards.yaml`; implementation status is authoritative in `registry/standard-implementation.yaml`.
>
> **Registry snapshot:** 505 standards · 75 families · current registry/implementation matrix dated 2026-09-14. The manifest MUST be regenerated when the registry changes.

## 1. Normative mandate

The responsible agent MUST comply with all standards applicable to the repository under `ATC-STD-IMPLEMENTATION-001`:

- `MANDATORY`: MUST be implemented and enforced.
- `CONDITIONAL`: MUST be implemented when its applicability condition is true.
- `REFERENCE`: informative unless another normative rule makes it applicable.
- `NOT_APPLICABLE`: requires an explicit recorded justification.

`ATC-STD-000 v1.3.0` is the governance authority and the registry is the source of truth. A copied list of standard IDs in this file MUST NOT override the registry.

## 2. Required machine-readable bindings

Every governed repository MUST expose the applicable governance metadata required by its ATC-STD-201 maturity level, including as applicable:

- `.atc/repository.yaml`
- `.atc/ownership.yaml`
- `.atc/lifecycle.yaml`
- `.atc/compliance.yaml`
- `.github/ai/agent.yaml`
- `AGENTS.md`
- this `AGENT_MANIFEST.md`
- `.github/workflows/` with the applicable governance and product validation gates

The exact requirements are determined by the current standards registry and MUST NOT be inferred from historical documentation.

## 3. Enforcement model

The organization follows:

`DISCOVER → CLASSIFY → DOCUMENT → IMPLEMENT/FIX → TEST → RE-AUDIT → VERIFY → DOCUMENT STATE`

No repository may be declared compliant from a README claim alone. A compliance state requires current evidence from the applicable validator/audit and, where runtime behavior is relevant, executable test evidence.

Agent actions MUST carry the repository's required audit/evidence records and comply with the applicable commit/PR governance rules.

## 4. Conflict handling

Conflicts MUST be recorded as findings and resolved according to the normative hierarchy in `ATC-STD-000`. Historical or archived documents MUST NOT silently override current normative artifacts.

If a generated manifest, README, roadmap, wiki page, registry entry, or implementation disagrees with the SSOT, the inconsistency is a finding until corrected and re-audited.

## 5. Current organization scope

The current GitHub organization inventory contains 31 repositories. Repository membership, classification, maturity, ownership, and implementation state MUST be read from their authoritative current metadata and the standards registry; this manifest intentionally does not duplicate a static per-repository status table.

## 6. Verification

The organization-wide offline auditor is:

`A-TownChain-Okosystems/atc-engineering/scripts/standards_enforcement_audit.py`

It checks the ATC-STD-201 repository baseline, CI/security controls, active placeholders, metadata consistency, agent-manifest synchronization, and exact duplicate content. Its findings are classified by severity, class, category, family, and tags.

The central fleet static audit remains:

`A-TownChain-Okosystems/atc-engineering/scripts/fleet_static_audit.sh`

GitHub Actions runtime evidence is authoritative when available. When Actions is unavailable or incomplete, static/source audit results MUST be marked as such and MUST NOT be represented as successful runtime CI evidence.

## 7. Change control

This file MUST NOT become an alternative registry. Changes to normative standards belong in `registry/standards.yaml` and the corresponding standard artifacts under the ATC standards lifecycle. Changes to generated metadata MUST be reproducible from the SSOT.

## 8. Audit status

As of the 2026-09-16 organization audit cycle, the organization-wide audit remains **IN PROGRESS**. Known open findings include the GlobusOS LKM dependency/API and symbol-resolution issues and the non-canonical Python Groth16 placeholder in `a-townchain`. These remain open until source changes and appropriate verification evidence exist.
