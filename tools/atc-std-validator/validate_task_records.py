#!/usr/bin/env python3
"""Strict repository-local validation for ATC AI Task Records.

The validator proves syntax, record/path identity, required fields, lifecycle
state, and uniqueness inside this checkout. It does NOT claim organization-wide
uniqueness: that requires an authoritative shared allocator/ledger.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path
from typing import Any

import yaml

TASK_ID_RE = re.compile(r"^ATC-TASK-[0-9]{4,}$")
ALLOWED_STATUS = {
    "CREATED", "ASSIGNED", "IN_PROGRESS", "BLOCKED",
    "READY_FOR_REVIEW", "CHANGES_REQUESTED", "COMPLETED", "CANCELLED",
}
REQUIRED_FIELDS = {
    "id", "title", "created", "agent", "task_reference", "status",
    "findings", "actions", "next_action", "human_review",
}


class DuplicateKeyError(ValueError):
    """Raised when a YAML mapping contains a repeated key."""


class StrictTaskLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: StrictTaskLoader, node: yaml.MappingNode, deep: bool = False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise DuplicateKeyError("duplicate YAML key: %r" % key)
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


StrictTaskLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


def validate_record(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        raw = path.read_text(encoding="utf-8")
        document = yaml.load(raw, Loader=StrictTaskLoader)
    except (OSError, UnicodeError, yaml.YAMLError, DuplicateKeyError) as exc:
        return ["cannot parse %s: %s" % (path, exc)]

    if not isinstance(document, dict) or set(document) != {"task"}:
        return ["%s: root must contain exactly one 'task' mapping" % path]
    task = document.get("task")
    if not isinstance(task, dict):
        return ["%s: 'task' must be a mapping" % path]

    missing = sorted(REQUIRED_FIELDS - set(task))
    if missing:
        errors.append("%s: missing required fields: %s" % (path, ", ".join(missing)))

    task_id = task.get("id")
    if not isinstance(task_id, str) or not TASK_ID_RE.fullmatch(task_id):
        errors.append("%s: id must match ATC-TASK-NNNN (minimum four digits)" % path)
    elif path.name != task_id + ".yaml":
        errors.append("%s: filename must be %s.yaml" % (path, task_id))

    for field in ("title", "created"):
        if not isinstance(task.get(field), str) or not task[field].strip():
            errors.append("%s: %s must be a non-empty string" % (path, field))

    created = task.get("created")
    if isinstance(created, str):
        try:
            dt.datetime.fromisoformat(created.replace("Z", "+00:00"))
        except ValueError:
            errors.append("%s: created must be an ISO-8601 timestamp" % path)

    for field in ("agent", "task_reference", "human_review"):
        if not isinstance(task.get(field), dict):
            errors.append("%s: %s must be a mapping" % (path, field))

    agent = task.get("agent")
    if isinstance(agent, dict):
        if not isinstance(agent.get("id"), str) or not agent["id"].strip():
            errors.append("%s: agent.id must be a non-empty string" % path)
        if not isinstance(agent.get("version"), str) or not agent["version"].strip():
            errors.append("%s: agent.version must be a non-empty string" % path)

    reference = task.get("task_reference")
    if isinstance(reference, dict) and not isinstance(reference.get("issue"), str):
        errors.append("%s: task_reference.issue must be a string" % path)

    status = task.get("status")
    if status not in ALLOWED_STATUS:
        errors.append("%s: unsupported task status %r" % (path, status))

    for field in ("findings", "actions"):
        if not isinstance(task.get(field), list):
            errors.append("%s: %s must be a list" % (path, field))

    actions = task.get("actions")
    if isinstance(actions, list):
        action_ids = []
        for index, action in enumerate(actions):
            if not isinstance(action, dict) or not isinstance(action.get("id"), str):
                errors.append("%s: actions[%d] must contain a string id" % (path, index))
                continue
            action_ids.append(action["id"])
        if len(action_ids) != len(set(action_ids)):
            errors.append("%s: duplicate action IDs" % path)

    next_action = task.get("next_action")
    if next_action is not None and not isinstance(next_action, dict):
        errors.append("%s: next_action must be a mapping or null" % path)
    if isinstance(next_action, dict):
        next_id = next_action.get("id")
        if next_id and isinstance(actions, list):
            known = {a.get("id") for a in actions if isinstance(a, dict)}
            if next_id not in known:
                errors.append("%s: next_action.id %r is not present in actions" % (path, next_id))

    history = task.get("history")
    if not isinstance(history, list) or not history:
        errors.append("%s: history must be a non-empty list" % path)
    elif any(not isinstance(item, dict) or item.get("status") not in ALLOWED_STATUS
             for item in history):
        errors.append("%s: history contains an invalid status entry" % path)
    elif status in ALLOWED_STATUS and history[-1].get("status") != status:
        errors.append("%s: last history status does not match task.status" % path)

    return errors


def validate_directory(task_dir: Path) -> list[str]:
    if not task_dir.is_dir():
        return ["task directory missing: %s" % task_dir]

    files = sorted(task_dir.glob("*.yaml"))
    if not files:
        return ["no Task Records found in %s" % task_dir]

    errors: list[str] = []
    seen: dict[str, Path] = {}
    for path in files:
        record_errors = validate_record(path)
        errors.extend(record_errors)
        try:
            doc = yaml.load(path.read_text(encoding="utf-8"), Loader=StrictTaskLoader)
            task = doc.get("task", {}) if isinstance(doc, dict) else {}
            task_id = task.get("id") if isinstance(task, dict) else None
            if isinstance(task_id, str) and TASK_ID_RE.fullmatch(task_id):
                if task_id in seen:
                    errors.append(
                        "duplicate repository Task ID %s: %s and %s"
                        % (task_id, seen[task_id], path)
                    )
                else:
                    seen[task_id] = path
        except Exception:
            # validate_record already reports parse/schema errors; do not hide them.
            pass
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / ".github" / "ai" / "tasks",
    )
    args = parser.parse_args()
    errors = validate_directory(args.task_dir)
    if errors:
        for error in errors:
            print("TASK-RECORD FAIL: " + error)
        print("TASK-RECORD RESULT: FAIL (%d error(s))" % len(errors))
        return 1
    count = len(list(args.task_dir.glob("*.yaml")))
    print("TASK-RECORD RESULT: PASS (%d record(s); repository-local uniqueness only)" % count)
    print("TASK-RECORD LIMITATION: organization-wide uniqueness is not proven without a shared allocator/ledger")
    return 0


if __name__ == "__main__":
    sys.exit(main())
