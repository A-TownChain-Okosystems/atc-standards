# KAI-OS Unified Build Schemas — SCR-0145 Draft

These files are proposal artifacts, not normative schemas. They become normative only after SCR-0145 and the related ATC-ARCH-001 amendment are approved and the standard ID is allocated in the registry.

## Files

- `unified-source-set.schema.json`: pins every participating repository commit, submodule gitlink and dependency-lock digest.
- `target-build-manifest.schema.json`: binds one build execution and artifact to the source set, target, toolchain, tests, signature, SBOM and provenance.
- `feature-capability-matrix.schema.json`: records capability status and evidence for each of the six mandatory targets.

## Six target IDs

- `native-x86_64`
- `native-aarch64`
- `linux-x86_64`
- `linux-aarch64`
- `windows-x86_64`
- `windows-aarch64`

The canonical architecture labels are `x86_64` and `aarch64`. The human-readable term ARM64 maps to `aarch64`.

## Digest rules proposed for review

1. Repository commit references use full Git object IDs (40- or 64-hex).
2. Dependency lock digests and artifact digests use lowercase SHA-256 hex.
3. The Unified Source Set digest is SHA-256 over RFC 8785 JSON Canonicalization Scheme bytes for the source-set object with `source_set_sha256` omitted. Repository entries are sorted by `repository_full_name`; submodules by `path`; dependency locks by `path`.
4. Artifact SHA-256 is computed over the exact final artifact bytes after signing and packaging. The manifest is generated only after the artifact digest is known.
5. A build ID is unique per target execution; it is not a substitute for product version or source-set identity.

## Capability status

`NATIVE`, `ADAPTED`, `LIMITED`, `UNAVAILABLE`, `NOT_TESTED`, `EXCLUDED`.

Each feature must have exactly one capability entry per target. The capability schema requires exactly one entry for each of the six target IDs. NATIVE/ADAPTED require an implementation reference and evidence; LIMITED requires limitations and evidence; UNAVAILABLE/EXCLUDED require a rationale. The validator tests duplicate/missing target rejection, unsupported capability claims and target/architecture mismatch. `NOT_TESTED` is never equivalent to supported.

## Validation

Run locally from the repository root:

```bash
python -m pip install jsonschema
python tools/validate_kai_os_build_schemas.py
```

The existing canonical workflow `.github/workflows/test-suite.yml` runs the same validator as part of ATC Test Suite (Tools-Smoke); no parallel schema-only workflow is introduced. Passing schema validation proves only schema conformance; it does not prove any build target, runtime, installer, hardware profile or product feature is implemented or verified.

## Governance

Track changes in [SCR-0145](../../change-requests/SCR-0145.md). Do not add the candidate standard ID to the registry or claim normative status until the SCR review chain and registry allocation are complete.
