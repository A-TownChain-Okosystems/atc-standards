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

def validate(root: Path = ROOT, registry_path: Path | None = None, schema_path: Path | None = None) -> list[str]:
    registry_path = registry_path or root / "registry" / "scr-registry.yaml"
    schema_path = schema_path or root / "schemas" / "scr-registry.schema.json"
    try:
        data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"cannot load registry/schema: {exc}"]
    errors = [f"schema: {e.message} at {list(e.absolute_path)}" for e in Draft202012Validator(schema).iter_errors(data)]
    entries = data.get("entries", []) if isinstance(data, dict) else []
    ids = [e.get("id") for e in entries if isinstance(e, dict)]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    if duplicates:
        errors.append("duplicate SCR IDs: " + ", ".join(duplicates))
    covered: set[int] = set()
    for entry in entries:
        match = ID_RE.fullmatch(str(entry.get("id", "")))
        if not match:
            continue
        number = int(match.group(1))
        if number in covered:
            errors.append(f"overlapping SCR allocation for {entry['id']}")
        covered.add(number)
        source = entry.get("source", {})
        if source.get("kind") == "FILE":
            rel = source.get("path", "")
            target = root / rel
            if not rel or not target.is_file():
                errors.append(f"{entry['id']}: referenced SCR file missing: {rel}")
            elif not FILE_RE.match(Path(rel).name):
                errors.append(f"{entry['id']}: source path does not encode SCR ID: {rel}")
        if entry.get("allocation_status") == "ASSIGNED" and entry.get("metadata_status") == "RECONCILED":
            if entry.get("lifecycle_status") == "UNKNOWN" or entry.get("decision") == "UNKNOWN":
                errors.append(f"{entry['id']}: reconciled metadata cannot contain UNKNOWN lifecycle/decision")
    for item in data.get("unresolved_ranges", []):
        sm = ID_RE.fullmatch(str(item.get("start", "")))
        em = ID_RE.fullmatch(str(item.get("end", "")))
        if not sm or not em:
            continue
        lo, hi = int(sm.group(1)), int(em.group(1))
        if lo > hi:
            errors.append(f"invalid unresolved range: {item['start']}..{item['end']}")
            continue
        for number in range(lo, hi + 1):
            if number in covered:
                errors.append(f"SCR-{number:04d}: overlaps explicit entry and unresolved range")
            covered.add(number)
    observed: dict[int, list[str]] = {}
    folder = root / "change-requests"
    if folder.is_dir():
        for path in folder.iterdir():
            if path.is_file():
                match = FILE_RE.match(path.name)
                if match:
                    observed.setdefault(int(match.group(1)), []).append(path.relative_to(root).as_posix())
    for number, found in sorted(observed.items()):
        if number not in covered:
            errors.append(f"unregistered observed SCR-{number:04d}: {', '.join(found)}")
    if any(str(e.get("allocation_status", "")).upper() == "FREE" for e in entries):
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
    data = yaml.safe_load((args.root / "registry" / "scr-registry.yaml").read_text(encoding="utf-8"))
    print(f"SCR REGISTRY: PASS — {len(data['entries'])} entries, {len(data['unresolved_ranges'])} blocked ranges; no ID auto-allocation")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
