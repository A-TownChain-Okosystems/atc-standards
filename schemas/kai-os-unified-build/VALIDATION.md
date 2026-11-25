# SCR-0145 Schema Validation Record

**Current proposal status:** DRAFT / NOT NORMATIVE.
**Validator:** `tools/validate_kai_os_build_schemas.py`.
**Canonical CI:** `.github/workflows/test-suite.yml` → `KAI-OS Unified Build Schema Validation (SCR-0145)`.

## Required checks

- JSON parsing for all three Draft 2020-12 schemas.
- Draft 2020-12 metaschema validation.
- Exact six target IDs in target and capability schemas.
- Unified Source Set sample validation.
- Six per-target build-manifest samples.
- Architecture/target mismatch rejection.
- Feature capability matrix with exactly one entry per target.
- Duplicate/missing capability target rejection.

## Evidence

- Run `45653650987` completed SUCCESS on earlier PR head `455c2e83e4c25488915888523af811c9e84e1224`; the schema validator step completed SUCCESS.
- Subsequent schema hardening added SemVer patterns, target/architecture binding and Draft 2020-12 `contains` cardinality constraints for each target. Those changes require a fresh run on the latest PR head.
- Do not transfer the earlier run's success to later commits.
- Latest-head verification remains PENDING until a new exact-head CI run completes.
