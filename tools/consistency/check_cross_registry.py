#!/usr/bin/env python3
"""check_cross_registry.py — Cross-Registry-Konsistenztest (SCR-0091, Owner-Bereinigungsplan).

Erzwingt die SSOT-Kette registry/standards.yaml -> registry.lock -> Views
-> Cross-Registry-Validierung. Bei JEGLICHER Abweichung: Exit-Code 1.

Regeln:
  R1  jede Standard-ID ist eindeutig
  R2  jede Registry-ID besitzt genau eine kanonische Datei (Ausnahme: dokumentiertes EXEMPT)
  R3  jede kanonische Standarddatei besitzt einen Registry-Eintrag
  R4  Versionen stimmen ueberein (Registry <-> Standarddatei-Frontmatter)
  R5  Statuswerte stimmen ueberein (Registry <-> Standarddatei-Frontmatter)
  R6  Taxonomie und Registry sind synchron
  R7  keine View enthaelt widerspruechliche aktuelle Zahlen (State-Block == Ist)
  R8  APPROVED wird nicht mit IMPLEMENTED gleichgesetzt (KPI-Trennung vorhanden)
  R9  keine View enthaelt veraltete hartcodierte Governance-Daten
      (ATC-STD-000-Version/Status in Views == Registry)
  R10 generierte Views sind reproduzierbar (Generator-Idempotenz)
"""
import hashlib, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "registry", "standards.yaml")
FAILS = []

def fail(rule, msg):
    FAILS.append(f"[{rule}] {msg}")

def _vge(a, b):
    return tuple(int(x) for x in a.split(".")) >= tuple(int(x) for x in b.split("."))

