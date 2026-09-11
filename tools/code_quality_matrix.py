#!/usr/bin/env python3
"""ATC Code Quality Matrix — Erhebung & Prüfung (ATC-STD-ENG-001 REQ-ENG-011)

Liest registry/code-quality-matrix.yaml (SSOT) und prüft je Repository gegen den
GitHub-API-Ist-Zustand: (1) Sprach-Match, (2) CI-Gates-Vorhandensein
(gemäß Matrix ci_gates — Vorhandensein von Workflows/Job-Steps),
(3) Determinism-Gate für D-CRITICAL-Repos.
Ergebnis: docs/CODE-QUALITY-MATRIX.md + Exit-Code != 0 bei Abweichung (Fail Closed,
REQ-ENG-012 Evidenz-Pflicht: keine synthetischen PASS-Nachweise).

Aufruf: python3 tools/code_quality_matrix.py [--repo NAME]
"""
import os, sys, json, re, yaml, urllib.request, datetime

ORG = "A-TownChain-Okosystems"
TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN", "")
H = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}
BASE = os.path.join(os.path.dirname(__file__), "..")
EXCLUDED = {"demo-repository"}  # Owner-Entscheidung 11.09.2026

def api(url):
    try:
        return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=H)).read())
    except Exception:
        return None

def repo_ist(name):
    """Ist-Daten: Primärsprache + Workflow-Dateien."""
    tree = api(f"https://api.github.com/repos/{ORG}/{name}/git/trees/main?recursive=1")
    wfs = [t["path"].split("/")[-1] for t in tree.get("tree", [])
           if t["path"].startswith(".github/workflows/")] if tree else []
    info = api(f"https://api.github.com/repos/{ORG}/{name}")
    return {"language": (info or {}).get("language") or "?", "workflows": wfs}

def wf_covers(wfs, gate):
    """Heuristik: Gate als Workflow-Name oder Job-Stichwort abgedeckt."""
    g = gate.lower()
    keys = {"determinism": ["determin", "consensus"], "security": ["security", "codeql", "dependency-review"],
            "dependency-audit": ["dependency", "dependabot", "audit"], "unit": ["test", "ci", "governance"],
            "integration": ["test", "integration"], "format": ["format", "lint", "ci"], "lint": ["lint", "ci"],
            "build": ["build", "ci"], "docs": ["docs", "md"], "conformance": ["conformance", "test"],
            "cross-registry": ["cross", "ci"], "registry-validation": ["registry", "ci", "governance"]}
    return any(any(k in w.lower() for k in keys.get(g, [g])) for w in wfs)

def main():
    matrix = yaml.safe_load(open(os.path.join(BASE, "registry/code-quality-matrix.yaml")))
    only = sys.argv[sys.argv.index("--repo") + 1] if "--repo" in sys.argv else None
    rows, fails = [], 0
    for name, m in matrix["repositories"].items():
        if name in EXCLUDED or (only and name != only):
            continue
        ist = repo_ist(name)
        lang_ok = ist["language"] in [l.capitalize() if l == "atclang" else l.capitalize() for l in m["language"]] or ist["language"].lower() in m["language"]
        gates_missing = [g for g in m["ci_gates"] if not wf_covers(ist["workflows"], g)]
        verdict = "PASS" if (lang_ok and not gates_missing) else "FINDING"
        if verdict == "FINDING":
            fails += 1
        rows.append((name, m["layer"], m["determinism"], ist["language"], "✅" if lang_ok else "❌",
                     ", ".join(m["ci_gates"]), ", ".join(gates_missing) or "—", verdict))
    # Report
    d = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"# ATC Code Quality Matrix — Ist-Erhebung ({d})",
             "", f"Standard: ATC-STD-ENG-001 (REQ-ENG-011) · SSOT: registry/code-quality-matrix.yaml · Exit: {'0' if not fails else '1'}",
             "", f"| Repository | Layer | Det.-Klasse | Ist-Sprache | Lang | CI-Gates (Soll) | Fehlt | Verdict |",
             "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} |")
    lines.append(f"\n**Ergebnis: {len(rows) - fails}/{len(rows)} PASS, {fails} FINDING(s)** (Fail Closed; Findings → ATC-STD-BUG-001)")
    out = os.path.join(BASE, "docs/CODE-QUALITY-MATRIX.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines[-3:]))
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
