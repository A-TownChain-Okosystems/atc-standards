#!/usr/bin/env python3
"""Read-only, fail-closed validator for the independent SCR relationship registry."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SCR_ID_RE = re.compile(r"^SCR-[0-9]{4}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, yaml.MappingNode):
            return super().construct_mapping(node, deep=deep)
        self.flatten_mapping(node)
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in result:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    f"found duplicate key {key!r}", key_node.start_mark,
                )
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def _load_yaml(path: Path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeySafeLoader)


def _source_identities(registry: dict) -> set[str]:
    identities = set()
    for entry in registry.get("entries", []):
        if not isinstance(entry, dict):
            continue
        sources = [entry.get("source")]
        sources.extend(
            item.get("source")
            for item in entry.get("related_sources", [])
            if isinstance(item, dict)
        )
        for source in sources:
            if isinstance(source, dict):
                digest = source.get("identity_sha256")
                if isinstance(digest, str) and SHA256_RE.fullmatch(digest):
                    identities.add(digest)
    return identities


def _reachable(graph: dict[str, set[str]], start: str, target: str) -> bool:
    pending = [start]
    visited = set()
    while pending:
        node = pending.pop()
        if node == target:
            return True
        if node in visited:
            continue
        visited.add(node)
        pending.extend(sorted(graph.get(node, ()), reverse=True))
    return False


def validate(
    root: Path = ROOT,
    relationship_path: Path | None = None,
    schema_path: Path | None = None,
    registry_path: Path | None = None,
    semantics_path: Path | None = None,
    mode: str = "structural",
) -> list[str]:
    """Validate structure, endpoint/evidence resolution, and approved graph rules."""
    if mode not in {"structural", "normative"}:
        return ["mode must be structural or normative"]
    relationship_path = relationship_path or root / "registry/scr-relationships/v1/relationships.yaml"
    schema_path = schema_path or root / "schemas/scr-relationships/v1/relationships.schema.json"
    registry_path = registry_path or root / "registry/scr-registry.yaml"
    semantics_path = semantics_path or root / "registry/scr-relationships/v1/semantics.yaml"

    try:
        data = _load_yaml(relationship_path)
        registry = _load_yaml(registry_path)
        semantics = _load_yaml(semantics_path)
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"cannot load relationship inputs: {exc}"]

    if not isinstance(data, dict):
        return ["relationship registry root must be an object"]
    if not isinstance(registry, dict) or registry.get("registry_version") != 1:
        return ["SCR identity registry is missing or has an unsupported registry_version"]
    if not isinstance(semantics, dict) or semantics.get("semantics_manifest_version") != 1:
        return ["semantics manifest is missing or has an unsupported version"]
    if semantics.get("status") != "NON_NORMATIVE":
        return ["semantics manifest status must remain NON_NORMATIVE until governance approval"]

    errors = [
        f"schema: {error.message} at {list(error.absolute_path)}"
        for error in Draft202012Validator(schema).iter_errors(data)
    ]
    candidates = semantics.get("candidate_relation_types")
    approved = semantics.get("approved_relation_types")
    acyclic = semantics.get("acyclic_relation_types")
    if not isinstance(candidates, list) or not isinstance(approved, list) or not isinstance(acyclic, list):
        return errors + ["semantics manifest candidate/approved/acyclic lists are invalid"]
    candidate_tokens = {
        item.get("token") for item in candidates
        if isinstance(item, dict) and item.get("status") == "PROPOSED"
    }
    if len(candidate_tokens) != len(candidates):
        errors.append("semantics manifest contains malformed or duplicate candidate entries")
    if len(set(approved)) != len(approved) or not set(approved).issubset(candidate_tokens):
        errors.append("approved relation types must be unique declared candidate tokens")
    if len(set(acyclic)) != len(acyclic) or not set(acyclic).issubset(set(approved)):
        errors.append("acyclic relation types must be unique approved relation types")

    entries = registry.get("entries", [])
    canonical_ids = {
        entry.get("id")
        for entry in entries
        if isinstance(entry, dict)
        and entry.get("allocation_status") == "ASSIGNED"
        and isinstance(entry.get("id"), str)
        and SCR_ID_RE.fullmatch(entry["id"])
    }
    evidence_ids = _source_identities(registry)
    relationships = data.get("relationships", [])
    if not isinstance(relationships, list):
        return errors + ["relationships must be an array"]

    seen_ids = set()
    seen_edges = set()
    graphs = {token: {} for token in acyclic}
    for index, item in enumerate(relationships):
        if not isinstance(item, dict):
            continue
        label = f"relationships[{index}]"
        rid = item.get("relationship_id")
        source = item.get("from_scr")
        target = item.get("to_scr")
        token = item.get("relation_type")
        if isinstance(rid, str):
            if rid in seen_ids:
                errors.append(f"{label}: duplicate relationship_id {rid}")
            seen_ids.add(rid)
        if isinstance(source, str) and SCR_ID_RE.fullmatch(source) and source not in canonical_ids:
            errors.append(f"{label}: unresolved or non-assigned from_scr endpoint {source}")
        if isinstance(target, str) and SCR_ID_RE.fullmatch(target) and target not in canonical_ids:
            errors.append(f"{label}: unresolved or non-assigned to_scr endpoint {target}")
        if isinstance(source, str) and isinstance(target, str) and source == target:
            errors.append(f"{label}: self-edge is rejected by the v1 technical safeguard")
        edge = (source, target, token)
        if edge in seen_edges:
            errors.append(f"{label}: duplicate relationship edge {edge}")
        seen_edges.add(edge)

        if token not in candidate_tokens:
            errors.append(f"{label}: unknown relation_type {token!r}")
        elif mode == "normative" and (
            token not in approved or item.get("governance_status") != "APPROVED"
        ):
            errors.append(f"{label}: relation_type {token} is not governance-approved for normative use")

        refs = item.get("evidence_refs")
        if isinstance(refs, list):
            for ref_index, ref in enumerate(refs):
                if not isinstance(ref, dict):
                    continue
                digest = ref.get("identity_sha256")
                if isinstance(digest, str) and SHA256_RE.fullmatch(digest) and digest not in evidence_ids:
                    errors.append(
                        f"{label}.evidence_refs[{ref_index}]: unresolved evidence identity {digest}"
                    )

        if token in graphs and isinstance(source, str) and isinstance(target, str):
            graph = graphs[token]
            if _reachable(graph, target, source):
                errors.append(f"{label}: cycle detected for approved acyclic relation_type {token}")
            graph.setdefault(source, set()).add(target)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--mode", choices=("structural", "normative"), default="structural")
    args = parser.parse_args()
    errors = validate(root=args.root, mode=args.mode)
    if errors:
        print("SCR RELATIONSHIP REGISTRY: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1
    print(f"SCR RELATIONSHIP REGISTRY: PASS — mode={args.mode}; read-only; no SCR lifecycle writes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
