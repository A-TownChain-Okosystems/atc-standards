"""Validate the MEMORY-001 contract package."""
import json
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas/memory-001"


def load(name):
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def main():
    schemas = [p for p in SCHEMA_DIR.glob("*.json")]
    loaded = {p.name: json.loads(p.read_text(encoding="utf-8")) for p in schemas}
    for schema in loaded.values():
        Draft202012Validator.check_schema(schema)

    memory = loaded["memory-record.schema.json"]
    node = loaded["node-identity.schema.json"]
    resolver = RefResolver.from_schema(memory, store={node["$id"]: node})
    validator = Draft202012Validator(memory, resolver=resolver)

    vectors = json.loads((ROOT / "test-vectors/memory-001/determinism.json").read_text(encoding="utf-8"))
    record = next(item["input"] for item in vectors["cases"] if item["id"] == "MEM-DET-001")
    errors = list(validator.iter_errors(record))
    if errors:
        raise SystemExit("\n".join(error.message for error in errors))

    for name in ("negative.json", "conflict.json"):
        json.loads((ROOT / "test-vectors/memory-001" / name).read_text(encoding="utf-8"))

    print(f"MEMORY-001 schema validation: PASS ({len(schemas)} JSON schemas)")


if __name__ == "__main__":
    main()
