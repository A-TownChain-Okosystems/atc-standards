#!/usr/bin/env python3
import argparse, json, os, re, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES={"Cargo.lock":"cargo","package-lock.json":"npm","npm-shrinkwrap.json":"npm","requirements.txt":"python","requirements-dev.txt":"python","go.sum":"go"}
SKIP={".git","target","node_modules",".venv","venv","__pycache__"}

def scan(root):
    out=[]; errors=[]
    for p in root.rglob("*"):
        if not p.is_file() or p.name not in FILES or any(x in p.parts for x in SKIP): continue
        eco=FILES[p.name]
        try:
            if eco=="cargo":
                import tomllib; data=tomllib.loads(p.read_text())
                for x in data.get("package",[]):
                    if x.get("name") and x.get("version"):
                        out.append({"ecosystem":"cargo","name":x["name"],"version":x["version"],"checksum":x.get("checksum"),"dependencies":[re.split(r"\\s+",d,1)[0] for d in x.get("dependencies",[])],"manifest":str(p.relative_to(root))})
            elif eco=="npm":
                data=json.loads(p.read_text())
                for loc,x in (data.get("packages") or {}).items():
                    if loc and x.get("name"):
                        out.append({"ecosystem":"npm","name":x["name"],"version":x.get("version"),"source":x.get("resolved"),"integrity":x.get("integrity"),"dependencies":list((x.get("dependencies") or {}).keys()),"manifest":str(p.relative_to(root))})
            elif eco=="python":
                for no,line in enumerate(p.read_text().splitlines(),1):
                    line=line.strip()
                    if not line or line.startswith("#"): continue
                    m=re.match(r"([A-Za-z0-9_.-]+)\\s*==\\s*([^;\\s]+)",line)
                    if not m: errors.append(f"{p}:{no}: unpinned/unsupported requirement: {line}")
                    else: out.append({"ecosystem":"python","name":m.group(1).lower(),"version":m.group(2),"dependencies":[],"manifest":str(p.relative_to(root))})
            else:
                seen=set()
                for line in p.read_text().splitlines():
                    m=re.match(r"([^\\s]+)\\s+(v[^\\s]+)\\s+h1:",line)
                    if m and (m.group(1),m.group(2)) not in seen:
                        seen.add((m.group(1),m.group(2))); out.append({"ecosystem":"go","name":m.group(1),"version":m.group(2),"dependencies":[],"manifest":str(p.relative_to(root))})
        except Exception as e: errors.append(f"{p}: {e}")
    return out,errors

def key(x): return (x.get("ecosystem"),x.get("name"),x.get("version"))
def graph(nodes,out):
    out.mkdir(parents=True,exist_ok=True); byname={}
    for n in nodes: byname.setdefault((n["ecosystem"],n["name"]),[]).append(n)
    edges=[]
    for n in nodes:
        src=f'{n["ecosystem"]}:{n["name"]}@{n["version"]}'
        for dep in n.get("dependencies",[]):
            for (eco,name),vals in byname.items():
                if name==dep:
                    v=vals[0]; edges.append({"from":src,"to":f'{v["ecosystem"]}:{v["name"]}@{v["version"]}'}); break
    g={"schema":"ATC-DEP-GRAPH-1","nodes":sorted(nodes,key=key),"edges":sorted(edges,key=lambda e:(e["from"],e["to"]))}
    (out/"dependency-graph.json").write_text(json.dumps(g,indent=2,sort_keys=True)+"\n")
    (out/"dependency-graph.dot").write_text("digraph dependencies {\n"+"\n".join(f'  "{e["from"]}" -> "{e["to"]}";' for e in g["edges"])+"\n}\n")
    return g

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True)
    g=sub.add_parser("graph"); g.add_argument("--root",default="."); g.add_argument("--out",default="artifacts/dependency")
    r=sub.add_parser("review"); r.add_argument("--out",default="artifacts/dependency"); r.add_argument("--advisories",default="security/advisories.json"); r.add_argument("--policy",default="security/dependency-policy.json")
    a=ap.parse_args(); root=(Path(a.root).resolve() if a.cmd=="graph" else ROOT); nodes,errors=scan(root); out=Path(a.out)
    if a.cmd=="graph":
        g=graph(nodes,out); result={"schema":"ATC-DEP-RESULT-1","status":"BLOCKED" if errors else "PASS","node_count":len(nodes),"errors":errors,"graph_sha256":hashlib.sha256(json.dumps(g,sort_keys=True).encode()).hexdigest()}; (out/"dependency-result.json").write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps(result)); return int(bool(errors))
    advis=(ROOT/a.advisories); advis=json.loads(advis.read_text()).get("advisories",[]) if advis.exists() else []; policy=json.loads((ROOT/a.policy).read_text()); findings=[]
    for n in nodes:
        for ad in advis:
            if ad.get("ecosystem")==n.get("ecosystem") and ad.get("package")==n.get("name") and n.get("version") in ad.get("versions",[]): findings.append({"severity":ad.get("severity","unknown"),"package":n["name"],"version":n["version"],"advisory":ad.get("id")})
    bad=[f for f in findings if f["severity"].lower() in {x.lower() for x in policy.get("block_severities",["critical","high"])}]; status="BLOCKED" if errors else ("FAIL" if bad else "PASS"); out.mkdir(parents=True,exist_ok=True)
    result={"schema":"ATC-DEP-REVIEW-1","status":status,"source_sha":os.getenv("GITHUB_SHA","unknown"),"dependency_count":len(nodes),"scan_errors":errors,"findings":findings,"blocking_findings":bad}; (out/"dependency-review.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); print(json.dumps({"status":status,"dependencies":len(nodes),"findings":len(findings)})); return int(status!="PASS")
if __name__=="__main__": raise SystemExit(main())