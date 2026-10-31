#!/usr/bin/env python3
"""ATC-STD-644 evidence validator: JSON Schema, graph closure, reverse traceability and live CI attestation."""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import requests
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
RECORD_SCHEMA_PATH = ROOT / "schemas/evidence/record.schema.json"
TRACE_SCHEMA_PATH = ROOT / "schemas/evidence/traceability.schema.json"
FIXTURE_PATH = ROOT / "tests/evidence/reference-system.json"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class EvidenceError(ValueError):
    """Raised when evidence is malformed, unresolved, or not bound to its source."""


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"cannot load JSON {path}: {exc}") from exc


def validate_schema(instance, schema, label):
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    if errors:
        details = "; ".join(f"{list(err.path)}: {err.message}" for err in errors[:8])
        raise EvidenceError(f"{label} schema validation failed: {details}")


def validate_graph(records, traceability, record_schema, trace_schema):
    validate_schema(traceability, trace_schema, "traceability")
    if not isinstance(records, list) or not records:
        raise EvidenceError("records must be a non-empty array")
    by_id = {}
    for record in records:
        validate_schema(record, record_schema, f"record {record.get('id', '<missing>')}")
        record_id = record["id"]
        if record_id in by_id:
            raise EvidenceError(f"duplicate evidence ID: {record_id}")
        by_id[record_id] = record
    for record in records:
        for reference in record.get("references", []):
            if reference not in by_id:
                raise EvidenceError(f"{record['id']} references missing evidence {reference}")

    adjacency = {record_id: set() for record_id in by_id}
    reverse = {record_id: set() for record_id in by_id}
    edge_keys = set()
    allowed_pairs = {
        "SPECIFIES": {("REQUIREMENT", "SPECIFICATION")},
        "CONTAINS": {("SPECIFICATION", "COMPONENT"), ("COMPONENT", "FUNCTION")},
        "IMPLEMENTS": {("FUNCTION", "IMPLEMENTATION")},
        "CHANGES": {("IMPLEMENTATION", "CHANGE")},
        "DOCUMENTS": {("CHANGE", "DOCUMENTATION")},
        "TESTS": {("CHANGE", "TEST")},
        "VERIFIES": {("TEST", "CI")},
        "VALIDATES": {("CI", "E2E"), ("E2E", "AUDIT")},
        "RELEASES": {("AUDIT", "RELEASE")},
        "AFFECTS": {
            ("CHANGE", "FUNCTION"),
            ("CHANGE", "COMPONENT"),
            ("CHANGE", "DOCUMENTATION"),
            ("CHANGE", "TEST"),
        },
    }
    for edge in traceability["edges"]:
        source, target, relation = edge["from"], edge["to"], edge["relation"]
        if source not in by_id or target not in by_id:
            raise EvidenceError(f"unresolved graph edge: {source} -> {target}")
        pair = (by_id[source]["type"], by_id[target]["type"])
        if pair not in allowed_pairs.get(relation, set()):
            raise EvidenceError(f"invalid {relation} edge type: {pair[0]} -> {pair[1]}")
        key = (source, target, relation)
        if key in edge_keys:
            raise EvidenceError(f"duplicate graph edge: {key}")
        edge_keys.add(key)
        adjacency[source].add(target)
        reverse[target].add(source)

    required_types = {
        "REQUIREMENT", "SPECIFICATION", "COMPONENT", "FUNCTION", "IMPLEMENTATION",
        "CHANGE", "DOCUMENTATION", "TEST", "CI", "E2E", "AUDIT", "RELEASE",
    }
    missing_types = required_types - {record["type"] for record in records}
    if missing_types:
        raise EvidenceError("missing required evidence types: " + ", ".join(sorted(missing_types)))

    def walk(graph, start):
        seen, pending = set(), [start]
        while pending:
            node = pending.pop()
            if node in seen:
                continue
            seen.add(node)
            pending.extend(graph[node] - seen)
        return seen

    roots = [key for key, value in by_id.items() if value["type"] == "REQUIREMENT"]
    releases = [key for key, value in by_id.items() if value["type"] == "RELEASE"]
    if len(roots) != 1 or len(releases) != 1:
        raise EvidenceError("reference graph requires exactly one root requirement and one release")
    if releases[0] not in walk(adjacency, roots[0]):
        raise EvidenceError("forward traceability does not reach RELEASE")
    if roots[0] not in walk(reverse, releases[0]):
        raise EvidenceError("reverse traceability does not reach REQUIREMENT")

    implementation = next(record for record in records if record["type"] == "IMPLEMENTATION")
    cursor = implementation["id"]
    for expected_type in ("FUNCTION", "COMPONENT", "SPECIFICATION", "REQUIREMENT"):
        candidates = [node for node in reverse[cursor] if by_id[node]["type"] == expected_type]
        if len(candidates) != 1:
            raise EvidenceError(
                f"reverse source traceability from {cursor} cannot uniquely resolve {expected_type}"
            )
        cursor = candidates[0]
    return by_id


def evaluate(records, traceability):
    by_type = {record["type"]: record for record in records}
    implementation = by_type["IMPLEMENTATION"]
    ci = by_type["CI"]
    exact_sha = implementation["commit_sha"] == ci["commit_sha"]
    ci_verified = (
        exact_sha
        and ci["result"] == "PASS"
        and bool(ci.get("run_id"))
        and bool(ci.get("job_id"))
        and bool(ci.get("step_name"))
    )
    trace_complete = traceability["status"] == "COMPLETE" and exact_sha
    if not ci_verified:
        return {"status": "NOT_PROVEN", "traceability": "INCOMPLETE", "release": "BLOCKED"}
    e2e_ok = by_type["E2E"].get("status") == "PASS"
    audit_ok = by_type["AUDIT"].get("status") == "PASS"
    release_ok = (
        trace_complete
        and e2e_ok
        and audit_ok
        and by_type["RELEASE"].get("status") == "RELEASE-READY"
    )
    return {
        "status": "RELEASE-READY" if release_ok else "CI-VERIFIED",
        "traceability": "COMPLETE" if trace_complete else "INCOMPLETE",
        "release": "READY" if release_ok else "BLOCKED",
    }


