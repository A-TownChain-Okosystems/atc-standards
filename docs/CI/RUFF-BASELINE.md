# Ruff Baseline — atc-standards

Status: VERIFIED / exact-SHA evidence
Date: 2026-10-03

## Raw baseline before format

Exact source HEAD:
`f870085f04dacd21faebbb88ab722537fef88164`

Run: `37082968604`
Job: `111087287417`

Ruff 0.16.7 reported **210** findings:

| Rule | Count | Classification at raw baseline |
|---|---:|---|
| E701 | 107 | formatting/mechanical debt |
| E702 | 70 | formatting/mechanical debt |
| I001 | 26 | mechanical |
| E401 | 5 | mechanical |
| F401 | 1 | mechanical |
| W292 | 1 | mechanical |
| **Total** | **210** | |

## Format result

Exact formatting implementation commit:
`94e948cce94c6a9e050735e082dbad1c78bede97`

Ruff 0.16.7 was run directly against the seven measured hotspots:

- `tests/test_dependency_guard.py`
- `tools/dependency_guard.py`
- `tools/dependency_sbom.py`
- `tools/gen_views/generate_views.py`
- `tools/osv_fetch.py`
- `tools/osv_snapshot.py`
- `tools/protocol/gen_protocol_registry.py`

The formatter changed all seven files. This was an explicit formatting operation, not Ruff lint `--fix`.

## Post-format gate baseline

Exact current source HEAD:
`bafcde76a6fbcc53dec8387e26b16adc41ff2107`

The centralized Ruff gate run:

Run: `37111889812`
Job: `111171241612`

performed policy TOML syntax validation successfully, then stale detection reported:

`RUFF_OVERRIDE_STALE: base-policy failures contain none of the relaxed rules: E701, E702`

This is exact evidence that **E701/E702 no longer occur in the base-policy Ruff report after formatting**. The temporary centralized override was therefore removed rather than retained.

The remaining current lint debt is the mechanical set:

- I001: 26
- E401: 5
- F401: 1
- W292: 1
- **Total: 32**

Thus the two numbers have distinct meanings:

- **210** = historical raw pre-format baseline
- **32** = current post-format base-policy baseline

The former 177 E701/E702 findings were eliminated by formatting; they are not suppressed policy debt.

## Format baseline evidence

Independent exact-head format baseline before the formatting commit:

Run: `37083386248`
Job: `111088534247`

Result: **FAIL — 7 files would be reformatted; 868 already formatted.**

After commit `94e948cce94c6a9e050735e082dbad1c78bede97`, those seven files are the measured formatting scope.

## Policy-bundle contract

The central reusable Ruff workflow now validates all policy TOML with Python 3.11 `tomllib`
before loading configuration or evaluating overrides. Malformed policy is classified as
`POLICY-BUNDLE-SYNTAX`, not as caller-code Ruff debt.

The C-1 override mechanism remains available for future temporary exceptions, including
fail-closed allowlist, stale detection, and sunset enforcement. No atc-standards override
is currently active.

## Fix order

1. verify the post-format generator/registry determinism;
2. remove I001/E401/F401/W292 mechanically;
3. rerun the complete gate;
4. keep the central override registry empty for atc-standards unless a new, evidenced exception is required.
