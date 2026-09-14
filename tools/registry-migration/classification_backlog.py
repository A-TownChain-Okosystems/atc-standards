#!/usr/bin/env python3
"""Build a non-canonical semantic classification backlog from the legacy inventory."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

import yaml

DOMAIN_BY_LEGACY_CATEGORY = {
    "os": "OS",
    "development": "Language / Development",
    "audit": "Audit / Evidence",
    "repository": "Repository / Supply Chain",
    "governance": "Governance",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", default="registry/migrations/standard-inventory.generated.yaml")
    ap.add_argument("--output", default="registry/migrations/classification-backlog.yaml")
    args = ap.parse_args()

    root = Path(".").resolve()
    inventory_path = root / args.inventory
    data = yaml.safe_load(inventory_path.read_text(encoding="utf-8"))
    entries = data.get("entries", [])

    backlog = []
    status_counts = Counter()
    category_counts = Counter()

    for entry in entries:
        legacy_id = str(entry["legacy_id"])
        category = entry.get("registry_category")
        is_600_range = bool(re.fullmatch(r"ATC-STD-6\d\d", legacy_id))

        if is_600_range and category in DOMAIN_BY_LEGACY_CATEGORY:
            status = "classified"
            semantic_domain = DOMAIN_BY_LEGACY_CATEGORY[category]
            basis = "legacy registry category and authoritative standard source path"
        else:
            status = "unreviewed"
            semantic_domain = None
            basis = None

        backlog.append(
            {
                "legacy_id": legacy_id,
                "title": entry.get("title"),
                "source": entry.get("source"),
                "legacy_namespace": entry.get("namespace"),
                "legacy_category": category,
                "classification": {
                    "status": status,
                    "semantic_domain": semantic_domain,
                    "basis": basis,
                    "family": {"id": None, "name": None},
                    "category": {"id": None, "name": None},
                    "class": {"id": None, "name": None},
                    "sequence": None,
                    "canonical_id": None,
                },
                "conflict": bool(entry.get("migration", {}).get("conflict", False)),
            }
        )
        status_counts[status] += 1
        category_counts[category or "<missing>"] += 1

    out = {
        "schema_version": "1.0.0",
        "status": "working_classification_backlog",
        "source_of_truth": args.inventory,
        "rules": {
            "canonical_ids_allocated": False,
            "family_assignments_allocated": False,
            "legacy_ids_modified": False,
            "numeric_range_implies_family": False,
            "semantic_classification_is_not_canonical_allocation": True,
        },
        "summary": {
            "total": len(backlog),
            "status_counts": dict(sorted(status_counts.items())),
            "legacy_category_counts": dict(sorted(category_counts.items())),
        },
        "entries": backlog,
    }

    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Generated classification backlog: {len(backlog)} entries")
    print(f"Status counts: {dict(sorted(status_counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
