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


def resolve_event_binding(event, run):
    """Resolve the exact commit and PR identity for pull_request and push events."""
    pull_request = event.get("pull_request")
    if pull_request:
        pr_number = pull_request.get("number")
        base_sha = pull_request.get("base", {}).get("sha")
        event_head_sha = pull_request.get("head", {}).get("sha")
        event_branch = pull_request.get("head", {}).get("ref")
    elif event.get("after"):
        event_head_sha = event.get("after")
        event_branch = event.get("ref", "").removeprefix("refs/heads/")
        run_prs = run.get("pull_requests", [])
        if len(run_prs) != 1:
            raise EvidenceError("push workflow run does not resolve to exactly one pull request")
        pr_number = run_prs[0].get("number")
        base_sha = run_prs[0].get("base", {}).get("sha")
        if event_branch != run.get("head_branch"):
            raise EvidenceError("push event branch does not match workflow run branch")
    else:
        raise EvidenceError("unsupported event: expected pull_request or push")
    if not isinstance(pr_number, int) or not SHA_RE.fullmatch(base_sha or ""):
        raise EvidenceError("event does not contain a valid PR number and base SHA")
    run_prs = run.get("pull_requests", [])
    if len(run_prs) != 1 or run_prs[0].get("number") != pr_number:
        raise EvidenceError("GitHub workflow run is not bound to the event pull request")
    if run_prs[0].get("head", {}).get("ref") != event_branch:
        raise EvidenceError("event branch does not match associated pull request head branch")
    return event_head_sha, base_sha, pr_number


def validate_live_run_identity(repo, run_id, expected_head, event_head_sha, pr_number, run):
    """Fail closed unless event, workflow run, repository and PR identities agree."""
    if event_head_sha != expected_head:
        raise EvidenceError("pull_request event head SHA does not match exact checkout SHA")
    if str(run.get("id")) != str(run_id):
        raise EvidenceError("GitHub workflow run identity does not match this run")
    if run.get("head_sha") != expected_head:
        raise EvidenceError("GitHub workflow run head SHA does not match exact checkout SHA")
    if run.get("repository", {}).get("full_name") != repo:
        raise EvidenceError("GitHub workflow run repository identity mismatch")
    run_prs = run.get("pull_requests", [])
    if len(run_prs) != 1 or run_prs[0].get("number") != pr_number:
        raise EvidenceError("GitHub workflow run is not bound to the event pull request")


def build_live_evidence_graph(repo, expected_head, base_sha, run_id, run, job, successful_steps):
    """Build a run-specific graph; unexecuted E2E/audit/release remain explicitly unproven."""
    if not SHA_RE.fullmatch(base_sha or ""):
        raise EvidenceError("PR base SHA is missing or malformed")
    pr_numbers = [item.get("number") for item in run.get("pull_requests", [])]
    if len(pr_numbers) != 1 or not isinstance(pr_numbers[0], int):
        raise EvidenceError("workflow run does not resolve to exactly one pull request")
    pr_number = pr_numbers[0]
    ids = {
        "requirement": "ATC-REQ-STD644-001",
        "specification": "ATC-SPEC-STD644-001",
        "component": "ATC-COMP-STD644-VALIDATOR",
        "function": "ATC-FUNC-STD644-GRAPH-VALIDATOR",
        "implementation": "ATC-IMPL-STD644-GRAPH-VALIDATOR",
        "change": f"ATC-CHANGE-PR-{pr_number}",
        "documentation": "ATC-DOC-STD644-CANDIDATE",
        "test": "ATC-TEST-STD644-EVIDENCE-SUITE",
        "ci": f"ATC-CI-RUN-{run_id}",
        "e2e": f"ATC-E2E-PR-{pr_number}",
        "audit": f"ATC-AUDIT-PR-{pr_number}",
        "release": f"ATC-REL-PR-{pr_number}",
    }
    validation_step = next(
        step for step in successful_steps
        if step["name"] == "Validate repository evidence graph"
    )
    records = [
        {"id": ids["requirement"], "type": "REQUIREMENT", "version": "1.0", "status": "SPECIFIED"},
        {"id": ids["specification"], "type": "SPECIFICATION", "version": "1.0", "status": "SPECIFIED", "references": [ids["requirement"]]},
        {"id": ids["component"], "type": "COMPONENT", "version": "1.0", "status": "PRESENT", "references": [ids["specification"]]},
        {"id": ids["function"], "type": "FUNCTION", "version": "1.0", "status": "IMPLEMENTED", "references": [ids["component"], ids["specification"]]},
        {
            "id": ids["implementation"],
            "type": "IMPLEMENTATION",
            "version": "1.0",
            "status": "IMPLEMENTED",
            "repository": repo,
            "path": "tools/validate_evidence_system.py",
            "module": "validate_evidence_system",
            "symbol": "validate_graph",
            "commit_sha": expected_head,
            "references": [ids["function"]],
        },
        {
            "id": ids["change"],
            "type": "CHANGE",
            "version": "1.0",
            "status": "TESTED",
            "base_sha": base_sha,
            "head_sha": expected_head,
            "classification": ["MODIFY"],
            "references": [ids["implementation"], ids["function"]],
        },
        {
            "id": ids["documentation"],
            "type": "DOCUMENTATION",
            "version": "1.0",
            "status": "DOCUMENTED",
            "path": "standards/audit/ATC-STD-644.md",
            "references": [ids["change"]],
        },
        {
            "id": ids["test"],
            "type": "TEST",
            "version": "1.0",
            "status": "TESTED",
            "test_kind": "regression",
            "path": "tests/evidence/test_validate_evidence_system.py",
            "references": [ids["function"], ids["implementation"]],
        },
        {
            "id": ids["ci"],
            "type": "CI",
            "version": "1.0",
            "status": "PASS",
            "commit_sha": expected_head,
            "run_id": str(run_id),
            "job_id": str(job["id"]),
            "step_name": validation_step["name"],
            "step_number": validation_step["number"],
            "result": "PASS",
            "references": [ids["test"], ids["implementation"]],
        },
        {"id": ids["e2e"], "type": "E2E", "version": "1.0", "status": "NOT_PROVEN", "references": [ids["ci"]]},
        {"id": ids["audit"], "type": "AUDIT", "version": "1.0", "status": "NOT_PROVEN", "references": [ids["e2e"]]},
        {"id": ids["release"], "type": "RELEASE", "version": "1.0", "status": "NOT_READY", "references": [ids["audit"]]},
    ]
    edges = [
        ("requirement", "specification", "SPECIFIES"),
        ("specification", "component", "CONTAINS"),
        ("component", "function", "CONTAINS"),
        ("function", "implementation", "IMPLEMENTS"),
        ("implementation", "change", "CHANGES"),
        ("change", "documentation", "DOCUMENTS"),
        ("change", "test", "TESTS"),
        ("test", "ci", "VERIFIES"),
        ("ci", "e2e", "VALIDATES"),
        ("e2e", "audit", "VALIDATES"),
        ("audit", "release", "RELEASES"),
    ]
    traceability = {
        "id": f"ATC-TRACE-PR-{pr_number}",
        "status": "INCOMPLETE",
        "edges": [
            {"from": ids[source], "to": ids[target], "relation": relation}
            for source, target, relation in edges
        ],
    }
    return records, traceability


