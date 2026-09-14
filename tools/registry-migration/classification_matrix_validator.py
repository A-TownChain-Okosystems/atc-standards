#!/usr/bin/env python3
"""Fail-closed validator for the Phase-2 semantic classification matrix.

The matrix is a non-authoritative proposal artifact. This validator proves that
it does not allocate or mutate canonical migration identifiers.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="registry/standards.yaml")
    parser.add_argument("--matrix", default="registry/migrations/classification-matrix.generated.yaml")
    args = parser.parse_args()

    registry = load_yaml(Path(args.registry))
    matrix = load_yaml(Path(args.matrix))

    source = registry.get("standards") if isinstance(registry, dict) else None
    entries = matrix.get("entries") if isinstance(matrix, dict) else None
    if not isinstance(source, list):
        fail("registry does not contain a standards list")
    if not isinstance(entries, list):
        fail("classification matrix does not contain an entries list")

    source_rows = [x for x in source if isinstance(x, dict) and str(x.get("id", "")).strip()]
    matrix_rows = [x for x in entries if isinstance(x, dict)]
    source_ids = [str(x["id"]).strip() for x in source_rows]
    matrix_ids = [str(x.get("legacy_id", "")).strip() for x in matrix_rows]

    if len(source_ids) != 505:
        fail(f"expected 505 source standards, found {len(source_ids)}")
    if len(matrix_rows) != 505:
        fail(f"coverage is not 505/505: found {len(matrix_rows)} matrix entries")
    if len(set(source_ids)) != len(source_ids):
        fail("duplicate legacy IDs exist in source registry")
    if len(set(matrix_ids)) != len(matrix_ids):
        fail("duplicate legacy IDs exist in classification matrix")
    if set(source_ids) != set(matrix_ids):
        missing = sorted(set(source_ids) - set(matrix_ids))
        extra = sorted(set(matrix_ids) - set(source_ids))
        fail(f"legacy-ID coverage mismatch; missing={missing[:10]} extra={extra[:10]}")

    source_by_id = {str(x["id"]).strip(): x for x in source_rows}
    forbidden = {
        "family_id": 0,
        "category_id": 0,
        "class_id": 0,
        "sequence": 0,
        "canonical_id": 0,
    }
    namespace_counts: dict[str, int] = {}
    review_counts: dict[str, int] = {}

    for row in matrix_rows:
        legacy_id = row["legacy_id"]
        if legacy_id != str(source_by_id[legacy_id]["id"]).strip():
            fail(f"legacy ID changed: {legacy_id}")
        if row.get("title", "") != str(source_by_id[legacy_id].get("title", "")):
            fail(f"source title changed for {legacy_id}")

        namespace = str(row.get("legacy_namespace", ""))
        namespace_counts[namespace] = namespace_counts.get(namespace, 0) + 1
        migration = row.get("migration") or {}
        for key in forbidden:
            if migration.get(key) is not None:
                forbidden[key] += 1
                fail(f"forbidden canonical allocation {key} for {legacy_id}: {migration.get(key)!r}")

        governance = row.get("governance") or {}
        status = str(governance.get("status", row.get("migration", {}).get("status", "")))
        review_counts[status] = review_counts.get(status, 0) + 1

        match = re.fullmatch(r"ATC-STD-(\d+)", legacy_id)
        if match and 600 <= int(match.group(1)) <= 699:
            if row.get("numeric_range_family_assignment") not in (None, False):
                fail(f"600-699 numeric range was used as family assignment for {legacy_id}")
            proposal = row.get("proposal") or {}
            if str(proposal.get("semantic_domain", "")).lower() == "blockchain & distributed systems" and str(source_by_id[legacy_id].get("category", "")).lower() == "os":
                fail(f"600-699 OS standard was bulk-classified as Blockchain: {legacy_id}")

        if legacy_id.startswith("FAM-") or str(row.get("legacy_namespace", "")).upper().startswith("FAM"):
            if governance.get("status") not in {"review_required", "blocked", "classified_proposal"}:
                fail(f"FAM-* entry lacks explicit review handling: {legacy_id}")

    if not all(v == 0 for v in forbidden.values()):
        fail(f"forbidden allocation detected: {forbidden}")

    if matrix.get("authority") != "non-authoritative working artifact":
        fail("matrix authority must remain non-authoritative working artifact")
    rules = matrix.get("rules") or {}
    required_false = [
        "family_ids_allocated",
        "category_ids_allocated",
        "class_ids_allocated",
        "sequences_allocated",
        "canonical_ids_allocated",
    ]
    for key in required_false:
        if rules.get(key) is not False:
            fail(f"matrix rule {key} must be false")
    if rules.get("legacy_ids_immutable") is not True:
        fail("legacy_ids_immutable must be true")
    if rules.get("numeric_range_implies_family") is not False:
        fail("numeric_range_implies_family must be false")

    print("Phase-2B classification matrix validation: PASS")
    print(f"Source standards: {len(source_ids)}")
    print(f"Matrix entries: {len(matrix_rows)}")
    print("Coverage: 505/505 (100%)")
    print("Duplicate legacy IDs: 0")
    print("Canonical IDs: 0")
    print("Family IDs: 0")
    print("Category IDs: 0")
    print("Class IDs: 0")
    print("Sequences: 0")
    print("Legacy IDs modified: 0")
    print(f"Namespaces: {namespace_counts}")
    print(f"Review states: {review_counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
