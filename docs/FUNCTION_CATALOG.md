# ATC Function Catalog

## Purpose

`docs/function-catalog.json` is the generated, machine-readable inventory of Python functions and methods in this repository. It is derived from Python ASTs, not maintained as a manual list.

## Regeneration

```bash
python3 tools/function-catalog/generate_function_catalog.py
python3 -m json.tool docs/function-catalog.json >/dev/null
```

Check a committed inventory after regeneration:

```bash
python3 tools/function-catalog/generate_function_catalog.py --check
```

The catalog records source path, line range, per-file SHA-256, qualified name, decorators, parameter kinds/defaults/annotations, return annotation, and docstring. It is intended to be regenerated whenever Python source changes.

## Semantic contract requirements

The generator records source facts only and does not invent behavior. For each function, a complete owner-reviewed contract should specify as applicable:

- Preconditions and accepted input domains.
- Postconditions and return-value semantics.
- Failure modes, exceptions, and process exit behavior.
- Filesystem, process, network, registry, and other side effects.
- Determinism and reproducibility expectations.
- Security invariants, trust boundaries, and fail-closed behavior.
- Tests and exact-SHA evidence supporting the claims.

`SIGNATURE_AND_DOCSTRING_PRESENT` means only that a docstring and annotated signature exist. It does not mean the semantic contract is complete or verified. Semantic fields remain `UNSPECIFIED` until reviewed; no conformance claim may be inferred from the inventory alone.

## Scope and limitations

The initial inventory covers Python AST functions and methods. YAML workflows, shell entrypoints, declarative registry data, and other languages require separate inventories. Parse errors must be reported and block a clean inventory. The catalog is an audit baseline, not a normative standard and not proof of correctness.

`docs/function-catalog.json` is generated; do not edit it manually.