def main():
    # Registry laden
    reg_text = open(REG, encoding="utf-8").read()
    entries, ids = [], []
    for line in reg_text.splitlines():
        m = re.search(r"- \{id: (ATC-\S+?),.*?version: \"?([\d.]+)\"?, status: (\w+)", line)
        if m:
            entries.append(m.group(1))
            ids.append({"id": m.group(1), "version": m.group(2), "status": m.group(3), "line": line})
    reg_sha = hashlib.sha256(open(REG, "rb").read()).hexdigest()

    # R1: Eindeutigkeit
    dup = {i for i in entries if entries.count(i) > 1}
    if dup:
        fail("R1", "Doppelte Registry-IDs: " + ", ".join(sorted(dup)))
    print(f"R1 Eindeutigkeit: {len(entries)} Eintraege, {len(dup)} Duplikate")

    # R2/R3: Registry <-> Dateien
    std_dir = os.path.join(ROOT, "standards")
    reg_by_id = {e["id"]: e for e in ids}
    files = []
    for dp, _, fs in os.walk(std_dir):
        for f in fs:
            if f.endswith(".md"):
                files.append((os.path.join(dp, f), os.path.splitext(f)[0]))
    file_ids = {fid for _, fid in files}
    no_file, masters = [], []
    for e in ids:
        i = e["id"]
        if i in file_ids:
            continue
        mf = re.search(r"file: (\S+?),", e["line"])
        if mf and os.path.exists(os.path.join(ROOT, mf.group(1))):
            masters.append(i); continue
        hits = [p for p in ("governance", "governance/constitution") if os.path.exists(os.path.join(ROOT, p, i + ".md"))]
        if os.path.exists(os.path.join(ROOT, "registry", "standards", i + ".yaml")):
            masters.append(i); continue
        if hits:
            masters.append(i); continue
        no_file.append(i)
    no_entry = [fid for _, fid in files if fid not in reg_by_id]
    if no_file:
        fail("R2", "Registry-IDs ohne kanonische Datei: " + ", ".join(no_file[:10]))
    if no_entry:
        fail("R3", "Standarddateien ohne Registry-Eintrag: " + ", ".join(no_entry[:10]))
    print(f"R2/R3 Datei-Relation: {len(no_file)} ohne Datei, {len(masters)} Master-Dokumente ausserhalb, {len(no_entry)} ohne Eintrag")

    # R4/R5: Version/Status Registry <-> Frontmatter
    v_drift = s_drift = 0
    for path, fid in files:
        e = reg_by_id.get(fid)
        if not e:
            continue
        head = open(path, encoding="utf-8").read(4000)
        mv = re.search(r'version:\s*"?([\d.]+)"?', head)
        ms = re.search(r'status:\s*(\w+)', head)
        if mv and mv.group(1) != e["version"]:
            v_drift += 1
            if v_drift <= 5: fail("R4", f"{fid}: Registry v{e['version']} vs Datei v{mv.group(1)}")
        if ms and ms.group(1).lower() != e["status"].lower():
            s_drift += 1
            if s_drift <= 5: fail("R5", f"{fid}: Registry {e['status']} vs Datei {ms.group(1)}")
    print(f"R4/R5 Version/Status-Drift: {v_drift}/{s_drift}")

    # R6: Taxonomie-Sync
    import yaml
    tax = yaml.safe_load(open(os.path.join(ROOT, "registry", "taxonomy.yaml"), encoding="utf-8"))
    reg_yaml = yaml.safe_load(open(REG, encoding="utf-8"))
    std_list = reg_yaml.get("standards", [])
    fam_by_name = {}
    for d in tax["taxonomy"]["domains"]:
        for f_ in d["families"]:
            fam_by_name[f_["name"]] = f_
    reg_counts = {}
    unmatched = []
    for e in std_list:
        cat = e.get("category", "?")
        key = cat + " (familie)" if (cat in fam_by_name and (cat + " (familie)") in fam_by_name) else cat
        reg_counts[key] = reg_counts.get(key, 0) + 1
        if key not in fam_by_name:
            unmatched.append(e.get("id", "?"))
    if unmatched:
        fail("R6", "Registry-Standards ohne Taxonomie-Familie: " + ", ".join(sorted(set(unmatched))[:10]))
    for name, f_ in fam_by_name.items():
        if f_.get("standards_count", 0) != reg_counts.get(name, 0):
            fail("R6", f"Taxonomie-Drift Familie '{name}': {f_.get('standards_count')} != Registry {reg_counts.get(name, 0)}")
    print(f"R6 Taxonomie: {len(fam_by_name)} Familien gespiegelt, {len(unmatched)} ohne Zuordnung")

    # R7: State-Block in README == Ist
    rd = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    m = re.search(r"standards_total: (\d+)", rd)
    if not m:
        fail("R7", "README State-Block fehlt")
    elif int(m.group(1)) != len(entries):
        fail("R7", f"README standards_total {m.group(1)} != Registry {len(entries)}")
    m = re.search(r'registry_sha256: "([0-9a-f]{16,64})"', rd)
    if not m:
        fail("R7", "README registry_sha256 fehlt")
    elif m.group(1) not in reg_sha:
        fail("R7", "README registry_sha256 != aktueller Registry-SHA")
    m = re.search(r"standards_approved: (\d+)", rd)
    n_app = sum(1 for e in ids if e["status"] == "approved")
    if m and int(m.group(1)) != n_app:
        fail("R7", f"README approved {m.group(1)} != Registry {n_app}")
    print(f"R7 State-Block: total/approved geprueft gegen Registry ({len(entries)}/{n_app})")

    # R8: KPI-Trennung
    if "Standards implementiert" in rd and "unzulässig" not in rd and "unzulaessig" not in rd:
        fail("R8", "README identifiziert APPROVED-als-IMPLEMENTED-Aussage nicht als unzulaessig")
    if "specification-only" not in rd and "specification_only" not in rd:
        fail("R8", "Implementierungs-KPI ohne specification-only-Trennung")
    print("R8 KPI-Trennung: geprueft")

    # R9: keine veraltete hartcodierte Governance-Daten in Views
    e000 = reg_by_id.get("ATC-STD-000", {})
    for view in ["README.md", "AGENT_MANIFEST.md", "STATUS.md"]:
        vt = open(os.path.join(ROOT, view), encoding="utf-8").read()
        if view == "STATUS.md":
            cut = vt.find("\n## ")
            vt = vt[:cut] if cut > 0 else vt  # Audit-Trail = historische Doku, erlaubt (SCR-0091)
        for mm in re.finditer(r"ATC-STD-000[^\n]{0,80}?v(\d+\.\d+\.\d+)", vt):
            if e000 and mm.group(1) != e000["version"]:
                fail("R9", f"{view}: ATC-STD-000 v{mm.group(1)} != Registry v{e000['version']}")
    print("R9 Hartcode-Drift in Views: geprueft")

    # R10: Reproduzierbarkeit (Generator idempotent bis auf Zeitstempel)
    before = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "gen_views", "generate_views.py")],
                       capture_output=True, text=True)
    after = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    norm = lambda t: re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}( UTC\+2)?", "TS", t)
    if r.returncode != 0 or norm(before) != norm(after):
        fail("R10", "generate_views.py nicht idempotent reproduzierbar")
    print("R10 Reproduzierbarkeit: geprueft")


    # R11: ATC-STD-000-Bootstrap-Sunset technisch erzwungen (Owner-Audit 11.09.2026 P0-2)
    std003 = open(os.path.join(ROOT, "standards", "governance", "ATC-STD-003.md"), encoding="utf-8").read()
    msun = re.search(r"Sunset mit ATC-STD-000 v([\d.]+)", std003)
    if not msun:
        fail("R11", "ATC-STD-003 par.6: keine maschinenlesbare Sunset-Version (Sunset mit ATC-STD-000 vX.Y.Z)")
    else:
        sunset = msun.group(1)
        e000 = reg_by_id.get("ATC-STD-000", {})
        cur = e000.get("version", "0")
        if _vge(cur, sunset):
            f000 = os.path.join(ROOT, "governance", "ATC-STD-000.md")
            if not os.path.exists(f000):
                fail("R11", "ATC-STD-000: Datei fehlt - EXEMPT endet mit v" + sunset)
            else:
                head = open(f000, encoding="utf-8").read(4000)
                mv = re.search(r'version:\s*"?([\d.]+)"?', head)
                mst = re.search(r"status:\s*(\w+)", head)
                if mv and mv.group(1) != cur:
                    fail("R11", "ATC-STD-000 Datei v" + mv.group(1) + " != Registry v" + cur)
                if mst and mst.group(1).lower() != e000.get("status", "").lower():
                    fail("R11", "ATC-STD-000 Datei-Status " + mst.group(1) + " != Registry " + str(e000.get("status")))
        if _vge(cur, sunset) and tuple(int(x) for x in cur.split(".")) > tuple(int(x) for x in sunset.split(".")) and e000.get("status") != "approved":
            fail("R11", "ATC-STD-000 v" + cur + " ueberschreitet Sunset v" + sunset + " ohne APPROVED - par.9-Freigabe (Owner) fehlt")
        print("R11 ATC-STD-000-Sunset: Sunset v" + sunset + ", Registry v" + cur + " - geprueft")

    print()
    if FAILS:
        print("RESULT: CROSS-REGISTRY NON-COMPLIANT")
        for f_ in FAILS:
            print("  " + f_)
        sys.exit(1)
    print("RESULT: CROSS-REGISTRY ALL COMPLIANT")

if __name__ == "__main__":
    main()
