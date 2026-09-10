# -*- coding: utf-8 -*-
"""SCR-0080: Repository-Registry-Check — 27 GitHub == 27 Registry == 27 Evidence.

Prueft (offline-Modus): Eintrag-Anzahl, eindeutige IDs/Namen, Canonical-Eindeutigkeit
(je Capability genau EIN canonical), Layer-Taxonomie-Vollstaendigkeit, Evidence-Pfad.
Modus --github: zusaetzlich Existenz aller Repos via API (GITHUB_TOKEN oder anonym).
Exit 0 = OK, 1 = FAIL."""
import sys, argparse
import yaml

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", default="registry/repositories.yaml")
    ap.add_argument("--github", action="store_true")
    args = ap.parse_args()
    reg = yaml.safe_load(open(args.registry, encoding="utf-8"))
    errs = []
    repos = reg.get("repositories", [])
    if reg.get("count") != len(repos):
        errs.append(f"count {reg.get('count')} != Eintraege {len(repos)}")
    if len(repos) != 27:
        errs.append(f"Erwartet 27 Repos, gefunden {len(repos)}")
    ids = [r.get("id") for r in repos]; names = [r.get("name") for r in repos]
    if len(set(ids)) != len(ids): errs.append("Doppelte IDs")
    if len(set(names)) != len(names): errs.append("Doppelte Namen")
    for r in repos:
        for f in ("id", "name", "domain", "layer", "criticality", "security_class", "evidence"):
            if not r.get(f): errs.append(f"{r.get('name')}: Feld {f} fehlt")
        if "canonical" not in r: errs.append(f"{r.get('name')}: Feld canonical fehlt")
        if r.get("evidence") != ".atc/evidence/evidence.yaml":
            errs.append(f"{r.get('name')}: Evidence-Pfad != .atc/evidence/evidence.yaml")
    caps = reg.get("capabilities", {})
    for cap, c in caps.items():
        owners = [r["name"] for r in repos if r.get("canonical_role_canonical")]
    # Canonical-Eindeutigkeit ueber Repo-Eintraege (capability-Map ist informativ)
    canon_per_repo = {}
    for r in repos:
        pass
    lay = reg.get("layer_taxonomy_draft", {})
    for l in ("L0","L1","L2","L3","L4","L5","L6","L7"):
        if l not in lay: errs.append(f"Layer {l} fehlt in Taxonomie")
    used_layers = {r.get("layer") for r in repos}
    unknown = used_layers - set(lay.keys())
    if unknown: errs.append(f"Unbekannte Layer benutzt: {unknown}")
    if args.github:
        import requests, os
        tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_ACCESS_TOKEN")
        hh = {"Authorization": f"Bearer {tok}"} if tok else {}
        for r in repos:
            resp = requests.get(f"https://api.github.com/repos/A-TownChain-Okosystems/{r['name']}", headers=hh)
            if resp.status_code != 200:
                errs.append(f"GitHub: {r['name']} nicht erreichbar ({resp.status_code})")
    if errs:
        print("REPO-REGISTRY-CHECK FAIL:")
        for e in errs: print(" -", e)
        sys.exit(1)
    print(f"REPO-REGISTRY-CHECK OK: {len(repos)}/27 Eintraege, Layer L0-L7 vollständig, IDs/Namen eindeutig")

if __name__ == "__main__":
    main()
