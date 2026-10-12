#!/usr/bin/env python3
"""Generate a source-derived, machine-readable inventory of Python functions."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "docs" / "function-catalog.json"
EXCLUDED = {".git", ".venv", "venv", "__pycache__", "node_modules", "target", "dist", "build", "site-packages"}

def git_value(*args: str) -> str | None:
    try:
        return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None

def unparse(node):
    return ast.unparse(node) if node is not None else None

def get_args(node: ast.arguments) -> list[dict]:
    positional = list(node.posonlyargs) + list(node.args)
    defaults = [None] * (len(positional) - len(node.defaults)) + list(node.defaults)
    result = []
    for i, (arg, default) in enumerate(zip(positional, defaults)):
        result.append({"name": arg.arg, "kind": "positional_only" if i < len(node.posonlyargs) else "positional_or_keyword", "annotation": unparse(arg.annotation), "default": unparse(default)})
    if node.vararg:
        result.append({"name": node.vararg.arg, "kind": "var_positional", "annotation": unparse(node.vararg.annotation), "default": None})
    for arg, default in zip(node.kwonlyargs, node.kw_defaults):
        result.append({"name": arg.arg, "kind": "keyword_only", "annotation": unparse(arg.annotation), "default": unparse(default)})
    if node.kwarg:
        result.append({"name": node.kwarg.arg, "kind": "var_keyword", "annotation": unparse(node.kwarg.annotation), "default": None})
    return result

def scan_file(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=path.relative_to(ROOT).as_posix())
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    found = []
    def walk(node: ast.AST, parents: list[str], in_class: bool = False):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.ClassDef):
                walk(child, parents + [child.name], True)
            elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = get_args(child.args)
                doc = ast.get_docstring(child, clean=False)
                typed = all(p["annotation"] is not None for p in args)
                returns = child.returns is not None
                gaps = []
                if not doc: gaps.append("missing_docstring")
                if not typed: gaps.append("missing_parameter_annotations")
                if not returns: gaps.append("missing_return_annotation")
                found.append({
                    "qualified_name": ".".join(parents + [child.name]),
                    "name": child.name,
                    "kind": "async_function" if isinstance(child, ast.AsyncFunctionDef) else ("method" if in_class else "function"),
                    "source": {"path": path.relative_to(ROOT).as_posix(), "line_start": child.lineno, "line_end": getattr(child, "end_lineno", child.lineno), "sha256": digest},
                    "signature": {"parameters": args, "return_annotation": unparse(child.returns), "decorators": [ast.unparse(d) for d in child.decorator_list]},
                    "docstring": doc,
                    "contract_status": "SIGNATURE_AND_DOCSTRING_PRESENT" if doc and typed and returns else "PARTIAL_SOURCE_CONTRACT",
                    "contract_gaps": gaps,
                    "semantic_contract": {"preconditions": "UNSPECIFIED", "postconditions": "UNSPECIFIED", "errors": "UNSPECIFIED", "side_effects": "UNSPECIFIED", "determinism": "UNSPECIFIED", "security_invariants": "UNSPECIFIED", "evidence": "NOT_ASSERTED_BY_INVENTORY"}
                })
                walk(child, parents + [child.name], False)
            else:
                walk(child, parents, in_class)
    walk(tree, [])
    return found

def build_catalog() -> dict:
    paths = sorted(p for p in ROOT.rglob("*.py") if not any(part in EXCLUDED for part in p.relative_to(ROOT).parts))
    functions, errors = [], []
    for path in paths:
        try:
            functions.extend(scan_file(path))
        except (OSError, UnicodeError, SyntaxError) as exc:
            errors.append({"path": path.relative_to(ROOT).as_posix(), "error_type": type(exc).__name__, "message": str(exc)})
    functions.sort(key=lambda f: (f["source"]["path"], f["source"]["line_start"], f["qualified_name"]))
    return {
        "catalog_id": "ATC-FUNCTION-CATALOG-001",
        "catalog_version": "1.0.0",
        "catalog_status": "GENERATED_AUDIT_BASELINE" if not errors else "BLOCKED_SOURCE_PARSE_ERRORS",
        "normative": False,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repository": "A-TownChain-Okosystems/atc-standards",
        "source_revision": git_value("rev-parse", "HEAD"),
        "working_tree": "CLEAN" if git_value("status", "--porcelain") == "" else "DIRTY_OR_UNAVAILABLE",
        "scope": {"language": "Python", "include": "All discovered *.py files excluding known generated/vendor/build directories", "limitations": [
            "Inventory is not proof that contracts are complete or functions are correct.",
            "Non-Python functions and declarative YAML workflows are outside this AST inventory.",
            "Runtime-generated callables and dynamic APIs may not be discoverable statically.",
            "UNSPECIFIED semantic fields require owner-reviewed specification before conformance can be claimed."
        ]},
        "summary": {
            "python_files_discovered": len(paths),
            "functions_discovered": len(functions),
            "source_parse_errors": len(errors),
            "functions_with_complete_signature_and_docstring": sum(f["contract_status"] == "SIGNATURE_AND_DOCSTRING_PRESENT" for f in functions),
            "functions_with_partial_source_contract": sum(f["contract_status"] == "PARTIAL_SOURCE_CONTRACT" for f in functions)
        },
        "source_errors": errors,
        "functions": functions
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if the committed catalog differs from regenerated output")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    rendered = json.dumps(build_catalog(), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != rendered:
            print("FAIL: function catalog is stale; regenerate it")
            return 1
        print("PASS: function catalog is current")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Generated {args.output.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
