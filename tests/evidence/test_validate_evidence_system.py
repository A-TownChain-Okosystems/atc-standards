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

    def test_live_graph_uses_real_run_and_head_and_remains_release_blocked(self):
        head = "a" * 40
        base = "b" * 40
        run = {"pull_requests": [{"number": 48}]}
        job = {"id": 123}
        steps = [
            {"name": "Validate repository evidence graph", "number": 5},
            {"name": "Run positive and negative evidence tests", "number": 6},
        ]
        records, trace = evidence.build_live_evidence_graph(
            "A-TownChain-Okosystems/atc-standards",
            head, base, "987654", run, job, steps
        )
        evidence.validate_graph(records, trace, self.record_schema, self.trace_schema)
        implementation = next(item for item in records if item["type"] == "IMPLEMENTATION")
        ci = next(item for item in records if item["type"] == "CI")
        self.assertEqual(implementation["commit_sha"], head)
        self.assertEqual(ci["commit_sha"], head)
        self.assertEqual(ci["run_id"], "987654")
        self.assertEqual(ci["job_id"], "123")
        self.assertEqual(
            evidence.evaluate(records, trace),
            {"status": "CI-VERIFIED", "traceability": "INCOMPLETE", "release": "BLOCKED"},
        )

    def test_live_run_rejects_head_sha_mismatch(self):
        head = "a" * 40
        run = {
            "id": 987654,
            "head_sha": "c" * 40,
            "repository": {"full_name": "A-TownChain-Okosystems/atc-standards"},
            "pull_requests": [{"number": 48}],
        }
        with self.assertRaisesRegex(evidence.EvidenceError, "run head SHA"):
            evidence.validate_live_run_identity(
                "A-TownChain-Okosystems/atc-standards",
                "987654",
                head,
                head,
                48,
                run,
            )

    def test_live_run_rejects_wrong_pull_request_identity(self):
        head = "a" * 40
        run = {
            "id": 987654,
            "head_sha": head,
            "repository": {"full_name": "A-TownChain-Okosystems/atc-standards"},
            "pull_requests": [{"number": 49}],
        }
        with self.assertRaisesRegex(evidence.EvidenceError, "event pull request"):
            evidence.validate_live_run_identity(
                "A-TownChain-Okosystems/atc-standards",
                "987654",
                head,
                head,
                48,
                run,
            )

    def test_push_event_resolves_exact_commit_and_associated_pr(self):
        head = "a" * 40
        base = "b" * 40
        event = {"after": head, "ref": "refs/heads/evidence/function-change-graph-2026-09-27"}
        run = {
            "head_branch": "evidence/function-change-graph-2026-09-27",
            "pull_requests": [{
                "number": 48,
                "head": {"ref": "evidence/function-change-graph-2026-09-27"},
                "base": {"sha": base},
            }],
        }
        self.assertEqual(evidence.resolve_event_binding(event, run), (head, base, 48))

    def test_pull_request_event_resolves_exact_head_and_base(self):
        head = "a" * 40
        base = "b" * 40
        event = {
            "pull_request": {
                "number": 48,
                "head": {"sha": head, "ref": "evidence/function-change-graph-2026-09-27"},
                "base": {"sha": base},
            }
        }
        run = {
            "head_branch": "evidence/function-change-graph-2026-09-27",
            "pull_requests": [{
                "number": 48,
                "head": {"ref": "evidence/function-change-graph-2026-09-27"},
                "base": {"sha": base},
            }],
        }
        self.assertEqual(evidence.resolve_event_binding(event, run), (head, base, 48))

    def test_push_event_rejects_branch_mismatch(self):
        event = {"after": "a" * 40, "ref": "refs/heads/other"}
        run = {
            "head_branch": "evidence/function-change-graph-2026-09-27",
            "pull_requests": [{
                "number": 48,
                "head": {"ref": "evidence/function-change-graph-2026-09-27"},
                "base": {"sha": "b" * 40},
            }],
        }
        with self.assertRaisesRegex(evidence.EvidenceError, "branch"):
            evidence.resolve_event_binding(event, run)


if __name__ == "__main__":
    unittest.main()
