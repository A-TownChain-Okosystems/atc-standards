import json
import unittest
from pathlib import Path

from tools import validate_evidence_system as evidence

ROOT = Path(__file__).resolve().parents[2]


class EvidenceSystemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = evidence.load_json(ROOT / "tests/evidence/reference-system.json")
        cls.record_schema = evidence.load_json(ROOT / "schemas/evidence/record.schema.json")
        cls.trace_schema = evidence.load_json(ROOT / "schemas/evidence/traceability.schema.json")

    def test_positive_graph_is_closed_and_release_ready(self):
        positive = self.fixture["positive"]
        evidence.validate_graph(
            positive["records"], positive["traceability"],
            self.record_schema, self.trace_schema
        )
        self.assertEqual(
            evidence.evaluate(positive["records"], positive["traceability"]),
            positive["expected"],
        )

    def test_negative_exact_sha_blocks_status_and_release(self):
        positive = self.fixture["positive"]
        records = json.loads(json.dumps(positive["records"]))
        mutation = self.fixture["negative"]["mutation"]
        target = next(item for item in records if item["id"] == mutation["record_id"])
        target[mutation["field"]] = mutation["value"]
        self.assertEqual(
            evidence.evaluate(records, positive["traceability"]),
            self.fixture["negative"]["expected"],
        )

    def test_duplicate_identity_is_rejected(self):
        positive = self.fixture["positive"]
        records = positive["records"] + [json.loads(json.dumps(positive["records"][0]))]
        with self.assertRaisesRegex(evidence.EvidenceError, "duplicate evidence ID"):
            evidence.validate_graph(
                records, positive["traceability"], self.record_schema, self.trace_schema
            )

    def test_missing_reference_is_rejected(self):
        positive = self.fixture["positive"]
        records = json.loads(json.dumps(positive["records"]))
        records[1]["references"] = ["ATC-FUNC-DOES-NOT-EXIST"]
        with self.assertRaisesRegex(evidence.EvidenceError, "references missing evidence"):
            evidence.validate_graph(
                records, positive["traceability"], self.record_schema, self.trace_schema
            )

    def test_unresolved_graph_edge_is_rejected(self):
        positive = self.fixture["positive"]
        trace = json.loads(json.dumps(positive["traceability"]))
        trace["edges"][0]["to"] = "ATC-SPEC-MISSING"
        with self.assertRaisesRegex(evidence.EvidenceError, "unresolved graph edge"):
            evidence.validate_graph(
                positive["records"], trace, self.record_schema, self.trace_schema
            )

    def test_invalid_relation_type_pair_is_rejected(self):
        positive = self.fixture["positive"]
        trace = json.loads(json.dumps(positive["traceability"]))
        trace["edges"][0]["relation"] = "RELEASES"
        with self.assertRaisesRegex(evidence.EvidenceError, "invalid RELEASES edge type"):
            evidence.validate_graph(
                positive["records"], trace, self.record_schema, self.trace_schema
            )


if __name__ == "__main__":
    unittest.main()
