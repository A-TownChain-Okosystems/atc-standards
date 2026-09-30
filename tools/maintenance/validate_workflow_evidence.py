#!/usr/bin/env python3
"""Validate SCR-0129 Workflow/Job evidence and Exact-SHA binding.

The validator is deliberately fail-closed:
- a PR merge ref is never accepted as Exact-SHA evidence for a PR;
- VERIFIED requires tested_sha == expected_sha;
- VERIFIED requires exact_sha=true;
- VERIFIED requires every job PASS with exit_code 0;
- VERIFIED requires every declared gate PASS;
- VERIFIED cannot coexist with RESIDUAL findings.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


MERGE_REF = re.compile(r"^refs/(?:remotes/)?pull/[0-9]+/merge$")


def load_document(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        if path.suffix.lower() in {".yaml", ".yml"}:
            return yaml.safe_load(handle)
        return json.load(handle)


def schema_path() -> Path:
    return Path(__file__).resolve().parents[2] / "schemas" / "maintenance" / "workflow-evidence.schema.json"


def validate_schema(document: dict) -> list[str]:
    schema = json.loads(schema_path().read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return [error.message for error in Draft202012Validator(schema).iter_errors(document)]


def validate_exact_sha(document: dict) -> list[str]:
    evidence = document["workflow_evidence"]
    run = evidence["run"]
    expected = evidence["expected_sha"]
    tested = run["tested_sha"]
    checkout_ref = run["checkout_ref"]
    errors: list[str] = []

    if tested != expected:
        errors.append(f"tested_sha {tested} != expected_sha {expected}")

    if MERGE_REF.fullmatch(checkout_ref):
        errors.append(f"PR merge ref is not Exact-SHA evidence: {checkout_ref}")

    computed_exact = tested == expected and not MERGE_REF.fullmatch(checkout_ref)
    if run["exact_sha"] != computed_exact:
        errors.append(
            f"exact_sha flag mismatch: declared={run['exact_sha']} computed={computed_exact}"
        )

    if evidence.get("pull_request") is not None and MERGE_REF.fullmatch(checkout_ref):
        errors.append("pull_request evidence cannot be VERIFIED from refs/pull/*/merge")

    return errors


def validate_verified(document: dict) -> list[str]:
    evidence = document["workflow_evidence"]
    run = evidence["run"]
    errors: list[str] = []

    if run["evidence_status"] != "VERIFIED":
        return errors

    errors.extend(validate_exact_sha(document))

    for job in evidence["jobs"]:
        if job["result"] != "PASS":
            errors.append(f"VERIFIED requires job PASS: {job['name']}")
        if job["exit_code"] != 0:
            errors.append(f"VERIFIED requires exit_code 0: {job['name']}")

    for gate in evidence.get("required_gates", []):
        if gate["result"] != "PASS":
            errors.append(f"VERIFIED requires gate PASS: {gate['name']}")

    for job in evidence["jobs"]:
        for finding in job.get("findings", []):
            if finding["status"] == "RESIDUAL":
                errors.append(f"VERIFIED cannot contain RESIDUAL finding: {finding['id']}")

    if not run["exact_sha"]:
        errors.append("VERIFIED requires exact_sha=true")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()

    try:
        document = load_document(args.evidence)
        schema_errors = validate_schema(document)
        if schema_errors:
            for error in schema_errors:
                print(f"SCHEMA-FAIL: {error}")
            return 1

        errors = validate_exact_sha(document)
        errors.extend(validate_verified(document))

        if errors:
            for error in errors:
                print(f"EXACT-SHA-FAIL: {error}")
            return 1

        print("WORKFLOW-EVIDENCE PASS")
        return 0
    except Exception as exc:
        print(f"VALIDATOR-ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
