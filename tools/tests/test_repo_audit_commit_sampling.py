#!/usr/bin/env python3
"""Regression test for V-16's non-merge sample boundary."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch, Mock

SCRIPT = Path(__file__).resolve().parents[1] / "atc-repo-audit" / "atc_repo_audit.py"
SPEC = importlib.util.spec_from_file_location("atc_repo_audit", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class NonMergeCommitSamplingTests(unittest.TestCase):
    def test_git_log_excludes_merges_before_limit_is_applied(self):
        output = "\n".join(f"{i:07x} feat: sample {i}" for i in range(20))
        fake = Mock(stdout=output)
        with patch.object(MODULE.subprocess, "run", return_value=fake) as run:
            subjects = MODULE.recent_non_merge_commit_subjects("/repo", 20)
        self.assertEqual(len(subjects), 20)
        self.assertTrue(all(subject.startswith("feat:") for subject in subjects))
        args = run.call_args.args[0]
        self.assertIn("--no-merges", args)
        self.assertEqual(args[-1], "-20")


if __name__ == "__main__":
    unittest.main()
