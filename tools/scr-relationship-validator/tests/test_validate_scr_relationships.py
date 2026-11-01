import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPT = Path(__file__).resolve().parents[1] / "validate_scr_relationships.py"
spec = importlib.util.spec_from_file_location("scr_relationship_validator", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RelationshipRegistryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "registry/scr-relationships/v1").mkdir(parents=True)
        (self.root / "schemas/scr-relationships/v1").mkdir(parents=True)
        self.schema_path = self.root / "schemas/scr-relationships/v1/relationships.schema.json"
        schema_source = SCRIPT.parents[2] / "schemas/scr-relationships/v1/relationships.schema.json"
        self.schema_path.write_text(schema_source.read_text(encoding="utf-8"), encoding="utf-8")
        self.registry_path = self.root / "registry/scr-registry.yaml"
        self.semantics_path = self.root / "registry/scr-relationships/v1/semantics.yaml"
        self.relationship_path = self.root / "registry/scr-relationships/v1/relationships.yaml"
        registry = {
            "registry_version": 1,
            "source_ref": "test",
            "source_commit": "d" * 40,
            "entries": [
                {
                    "id": "SCR-0001",
                    "allocation_status": "ASSIGNED",
                    "source": {"identity_sha256": "a" * 64},
                },
                {
                    "id": "SCR-0002",
                    "allocation_status": "ASSIGNED",
                    "source": {"identity_sha256": "b" * 64},
                },
                {
                    "id": "SCR-0003",
                    "allocation_status": "RESERVED",
                    "source": {"identity_sha256": "c" * 64},
                },
            ],
        }
        self.registry_path.write_text(yaml.safe_dump(registry), encoding="utf-8")
        tokens = ("DEPENDS_ON", "SUPERSEDES", "SPLIT_FROM", "MERGED_INTO", "RELATED_TO")
        semantics = {
            "semantics_manifest_version": 1,
            "module": "scr-relationship-registry",
            "status": "NON_NORMATIVE",
            "governance_decision": None,
            "approved_relation_types": [],
            "acyclic_relation_types": [],
            "candidate_relation_types": [
                {
                    "token": token,
                    "status": "PROPOSED",
                    "proposed_interpretation": "test only",
                }
                for token in tokens
            ],
        }
        self.semantics_path.write_text(yaml.safe_dump(semantics), encoding="utf-8")
        self.write_relationships([])

    def tearDown(self):
        self.tmp.cleanup()

    def write_relationships(self, relationships, version=1):
        data = {
            "relationship_registry_version": version,
            "repository": "A-TownChain-Okosystems/atc-standards",
            "scr_registry_ref": "test",
            "scr_registry_commit": "d" * 40,
            "relationships": relationships,
        }
        self.relationship_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def edge(self, **overrides):
        item = {
            "relationship_id": "SCR-REL-0001",
            "from_scr": "SCR-0001",
            "to_scr": "SCR-0002",
            "relation_type": "RELATED_TO",
            "governance_status": "PROPOSED",
            "scope": "Non-normative test edge",
            "evidence_refs": [{"identity_sha256": "a" * 64, "scope": "source record"}],
        }
        item.update(overrides)
        return item

    def validate(self, mode="structural"):
        return module.validate(
            root=self.root,
            relationship_path=self.relationship_path,
            schema_path=self.schema_path,
            registry_path=self.registry_path,
            semantics_path=self.semantics_path,
            mode=mode,
        )

    def test_empty_registry_passes_structural_mode(self):
        self.assertEqual(self.validate(), [])

    def test_candidate_relation_passes_structural_mode_only(self):
        self.write_relationships([self.edge()])
        self.assertEqual(self.validate(), [])
        errors = self.validate("normative")
        self.assertTrue(any("not governance-approved" in error for error in errors), errors)

    def test_unknown_endpoint_fails_closed(self):
        self.write_relationships([self.edge(to_scr="SCR-9999")])
        self.assertTrue(
            any("unresolved or non-assigned to_scr" in error for error in self.validate())
        )

    def test_reserved_endpoint_is_not_canonical(self):
        self.write_relationships([self.edge(to_scr="SCR-0003")])
        self.assertTrue(
            any("unresolved or non-assigned to_scr" in error for error in self.validate())
        )

    def test_duplicate_relationship_ids_fail(self):
        first = self.edge()
        second = self.edge(from_scr="SCR-0002", to_scr="SCR-0001")
        self.write_relationships([first, second])
        self.assertTrue(any("duplicate relationship_id" in error for error in self.validate()))

    def test_invalid_scr_identifier_fails_schema(self):
        self.write_relationships([self.edge(from_scr="SCR-ABC")])
        self.assertTrue(any("SCR-ABC" in error for error in self.validate()))

    def test_unknown_relation_type_fails_closed(self):
        self.write_relationships([self.edge(relation_type="OWNER_APPROVED")])
        self.assertTrue(any("unknown relation_type" in error for error in self.validate()))

    def test_missing_evidence_reference_fails_schema(self):
        self.write_relationships([self.edge(evidence_refs=[])])
        self.assertTrue(any("non-empty" in error for error in self.validate()))

    def test_unresolved_evidence_reference_fails_closed(self):
        refs = [{"identity_sha256": "f" * 64, "scope": "not in SCR registry"}]
        self.write_relationships([self.edge(evidence_refs=refs)])
        self.assertTrue(any("unresolved evidence identity" in error for error in self.validate()))

    def test_unsupported_schema_version_fails(self):
        self.write_relationships([], version=2)
        self.assertTrue(
            any("const" in error or "2 was expected" in error for error in self.validate())
        )

    def test_self_edge_fails(self):
        self.write_relationships([self.edge(to_scr="SCR-0001")])
        self.assertTrue(any("self-edge" in error for error in self.validate()))

    def test_duplicate_edge_fails_even_with_distinct_record_ids(self):
        first = self.edge()
        second = self.edge(relationship_id="SCR-REL-0002")
        self.write_relationships([first, second])
        self.assertTrue(any("duplicate relationship edge" in error for error in self.validate()))

    def test_acyclic_check_is_relation_specific(self):
        semantics = yaml.safe_load(self.semantics_path.read_text(encoding="utf-8"))
        semantics["status"] = "GOVERNANCE_APPROVED"
        semantics["governance_decision"] = "TEST-DECISION-REF"
        semantics["approved_relation_types"] = ["DEPENDS_ON"]
        semantics["acyclic_relation_types"] = ["DEPENDS_ON"]
        self.semantics_path.write_text(yaml.safe_dump(semantics), encoding="utf-8")
        edges = [
            self.edge(
                relationship_id="SCR-REL-0001",
                relation_type="DEPENDS_ON",
            ),
            self.edge(
                relationship_id="SCR-REL-0002",
                from_scr="SCR-0002",
                to_scr="SCR-0001",
                relation_type="DEPENDS_ON",
            ),
        ]
        self.write_relationships(edges)
        errors = self.validate()
        self.assertTrue(any("cycle detected" in error for error in errors), errors)

    def test_non_normative_manifest_cannot_declare_acyclic_types(self):
        semantics = yaml.safe_load(self.semantics_path.read_text(encoding="utf-8"))
        semantics["acyclic_relation_types"] = ["DEPENDS_ON"]
        self.semantics_path.write_text(yaml.safe_dump(semantics), encoding="utf-8")
        self.assertTrue(
            any("NON_NORMATIVE semantics manifest" in error for error in self.validate())
        )

    def test_duplicate_yaml_keys_fail_closed(self):
        self.relationship_path.write_text(
            "relationship_registry_version: 1\nrelationship_registry_version: 1\n",
            encoding="utf-8",
        )
        self.assertTrue(any("duplicate key" in error for error in self.validate()))

    def test_unknown_mode_fails_closed(self):
        errors = module.validate(root=self.root, mode="guess")
        self.assertTrue(any("mode must be" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
