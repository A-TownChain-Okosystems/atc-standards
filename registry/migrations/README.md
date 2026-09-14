# Standard Registry Migration Inventory

## Purpose

This directory contains the controlled migration inventory for the Family → Category → Class → Standard taxonomy approved through SCR-0125.

## Rules

- Legacy IDs are immutable and reserved.
- No legacy ID is silently renamed, reused, or deleted.
- No canonical ID is allocated without an explicit registry record.
- Classification is semantic and must be reviewed per standard.
- Existing numeric IDs are **not** presumed to belong to the Blockchain family.
- A migration record is incomplete until Family, Category, Class, sequence, canonical ID, legacy ID, and migration status are present.
- Conflicts are recorded explicitly and block automatic migration.

## Migration status

Allowed states:

- `unreviewed`
- `classified`
- `mapped`
- `conflict`
- `blocked`
- `migrated`
- `retired`

## Phase 1 inventory

`standard-inventory.yaml` is the authoritative working inventory for Phase 1. It records legacy identifiers and the evidence required for later semantic classification. Canonical IDs are not assigned merely because an entry exists in the inventory.

## Required review order

1. Discover every standard source and registry entry.
2. Normalize legacy identifiers without changing them.
3. Detect duplicate legacy identifiers and conflicting definitions.
4. Determine semantic Family, Category, and Class from the standard's actual scope.
5. Allocate a Family-local sequence only after classification is accepted.
6. Create explicit legacy → canonical mappings.
7. Validate the complete migration set before modifying standard filenames or IDs.
