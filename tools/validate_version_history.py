#!/usr/bin/env python3
"""Fail-closed validation for machine-readable ATC standard version histories."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/version-history.schema.json"
HISTORY_DIR = ROOT / "registry/version-history"
REGISTRY = ROOT / "registry/standards.yaml"


def fail(message: str) -> None:
    print(f"::error::{message}")
    raise SystemExit(1)


def semver_key(version: str):
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?", version)
    if not match:
        fail(f"Invalid semantic version: {version}")
    major, minor, patch, prerelease = match.groups()
    # Stable releases sort above prereleases with the same numeric triplet.
    return (int(major), int(minor), int(patch), 1 if prerelease is None else 0, prerelease or "")


def main() -> None:
    try:
        import jsonschema
    except ImportError:
        fail("jsonschema is required; install the pinned CI dependency")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    )
    files = sorted(HISTORY_DIR.glob("*.json"))
    if not files:
        fail(f"No version-history records found in {HISTORY_DIR.relative_to(ROOT)}")

    registry_text = REGISTRY.read_text(encoding="utf-8")
    for path in files:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")

        errors = sorted(validator.iter_errors(record), key=lambda err: list(err.path))
        if errors:
            first = errors[0]
            fail(f"{path.relative_to(ROOT)}: schema violation at {list(first.path)}: {first.message}")

        versions = [item["version"] for item in record["history"]]
        if len(versions) != len(set(versions)):
            fail(f"{path.relative_to(ROOT)}: duplicate version entries")
        keys = [semver_key(version) for version in versions]
        if keys != sorted(keys, reverse=True):
            fail(f"{path.relative_to(ROOT)}: history must be ordered by descending SemVer precedence")

        canonical = ROOT / record["canonical_source"]
        if not canonical.is_file():
            fail(f"{path.relative_to(ROOT)}: canonical source missing: {record['canonical_source']}")
        canonical_text = canonical.read_text(encoding="utf-8")
        frontmatter_version = re.search(r"(?m)^  version:\s*['\"]?([^'\"\s]+)", canonical_text)
        if not frontmatter_version:
            fail(f"{record['standard_id']}: canonical frontmatter version not found")
        current_version = frontmatter_version.group(1)
        if versions[0] != current_version:
            fail(f"{record['standard_id']}: newest history version {versions[0]} != canonical version {current_version}")

        # Registry SSOT check: require a single registry record with matching id/version.
        registry_rows = [
            line for line in registry_text.splitlines()
            if re.search(r"\bid:\s*" + re.escape(record["standard_id"]) + r"(?:\s*,|\s*})", line)
        ]
        if len(registry_rows) != 1:
            fail(f"{record['standard_id']}: expected exactly one standards.yaml registry row, found {len(registry_rows)}")
        registry_version = re.search(r"\bversion:\s*['\"]?([^,'\"\s}]+)", registry_rows[0])
        if not registry_version or registry_version.group(1) != current_version:
            fail(f"{record['standard_id']}: registry version does not match canonical version {current_version}")

        for entry in record["history"]:
            source_sha = entry["source"]["commit_sha"]
            evidence = entry["evidence"]
            if evidence["status"] == "verified":
                sha = evidence.get("verified_commit_sha")
                run_url = evidence.get("workflow_run_url")
                if not sha or not run_url:
                    fail(f"{record['standard_id']} {entry['version']}: VERIFIED requires exact commit SHA and workflow run URL")
                try:
                    subprocess.run(
                        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                        cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                except subprocess.CalledProcessError:
                    fail(f"{record['standard_id']} {entry['version']}: verified commit {sha} is not present in the checkout")
            if entry["publication_status"] == "published" and source_sha is None:
                print(f"::warning file={path.relative_to(ROOT)}::Published historical entry {entry['version']} has unresolved source commit provenance")
        print(f"Validated {record['standard_id']}: {len(versions)} versions; current={current_version}")

    print(f"PASS: schema, SemVer ordering, canonical version and registry version checked for {len(files)} history file(s).")


if __name__ == "__main__":
    main()