def validate_fixture():
    fixture = load_json(FIXTURE_PATH)
    record_schema = load_json(RECORD_SCHEMA_PATH)
    trace_schema = load_json(TRACE_SCHEMA_PATH)
    positive = fixture["positive"]
    validate_graph(positive["records"], positive["traceability"], record_schema, trace_schema)
    actual_positive = evaluate(positive["records"], positive["traceability"])
    if actual_positive != positive["expected"]:
        raise EvidenceError(f"positive vector mismatch: {actual_positive}")

    negative_records = json.loads(json.dumps(positive["records"]))
    mutation = fixture["negative"]["mutation"]
    target = next(record for record in negative_records if record["id"] == mutation["record_id"])
    if mutation["field"] not in target:
        raise EvidenceError("negative vector mutation field does not exist")
    target[mutation["field"]] = mutation["value"]
    validate_graph(negative_records, positive["traceability"], record_schema, trace_schema)
    actual_negative = evaluate(negative_records, positive["traceability"])
    if actual_negative != fixture["negative"]["expected"]:
        raise EvidenceError(f"negative vector mismatch: {actual_negative}")
    return actual_positive, actual_negative


def validate_repository_head(expected_head):
    if not SHA_RE.fullmatch(expected_head or ""):
        raise EvidenceError("expected head SHA is missing or malformed")
    actual = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    if actual != expected_head:
        raise EvidenceError(f"checkout SHA mismatch: expected {expected_head}, got {actual}")
    validate_fixture()
    return actual


def attest_github_run(expected_head):
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    token = os.environ.get("GITHUB_TOKEN", "")
    if not repo or not run_id or not token:
        raise EvidenceError(
            "GITHUB_REPOSITORY, GITHUB_RUN_ID and GITHUB_TOKEN are required for live attestation"
        )
    checked_out_sha = validate_repository_head(expected_head)
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    base = f"https://api.github.com/repos/{repo}"
    run_response = requests.get(
        f"{base}/actions/runs/{run_id}", headers=headers, timeout=20
    )
    run_response.raise_for_status()
    run = run_response.json()
    if str(run.get("id")) != run_id:
        raise EvidenceError("GitHub workflow run identity does not match this run")
    jobs_response = requests.get(
        f"{base}/actions/runs/{run_id}/jobs?per_page=100",
        headers=headers,
        timeout=20,
    )
    jobs_response.raise_for_status()
    jobs = jobs_response.json().get("jobs", [])
    validation_jobs = [
        job for job in jobs if job.get("name") == "Evidence graph validation"
    ]
    if len(validation_jobs) != 1:
        raise EvidenceError("cannot uniquely resolve Evidence graph validation job")
    job = validation_jobs[0]
    if job.get("status") != "completed" or job.get("conclusion") != "success":
        raise EvidenceError("evidence validation job is not completed successfully")
    required_steps = {
        "Validate repository evidence graph",
        "Run positive and negative evidence tests",
    }
    successful_steps = [
        step
        for step in job.get("steps", [])
        if step.get("name") in required_steps
        and step.get("status") == "completed"
        and step.get("conclusion") == "success"
    ]
    if {step["name"] for step in successful_steps} != required_steps:
        raise EvidenceError("required validation steps are missing, skipped, or failed")

    evidence = {
        "schema": "ATC-STD-644-LIVE-CI-EVIDENCE-v1",
        "repository": repo,
        "source_commit_sha": checked_out_sha,
        "workflow_run_id": str(run_id),
        "workflow_run_url": run.get("html_url"),
        "run_head_sha": run.get("head_sha"),
        "job_id": str(job["id"]),
        "job_name": job["name"],
        "job_url": job.get("html_url"),
        "steps": [
            {
                "step_number": step["number"],
                "step_name": step["name"],
                "result": step["conclusion"],
            }
            for step in sorted(successful_steps, key=lambda item: item["number"])
        ],
    }
    output = ROOT / "atc-std-644-evidence.json"
    output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f"PASS: exact source checkout SHA {checked_out_sha}")
    print(f"PASS: GitHub Run {run_id} / Job {job['id']} ({job['name']})")
    for step in evidence["steps"]:
        print(
            f"PASS: Step {step['step_number']} {step['step_name']} — {step['result']}"
        )
    print(f"EVIDENCE_ARTIFACT: {output.name}")
    print(f"EVIDENCE_SHA256: {digest}")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-repository", action="store_true")
    parser.add_argument("--attest-github-run", action="store_true")
    parser.add_argument(
        "--expected-head-sha", default=os.environ.get("ATC_EXPECTED_HEAD_SHA", "")
    )
    args = parser.parse_args()
    try:
        if args.attest_github_run:
            return attest_github_run(args.expected_head_sha)
        positive, negative = validate_fixture()
        print("PASS: JSON Schema, evidence identity, graph closure and reverse traversal")
        print(f"PASS: positive vector => {positive}")
        print(f"PASS: negative exact-SHA vector => {negative}")
        if args.check_repository:
            checked_out = validate_repository_head(args.expected_head_sha)
            print(f"PASS: exact repository checkout SHA {checked_out}")
        return 0
    except (EvidenceError, requests.RequestException, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
