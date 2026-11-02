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
  actions:
    - {id: ACT-001, description: "Implement validator"}
  next_action: {id: ACT-001, priority: P1, depends_on: []}
  human_review: {required: true, requested: false}
  history:
    - {status: CREATED, timestamp: "2026-11-02T01:00:00Z", note: "created"}
    - {status: IN_PROGRESS, timestamp: "2026-11-02T01:00:00Z", note: "started"}
"""


class TaskRecordValidatorTests(unittest.TestCase):
    def write(self, directory: Path, name: str, content: str) -> Path:
        path = directory / name
        path.write_text(content, encoding="utf-8")
        return path

    def test_valid_record_passes(self):
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

    def test_duplicate_ids_in_directory_fail(self):
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

    def test_missing_task_directory_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing"
            self.assertTrue(any("task directory missing" in e for e in validate_directory(missing)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
