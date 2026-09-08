#!/usr/bin/env python3
"""Generiert registry/taxonomy.yaml — die ATC Standards Taxonomy (ATC-STD-TAXONOMY-001 §8).
SSOT der vierstufigen Hierarchie (Domain→Familie→Kategorie→Standard); Bestands-Abbild
aus registry/categories.yaml + registry/standards.yaml. Regenerierung nur via TCR + SCR."""
import yaml

# ── Domain-Zuordnung: JEDER Bestands-Familie MUSS ein Domain zugewiesen sein.
# Neue Kategorien ohne Mapping → AssertionError (erzwingt TAX-CHECK-013-Vollständigkeit).
DOMAIN_MAP = {
    # numerische ID-Bereiche (ATC-STD-000 §7)
    "governance": "GOV", "architecture": "SW", "repository": "SW", "development": "SW",
    "security": "TRUST", "protocol": "CHAIN", "blockchain": "CHAIN", "ai": "AI",
    "os": "SW", "infrastructure": "SW", "applications": "SW",
    # benannte Familien
    "bug": "GOV", "zkp": "TRUST", "ai-dev": "AI", "aas": "AI", "enterprise": "GOV", "v2s": "GOV",
    "readme": "SW", "md": "SW", "sc": "CHAIN", "net": "CHAIN", "desc": "GOV",
    "version": "GOV", "audit": "GOV", "ai-decision": "AI", "update": "GOV",
    "repo-audit": "GOV", "repo-maint": "GOV", "err": "GOV", "implementation": "GOV", "agent-operating": "AI", "master-audit": "GOV",
    "framework": "GOV", "milestone": "GOV", "compat": "GOV", "governance-core": "GOV",
    # neu via SCR-0024/SCR-0037
    "taxonomy": "GOV", "license": "GOV",
}
DOMAINS = {
    "GOV":   "Governance & Meta-Standards",
    "SW":    "Software Engineering",
    "CHAIN": "Blockchain, Smart Contracts & Protokolle",
    "AI":    "Artificial Intelligence & Agenten",
    "TRUST": "Security & Trust",
}
# Familien-Codes (global eindeutig, TAX-CHECK-003)
FAMILY_CODES = {
    "bug": "BUG", "v2s": "V2S", "zkp": "ZKP", "ai-dev": "AID", "aas": "AAS", "enterprise": "ENT",
    "readme": "RDM", "md": "MD", "sc": "SC", "net": "NET", "desc": "DESC",
    "version": "VER", "audit": "AUD", "ai-decision": "AIDEC", "update": "UPD",
    "repo-audit": "RA", "repo-maint": "RM", "err": "ER", "implementation": "IM", "protocol": "PROT", "agent-operating": "AOS",
    "master-audit": "MAUD", "framework": "FW", "milestone": "MIL", "compat": "CMP",
    "taxonomy": "TAX", "governance-core": "SGC", "license": "LIC",
}

cats = yaml.safe_load(open("registry/categories.yaml", encoding="utf-8"))
std = yaml.safe_load(open("registry/standards.yaml", encoding="utf-8"))

# Familien sammeln: numerische Bereiche + benannte
families = {}
for num, meta in cats.get("categories", {}).items():
    families[meta["name"]] = {"code": "N" + str(num), "range": meta["range"],
                              "description": meta["description"], "source": "numeric-§7"}
for key, meta in cats.items():
    if key == "categories" or not isinstance(meta, dict):
        continue
    if meta["name"] in families:  # Namenskollision numeric/named (protocol)
        families[meta["name"] + " (familie)"] = {"code": FAMILY_CODES[meta["name"]],
            "range": meta["range"], "description": meta["description"], "source": "named-family"}
    else:
        families[meta["name"]] = {"code": FAMILY_CODES[meta["name"]], "range": meta["range"],
                                  "description": meta["description"], "source": "named-family"}
families["taxonomy"] = {"code": "TAX", "range": "ATC-STD-TAXONOMY-001-999",
    "description": "Standards Taxonomy & Family Creation (Meta-Governance, SCR-0024)", "source": "named-family"}

# Standards je Familie zählen (Registry-Konsistenz TAX-CHECK-013/014)
std_count = {}
for e in std["standards"]:
    cat = e.get("category", "?")
    # Namenskollision numeric/named ("protocol"): Standards gehoeren zur benannten Familie
    key = cat + " (familie)" if (cat in families and (cat + " (familie)") in families) else cat
    std_count[key] = std_count.get(key, 0) + 1

