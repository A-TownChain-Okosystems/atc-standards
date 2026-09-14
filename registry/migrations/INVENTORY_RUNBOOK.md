# Registry Migration Inventory Runbook

## Purpose

Generate the complete Phase-1 legacy inventory before any Family/Category/Class allocation or standard ID migration.

## Command

From the repository root:

```bash
python3 tools/registry-migration/inventory.py
```

The generator reads `registry/standards.yaml`, scans the configured registry/standard sources for references, and writes:

```text
registry/migrations/standard-inventory.generated.yaml
```

## Fail-closed guarantees

The generator MUST:

- preserve every registry ID as `legacy_id`;
- preserve registry title, version, status, category and source;
- leave `family.id`, `category.id`, `class.id`, `sequence` and `canonical_id` unset;
- never rename, delete, recycle, or rewrite a legacy ID;
- mark duplicate legacy IDs as `conflict`;
- report the authoritative registry SHA-256;
- report namespace counts;
- never infer a canonical Family from a numeric range;
- never allocate canonical IDs.

## Classification workflow

```text
registry/standards.yaml
        |
        v
legacy inventory
        |
        +--> duplicate IDs
        +--> namespace collisions
        +--> source/reference collisions
        +--> existing category/family evidence
        +--> generated-state drift
        |
        v
conflict register
        |
        v
semantic review
        |
        v
approved Family/Category/Class allocation
```

## Important

`standard-inventory.generated.yaml` is a generated working artifact. It is not permission to migrate IDs. Canonical allocation remains a separate governed step after semantic review and approval of the successor taxonomy.
