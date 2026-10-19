#!/usr/bin/env python3
"""Validate the Proof-of-System fixture contract only; not consensus conformance."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "conformance/proof-of-system/fixtures/vectors.json"
EXPECTED_IDS = [f"POS-V-{i:03d}" for i in range(1, 8)] + [
    f"POS-N-{i:03d}" for i in range(1, 13)
]
ALLOWED_DECISIONS = {
    "ACCEPT",
    "REJECT",
    "FINALIZE",
    "NOT_FINALIZED",
    "SECURITY_STOP",
}
errors = []


def fail(message):
    errors.append(message)


def main():
    try:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: cannot read fixture JSON: {exc}")
        return 2

    if data.get("contract_id") != "ATC-POS-CONFORMANCE-001":
        fail("wrong contract_id")
    if data.get("status") != "PROPOSED_NOT_NORMATIVE":
        fail("contract must remain proposed/non-normative")
    if data.get("chain_id") != 658467:
        fail("unexpected chain_id")

    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) != 19:
        fail("expected exactly 19 cases")
        cases = cases if isinstance(cases, list) else []

    ids = [case.get("case_id") for case in cases if isinstance(case, dict)]
    if ids != EXPECTED_IDS:
        fail("case IDs must be complete and in canonical order")
    if len(ids) != len(set(ids)):
        fail("duplicate case IDs")

    for case in cases:
        cid = case.get("case_id", "<missing>")
        if case.get("contract_status") != "BLOCKED":
            fail(f"{cid}: status must remain BLOCKED")
        if case.get("fixture_status") != "PLACEHOLDERS_UNRESOLVED":
            fail(f"{cid}: unresolved fixtures must not be treated as runnable")
        if not case.get("blocked_by_parameters"):
            fail(f"{cid}: no parameter blockers listed")

        inp = case.get("input", {})
        if (
            inp.get("contract_id") != data.get("contract_id")
            or inp.get("chain_id") != 658467
        ):
            fail(f"{cid}: input envelope mismatch")

        exp = case.get("expected", {})
        if exp.get("decision") not in ALLOWED_DECISIONS:
            fail(f"{cid}: invalid expected decision")
        if (
            exp.get("decision_is_normative") is not False
            or exp.get("error_code_is_normative") is not False
        ):
            fail(f"{cid}: proposed values must not be represented as normative")
        if not re.fullmatch(r"E_[A-Z0-9_]+", str(exp.get("error_code", ""))):
            fail(f"{cid}: invalid provisional harness error code")
        if "FIXTURE:" not in json.dumps(inp, sort_keys=True):
            fail(
                f"{cid}: fixture placeholders missing; expected contract "
                "to remain explicitly blocked"
            )

    if errors:
        print("FAIL: contract validation")
        for item in errors:
            print(f"- {item}")
        return 1

    print(
        "PASS: 19 contract records, unique IDs, contract invariants "
        "and BLOCKED guard verified."
    )
    print(
        "NOT RUN: consensus behavior, cryptographic verification, finality, "
        "fork choice, multi-node or recovery."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
