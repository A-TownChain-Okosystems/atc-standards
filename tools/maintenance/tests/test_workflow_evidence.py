#!/usr/bin/env python3
"""Positive/negative tests for SCR-0129 Exact-SHA validation."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "validate_workflow_evidence.py"


def envelope(checkout_ref: str, tested_sha: str, expected_sha: str, exact_sha: bool, status: str = "ANALYZED") -> dict:
    return {
        "workflow_evidence": {
            "workflow": "Test Workflow",
            "repository": "A-TownChain-Okosystems/test",
            "expected_sha": expected_sha,
            "run": {
                "id": 1,
                "status": "SUCCESS",
                "tested_sha": tested_sha,
                "checkout_ref": checkout_ref,
                "exact_sha": exact_sha,
                "evidence_status": status,
            },
            "jobs": [
                {
                    "id": 2,
                    "name": "test",
                    "result": "PASS",
                    "exit_code": 0,
                    "steps": [{"name": "test", "result": "PASS", "exit_code": 0, "error": None}],
                }
            ],
            "required_gates": [{"name": "workflow-evidence-validator", "result": "PASS"}],
            "rerun": None,
        }
    }


def run(document: dict) -> subprocess.CompletedProcess[str]:
    path = Path(__file__).with_name("fixture.json")
    path.write_text(json.dumps(document), encoding="utf-8")
    try:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(path)],
            cwd=ROOT.parent.parent,
            capture_output=True,
            text=True,
            check=False,
        )
    finally:
        path.unlink(missing_ok=True)


def test_merge_ref_is_rejected() -> None:
    sha = "a" * 40
    result = run(envelope("refs/pull/82/merge", sha, sha, True))
    assert result.returncode != 0
    assert "merge ref" in result.stdout


def test_mismatched_sha_is_rejected() -> None:
    result = run(envelope("refs/heads/main", "a" * 40, "b" * 40, False))
    assert result.returncode != 0
    assert "tested_sha" in result.stdout


def test_identical_commit_sha_passes() -> None:
    sha = "c" * 40
    result = run(envelope("refs/heads/main", sha, sha, True))
    assert result.returncode == 0, result.stdout + result.stderr


def test_verified_requires_exact_sha() -> None:
    sha = "d" * 40
    result = run(envelope("refs/heads/main", sha, sha, False, "VERIFIED"))
    assert result.returncode != 0
    assert "exact_sha" in result.stdout
