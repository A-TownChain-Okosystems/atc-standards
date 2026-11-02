#!/usr/bin/env python3
"""Unit tests for validate_task_records.py."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "validate_task_records.py"
MODULE_SPEC = importlib.util.spec_from_file_location("validate_task_records", MODULE_PATH)
MODULE = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(MODULE)
validate_directory = MODULE.validate_directory
validate_record = MODULE.validate_record


VALID = """task:
  id: ATC-TASK-0161
  title: "Validator implementation"
  created: "2026-11-02T01:00:00Z"
  agent: {id: ATC-AI-ARCH-001, version: "1.1.0"}
  task_reference: {issue: "#122", milestone: null, standard: "ATC-STD-AI-DEV-004"}
  status: IN_PROGRESS
  findings: [F-122-01]
  actions: [ACT-001, ACT-002]
  next_action: {id: ACT-001, priority: P1, depends_on: []}
  human_review: {required: true, requested: false}
  history:
    - {status: CREATED, timestamp: "2026-11-02T01:00:00Z", note: "created"}
    - {status: ASSIGNED, timestamp: "2026-11-02T01:00:30Z", note: "assigned"}
    - {status: IN_PROGRESS, timestamp: "2026-11-02T01:01:00Z", note: "started"}
"""


class TaskRecordValidatorTests(unittest.TestCase):
    def write(self, directory: Path, name: str, content: str) -> Path:
        path = directory / name
        path.write_text(content, encoding="utf-8")
        return path

    def test_normative_action_id_list_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(Path(tmp), "ATC-TASK-0161.yaml", VALID)
            self.assertEqual(validate_record(path), [])

    def test_noncanonical_id_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(
                Path(tmp),
                "TASK-20261102-001.yaml",
                VALID.replace("ATC-TASK-0161", "TASK-20261102-001"),
            )
            self.assertTrue(any("ATC-TASK-NNNN" in e for e in validate_record(path)))

    def test_filename_must_match_record_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(Path(tmp), "ATC-TASK-0162.yaml", VALID)
            self.assertTrue(any("filename must be" in e for e in validate_record(path)))

    def test_duplicate_yaml_key_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(
                Path(tmp),
                "ATC-TASK-0161.yaml",
                VALID.replace("  status: IN_PROGRESS", "  status: CREATED\n  status: IN_PROGRESS"),
            )
            self.assertTrue(any("duplicate YAML key" in e for e in validate_record(path)))

    def test_duplicate_action_ids_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(
                Path(tmp),
                "ATC-TASK-0161.yaml",
                VALID.replace("actions: [ACT-001, ACT-002]", "actions: [ACT-001, ACT-001]"),
            )
            self.assertTrue(any("duplicate action IDs" in e for e in validate_record(path)))

    def test_action_object_shape_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(
                Path(tmp),
                "ATC-TASK-0161.yaml",
                VALID.replace("actions: [ACT-001, ACT-002]", "actions: [{id: ACT-001}]"),
            )
            self.assertTrue(any("Action ID matching ACT-NNN" in e for e in validate_record(path)))

    def test_unhashable_status_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(
                Path(tmp),
                "ATC-TASK-0161.yaml",
                VALID.replace("status: IN_PROGRESS", "status: [IN_PROGRESS]"),
            )
            self.assertTrue(any("unsupported task status" in e for e in validate_record(path)))

    def test_filename_mismatch_directory_duplicate_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.write(directory, "ATC-TASK-0161.yaml", VALID)
            self.write(directory, "ATC-TASK-0161-copy.yaml", VALID)
            errors = validate_directory(directory)
            self.assertTrue(any("duplicate repository Task ID" in e for e in errors))

    def test_history_must_end_in_current_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(
                Path(tmp),
                "ATC-TASK-0161.yaml",
                VALID.replace("status: IN_PROGRESS, timestamp:", "status: CREATED, timestamp:"),
            )
            self.assertTrue(any("last history status" in e for e in validate_record(path)))


    def test_finding_ids_must_match_normative_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(Path(tmp), "ATC-TASK-0161.yaml", VALID.replace("F-122-01", "F-12"))
            self.assertTrue(any("Finding ID matching F-NNN" in e for e in validate_record(path)))

    def test_next_action_dependency_must_exist_in_actions(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(
                Path(tmp),
                "ATC-TASK-0161.yaml",
                VALID.replace("depends_on: []", "depends_on: [ACT-099]"),
            )
            self.assertTrue(
                any(
                    "dependency" in e and "not present in actions" in e
                    for e in validate_record(path)
                )
            )

    def test_next_action_id_must_exist_in_actions(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(
                Path(tmp), "ATC-TASK-0161.yaml", VALID.replace("id: ACT-001", "id: ACT-099")
            )
            self.assertTrue(
                any(
                    "next_action.id" in e and "not present in actions" in e
                    for e in validate_record(path)
                )
            )

    def test_history_timestamp_is_required_and_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(
                Path(tmp),
                "ATC-TASK-0161.yaml",
                VALID.replace('timestamp: "2026-11-02T01:00:00Z"', 'timestamp: "not-a-time"', 1),
            )
            self.assertTrue(any("valid ISO-8601 timestamp" in e for e in validate_record(path)))

    def test_history_rejects_skipped_lifecycle_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            invalid = VALID.replace(
                '    - {status: ASSIGNED, timestamp: "2026-11-02T01:00:30Z", note: "assigned"}\n',
                "",
            )
            path = self.write(Path(tmp), "ATC-TASK-0161.yaml", invalid)
            self.assertTrue(any("invalid history transition" in e for e in validate_record(path)))

    def test_history_note_is_not_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(
                Path(tmp), "ATC-TASK-0161.yaml", VALID.replace(', note: "created"', "")
            )
            self.assertEqual(validate_record(path), [])

    def test_task_reference_nullable_fields_accept_null(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(
                Path(tmp),
                "ATC-TASK-0161.yaml",
                VALID.replace('standard: "ATC-STD-AI-DEV-004"', "standard: null"),
            )
            self.assertEqual(validate_record(path), [])

    def test_task_reference_rejects_empty_issue(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(
                Path(tmp), "ATC-TASK-0161.yaml", VALID.replace('issue: "#122"', 'issue: ""')
            )
            self.assertTrue(
                any("issue must be a non-empty string" in e for e in validate_record(path))
            )

    def test_missing_task_directory_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing"
            self.assertTrue(any("task directory missing" in e for e in validate_directory(missing)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
