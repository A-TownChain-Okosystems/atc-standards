#!/usr/bin/env python3
"""Generate the complete Phase-2 semantic classification matrix.

This tool is deliberately non-authoritative:
- it reads registry/standards.yaml;
- it never allocates Family IDs, Category IDs, Class IDs, sequences, or canonical IDs;
- it produces proposals only, with an explicit heuristic basis and review flag;
- existing legacy IDs remain immutable.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

FAMILY_MAP = {
    "governance": "Governance",
    "governance-core": "Governance",
    "taxonomy": "Governance",
    "ai-dev": "AI & Agent Systems",
    "ai-gov": "AI & Agent Systems",
    "ai-decision": "AI & Agent Systems",
    "aas": "AI & Agent Systems",
    "agent-operating": "AI & Agent Systems",
    "blockchain": "Blockchain & Distributed Systems",
    "protocol": "Blockchain & Distributed Systems",
    "net": "Blockchain & Distributed Systems",
    "zkp": "Blockchain & Distributed Systems",
    "os": "Systems & Platform",
    "applications": "Systems & Platform",
    "infrastructure": "Systems & Platform",
    "sc": "Systems & Platform",
    "development": "Software Engineering & Architecture",
    "architecture": "Software Engineering & Architecture",
    "implementation": "Software Engineering & Architecture",
    "eng": "Software Engineering & Architecture",
    "compat": "Software Engineering & Architecture",
    "version": "Software Engineering & Architecture",
    "repository": "Repository Engineering",
    "repo-audit": "Repository Engineering",
    "repo-discovery": "Repository Engineering",
    "repo-maint": "Repository Engineering",
    "cicd": "Repository Engineering",
    "maint": "Repository Engineering",
    "bug": "Repository Engineering",
    "readme": "Repository Engineering",
    "md": "Repository Engineering",
    "desc": "Repository Engineering",
    "err": "Repository Engineering",
    "update": "Repository Engineering",
    "improvement": "Repository Engineering",
    "milestone": "Repository Engineering",
    "audit": "Audit & Evidence",
    "master-audit": "Audit & Evidence",
    "security": "Security & Trust",
    "legal": "Security, Legal & Compliance",
    "license": "Security, Legal & Compliance",
    "enterprise": "Security, Legal & Compliance",
    "framework": "Framework & Integration",
    "v2s": "Framework & Integration",
    "protocol": "Blockchain & Distributed Systems",
}

CATEGORY_MAP = {
    "repository": "Repository Governance",
    "repo-audit": "Repository Audit",
    "repo-discovery": "Repository Discovery",
    "repo-maint": "Repository Maintenance",
    "cicd": "CI/CD & Automation",
    "maint": "Maintenance & Operations",
    "bug": "Defect Management",
    "ai-dev": "AI Development",
    "ai-gov": "AI Governance",
    "ai-decision": "AI Decision Governance",
    "aas": "Agent Architecture & Safety",
    "agent-operating": "Agent Operations",
    "blockchain": "Blockchain Protocol",
    "protocol": "Protocol",
    "net": "Network Lifecycle",
    "zkp": "Zero-Knowledge Systems",
    "os": "Operating Systems",
    "applications": "Applications & Services",
    "infrastructure": "Infrastructure",
    "sc": "ShivaCore / System Core",
    "development": "Software Development",
    "architecture": "Architecture",
    "implementation": "Implementation",
    "security": "Security",
    "audit": "Audit & Evidence",
    "master-audit": "Master Audit",
    "governance": "Standards Governance",
    "governance-core": "Governance Core",
    "taxonomy": "Taxonomy & Classification",
    "legal": "Legal Compliance",
    "license": "Licensing",
    "enterprise": "Enterprise Governance",
    "framework": "Framework",
    "v2s": "Verification & Standards",
    "compat": "Compatibility",
    "version": "Versioning",
}

KEYWORD_CLASSES = [
    (r"identity|capabilities|permission|access|key|credential", "Identity & Access"),
    (r"security|vulnerab|threat|hardening|disclosure", "Security"),
    (r"audit|evidence|log|record|trace|retention", "Audit & Evidence"),
    (r"test|validation|verify|verification|check|gate", "Verification & Quality"),
    (r"network|devnet|testnet|mainnet|p2p|peer", "Networking & Lifecycle"),
    (r"genesis|chain identity|transaction|consensus|state|block", "Blockchain Protocol"),
    (r"vm|compiler|language|repl|package|library", "Language & Runtime"),
    (r"repository|repo|dependency|sbom|artifact|release|merge|commit|pull request", "Repository Engineering"),
    (r"documentation|readme|markdown|specification|schema", "Documentation & Specification"),
    (r"governance|policy|standard|taxonomy|classification|contributor|cla", "Governance & Policy"),
    (r"license|legal|impressum|privacy|terms", "Legal & Licensing"),
    (r"os|kernel|device|desktop|mobile|offline", "Operating System & Platform"),
    (r"ai|agent|model|decision|multi-agent", "AI & Agent Systems"),
    (r"zk|zero knowledge|proof|circuit|rollup|nullifier|commitment", "Zero-Knowledge Systems"),
]


def load_registry(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("standards"), list):
        raise SystemExit(f"ERROR: invalid registry structure: {path}")
    return [x for x in data["standards"] if isinstance(x, dict) and str(x.get("id", "")).strip()]


def candidate_class(title: str, category: str) -> str:
    text = f"{title} {category}".lower()
    for pattern, value in KEYWORD_CLASSES:
        if re.search(pattern, text):
            return value
    return "General Domain Standard"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--output", default="registry/migrations/classification-matrix.generated.yaml")
    args = ap.parse_args()
    root = Path(args.repo).resolve()
    registry = root / "registry/standards.yaml"
    records = load_registry(registry)

    rows = []
    for record in records:
        legacy_id = str(record["id"]).strip()
        title = str(record.get("title", "")).strip()
        source = str(record.get("file", "registry/standards.yaml"))
        legacy_category = str(record.get("category", "unclassified")).strip()
        family = FAMILY_MAP.get(legacy_category, "UNCLASSIFIED")
        category = CATEGORY_MAP.get(legacy_category, legacy_category.replace("-", " ").title())
        cls = candidate_class(title, legacy_category)
        high_confidence = legacy_category in FAMILY_MAP and legacy_category in CATEGORY_MAP
        rows.append({
            "legacy_id": legacy_id,
            "title": title,
            "source": source,
            "legacy_namespace": (
                "ATC-STD-numeric" if re.fullmatch(r"ATC-STD-\d+", legacy_id)
                else "ATC-STD-domain-prefixed" if legacy_id.startswith("ATC-STD-")
                else "other"
            ),
            "legacy_category": legacy_category,
            "proposal": {
                "semantic_domain": family,
                "category": category,
                "class": cls,
                "basis": "legacy registry category + title keyword analysis",
                "confidence": "high" if high_confidence else "low",
            },
            "governance_review_required": True,
            "migration": {
                "family_id": None,
                "category_id": None,
                "class_id": None,
                "sequence": None,
                "canonical_id": None,
                "status": "classified_proposal",
            },
        })

    out = {
        "schema_version": "1.0.0",
        "status": "generated_semantic_classification_proposals",
        "authority": "non-authoritative working artifact",
        "source_of_truth": "registry/standards.yaml",
        "purpose": "Complete semantic classification matrix before governance-approved canonical allocation",
        "rules": {
            "legacy_ids_immutable": True,
            "numeric_range_implies_family": False,
            "proposals_are_not_canonical_assignments": True,
            "family_ids_allocated": False,
            "category_ids_allocated": False,
            "class_ids_allocated": False,
            "sequences_allocated": False,
            "canonical_ids_allocated": False,
            "governance_review_required": True,
        },
        "summary": {
            "total": len(rows),
            "proposal_status": "all rows require governance review",
            "canonical_ids": 0,
        },
        "entries": rows,
    }
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Generated {len(rows)} classification proposals -> {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
