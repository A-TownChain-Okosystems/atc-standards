import importlib.util
import tempfile
import unittest
from unittest.mock import patch
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

    def test_reconciled_metadata_can_have_unknown_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            requests = root / "change-requests"
            requests.mkdir()
            (requests / "SCR-0001.md").write_text("# SCR-0001", encoding="utf-8")
            entry = {
                "id": "SCR-0001",
                "allocation_status": "ASSIGNED",
                "metadata_status": "RECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {
                    "kind": "FILE",
                    "path": "change-requests/SCR-0001.md",
                },
                "notes": "Metadata is reconciled; lifecycle decision remains independent.",
            }
            errors = self._fixture(root, [entry])
            self.assertEqual(errors, [])

    def test_related_sources_support_external_pull_request_bindings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            requests = root / "change-requests"
            requests.mkdir()
            (requests / "SCR-0001.md").write_text("# SCR-0001", encoding="utf-8")
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
                "related_sources": [
                    {
                        "relationship": "IMPLEMENTATION_EVIDENCE",
                        "scope": "External organization hub implementation",
                        "source": {
                            "kind": "HISTORICAL_REFERENCE",
                            "repository": "A-TownChain-Okosystems/.github",
                            "pr": 8,
                            "url": "https://github.com/A-TownChain-Okosystems/.github/pull/8",
                        },
                    }
                ],
                "notes": "Primary and related evidence are separate bindings.",
            }
            with patch(
                "scr_validator.subprocess.run",
                side_effect=[
                    type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})(),
                    type("Result", (), {"returncode": 0, "stdout": "AA:BB", "stderr": ""})(),
                ],
            ):
                self.assertEqual(self._fixture(root, [entry]), [])

    def test_related_external_pull_request_url_must_bind_repository_and_number(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = {
                "id": "SCR-0001",
                "allocation_status": "UNRESOLVED",
                "metadata_status": "UNRECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {"kind": "HISTORICAL_REFERENCE"},
                "related_sources": [
                    {
                        "relationship": "IMPLEMENTATION_EVIDENCE",
                        "scope": "External organization hub implementation",
                        "source": {
                            "kind": "HISTORICAL_REFERENCE",
                            "repository": "A-TownChain-Okosystems/.github",
                            "pr": 8,
                            "url": "https://github.com/A-TownChain-Okosystems/atc-standards/pull/8",
                        },
                    }
                ],
                "notes": "Mismatched repository binding must fail.",
            }
            errors = self._fixture(root, [entry])
            self.assertTrue(
                any(
                    "historical pull-request URL does not bind repository and PR number" in e
                    for e in errors
                ),
                errors,
            )

    def test_related_source_relationship_must_be_known(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entry = {
                "id": "SCR-0001",
                "allocation_status": "UNRESOLVED",
                "metadata_status": "UNRECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {"kind": "HISTORICAL_REFERENCE"},
                "related_sources": [
                    {
                        "relationship": "OWNER_APPROVED_AND_CLOSED",
                        "scope": "Unverified assertion",
                        "source": {"kind": "HISTORICAL_REFERENCE"},
                    }
                ],
                "notes": "Unknown relationship must fail schema validation.",
            }
            errors = self._fixture(root, [entry])
            self.assertTrue(any("OWNER_APPROVED_AND_CLOSED" in e for e in errors), errors)

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

    def test_symlink_loop_source_path_fails_without_crashing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            requests = root / "change-requests"
            requests.mkdir()
            loop = requests / "SCR-0001.md"
            loop.symlink_to(loop)
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
            self.assertTrue(
                any("cannot safely resolve source path" in error for error in errors),
                errors,
            )

    def test_source_kind_rejects_unrelated_or_conflicting_fields(self):
        cases = [
            (
                "FILE",
                {
                    "kind": "FILE",
                    "path": "change-requests/SCR-0001.md",
                    "pr": 92,
                    "url": "https://github.com/A-TownChain-Okosystems/atc-standards/pull/92",
                },
                "source fields invalid for FILE",
            ),
            (
                "PULL_REQUEST",
                {
                    "kind": "PULL_REQUEST",
                    "pr": 92,
                    "url": "https://github.com/A-TownChain-Okosystems/atc-standards/pull/92",
                    "path": "change-requests/SCR-0001.md",
                },
                "source fields invalid for PULL_REQUEST",
            ),
            (
                "HISTORICAL_REFERENCE",
                {
                    "kind": "HISTORICAL_REFERENCE",
                    "path": "evidence.md",
                    "pr": 92,
                    "repository": "A-TownChain-Okosystems/example",
                    "commit": "a" * 40,
                    "url": "https://github.com/A-TownChain-Okosystems/example/commit/" + "a" * 40,
                },
                "source bindings are mutually exclusive",
            ),
        ]
        for kind, source, expected in cases:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                if kind == "HISTORICAL_REFERENCE":
                    (root / "evidence.md").write_text("# fixture", encoding="utf-8")
                entry = {
                    "id": "SCR-0001",
                    "allocation_status": "RESERVED"
                    if kind == "PULL_REQUEST"
                    else ("ASSIGNED" if kind == "FILE" else "UNRESOLVED"),
                    "metadata_status": "UNRECONCILED",
                    "lifecycle_status": "REVIEW" if kind == "PULL_REQUEST" else "UNKNOWN",
                    "decision": "PENDING" if kind == "PULL_REQUEST" else "UNKNOWN",
                    "source": source,
                    "notes": "fixture",
                }
                errors = self._fixture(root, [entry])
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_duplicate_yaml_mapping_keys_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "registry").mkdir()
            (root / "schemas").mkdir()
            schema_src = SCRIPT.parents[2] / "schemas" / "scr-registry.schema.json"
            schema_path = root / "schemas" / "scr-registry.schema.json"
            schema_path.write_text(schema_src.read_text(encoding="utf-8"), encoding="utf-8")
            registry_path = root / "registry" / "scr-registry.yaml"
            registry_path.write_text(
                "registry_version: 1\nregistry_version: 1\n",
                encoding="utf-8",
            )
            errors = module.validate(root, registry_path, schema_path)
            self.assertTrue(any("duplicate key" in error for error in errors))

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

    def test_historical_pull_request_url_must_bind_number(self):
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
                    "pr": 92,
                    "url": "https://github.com/A-TownChain-Okosystems/atc-standards/pull/999",
                },
                "notes": "fixture",
            }
            errors = self._fixture(root, [entry])
            self.assertIn(
                "historical pull-request URL does not bind repository and PR number",
                "\\n".join(errors),
            )

    def test_partial_historical_pull_request_binding_fails(self):
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
                    "url": "https://github.com/A-TownChain-Okosystems/atc-standards/pull/92",
                },
                "notes": "fixture",
            }
            errors = self._fixture(root, [entry])
            self.assertIn(
                "historical pull-request URL does not bind repository and PR number",
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

    def test_file_blob_sha_rejects_changed_source_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "change-requests"
            folder.mkdir()
            (folder / "SCR-0001.md").write_text("# SCR-0001\\n", encoding="utf-8")
            entry = {
                "id": "SCR-0001",
                "allocation_status": "ASSIGNED",
                "metadata_status": "RECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {
                    "kind": "FILE",
                    "path": "change-requests/SCR-0001.md",
                    "blob_sha": "0" * 40,
                },
                "notes": "Fixture for immutable Git blob verification.",
            }
            errors = self._fixture(root, [entry])
            self.assertTrue(any("blob SHA mismatch" in error for error in errors), errors)

    def test_signature_validity_does_not_imply_decision_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "change-requests"
            folder.mkdir()
            (folder / "SCR-0001.md").write_text("# SCR-0001", encoding="utf-8")
            entry = {
                "id": "SCR-0001",
                "allocation_status": "ASSIGNED",
                "metadata_status": "RECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {
                    "kind": "FILE",
                    "path": "change-requests/SCR-0001.md",
                    "commit": "a" * 40,
                    "attestation": {
                        "signature_status": "VERIFIED",
                        "signer_identity": "AA:BB",
                        "authority_status": "NOT_ESTABLISHED",
                    },
                },
                "notes": "A valid signature is not an authority decision.",
            }
            self.assertEqual(self._fixture(root, [entry]), [])

    def test_established_authority_requires_authority_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "change-requests"
            folder.mkdir()
            (folder / "SCR-0001.md").write_text("# SCR-0001", encoding="utf-8")
            entry = {
                "id": "SCR-0001",
                "allocation_status": "ASSIGNED",
                "metadata_status": "RECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {
                    "kind": "FILE",
                    "path": "change-requests/SCR-0001.md",
                    "attestation": {
                        "signature_status": "UNSIGNED",
                        "authority_status": "ESTABLISHED",
                    },
                },
                "notes": "Authority needs its own evidence.",
            }
            errors = self._fixture(root, [entry])
            self.assertTrue(any("authority_evidence" in error for error in errors), errors)



    def test_status_contradiction_detector_parses_frontmatter_newlines(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            standards = root / "standards"
            standards.mkdir()
            (standards / "ATC-STD-041.md").write_text(
                "---\nstatus: approved\nnormative: true\neffective_date: null\n---\n"
                "This standard is not effective until the §9 release gate is satisfied.\n",
                encoding="utf-8",
            )
            residuals = module.find_status_contradictions(root)
            self.assertEqual(len(residuals), 1, residuals)
            self.assertIn("ATC-STD-041.md", residuals[0])

    def test_source_identity_is_deterministic_and_uses_registry_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "change-requests"
            folder.mkdir()
            (folder / "SCR-0001.md").write_text("# SCR-0001", encoding="utf-8")
            source = {"kind": "FILE", "path": "change-requests/SCR-0001.md"}
            first = module.derive_source_identity(
                source, root, "A-TownChain-Okosystems/atc-standards", "a" * 40
            )
            second = module.derive_source_identity(
                source, root, "A-TownChain-Okosystems/atc-standards", "a" * 40
            )
            other_commit = module.derive_source_identity(
                source, root, "A-TownChain-Okosystems/atc-standards", "b" * 40
            )
            self.assertEqual(first, second)
            self.assertNotEqual(first, other_commit)

    def test_source_identity_does_not_read_path_outside_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            outside = Path(tmp) / "outside-secret.txt"
            outside.write_text("must not be read", encoding="utf-8")
            source = {"kind": "HISTORICAL_REFERENCE", "path": "../outside-secret.txt"}
            identity = module.derive_source_identity(
                source, root, "A-TownChain-Okosystems/atc-standards"
            )
            self.assertRegex(identity, r"^[0-9a-f]{64}$")

    def test_verified_attestation_requires_commit_and_signer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "change-requests"
            folder.mkdir()
            (folder / "SCR-0001.md").write_text("# SCR-0001", encoding="utf-8")
            entry = {
                "id": "SCR-0001",
                "allocation_status": "ASSIGNED",
                "metadata_status": "RECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {
                    "kind": "FILE",
                    "path": "change-requests/SCR-0001.md",
                    "attestation": {
                        "signature_status": "VERIFIED",
                        "signer_identity": "AA:BB",
                        "authority_status": "NOT_ESTABLISHED",
                    },
                },
                "notes": "A verified signature must bind an actual commit.",
            }
            errors = self._fixture(root, [entry])
            self.assertTrue(any("requires a commit SHA" in error for error in errors), errors)




    def test_identity_sha256_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "change-requests"
            folder.mkdir()
            (folder / "SCR-0001.md").write_text("# SCR-0001", encoding="utf-8")
            entry = {
                "id": "SCR-0001",
                "allocation_status": "ASSIGNED",
                "metadata_status": "RECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {
                    "kind": "FILE",
                    "path": "change-requests/SCR-0001.md",
                    "identity_sha256": "0" * 64,
                },
                "notes": "Declared identity must match immutable coordinates.",
            }
            errors = self._fixture(root, [entry])
            self.assertTrue(
                any("identity_sha256 does not match" in error for error in errors), errors
            )

    def test_verified_attestation_runs_git_signature_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "change-requests"
            folder.mkdir()
            (folder / "SCR-0001.md").write_text("# SCR-0001", encoding="utf-8")
            entry = {
                "id": "SCR-0001",
                "allocation_status": "ASSIGNED",
                "metadata_status": "RECONCILED",
                "lifecycle_status": "UNKNOWN",
                "decision": "UNKNOWN",
                "source": {
                    "kind": "FILE",
                    "path": "change-requests/SCR-0001.md",
                    "commit": "b" * 40,
                    "attestation": {
                        "signature_status": "VERIFIED",
                        "signer_identity": "AA:BB",
                        "authority_status": "NOT_ESTABLISHED",
                    },
                },
                "notes": "A VERIFIED claim must pass git verify-commit.",
            }
            errors = self._fixture(root, [entry])
            self.assertTrue(
                any("commit signature verification failed" in error for error in errors), errors
            )



if __name__ == "__main__":
    unittest.main()
