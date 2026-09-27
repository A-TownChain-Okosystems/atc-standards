"""Independent MEMORY-001 contract verifier."""
import base64
import hashlib
import json
from pathlib import Path

import rfc8785
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ROOT = Path(__file__).resolve().parents[1]
VECTOR = ROOT / "test-vectors/memory-001/determinism.json"


def canonical_bytes(value):
    return rfc8785.dumps(value)


def main():
    payload = json.loads(VECTOR.read_text(encoding="utf-8"))
    case = next(item for item in payload["cases"] if item["id"] == "MEM-DET-001")
    actual = canonical_bytes(case["input"])
    assert actual == case["canonical_utf8"].encode("utf-8")
    assert actual.hex() == case["canonical_utf8_hex"]
    assert "sha256:" + hashlib.sha256(actual).hexdigest() == case["record_hash"]

    signature = base64.urlsafe_b64decode(case["signature"].removeprefix("ed25519:") + "==")
    public_key = base64.urlsafe_b64decode(case["public_key"] + "==")
    Ed25519PublicKey.from_public_bytes(public_key).verify(
        signature, case["signing_domain"].encode("ascii") + b"\x00" + actual
    )
    print("MEMORY-001 reference vector: PASS")


if __name__ == "__main__":
    main()
