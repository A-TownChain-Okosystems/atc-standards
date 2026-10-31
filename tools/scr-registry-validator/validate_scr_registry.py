#!/usr/bin/env python3
"""Fail-closed validator for the machine-readable SCR identity registry."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
ID_RE = re.compile(r"^SCR-(\d{4})$")
FILE_RE = re.compile(r"^SCR-(\d{4})(?:[-.]|$)")


class UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, yaml.MappingNode):
            return super().construct_mapping(node, deep=deep)
        self.flatten_mapping(node)
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                duplicate = key in mapping
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found an unhashable mapping key",
                    key_node.start_mark,
                ) from exc
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key {key!r}",
                    key_node.start_mark,
                )
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def validate_source(
    entry_id: str,
    source: object,
    label: str,
    root: Path,
    id_match: re.Match[str],
    errors: list[str],
    registry_commit: str,
) -> None:
    """Validate one primary or related source binding."""
    if not isinstance(source, dict):
        errors.append(f"{entry_id}: {label} must be an object")
        return

    source_kind = source.get("kind")
    allowed_source_fields = {
        "FILE": {"kind", "path", "commit", "blob_sha", "identity_sha256", "attestation"},
        "PULL_REQUEST": {"kind", "pr", "branch", "url", "commit", "identity_sha256", "attestation"},
        "HISTORICAL_REFERENCE": {
            "kind",
            "path",
            "pr",
            "url",
            "repository",
            "commit",
            "blob_sha",
            "identity_sha256",
            "attestation",
        },
    }
    unexpected_source_fields = set(source) - allowed_source_fields.get(source_kind, {"kind"})
    if unexpected_source_fields:
        errors.append(
            f"{entry_id}: {label} fields invalid for {source_kind}: "
            f"{', '.join(sorted(unexpected_source_fields))}"
        )

    attestation = source.get("attestation", {})
    if isinstance(attestation, dict) and attestation.get("signature_status") == "VERIFIED":
        commit_sha = source.get("commit")
        signer_identity = attestation.get("signer_identity", "")
        if not commit_sha:
            errors.append(f"{entry_id}: {label} VERIFIED signature requires a commit SHA")
        elif signer_identity:
            verify_result = subprocess.run(
                ["git", "verify-commit", commit_sha],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            if verify_result.returncode != 0:
                errors.append(
                    f"{entry_id}: {label} commit signature verification failed for {commit_sha}"
                )
            else:
                fingerprint_result = subprocess.run(
                    ["git", "show", "-s", "--format=%GF", commit_sha],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                fingerprint = fingerprint_result.stdout.strip()
                if fingerprint_result.returncode != 0 or not fingerprint:
                    errors.append(
                        f"{entry_id}: {label} verified commit has no extractable signer fingerprint"
                    )
                elif fingerprint.casefold() != signer_identity.casefold():
                    errors.append(
                        f"{entry_id}: {label} signer fingerprint does not match signer_identity"
                    )

    if source_kind == "PULL_REQUEST":
        pr_number = source.get("pr")
        expected_url = f"https://github.com/A-TownChain-Okosystems/atc-standards/pull/{pr_number}"
        if (
            not isinstance(pr_number, int)
            or isinstance(pr_number, bool)
            or source.get("url") != expected_url
        ):
            errors.append(
                f"{entry_id}: {label} pull-request URL does not bind repository and PR number"
            )

    if source_kind == "HISTORICAL_REFERENCE":
        has_commit_binding = "commit" in source
        has_pr_binding = "pr" in source
        if has_commit_binding and has_pr_binding:
            errors.append(
                f"{entry_id}: {label} historical source bindings are mutually exclusive "
                "for commit and pull-request references"
            )
        elif has_commit_binding:
            repository = source.get("repository", "")
            commit = source.get("commit", "")
            url = source.get("url", "")
            expected_url = f"https://github.com/{repository}/commit/{commit}"
            if not all((repository, commit, url)):
                errors.append(
                    f"{entry_id}: {label} external historical source requires repository, commit and URL"
                )
            elif not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
                errors.append(f"{entry_id}: {label} invalid external source repository")
            elif not re.fullmatch(r"[0-9a-f]{40}", commit):
                errors.append(f"{entry_id}: {label} invalid external source commit SHA")
            elif url != expected_url:
                errors.append(
                    f"{entry_id}: {label} external source URL does not bind repository and commit"
                )
        elif has_pr_binding:
            pr_number = source.get("pr")
            repository = source.get("repository", "A-TownChain-Okosystems/atc-standards")
            expected_url = f"https://github.com/{repository}/pull/{pr_number}"
            if (
                not isinstance(pr_number, int)
                or isinstance(pr_number, bool)
                or not isinstance(repository, str)
                or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository)
                or source.get("url") != expected_url
            ):
                errors.append(
                    f"{entry_id}: {label} historical pull-request URL does not bind repository and PR number"
                )
        elif "url" in source:
            errors.append(
                f"{entry_id}: {label} historical pull-request URL does not bind repository and PR number"
            )
        elif "repository" in source:
            errors.append(
                f"{entry_id}: {label} external historical source requires repository, commit and URL"
            )
        elif not source.get("path"):
            errors.append(f"{entry_id}: {label} historical reference requires a path, commit or PR")

    if source_kind == "FILE" or (source_kind == "HISTORICAL_REFERENCE" and source.get("path")):
        relative_path = source.get("path", "")
        if not isinstance(relative_path, str) or not relative_path:
            errors.append(f"{entry_id}: {label} {source_kind} source requires a path")
            return
        candidate = Path(relative_path)
        if candidate.is_absolute() or ".." in candidate.parts:
            errors.append(f"{entry_id}: {label} source path escapes repository root")
            return
        target = root / candidate
        try:
            resolved_target = target.resolve()
            resolved_target.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{entry_id}: {label} source path escapes repository root")
            return
        except (OSError, RuntimeError) as exc:
            errors.append(
                f"{entry_id}: {label} cannot safely resolve source path {relative_path}: {exc}"
            )
            return
        if not target.is_file():
            errors.append(f"{entry_id}: {label} referenced source file missing: {relative_path}")
        else:
            blob_sha = source.get("blob_sha")
            source_commit = source.get("commit") or registry_commit
            if not blob_sha:
                errors.append(f"{entry_id}: {label} path source requires blob_sha")
            elif not source_commit:
                errors.append(f"{entry_id}: {label} path source requires an immutable commit SHA")
            else:
                blob_result = subprocess.run(
                    ["git", "rev-parse", "--verify", f"{source_commit}:{relative_path}"],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if blob_result.returncode != 0:
                    errors.append(
                        f"{entry_id}: {label} cannot resolve source blob at commit {source_commit}"
                    )
                elif blob_result.stdout.strip() != blob_sha:
                    errors.append(
                        f"{entry_id}: {label} blob SHA mismatch for {relative_path} at {source_commit}"
                    )
        if target.is_file() and source_kind == "FILE":
            file_match = FILE_RE.match(candidate.name)
            if not file_match:
                errors.append(f"{entry_id}: source path does not encode SCR ID: {relative_path}")
            elif file_match.group(1) != id_match.group(1):
                errors.append(
                    f"{entry_id}: source filename SCR ID does not match registry entry: "
                    f"{relative_path}"
                )


def derive_source_identity(
    source: dict, root: Path, repository: str, registry_commit: str = ""
) -> str:
    """Derive a stable SHA-256 identity without reading outside the repository."""
    identity = {"repository": repository, "kind": str(source.get("kind", ""))}
    source_repository = source.get("repository", repository)
    if source_repository:
        identity["repository"] = str(source_repository)
    commit = source.get("commit") or (registry_commit if source.get("kind") == "FILE" else "")
    if commit:
        identity["commit"] = str(commit)
    if source.get("pr"):
        identity["pr"] = int(source["pr"])
    if source.get("path"):
        relative = Path(str(source["path"]))
        identity["path"] = relative.as_posix()
        if not relative.is_absolute() and ".." not in relative.parts:
            target = root / relative
            try:
                resolved = target.resolve()
                resolved.relative_to(root.resolve())
                if resolved.is_file():
                    content = resolved.read_bytes()
                    actual_blob = hashlib.sha1(
                        f"blob {len(content)}\0".encode("ascii") + content
                    ).hexdigest()
                    identity["blob_sha"] = source.get("blob_sha") or actual_blob
            except (OSError, RuntimeError, ValueError):
                pass
        if source.get("blob_sha"):
            identity["blob_sha"] = source["blob_sha"]
    elif source.get("blob_sha"):
        identity["blob_sha"] = source["blob_sha"]
    if source.get("url"):
        identity["url"] = str(source["url"])
    canonical = json.dumps(identity, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def find_status_contradictions(root: Path) -> list[str]:
    """Find approved normative metadata that conflicts with explicit body wording."""
    residuals: list[str] = []
    standards = root / "standards"
    if not standards.is_dir():
        return residuals
    markers = ("not effective until", "not yet effective", "remains a candidate")
    for path in sorted(standards.rglob("*.md")):
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if not content.startswith("---\n"):
            continue
        end = content.find("\n---", 4)
        if end < 0:
            continue
        try:
            metadata = yaml.safe_load(content[4:end])
        except yaml.YAMLError:
            continue
        if not isinstance(metadata, dict):
            continue
        status = str(metadata.get("status", "")).strip().lower()
        if (
            status not in {"approved", "active", "effective"}
            or metadata.get("normative") is not True
        ):
            continue
        body = content[end + 4 :].lower()
        conflicts = [marker for marker in markers if marker in body]
        metadata_conflicts = []
        if metadata.get("effective_date") is None:
            metadata_conflicts.append("effective_date is null")
        if conflicts or metadata_conflicts:
            details = metadata_conflicts + [f"body marker: {marker}" for marker in conflicts]
            residuals.append(
                f"{path.relative_to(root).as_posix()}: status={status}, normative=true, "
                f"structured metadata/body contradiction: {'; '.join(details)}"
            )
    return residuals


def validate(
    root: Path = ROOT, registry_path: Path | None = None, schema_path: Path | None = None
) -> list[str]:
    registry_path = registry_path or root / "registry" / "scr-registry.yaml"
    schema_path = schema_path or root / "schemas" / "scr-registry.schema.json"
    try:
        data = yaml.load(registry_path.read_text(encoding="utf-8"), Loader=UniqueKeySafeLoader)
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"cannot load registry/schema: {exc}"]

    if not isinstance(data, dict):
        return ["registry root must be an object"]

    errors = [
        f"schema: {error.message} at {list(error.absolute_path)}"
        for error in Draft202012Validator(schema).iter_errors(data)
    ]
    raw_entries = data.get("entries", [])
    entries = raw_entries if isinstance(raw_entries, list) else []
    ids = [
        str(entry["id"])
        for entry in entries
        if isinstance(entry, dict) and entry.get("id") is not None
    ]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        errors.append("duplicate SCR IDs: " + ", ".join(duplicates))

    covered: set[int] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        match = ID_RE.fullmatch(str(entry.get("id", "")))
        if not match:
            continue
        number = int(match.group(1))
        if number in covered:
            errors.append(f"overlapping SCR allocation for {entry['id']}")
        covered.add(number)

        source_bindings = [("source", entry.get("source", {}))]
        related_sources = entry.get("related_sources", [])
        if isinstance(related_sources, list):
            for index, related in enumerate(related_sources):
                if isinstance(related, dict):
                    source_bindings.append(
                        (f"related_sources[{index}].source", related.get("source", {}))
                    )
        seen_relationship_sources: set[tuple[str, str]] = set()
        repository = str(data.get("repository", ""))
        registry_commit = str(data.get("source_commit", ""))
        primary_source = entry.get("source", {})
        primary_source_id = (
            derive_source_identity(primary_source, root, repository, registry_commit)
            if isinstance(primary_source, dict)
            else None
        )
        for label, source in source_bindings:
            validate_source(entry["id"], source, label, root, match, errors, registry_commit)
            if isinstance(source, dict) and label.startswith("related_sources["):
                index = int(label.split("[", 1)[1].split("]", 1)[0])
                relation = related_sources[index].get("relationship", "")
                source_id = derive_source_identity(source, root, repository, registry_commit)
                if source_id == primary_source_id:
                    errors.append(
                        f"{entry['id']}: related source duplicates primary source identity"
                    )
                key = (str(relation), source_id)
                if key in seen_relationship_sources:
                    errors.append(
                        f"{entry['id']}: duplicate related source identity "
                        f"for relationship {relation}"
                    )
                seen_relationship_sources.add(key)

    raw_ranges = data.get("unresolved_ranges", [])
    ranges = raw_ranges if isinstance(raw_ranges, list) else []
    for item in ranges:
        if not isinstance(item, dict):
            continue
        start_match = ID_RE.fullmatch(str(item.get("start", "")))
        end_match = ID_RE.fullmatch(str(item.get("end", "")))
        if not start_match or not end_match:
            continue
        lower, upper = int(start_match.group(1)), int(end_match.group(1))
        if lower > upper:
            errors.append(f"invalid unresolved range: {item['start']}..{item['end']}")
            continue
        for number in range(lower, upper + 1):
            if number in covered:
                errors.append(f"SCR-{number:04d}: overlaps explicit entry and unresolved range")
            covered.add(number)

    observed: dict[int, list[str]] = {}
    folder = root / "change-requests"
    if folder.is_dir():
        for path in folder.rglob("*"):
            if path.is_file():
                match = FILE_RE.match(path.name)
                if match:
                    observed.setdefault(int(match.group(1)), []).append(
                        path.relative_to(root).as_posix()
                    )

    for number, found in sorted(observed.items()):
        if number not in covered:
            errors.append(f"unregistered observed SCR-{number:04d}: {', '.join(found)}")

    if any(
        str(entry.get("allocation_status", "")).upper() == "FREE"
        for entry in entries
        if isinstance(entry, dict)
    ):
        errors.append("FREE is forbidden: missing/unresolved evidence must remain blocked")
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        sources = [entry.get("source", {})]
        sources.extend(
            related.get("source", {})
            for related in entry.get("related_sources", [])
            if isinstance(related, dict)
        )
        for source in sources:
            if isinstance(source, dict) and source.get("identity_sha256"):
                expected = derive_source_identity(
                    source,
                    root,
                    str(data.get("repository", "")),
                    str(data.get("source_commit", "")),
                )
                if source["identity_sha256"] != expected:
                    errors.append(
                        f"{entry.get('id', 'UNKNOWN')}: source identity_sha256 does not "
                        "match immutable source coordinates"
                    )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        print("SCR REGISTRY: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1

    data = yaml.safe_load(
        (args.root / "registry" / "scr-registry.yaml").read_text(encoding="utf-8")
    )
    unresolved_entries = sum(
        entry.get("allocation_status") == "UNRESOLVED"
        for entry in data["entries"]
        if isinstance(entry, dict)
    )
    print(
        f"SCR REGISTRY: PASS — {len(data['entries'])} entries, "
        f"{unresolved_entries} unresolved entries, "
        f"{len(data['unresolved_ranges'])} unresolved ranges; "
        "no ID auto-allocation"
    )
    identities = 0
    for entry in data["entries"]:
        if not isinstance(entry, dict):
            continue
        sources = [entry.get("source", {})]
        sources.extend(
            item.get("source", {})
            for item in entry.get("related_sources", [])
            if isinstance(item, dict)
        )
        identities += sum(isinstance(source, dict) for source in sources)
    print(f"SCR EVIDENCE: {identities} source identities are deterministically derivable")
    for residual in find_status_contradictions(args.root):
        print(f"RESIDUAL: {residual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
