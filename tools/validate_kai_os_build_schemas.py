#!/usr/bin/env python3
"""Validate the SCR-0145 draft schemas and six-target contract.

This is proposal validation, not a normative release verifier.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas" / "kai-os-unified-build"
TARGETS = {
    "native-x86_64",
    "native-aarch64",
    "linux-x86_64",
    "linux-aarch64",
    "windows-x86_64",
    "windows-aarch64",
}
SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
SHA = "a" * 64
COMMIT = "b" * 40


def load_schema(name: str) -> dict:
    path = SCHEMAS / name
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    print(f"PASS Draft 2020-12 schema: {path.relative_to(ROOT)}")
    return schema


def main() -> int:
    source_schema = load_schema("unified-source-set.schema.json")
    target_schema = load_schema("target-build-manifest.schema.json")
    matrix_schema = load_schema("feature-capability-matrix.schema.json")

    source_targets = set(target_schema["properties"]["build_target"]["enum"])
    matrix_targets = set(matrix_schema["properties"]["targets"]["items"]["enum"])
    capability_targets = set(
        matrix_schema["properties"]["features"]["items"]["properties"]["capabilities"]["items"]["properties"]["target"]["enum"]
    )
    for name, actual in (
        ("target manifest", source_targets),
        ("matrix targets", matrix_targets),
        ("per-feature capabilities", capability_targets),
    ):
        if actual != TARGETS:
            raise AssertionError(f"{name}: expected {sorted(TARGETS)}, got {sorted(actual)}")

    version = "1.2.3"
    if not SEMVER.fullmatch(version):
        raise AssertionError("internal SemVer fixture invalid")

    source_instance = {
        "schema_version": "0.1.0",
        "product": "KAI-OS",
        "product_version": version,
        "source_set_id": "KAI-OS-SOURCE-1.2.3",
        "captured_at_utc": "2026-11-25T00:00:00Z",
        "repositories": [{
            "repository_full_name": "A-TownChain-Okosystems/globus-os",
            "commit_sha": COMMIT,
            "components": ["GlobusOS", "ShivaCore"],
        }],
        "source_set_sha256": SHA,
    }
    Draft202012Validator(source_schema).validate(source_instance)
    print("PASS Unified Source Set fixture")

    for target in sorted(TARGETS):
        architecture = "aarch64" if target.endswith("aarch64") else "x86_64"
        manifest = {
            "schema_version": "0.1.0",
            "product": "KAI-OS",
            "product_version": version,
            "release_id": "KAI-OS-1.2.3",
            "source_set_id": "KAI-OS-SOURCE-1.2.3",
            "source_set_sha256": SHA,
            "build_id": f"fixture-{target}",
            "build_target": target,
            "architecture": architecture,
            "toolchain": {
                "builder_id": "fixture-builder",
                "compiler": "fixture-compiler",
                "linker": "fixture-linker",
                "runner_os": "fixture-runner",
            },
            "dependency_lock_sha256": SHA,
            "tests": [{
                "test_level": "unit",
                "status": "PASS",
                "source_commit": COMMIT,
                "evidence_uri": "https://example.invalid/evidence",
            }],
            "artifact": {
                "filename": f"{target}.bin",
                "size_bytes": 1,
                "sha256": SHA,
                "media_type": "application/octet-stream",
            },
            "provenance": {
                "attestation_ref": "fixture-attestation",
                "attestation_sha256": SHA,
                "verified": True,
            },
        }
        Draft202012Validator(target_schema).validate(manifest)
        wrong = dict(manifest)
        wrong["architecture"] = "x86_64" if architecture == "aarch64" else "aarch64"
        errors = list(Draft202012Validator(target_schema).iter_errors(wrong))
        if not errors:
            raise AssertionError(f"{target}: architecture mismatch was accepted")
    print("PASS six target manifests and architecture binding")

    capabilities = [
        {"target": target, "status": "NOT_TESTED", "evidence": []}
        for target in sorted(TARGETS)
    ]
    matrix_instance = {
        "schema_version": "0.1.1",
        "product_version": version,
        "targets": sorted(TARGETS),
        "features": [{
            "feature_id": "KAI-TEST-001",
            "description": "Schema conformance fixture",
            "capabilities": capabilities,
        }],
    }
    Draft202012Validator(matrix_schema).validate(matrix_instance)
    observed = [item["target"] for item in capabilities]
    if len(observed) != 6 or set(observed) != TARGETS:
        raise AssertionError("each feature must define exactly one capability per target")
    print("PASS feature capability matrix: exactly six distinct targets")
    print("RESULT: SCR-0145 draft schema checks PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
