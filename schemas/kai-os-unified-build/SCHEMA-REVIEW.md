# SCR-0145 Schema Review Notes

**Status:** DRAFT / NOT NORMATIVE.

The current schema proposal enforces:
- SemVer syntax in source-set, target-build and feature-matrix product versions.
- Exact six target IDs.
- Target ID to `x86_64` / `aarch64` architecture consistency.
- Signed artifact reference, signature-verification field and SBOM digest presence in each target manifest.
- Exactly one capability entry per target.
- `NATIVE` / `ADAPTED` require implementation reference and non-empty evidence.
- `LIMITED` requires limitations and non-empty evidence.
- `UNAVAILABLE` / `EXCLUDED` require an explicit rationale.
- `NOT_TESTED` is allowed without implementation evidence and must not be represented as supported.

The validator contains positive fixtures and negative tests for target/architecture mismatch, duplicate/missing target entries and unsupported capability claims.

Schema conformance remains separate from actual product implementation, runtime testing, hardware validation, signature validity and release verification. All six product targets remain NOT VERIFIED until actual artifacts and exact-head evidence exist.
