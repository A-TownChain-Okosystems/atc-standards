import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPT = Path(__file__).resolve().parents[1] / "validate_scr_registry.py"
spec = importlib.util.spec_from_file_location("scr_validator", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ScrRegistryTests(unittest.TestCase):
    def test_repository_inventory_passes(self):
        self.assertEqual(module.validate(), [])

    def _fixture(self, root, entries, ranges=None):
        (root / "registry").mkdir(exist_ok=True)
        (root / "schemas").mkdir(exist_ok=True)
        schema_src = SCRIPT.parents[2] / "schemas" / "scr-registry.schema.json"
        (root / "schemas" / "scr-registry.schema.json").write_text(
            schema_src.read_text(encoding="utf-8"), encoding="utf-8"
        )
        payload = {
            "registry_version": 1,
            "repository": "A-TownChain-Okosystems/atc-standards",
            "source_ref": "test",
            "source_commit": "a" * 40,
            "allocation_policy": {
                "unknown_is_blocked": True,
                "missing_file_is_not_free": True,
                "automatic_number_assignment": False,
                "reuse_permitted": False,
            },
            "entries": entries,
            "unresolved_ranges": ranges or [],
        }
        path = root / "registry" / "scr-registry.yaml"
        path.write_text(yaml.safe_dump(payload), encoding="utf-8")
        return module.validate(root, path, root / "schemas" / "scr-registry.schema.json")

    def test_duplicate_ids_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = {
                "id": "SCR-0001",
                "allocation_status": "RESERVED",
                "metadata_status": "UNRECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {"kind": "HISTORICAL_REFERENCE"},
                "notes": "fixture",
            }
            errors = self._fixture(root, [entry, dict(entry)])
            self.assertTrue(any("duplicate SCR IDs" in error for error in errors))

    def test_unregistered_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "change-requests").mkdir()
            (root / "change-requests" / "SCR-9999.md").write_text("# fixture", encoding="utf-8")
            errors = self._fixture(root, [])
            self.assertTrue(any("unregistered observed SCR-9999" in error for error in errors))

    def test_entry_range_overlap_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = {
                "id": "SCR-0005",
                "allocation_status": "RESERVED",
                "metadata_status": "UNRECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {"kind": "HISTORICAL_REFERENCE"},
                "notes": "fixture",
            }
            blocked = {
                "start": "SCR-0005",
                "end": "SCR-0007",
                "allocation_status": "CONFLICT",
                "evidence": "fixture",
                "required_action": "reconcile",
            }
            errors = self._fixture(root, [entry], [blocked])
            self.assertTrue(any("overlaps explicit entry" in error for error in errors))

    def test_file_source_filename_must_match_registry_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            requests = root / "change-requests"
            requests.mkdir()
            (requests / "SCR-0002.md").write_text("# fixture", encoding="utf-8")
            entry = {
                "id": "SCR-0001",
                "allocation_status": "ASSIGNED",
                "metadata_status": "UNRECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {
                    "kind": "FILE",
                    "path": "change-requests/SCR-0002.md",
                },
                "notes": "fixture",
            }
            errors = self._fixture(root, [entry])
            self.assertIn(
                "source filename SCR ID does not match registry entry",
                "\\n".join(errors),
            )

    def test_missing_referenced_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = {
                "id": "SCR-0001",
                "allocation_status": "ASSIGNED",
                "metadata_status": "UNRECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {
                    "kind": "FILE",
                    "path": "change-requests/SCR-0001.md",
                },
                "notes": "fixture",
            }
            errors = self._fixture(root, [entry])
            self.assertIn("referenced source file missing", "\n".join(errors))

    def test_free_identifier_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = {
                "id": "SCR-0001",
                "allocation_status": "FREE",
                "metadata_status": "UNRECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {"kind": "HISTORICAL_REFERENCE"},
                "notes": "fixture",
            }
            errors = self._fixture(root, [entry])
            self.assertTrue(any("FREE is forbidden" in error for error in errors))

    def test_historical_source_file_must_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = {
                "id": "SCR-0001",
                "allocation_status": "UNRESOLVED",
                "metadata_status": "UNRECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {
                    "kind": "HISTORICAL_REFERENCE",
                    "path": "missing-evidence.md",
                },
                "notes": "fixture",
            }
            errors = self._fixture(root, [entry])
            self.assertIn("referenced source file missing", "\n".join(errors))

    def test_source_path_traversal_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = {
                "id": "SCR-0001",
                "allocation_status": "UNRESOLVED",
                "metadata_status": "UNRECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {
                    "kind": "HISTORICAL_REFERENCE",
                    "path": "../outside.md",
                },
                "notes": "fixture",
            }
            errors = self._fixture(root, [entry])
            self.assertIn("source path escapes repository root", "\n".join(errors))

    def test_symlink_source_path_cannot_escape_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            outside = Path(tmp) / "outside.md"
            outside.write_text("# outside", encoding="utf-8")
            requests = root / "change-requests"
            requests.mkdir()
            (requests / "SCR-0001.md").symlink_to(outside)
            entry = {
                "id": "SCR-0001",
                "allocation_status": "UNRESOLVED",
                "metadata_status": "UNRECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {
                    "kind": "HISTORICAL_REFERENCE",
                    "path": "change-requests/SCR-0001.md",
                },
                "notes": "fixture",
            }
            errors = self._fixture(root, [entry])
            self.assertIn(
                "source path escapes repository root",
                "\\n".join(errors),
            )

    def test_non_object_registry_fails_without_crashing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "registry").mkdir()
            (root / "schemas").mkdir()
            schema_src = SCRIPT.parents[2] / "schemas" / "scr-registry.schema.json"
            schema_path = root / "schemas" / "scr-registry.schema.json"
            schema_path.write_text(schema_src.read_text(encoding="utf-8"), encoding="utf-8")
            registry_path = root / "registry" / "scr-registry.yaml"
            registry_path.write_text("[]", encoding="utf-8")
            errors = module.validate(root, registry_path, schema_path)
            self.assertEqual(errors, ["registry root must be an object"])

    def test_pull_request_url_must_bind_repository_and_number(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = {
                "id": "SCR-0001",
                "allocation_status": "RESERVED",
                "metadata_status": "UNRECONCILED",
                "lifecycle_status": "REVIEW",
                "decision": "PENDING",
                "source": {
                    "kind": "PULL_REQUEST",
                    "pr": 116,
                    "url": "https://github.com/attacker/other-repo/pull/999",
                },
                "notes": "fixture",
            }
            errors = self._fixture(root, [entry])
            self.assertIn(
                "pull-request URL does not bind repository and PR number",
                "\\n".join(errors),
            )

    def test_mixed_historical_source_validates_external_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / "evidence.md"
            evidence.write_text("# fixture", encoding="utf-8")
            entry = {
                "id": "SCR-0001",
                "allocation_status": "UNRESOLVED",
                "metadata_status": "UNRECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {
                    "kind": "HISTORICAL_REFERENCE",
                    "path": "evidence.md",
                    "repository": "A-TownChain-Okosystems/example",
                    "commit": "a" * 40,
                    "url": "https://github.com/A-TownChain-Okosystems/example/commit/" + "b" * 40,
                },
                "notes": "fixture",
            }
            errors = self._fixture(root, [entry])
            self.assertIn(
                "external source URL does not bind repository and commit",
                "\\n".join(errors),
            )

    def test_partial_external_historical_binding_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / "evidence.md"
            evidence.write_text("# fixture", encoding="utf-8")
            entry = {
                "id": "SCR-0001",
                "allocation_status": "UNRESOLVED",
                "metadata_status": "UNRECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {
                    "kind": "HISTORICAL_REFERENCE",
                    "path": "evidence.md",
                    "repository": "A-TownChain-Okosystems/example",
                },
                "notes": "fixture",
            }
            errors = self._fixture(root, [entry])
            self.assertIn(
                "external historical source requires repository, commit and URL",
                "\\n".join(errors),
            )

    def test_external_reference_url_must_bind_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = {
                "id": "SCR-0001",
                "allocation_status": "UNRESOLVED",
                "metadata_status": "UNRECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {
                    "kind": "HISTORICAL_REFERENCE",
                    "repository": "A-TownChain-Okosystems/example",
                    "commit": "a" * 40,
                    "url": "https://github.com/A-TownChain-Okosystems/example/commit/" + "b" * 40,
                },
                "notes": "fixture",
            }
            errors = self._fixture(root, [entry])
            self.assertIn("external source URL does not bind", "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
