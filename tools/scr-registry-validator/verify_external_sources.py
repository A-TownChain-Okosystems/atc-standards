#!/usr/bin/env python3
"""Verify pinned external SCR commit trees and path-level Git blob identities."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

OWNER = "A-TownChain-Okosystems"
MANIFEST = Path(__file__).resolve().parents[2] / "evidence" / "scr-reconciliation" / "external-source-bindings.json"
REPO_RE = re.compile(r"^A-TownChain-Okosystems/[A-Za-z0-9_.-]+$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
PATH_RE = re.compile(r"^[A-Za-z0-9._/-]+$")


class VerificationError(ValueError):
    """Raised when an external source pin cannot be safely verified."""


def load_manifest(path: Path = MANIFEST) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise VerificationError("external source manifest must use schema_version 1")
    if data.get("repository") != f"{OWNER}/atc-standards":
        raise VerificationError("external source manifest repository identity is invalid")
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        raise VerificationError("external source manifest must contain a non-empty sources array")

    seen = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            raise VerificationError(f"sources[{index}] must be an object")
        if not all(key in source for key in ("scr_id", "repository", "commit", "path", "blob_sha")):
            raise VerificationError(f"sources[{index}] is missing a required field")
        if not re.fullmatch(r"SCR-[0-9]{4}", str(source["scr_id"])):
            raise VerificationError(f"sources[{index}] has an invalid SCR identifier")
        repository = source["repository"]
        commit = source["commit"]
        path = source["path"]
        blob_sha = source["blob_sha"]
        if not isinstance(repository, str) or not REPO_RE.fullmatch(repository):
            raise VerificationError(
                f"sources[{index}] repository is outside the allowed organization"
            )
        if not isinstance(commit, str) or not SHA_RE.fullmatch(commit):
            raise VerificationError(f"sources[{index}] commit must be a lowercase 40-hex SHA")
        if not isinstance(blob_sha, str) or not SHA_RE.fullmatch(blob_sha):
            raise VerificationError(f"sources[{index}] blob_sha must be a lowercase 40-hex SHA")
        if (
            not isinstance(path, str)
            or not PATH_RE.fullmatch(path)
            or path.startswith("/")
            or "\\" in path
            or any(part in {"", ".", ".."} for part in path.split("/"))
        ):
            raise VerificationError(f"sources[{index}] path is not a safe repository-relative path")
        key = (repository, commit, path)
        if key in seen:
            raise VerificationError(
                f"sources[{index}] duplicates an existing repository/commit/path pin"
            )
        seen.add(key)
    return data


def git(repo_dir: Path, args: list[str], runner=subprocess.run) -> str:
    result = runner(
        ["git", *args],
        cwd=repo_dir,
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
    )
    return result.stdout.strip()


def verify_manifest(data: dict, runner=subprocess.run) -> dict:
    """Acquire exact public Git objects and verify each pinned path/blob pair."""
    records = []
    with tempfile.TemporaryDirectory(prefix="atc-scr-external-") as temp:
        root = Path(temp)
        repositories: dict[str, Path] = {}
        fetched: set[tuple[str, str]] = set()
        for source in data["sources"]:
            repository = source["repository"]
            commit = source["commit"]
            path = source["path"]
            expected_blob = source["blob_sha"]
            repo_dir = repositories.get(repository)
            if repo_dir is None:
                repo_dir = root / repository.split("/", 1)[1]
                repo_dir.mkdir(parents=True)
                git(repo_dir, ["init", "--bare"], runner)
                repositories[repository] = repo_dir

            fetch_key = (repository, commit)
            if fetch_key not in fetched:
                git(
                    repo_dir,
                    [
                        "fetch",
                        "--no-tags",
                        "--depth=1",
                        f"https://github.com/{repository}.git",
                        commit,
                    ],
                    runner,
                )
                fetched.add(fetch_key)

            git(repo_dir, ["cat-file", "-e", f"{commit}^{{commit}}"], runner)
            tree_sha = git(repo_dir, ["rev-parse", "--verify", f"{commit}^{{tree}}"], runner)
            if not SHA_RE.fullmatch(tree_sha):
                raise VerificationError(f"{repository}@{commit}: invalid commit tree object")
            actual_blob = git(repo_dir, ["rev-parse", "--verify", f"{commit}:{path}"], runner)
            if not SHA_RE.fullmatch(actual_blob):
                raise VerificationError(f"{repository}@{commit}:{path}: invalid blob object")
            object_type = git(repo_dir, ["cat-file", "-t", actual_blob], runner)
            if object_type != "blob":
                raise VerificationError(
                    f"{repository}@{commit}:{path}: expected blob, got {object_type}"
                )
            if actual_blob != expected_blob:
                raise VerificationError(
                    f"{repository}@{commit}:{path}: blob mismatch "
                    f"(expected {expected_blob}, got {actual_blob})"
                )
            records.append(
                {
                    "scr_id": source["scr_id"],
                    "repository": repository,
                    "commit": commit,
                    "tree_sha": tree_sha,
                    "path": path,
                    "expected_blob_sha": expected_blob,
                    "actual_blob_sha": actual_blob,
                    "status": "VERIFIED",
                }
            )

    return {
        "schema_version": 1,
        "verifier": "verify_external_sources.py",
        "source_count": len(records),
        "verified_count": len(records),
        "failed_count": 0,
        "sources": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = verify_manifest(load_manifest(args.manifest))
    except (OSError, ValueError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(f"EXTERNAL SOURCE VERIFICATION: FAIL — {exc}")
        return 1
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(
        "EXTERNAL SOURCE VERIFICATION: PASS — "
        f"{report['verified_count']} path/blob bindings across exact commit trees"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
