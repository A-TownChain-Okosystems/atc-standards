import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "verify_external_sources.py"
SPEC = importlib.util.spec_from_file_location("verify_external_sources", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ExternalSourceVerificationTests(unittest.TestCase):
    def _manifest(self, path: Path, blob_sha: str = "b" * 40) -> dict:
        data = {
            "schema_version": 1,
            "repository": "A-TownChain-Okosystems/atc-standards",
            "sources": [
                {
                    "scr_id": "SCR-0133",
                    "repository": "A-TownChain-Okosystems/aurora-ai",
                    "commit": "a" * 40,
                    "path": path.as_posix(),
                    "blob_sha": blob_sha,
                }
            ],
        }
        return data

    def test_manifest_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            data = self._manifest(Path("../outside.txt"))
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(MODULE.VerificationError, "safe repository-relative path"):
                MODULE.load_manifest(path)

    def test_manifest_rejects_repository_outside_organization(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            data = self._manifest(Path("src/lib.rs"))
            data["sources"][0]["repository"] = "untrusted-owner/repo"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(MODULE.VerificationError, "allowed organization"):
                MODULE.load_manifest(path)

    def test_exact_commit_tree_and_blob_are_verified(self):
        expected_blob = "b" * 40
        tree_sha = "c" * 40
        calls = []

        def fake_run(command, **kwargs):
            calls.append(command)
            args = command[1:]
            stdout = ""
            if args[:2] == ["rev-parse", "--verify"]:
                stdout = tree_sha if args[2].endswith("^{tree}") else expected_blob
            elif args[:2] == ["cat-file", "-t"]:
                stdout = "blob"
            return subprocess.CompletedProcess(command, 0, stdout, "")

        data = {
            "schema_version": 1,
            "repository": "A-TownChain-Okosystems/atc-standards",
            "sources": [
                {
                    "scr_id": "SCR-0133",
                    "repository": "A-TownChain-Okosystems/aurora-ai",
                    "commit": "a" * 40,
                    "path": "src/first.rs",
                    "blob_sha": expected_blob,
                },
                {
                    "scr_id": "SCR-0133",
                    "repository": "A-TownChain-Okosystems/aurora-ai",
                    "commit": "a" * 40,
                    "path": "src/second.rs",
                    "blob_sha": expected_blob,
                },
            ],
        }
        report = MODULE.verify_manifest(data, runner=fake_run)
        self.assertEqual(report["verified_count"], 2)
        self.assertEqual(report["failed_count"], 0)
        self.assertTrue(all(item["tree_sha"] == tree_sha for item in report["sources"]))
        fetches = [call for call in calls if len(call) > 1 and call[1] == "fetch"]
        self.assertEqual(len(fetches), 1)

    def test_blob_mismatch_fails_closed(self):
        calls = []

        def fake_run(command, **kwargs):
            calls.append(command)
            args = command[1:]
            stdout = ""
            if args[:2] == ["rev-parse", "--verify"]:
                stdout = "c" * 40 if args[2].endswith("^{tree}") else "d" * 40
            elif args[:2] == ["cat-file", "-t"]:
                stdout = "blob"
            return subprocess.CompletedProcess(command, 0, stdout, "")

        data = {
            "schema_version": 1,
            "repository": "A-TownChain-Okosystems/atc-standards",
            "sources": [
                {
                    "scr_id": "SCR-0133",
                    "repository": "A-TownChain-Okosystems/aurora-ai",
                    "commit": "a" * 40,
                    "path": "src/file.rs",
                    "blob_sha": "b" * 40,
                }
            ],
        }
        with self.assertRaisesRegex(MODULE.VerificationError, "blob mismatch"):
            MODULE.verify_manifest(data, runner=fake_run)


if __name__ == "__main__":
    unittest.main()
