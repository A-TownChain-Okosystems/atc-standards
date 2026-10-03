"""Regression tests for the protocol registry generator's SSOT mappings."""

from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS / "protocol"))

import gen_protocol_registry as generator  # noqa: E402


def _protocol(domain: str) -> tuple:
    return next(item for item in generator.PROTOCOLS if item[0] == domain)


class ProtocolRegistryGeneratorTests(unittest.TestCase):
    def test_consensus_override_targets_consensus_spec(self) -> None:
        self.assertTrue(
            generator.SPEC_OVERRIDES["CONSENSUS"].startswith(
                "protocols/consensus/ATC-PROTO-CONSENSUS-001.md"
            )
        )

    def test_override_paths_match_their_protocol_domains(self) -> None:
        for domain, specification in generator.SPEC_OVERRIDES.items():
            expected_prefix = f"protocols/{domain.lower()}/ATC-PROTO-{domain}-001.md"
            with self.subTest(domain=domain):
                self.assertTrue(specification.startswith(expected_prefix))

    def test_ai_status_is_draft(self) -> None:
        self.assertEqual(_protocol("AI")[3], "draft")

    def test_protocol_family_count_remains_26(self) -> None:
        self.assertEqual(len(generator.PROTOCOLS), 26)

    def test_ai_override_is_present(self) -> None:
        self.assertTrue(
            generator.SPEC_OVERRIDES["AI"].startswith(
                "protocols/ai/ATC-PROTO-AI-001.md"
            )
        )


if __name__ == "__main__":
    unittest.main()
