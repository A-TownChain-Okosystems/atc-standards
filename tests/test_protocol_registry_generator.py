"""Regression tests for the protocol registry generator's SSOT mappings."""

from pathlib import Path
import sys

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS / "protocol"))

import gen_protocol_registry as generator  # noqa: E402


def _protocol(domain: str) -> tuple:
    return next(item for item in generator.PROTOCOLS if item[0] == domain)


def test_consensus_override_targets_consensus_spec() -> None:
    assert generator.SPEC_OVERRIDES["CONSENSUS"].startswith(
        "protocols/consensus/ATC-PROTO-CONSENSUS-001.md"
    )


def test_override_paths_match_their_protocol_domains() -> None:
    for domain, specification in generator.SPEC_OVERRIDES.items():
        expected_prefix = f"protocols/{domain.lower()}/ATC-PROTO-{domain}-001.md"
        assert specification.startswith(expected_prefix), domain


def test_ai_status_is_draft() -> None:
    assert _protocol("AI")[3] == "draft"


def test_ai_override_is_present() -> None:
    assert generator.SPEC_OVERRIDES["AI"].startswith(
        "protocols/ai/ATC-PROTO-AI-001.md"
    )
