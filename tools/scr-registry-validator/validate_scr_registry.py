#!/usr/bin/env python3
"""Fail-closed validator for the machine-readable SCR identity registry."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
ID_RE = re.compile(r"^SCR-(\d{4})$")
FILE_RE = re.compile(r"^SCR-(\d{4})(?:[-.]|$)")


def validate(
    root: Path = ROOT, registry_path: Path | None = None, schema_path: Path | None = None
) -> list[str]:
    registry_path = registry_path or root / "registry" / "scr-registry.yaml"
    schema_path = schema_path or root / "schemas" / "scr-registry.schema.json"
    try:
        data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"cannot load registry/schema: {exc}"]

    if not isinstance(data, dict):
        return ["registry root must be an object"]

    errors = [
        f"schema: {error.message} at {list(error.absolute_path)}"
        for error in Draft202012Validator(schema).iter_errors(data)
    ]
    raw_entries = data.get("entries", [])
    entries = raw_entries if isinstance(raw_entries, list) else []
    ids = [
        str(entry["id"])
        for entry in entries
        if isinstance(entry, dict) and entry.get("id") is not None
    ]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        errors.append("duplicate SCR IDs: " + ", ".join(duplicates))

    covered: set[int] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        match = ID_RE.fullmatch(str(entry.get("id", "")))
        if not match:
            continue
        number = int(match.group(1))
        if number in covered:
            errors.append(f"overlapping SCR allocation for {entry['id']}")
        covered.add(number)

        source = entry.get("source", {})
        if not isinstance(source, dict):
            continue
        source_kind = source.get("kind")
        if source_kind == "FILE" or (
            source_kind == "HISTORICAL_REFERENCE" and source.get("path")
        ):
            relative_path = source.get("path", "")
            if not isinstance(relative_path, str) or not relative_path:
                errors.append(f"{entry['id']}: {source_kind} source requires a path")
                continue
            candidate = Path(relative_path)
            if candidate.is_absolute() or ".." in candidate.parts:
                errors.append(f"{entry['id']}: source path escapes repository root")
                continue
            target = root / candidate
            try:
                target.resolve().relative_to(root.resolve())
            except ValueError:
                errors.append(f"{entry['id']}: source path escapes repository root")
                continue
            if not target.is_file():
                errors.append(f"{entry['id']}: referenced source file missing: {relative_path}")
            elif source_kind == "FILE" and not FILE_RE.match(candidate.name):
                errors.append(f"{entry['id']}: source path does not encode SCR ID: {relative_path}")
        elif source_kind == "HISTORICAL_REFERENCE":
            repository = source.get("repository", "")
            commit = source.get("commit", "")
            url = source.get("url", "")
            expected_url = f"https://github.com/{repository}/commit/{commit}"
            if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
                errors.append(f"{entry['id']}: invalid external source repository")
            elif not re.fullmatch(r"[0-9a-f]{40}", commit):
                errors.append(f"{entry['id']}: invalid external source commit SHA")
            elif url != expected_url:
                errors.append(f"{entry['id']}: external source URL does not bind repository and commit")

        if (
            entry.get("allocation_status") == "ASSIGNED"
            and entry.get("metadata_status") == "RECONCILED"
        ):
            if entry.get("lifecycle_status") == "UNKNOWN" or entry.get("decision") == "UNKNOWN":
                errors.append(
                    f"{entry['id']}: reconciled metadata cannot contain UNKNOWN lifecycle/decision"
                )

    raw_ranges = data.get("unresolved_ranges", [])
    ranges = raw_ranges if isinstance(raw_ranges, list) else []
    for item in ranges:
        if not isinstance(item, dict):
            continue
        start_match = ID_RE.fullmatch(str(item.get("start", "")))
        end_match = ID_RE.fullmatch(str(item.get("end", "")))
        if not start_match or not end_match:
            continue
        lower, upper = int(start_match.group(1)), int(end_match.group(1))
        if lower > upper:
            errors.append(f"invalid unresolved range: {item['start']}..{item['end']}")
            continue
        for number in range(lower, upper + 1):
            if number in covered:
                errors.append(f"SCR-{number:04d}: overlaps explicit entry and unresolved range")
            covered.add(number)

    observed: dict[int, list[str]] = {}
    folder = root / "change-requests"
    if folder.is_dir():
        for path in folder.rglob("*"):
            if path.is_file():
                match = FILE_RE.match(path.name)
                if match:
                    observed.setdefault(int(match.group(1)), []).append(
                        path.relative_to(root).as_posix()
                    )

    for number, found in sorted(observed.items()):
        if number not in covered:
            errors.append(f"unregistered observed SCR-{number:04d}: {', '.join(found)}")

    if any(
        str(entry.get("allocation_status", "")).upper() == "FREE"
        for entry in entries
        if isinstance(entry, dict)
    ):
        errors.append("FREE is forbidden: missing/unresolved evidence must remain blocked")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        print("SCR REGISTRY: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1

    data = yaml.safe_load(
        (args.root / "registry" / "scr-registry.yaml").read_text(encoding="utf-8")
    )
    print(
        f"SCR REGISTRY: PASS — {len(data['entries'])} entries, "
        f"{len(data['unresolved_ranges'])} blocked ranges; no ID auto-allocation"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
