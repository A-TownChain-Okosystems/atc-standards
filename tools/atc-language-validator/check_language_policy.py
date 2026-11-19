#!/usr/bin/env python3
"""Validate the machine-readable Rust-first language policy."""
from __future__ import annotations

import argparse
import pathlib
import sys

import yaml

BOUNDARY = {"C", "C++", "Assembly"}
REQUIRED_RULES = {
    "LANG-RUST-001",
    "LANG-BOUNDARY-001",
    "LANG-PYTHON-001",
    "LANG-TS-001",
    "LANG-WASM-001",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = pathlib.Path(args.root)
    path = root / "registry" / "language-policy.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    failures: list[str] = []

    if data.get("standard") != "ATC-STD-100":
        failures.append("policy standard must be ATC-STD-100")
    if data.get("standard_version") != "2.1.0":
        failures.append("policy standard_version must be 2.1.0")
    if data.get("rust_first") is not True:
        failures.append("rust_first must be true")

    rules = data.get("rules", [])
    rule_ids = {rule.get("id") for rule in rules}
    failures.extend(
        f"missing required rule: {rule_id}"
        for rule_id in sorted(REQUIRED_RULES - rule_ids)
    )

    repos = data.get("repositories", {})
    for name, profile in repos.items():
        primary = profile.get("primary")
        secondary = set(profile.get("secondary", []))
        scopes = set(profile.get("secondary_scope", []))

        if not primary:
            failures.append(f"{name}: missing primary language")
        if primary in {"Python", "TypeScript", "Go", "JavaScript", "C", "C++"}:
            failures.append(f"{name}: non-Rust primary requires explicit architecture exception")

        for language in secondary & BOUNDARY:
            if not profile.get("boundary") and "external_engine_boundary" not in scopes:
                failures.append(f"{name}: boundary language {language} lacks explicit boundary declaration")

        if name in {"a-townchain", "atc-node", "atc-vm", "atc-shivacore", "globus-os", "aurora-ai"} and primary != "Rust":
            failures.append(f"{name}: Rust is mandatory for this system-critical profile")

    if failures:
        print("LANGUAGE POLICY: FAIL")
        for failure in failures:
            print(f"  [FAIL] {failure}")
        return 1

    print(f"LANGUAGE POLICY: PASS ({len(repos)} repository profiles, Rust-first)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
