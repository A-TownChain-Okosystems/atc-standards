#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generiert registry/maintenance-conformance.yaml (SSOT der machine-readable
Maintenance-Conformance, ATC-STD-MAINT-000 §12, SCR-0120 v4).
Leitet Gruppen/Prioritaeten/REQs aus den normativen Dokumenten (standards/maintenance/)
und der Registry ab. Regenerierung nach jeder Aenderung an der MAINT-Familie."""
import io, os, re, sys, yaml

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MD_DIR = os.path.join(BASE, "standards", "maintenance")
OUT = os.path.join(BASE, "registry", "maintenance-conformance.yaml")

META = {
 "000": ("governance_classification", "P0"), "001": ("governance_classification", "P0"),
 "002": ("governance_classification", "P0"), "003": ("engineering", "P1"),
 "004": ("engineering", "P0"), "005": ("security", "P0"), "006": ("engineering", "P1"),
 "007": ("platform", "P0"), "008": ("platform", "P0"), "009": ("platform", "P0"),
 "010": ("platform", "P1"), "011": ("governance_assets", "P1"), "012": ("governance_assets", "P1"),
 "013": ("governance_assets", "P2"), "014": ("engineering", "P1"), "015": ("assurance", "P0"),
 "016": ("lifecycle", "P1"), "017": ("lifecycle", "P0"), "018": ("security", "P0"),
 "019": ("assurance", "P0"), "020": ("assurance", "P1"), "021": ("security", "P1"),
 "022": ("lifecycle", "P2"), "023": ("supply_ecosystem", "P2"), "024": ("supply_ecosystem", "P2"),
}
GROUPS = {
 "governance_classification": "Governance & Classification", "engineering": "Engineering",
 "security": "Security", "platform": "Platform", "governance_assets": "Governance Assets",
 "lifecycle": "Lifecycle", "assurance": "Assurance", "supply_ecosystem": "Supply & Ecosystem",
}

def main():
    reg = yaml.safe_load(io.open(os.path.join(BASE, "registry", "standards.yaml"), encoding="utf-8"))
    reg_ids = {s["id"]: s for s in reg["standards"] if s.get("category") == "maint"}
    standards = []
    for nr in sorted(META):
        sid = f"ATC-STD-MAINT-{nr}"
        md_path = os.path.join(MD_DIR, f"{sid}.md")
        if not os.path.exists(md_path):
            sys.exit(f"FEHLER: {md_path} fehlt")
        if sid not in reg_ids:
            sys.exit(f"FEHLER: {sid} nicht in Registry")
        md = io.open(md_path, encoding="utf-8").read()
        reqs = re.findall(r"\| (REQ-MAINT-\d{3}-\d{3}) \|", md)
        group, prio = META[nr]
        standards.append({
            "id": sid, "group": GROUPS[group], "group_key": group,
            "priority_kai_os": prio, "parent_standard": None if nr == "000" else "ATC-STD-MAINT-000",
            "inherits_mandatory_baseline": nr != "000",
            "req_count": len(reqs), "reqs": reqs,
            "version": str(reg_ids[sid].get("version", "")), "status": reg_ids[sid].get("status", ""),
        })
    doc = {
        "maintenance_conformance": {
            "standard": "ATC-STD-MAINT-000 §12", "version": "1.0.0",
            "generated_note": "GENERIERT aus standards/maintenance/ + registry/standards.yaml — nicht manuell pflegen (SCR-0120 v4)",
            "parent_standard": "ATC-STD-MAINT-000",
            "family_range": "ATC-STD-MAINT-000..024 (ab 025 frei via SCR)",
            "ecosystem_positioning": "Uebergeordnete Ecosystem-Governance-Capability (nicht Teil von KAI-OS); wiederverwendbar ausserhalb KAI-OS (P10)",
            "normative_release_gate": "A system MUST NOT be released to a lifecycle state requiring operational support unless its required maintenance capabilities are implemented, validated, documented, and evidenced.",
            "schemas": {
                "record": "schemas/maintenance/maintenance-record.schema.json",
                "readiness": "schemas/maintenance/maintenance-readiness.schema.json",
                "evidence": "schemas/maintenance/maintenance-evidence.schema.json",
            },
            "conformance_workflow": ".github/workflows/maintenance-conformance.yml",
            "conformance_workflow_repo": "registry/standards (ATC-*.yaml, kanonisch via tools/gen_views/gen_registry_records.py)",
            "standards": standards,
        }
    }
    with io.open(OUT, "w", encoding="utf-8") as f:
        yaml.safe_dump(doc, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=110)
    p0 = [s["id"] for s in standards if s["priority_kai_os"] == "P0"]
    print(f"OK registry/maintenance-conformance.yaml: {len(standards)} Standards, "
          f"{len(p0)} x P0, {sum(s['req_count'] for s in standards)} REQs gesamt")

if __name__ == "__main__":
    main()