def attest_github_run(expected_head):
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    token = os.environ.get("GITHUB_TOKEN", "")
    event_path = os.environ.get("GITHUB_EVENT_PATH", "")
    if not repo or not run_id or not token or not event_path:
        raise EvidenceError(
            "GITHUB_REPOSITORY, GITHUB_RUN_ID, GITHUB_TOKEN and GITHUB_EVENT_PATH are required"
        )
    checked_out_sha = validate_repository_head(expected_head)
    try:
        event = load_json(event_path)
    except EvidenceError:
        raise
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
    event_head_sha, base_sha, pr_number = resolve_event_binding(event, run)
    validate_live_run_identity(
        repo, run_id, checked_out_sha, event_head_sha, pr_number, run
    )

    jobs_response = requests.get(
        f"{base}/actions/runs/{run_id}/jobs?per_page=100",
        headers=headers,
        timeout=20,
    )
    jobs_response.raise_for_status()
    jobs = jobs_response.json().get("jobs", [])
    validation_jobs = [
        item for item in jobs if item.get("name") == "Evidence graph validation"
    ]
    if len(validation_jobs) != 1:
        raise EvidenceError("cannot uniquely resolve Evidence graph validation job")
    job = validation_jobs[0]
    if str(job.get("run_id")) != run_id:
        raise EvidenceError("validation job belongs to a different workflow run")
    if job.get("head_sha") and job.get("head_sha") != checked_out_sha:
        raise EvidenceError("validation job head SHA does not match exact checkout SHA")
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

    record_schema = load_json(RECORD_SCHEMA_PATH)
    trace_schema = load_json(TRACE_SCHEMA_PATH)
    records, traceability = build_live_evidence_graph(
        repo, checked_out_sha, base_sha, run_id, run, job, successful_steps
    )
    validate_graph(records, traceability, record_schema, trace_schema)
    evaluation = evaluate(records, traceability)
    expected_evaluation = {
        "status": "CI-VERIFIED",
        "traceability": "INCOMPLETE",
        "release": "BLOCKED",
    }
    if evaluation != expected_evaluation:
        raise EvidenceError(f"live evidence graph status mismatch: {evaluation}")

    evidence = {
        "schema": "ATC-STD-644-LIVE-CI-EVIDENCE-v2",
        "repository": repo,
        "source_commit_sha": checked_out_sha,
        "base_commit_sha": base_sha,
        "pull_request_number": pr_number,
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
        "records": records,
        "traceability": traceability,
        "evaluation": evaluation,
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
    print(f"PASS: live evidence graph => {evaluation}")
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
