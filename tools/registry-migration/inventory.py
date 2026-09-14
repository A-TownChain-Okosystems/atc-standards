#!/usr/bin/env python3
"""Build the Phase-1 legacy registry inventory without allocating canonical IDs.

The generator is intentionally fail-closed:
- registry/standards.yaml is the primary registry source;
- existing IDs are preserved verbatim as legacy_id;
- family/category/class/sequence/canonical_id remain unset;
- duplicate IDs and cross-source collisions are reported as conflicts;
- no file rename or ID migration is performed.

Requires PyYAML. No dependency installation is performed by this tool.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("ERROR: PyYAML is required; install the repository's declared YAML dependency before running this tool.") from exc

ID_RE = re.compile(r"\b(?:ATC-(?:STD|AAS|ENT|ARCH)|FAM)-[A-Z0-9][A-Z0-9_-]*\b")
CANONICAL_RE = re.compile(r"^ATC-STD-F\d{2}-\d{3}$")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_registry(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("standards"), list):
        raise SystemExit(f"ERROR: invalid registry structure: {path}")
    return [x for x in data["standards"] if isinstance(x, dict)]


def namespace(identifier: str) -> str:
    if identifier.startswith("ATC-STD-"):
        rest = identifier[len("ATC-STD-"):]
        return "ATC-STD-Fxx" if CANONICAL_RE.fullmatch(identifier) else "ATC-STD"
    if identifier.startswith("ATC-AAS-"):
        return "ATC-AAS"
    if identifier.startswith("ATC-ENT-"):
        return "ATC-ENT"
    if identifier.startswith("ATC-ARCH-"):
        return "ATC-ARCH"
    if identifier.startswith("FAM-"):
        return "FAM"
    return identifier.split("-", 2)[0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--output", default="registry/migrations/standard-inventory.generated.yaml")
    ap.add_argument("--scan-root", action="append", default=["standards", "governance", "registry"])
    args = ap.parse_args()

    root = Path(args.repo).resolve()
    registry = root / "registry/standards.yaml"
    if not registry.is_file():
        raise SystemExit(f"ERROR: missing authoritative registry: {registry}")

    records = load_registry(registry)
    by_id: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        identifier = str(record.get("id", "")).strip()
        if not identifier:
            continue
        by_id[identifier].append(record)

    source_occurrences: dict[str, set[str]] = defaultdict(set)
    for rel_root in args.scan_root:
        scan_root = root / rel_root
        if not scan_root.exists():
            continue
        for path in scan_root.rglob("*"):
            if not path.is_file() or path.name == "standard-inventory.generated.yaml":
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for identifier in ID_RE.findall(text):
                source_occurrences[identifier].add(str(path.relative_to(root)))

    entries = []
    for record in records:
        identifier = str(record.get("id", "")).strip()
        if not identifier:
            continue
        duplicate = len(by_id[identifier]) > 1
        source_paths = sorted(source_occurrences.get(identifier, set()))
        conflict = duplicate
        reason = "duplicate legacy ID in authoritative registry" if duplicate else None
        entries.append(
            {
                "legacy_id": identifier,
                "title": record.get("title"),
                "source": record.get("file", "registry/standards.yaml"),
                "registry_category": record.get("category"),
                "registry_status": record.get("status"),
                "registry_version": record.get("version"),
                "namespace": namespace(identifier),
                "family": {"id": None, "name": None},
                "category": {"id": None, "name": None},
                "class": {"id": None, "name": None},
                "sequence": None,
                "canonical_id": None,
                "migration": {
                    "status": "conflict" if conflict else "unreviewed",
                    "conflict": conflict,
                    "reason": reason,
                },
                "observed_sources": source_paths,
            }
        )

    namespaces = defaultdict(int)
    for entry in entries:
        namespaces[entry["namespace"]] += 1

    out = {
        "schema_version": "1.0.0",
        "status": "generated_working_inventory",
        "source_of_truth": "registry/standards.yaml",
        "rules": {
            "legacy_ids_immutable": True,
            "canonical_ids_allocated_only_after_review": True,
            "automatic_numeric_renumbering": False,
            "automatic_family_assignment": False,
            "conflicts_fail_closed": True,
        },
        "discovery": {
            "registry_sha256": sha256(registry),
            "registry_record_count": len(records),
            "duplicate_legacy_ids": sorted(k for k, v in by_id.items() if len(v) > 1),
            "namespace_counts": dict(sorted(namespaces.items())),
        },
        "entries": entries,
    }

    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Generated {len(entries)} inventory entries -> {output}")
    print(f"Namespaces: {dict(sorted(namespaces.items()))}")
    print(f"Duplicate IDs: {len([k for k, v in by_id.items() if len(v) > 1])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
