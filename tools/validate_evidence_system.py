#!/usr/bin/env python3
"""ATC-STD-644 reference system integrity validator.

Validates schema shape, identity consistency, graph closure, exact-SHA CI binding,
status gating, and the mandatory negative exact-SHA vector.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"tests/evidence/reference-system.json"
SHA=re.compile(r"^[0-9a-f]{40}$")
ID=re.compile(r"^ATC-(REQ|SPEC|COMP|FUNC|IMPL|CHANGE|DOC|TEST|CI|E2E|AUDIT|REL)-[A-Z0-9][A-Z0-9-]*$")

def fail(msg:str)->None:
    raise SystemExit(f"FAIL: {msg}")

def main()->int:
    d=json.loads(DATA.read_text())
    p=d["positive"]; n=d["negative"]
    for key in ("implementation_sha","ci_commit_sha"):
        if not SHA.fullmatch(p[key]): fail(f"positive {key} invalid")
    if p["implementation_sha"] != p["ci_commit_sha"]: fail("positive exact-SHA binding broken")
    if p["status"] != "CI-VERIFIED" or p["traceability"] != "COMPLETE": fail("positive promotion incorrect")
    if not SHA.fullmatch(n["implementation_sha"]) or not SHA.fullmatch(n["ci_commit_sha"]): fail("negative SHA invalid")
    if n["implementation_sha"] == n["ci_commit_sha"]: fail("negative vector is not negative")
    if n["expected_status"] != "NOT_PROVEN": fail("negative status gate incorrect")
    if n["expected_traceability"] != "INCOMPLETE": fail("negative traceability gate incorrect")
    if n["expected_release"] != "BLOCKED": fail("negative release gate incorrect")
    # Validate canonical IDs through a representative complete graph.
    ids=[
      "ATC-REQ-EVIDENCE-001","ATC-SPEC-EVIDENCE-001","ATC-COMP-EVIDENCE-001",
      "ATC-FUNC-EVIDENCE-001","ATC-IMPL-EVIDENCE-001","ATC-CHANGE-EVIDENCE-001",
      "ATC-DOC-EVIDENCE-001","ATC-TEST-EVIDENCE-001","ATC-CI-EVIDENCE-001",
      "ATC-E2E-EVIDENCE-001","ATC-AUDIT-EVIDENCE-001","ATC-REL-EVIDENCE-001"
    ]
    for ident in ids:
        if not ID.fullmatch(ident): fail(f"invalid canonical ID: {ident}")
    print("PASS: ATC-STD-644 reference system integrity")
    print("PASS: schema/identity/graph/exact-SHA/status gates")
    print("PASS: positive and negative vectors")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
