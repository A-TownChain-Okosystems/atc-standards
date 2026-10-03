# Ruff Baseline — atc-standards

Status: VERIFIED / exact-SHA evidence
Date: 2026-10-03

## Raw baseline without centralized override

Exact source HEAD:
`f870085f04dacd21faebbb88ab722537fef88164`

Run: `37082968604`
Job: `111087287417`

Ruff 0.16.7 reported **210** findings:

| Rule | Count | Classification |
|---|---:|---|
| E701 | 107 | temporary policy override |
| E702 | 70 | temporary policy override |
| I001 | 26 | mechanical |
| E401 | 5 | mechanical |
| F401 | 1 | mechanical |
| W292 | 1 | mechanical |
| **Total** | **210** | |

The 177 E701/E702 findings are not fixed by the centralized exception.

## Gate baseline with centralized override

Exact source HEAD:
`80c241dbc53f158e3c608d4b56a7ca0ed24313db`

Run: `37083613526`
Job: `111089221333`

The central policy bundle accepted the override after TOML parsing, allowlist validation, and stale detection. The Ruff lint step then reported **32 active findings**:

- I001: 26
- E401: 5
- F401: 1
- W292: 1

The Ruff job failed with exit code 1. Format was skipped because lint failed.

Therefore:

- **210 = raw baseline under the base policy**
- **32 = active gate baseline with E701/E702 override**
- **177 = suppressed by temporary override, not remediated**

## Format baseline

Independent exact-head format baseline:

Run: `37083386248`
Job: `111088534247`

Result: **FAIL — 7 files would be reformatted; 868 already formatted.**

Affected files:

- `tests/test_dependency_guard.py`
- `tools/dependency_guard.py`
- `tools/dependency_sbom.py`
- `tools/gen_views/generate_views.py`
- `tools/osv_fetch.py`
- `tools/osv_snapshot.py`
- `tools/protocol/gen_protocol_registry.py`

The generator source is deliberately included in the mechanical format cycle before the next registry regeneration.

## Policy-bundle contract

The centralized policy now validates all TOML syntax with Python 3.11 `tomllib` before override evaluation. Malformed policy is classified as `POLICY-BUNDLE-SYNTAX`, not as caller-code Ruff debt.

The temporary E701/E702 override has:

- sunset: 2027-03-31
- tracking issue: A-TownChain-Okosystems/.github#25

## Fix order

1. format the 7 measured files;
2. regenerate and verify the protocol registry deterministically;
3. remove mechanical I001/E401/F401/W292 findings;
4. treat E701/E702 as a separate refactoring cycle;
5. remove the centralized override after remediation and before the sunset date.