dom_fams = {d: [] for d in DOMAINS}
for name, meta in families.items():
    dom = DOMAIN_MAP[name.replace(" (familie)", "")]
    assert dom in DOMAINS, f"unbekannter Domain fuer {name}"
    fam = {
        "id": meta["code"], "name": name, "status": "ACTIVE", "lifecycle": "ACTIVE",
        "id_range": meta["range"], "source": meta["source"],
        "description": meta["description"],
        "standards_count": std_count.get(name, 0),
        "categories": [{"id": "GENERAL", "name": "Allgemein (Bestand, keine Unterteilung)",
                        "status": "ACTIVE", "lifecycle": "ACTIVE"}],
    }
    dom_fams[dom].append(fam)

# Kategorie-Ebene: für neue Familien via ATC-CAT-REQ; Bestand führt GENERAL (Grandfathering)
data = {
    "taxonomy": {
        "standard": "ATC-STD-TAXONOMY-001",
        "version": "1.0.0",
        "generated": "2026-09-08",
        "hierarchy": ["DOMAIN", "FAMILY", "CATEGORY", "STANDARD"],
        "id_scheme_new_families": "ATC-STD-<FAMCODE>[-<CATEGORY>]-NNN",
        "grandfathering": "Bestehende Standards behalten ihre IDs (§30); Bestands-Familien fuehren Kategorie GENERAL bis Unterteilung via ATC-CAT-REQ.",
        "lifecycle": ["PROPOSED", "ANALYZED", "APPROVED", "ACTIVE", "DEPRECATED", "RETIRED"],
        "requests": {"family": "ATC-FAM-REQ-NNN", "category": "ATC-CAT-REQ-NNN", "change": "ATC-TCR-NNN"},
        "tax_checks": "TAX-CHECK-001..018 (S-24 automatisiert 001-006, 013, 014, 015)",
        "governance_core": {
            "family": "FAM-43 Standards Governance Core",
            "members": [
                {"id": "ATC-STD-TAXONOMY-001", "status": "DRAFT (SCR-0024, §9 ausstehend)"},
                {"id": "ATC-STD-STDDEV-001", "status": "GEPLANT (Standards-Development-Standard)"},
                {"id": "ATC-STD-REGISTRY-001", "status": "GEPLANT (Registry-Management)"},
                {"id": "ATC-STD-CHANGE-001", "status": "GEPLANT (Change-Control-Dachnorm; konsolidiert ATC-STD-000 §19-33 + UPDATE-001 + COMPAT-001; Abgrenzung bei Erstellung klaeren)"},
                {"id": "ATC-STD-AUDIT-001", "status": "APPROVED"},
            ],
        },
        "documented_negativfall": "Owner-Beispielfamilie AIA (AI Agents) ueberlappt Bestands-Familie AAS (ATC-AAS-001..025) — TAX-CHECK-008/010 wuerden ATC-FAM-REQ zurueckweisen bzw. auf MERGE lenken.",
        "domains": [
            {"id": code, "name": name, "status": "ACTIVE", "lifecycle": "ACTIVE",
             "families": dom_fams[code]}
            for code, name in DOMAINS.items()
        ],
    }
}
# Validierung der Eindeutigkeit (TAX-CHECK-002..005)
codes = [f["id"] for d in data["taxonomy"]["domains"] for f in d["families"]]
assert len(codes) == len(set(codes)), "Familien-Codes nicht eindeutig"
names = [f["name"] for d in data["taxonomy"]["domains"] for f in d["families"]]
assert len(names) == len(set(names)), "Familien-Namen nicht eindeutig"

with open("registry/taxonomy.yaml", "w", encoding="utf-8") as fh:
    fh.write("# ATC Standards Taxonomy — ATC-STD-TAXONOMY-001 §8 (SSOT)\n")
    fh.write("# Generiert von tools/taxonomy/gen_taxonomy.py — Aenderungen nur via ATC-TCR + SCR.\n")
    yaml.dump(data, fh, allow_unicode=True, sort_keys=False, width=200)

total_std = sum(f["standards_count"] for d in data["taxonomy"]["domains"] for f in d["families"])
print(f"taxonomy.yaml: {len(DOMAINS)} Domains, {len(codes)} Familien "
      f"({sum(1 for c in codes if c.startswith('N'))} numerisch, {len(codes)-sum(1 for c in codes if c.startswith('N'))} benannt), "
      f"{total_std} Standards zugeordnet (Registry-Konsistenz)")
