import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "atc_repo_audit.py"
SPEC = importlib.util.spec_from_file_location("atc_repo_audit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ConventionalCommitThresholdTests(unittest.TestCase):
    def _status(self, conventional_count: int, total: int = 20) -> str:
        subjects = [
            f"feat(scope): valid commit {index}"
            for index in range(conventional_count)
        ]
        subjects.extend(
            f"legacy commit {index}" for index in range(total - conventional_count)
        )
        output = "\n".join(f"{index:040x} {subject}" for index, subject in enumerate(subjects))
        original_run = subprocess.run

        def fake_run(command, *args, **kwargs):
            if command[:2] == ["git", "log"]:
                return subprocess.CompletedProcess(command, 0, output, "")
            return original_run(command, *args, **kwargs)

        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(MODULE.subprocess, "run", side_effect=fake_run):
                audit = MODULE.audit_repo(tmp, "R3")
        return next(status for rule, status, *_ in audit.results if rule == "V-16")

    def test_79_percent_is_a_must_fail(self):
        self.assertEqual(self._status(15), "FAIL")

    def test_80_percent_is_pass(self):
        self.assertEqual(self._status(16), "PASS")


if __name__ == "__main__":
    unittest.main()
