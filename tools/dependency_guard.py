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
                        out.append({"ecosystem":"cargo","name":x["name"],"version":x["version"],"checksum":x.get("checksum"),"dependencies":[re.split(r"\s+",d,1)[0] for d in x.get("dependencies",[])],"manifest":str(p.relative_to(root))})
            elif eco=="npm":
                data=json.loads(p.read_text())
                for loc,x in (data.get("packages") or {}).items():
                    if loc and x.get("name"):
                        out.append({"ecosystem":"npm","name":x["name"],"version":x.get("version"),"source":x.get("resolved"),"integrity":x.get("integrity"),"dependencies":list((x.get("dependencies") or {}).keys()),"manifest":str(p.relative_to(root))})
            elif eco=="python":
                for no,line in enumerate(p.read_text().splitlines(),1):
                    line=line.strip()
                    if not line or line.startswith("#"): continue
                    m=re.match(r"([A-Za-z0-9_.-]+)\s*==\s*([^;\s]+)",line)
                    if not m: errors.append(f"{p}:{no}: unpinned/unsupported requirement: {line}")
                    else: out.append({"ecosystem":"python","name":m.group(1).lower(),"version":m.group(2),"dependencies":[],"manifest":str(p.relative_to(root))})
            else:
                seen=set()
                for line in p.read_text().splitlines():
                    m=re.match(r"([^\s]+)\s+(v[^\s]+)\s+h1:",line)
                    if m and (m.group(1),m.group(2)) not in seen:
                        seen.add((m.group(1),m.group(2))); out.append({"ecosystem":"go","name":m.group(1),"version":m.group(2),"dependencies":[],"manifest":str(p.relative_to(root))})
        except Exception as e: errors.append(f"{p}: {e}")
    return out,errors

def key(x): return (x.get("ecosystem"),x.get("name"),x.get("version"))
def fingerprint(nodes): return {key(x): x for x in nodes}
def compare_nodes(base,head):
    b,h=fingerprint(base),fingerprint(head); added=sorted([h[k] for k in set(h)-set(b)],key=key); removed=sorted([b[k] for k in set(b)-set(h)],key=key); changed=[]
    for bk,bv in b.items():
        candidates=[x for x in h.values() if x.get("ecosystem")==bv.get("ecosystem") and x.get("name")==bv.get("name")]
        for x in candidates:
            if x.get("version")!=bv.get("version") and key(x) not in b: changed.append({"from":bv,"to":x})
    return added,removed,changed

def graph(nodes,out):
    out.mkdir(parents=True,exist_ok=True); byname={}
    for n in nodes: byname.setdefault((n["ecosystem"],n["name"]),[]).append(n)
    edges=[]
    for n in nodes:
        src=f'{n["ecosystem"]}:{n["name"]}@{n["version"]}'
        for dep in n.get("dependencies",[]):
            matches=[v for (eco,name),vals in byname.items() if eco==n["ecosystem"] and name==dep for v in vals]
            if matches:
                v=sorted(matches,key=key)[0]; edges.append({"from":src,"to":f'{v["ecosystem"]}:{v["name"]}@{v["version"]}'})
    g={"schema":"ATC-DEP-GRAPH-1","nodes":sorted(nodes,key=key),"edges":sorted(set((e["from"],e["to"]) for e in edges))}
    g["edges"]=[{"from":a,"to":b} for a,b in g["edges"]]
    (out/"dependency-graph.json").write_text(json.dumps(g,indent=2,sort_keys=True)+"\n")
    (out/"dependency-graph.dot").write_text("digraph dependencies {\n"+"\n".join(f'  "{e["from"]}" -> "{e["to"]}";' for e in g["edges"])+"\n}\n")
    return g

def load_base():
    raw=os.getenv("ATC_DEP_BASE_JSON"); ref=os.getenv("ATC_DEP_BASE_REF")
    if not raw: return [],ref,[]
    p=Path(raw)
    if not p.exists(): return [],ref,[f"base graph not found: {p}"]
    try:
        d=json.loads(p.read_text())
        if d.get("schema")!="ATC-DEP-GRAPH-1": return [],ref,["invalid base graph schema"]
        return d.get("nodes",[]),ref,[]
    except Exception as e: return [],ref,[f"invalid base graph: {e}"]

def semver(v):
    v=v.lstrip("v="); m=re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?",v)
    return (int(m.group(1)),int(m.group(2)),int(m.group(3)),m.group(4) or "") if m else None

def pep440(v):
    m=re.match(r"^(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:[-_.]?([A-Za-z]+)(\d+)?)?",v)
    if not m:return None
    return (int(m.group(1)),int(m.group(2) or 0),int(m.group(3) or 0),(m.group(4) or "").lower(),int(m.group(5) or 0))

def version_cmp(a,b,eco):
    x=pep440(a) if eco=="python" else semver(a); y=pep440(b) if eco=="python" else semver(b)
    if x is None or y is None:return None
    return (x>y)-(x<y)

def range_match(version,events,ecosystem):
    if version is None or not events:return False,"unknown"
    if ecosystem not in {"cargo","npm","go","python"}:return False,"unsupported"
    if (pep440(version) if ecosystem=="python" else semver(version)) is None:return False,"unsupported"
    affected=False
    for ev in events:
        intro=ev.get("introduced")
        if intro not in (None,"0"):
            c=version_cmp(version,intro,ecosystem)
            if c is None:return False,"unsupported"
            if c<0:continue
        fixed=ev.get("fixed")
        if fixed:
            c=version_cmp(version,fixed,ecosystem)
            if c is None:return False,"unsupported"
            if c>=0:continue
        last=ev.get("last_affected")
        if last:
            c=version_cmp(version,last,ecosystem)
            if c is None:return False,"unsupported"
            if c>0:continue
        affected=True
    return affected,"range"

def advisory_matches(n,ad):
    for a in ad.get("affected",[]):
        if a.get("ecosystem")!=n.get("ecosystem") or a.get("package")!=n.get("name"):continue
        if n.get("version") in a.get("versions",[]):return True,"exact"
        matched,mode=range_match(n.get("version"),a.get("ranges",[]),n.get("ecosystem"))
        if matched:return True,mode
        if mode=="unsupported":return False,"unsupported"
    return False,"none"

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True)
    g=sub.add_parser("graph");g.add_argument("--root",default=".");g.add_argument("--out",default="artifacts/dependency")
    r=sub.add_parser("review");r.add_argument("--out",default="artifacts/dependency");r.add_argument("--advisories",default="security/advisories.json");r.add_argument("--policy",default="security/dependency-policy.json")
    a=ap.parse_args();root=Path(a.root).resolve() if a.cmd=="graph" else ROOT;nodes,errors=scan(root);out=Path(a.out)
    if a.cmd=="graph":
        g=graph(nodes,out); result={"schema":"ATC-DEP-RESULT-1","status":"BLOCKED" if errors else "PASS","node_count":len(nodes),"errors":errors,"graph_sha256":hashlib.sha256(json.dumps(g,sort_keys=True).encode()).hexdigest()};(out/"dependency-result.json").write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result));return int(bool(errors))
    advis=json.loads((ROOT/a.advisories).read_text()).get("advisories",[]) if (ROOT/a.advisories).exists() else [];policy=json.loads((ROOT/a.policy).read_text());findings=[];range_errors=[]
    for n in nodes:
        for ad in advis:
            matched,mode=advisory_matches(n,ad)
            if mode=="unsupported":range_errors.append({"advisory":ad.get("id"),"package":n.get("name"),"version":n.get("version")})
            if matched:findings.append({"severity":ad.get("severity","unknown"),"package":n["name"],"version":n["version"],"advisory":ad.get("id"),"match_type":mode})
    bad=[f for f in findings if f["severity"].lower() in {x.lower() for x in policy.get("block_severities",["critical","high"])}]
    base_nodes,base_ref,base_errors=load_base()
    if base_errors:errors.extend(base_errors)
    added,removed,changed=compare_nodes(base_nodes,nodes) if os.getenv("ATC_DEP_BASE_JSON") and not base_errors else (nodes,[],[])
    if range_errors:errors.append("unsupported advisory range evaluation: "+json.dumps(range_errors,sort_keys=True))
    status="BLOCKED" if errors else ("FAIL" if bad else "PASS")
    result={"schema":"ATC-DEP-REVIEW-1","status":status,"source_sha":os.getenv("GITHUB_SHA","unknown"),"base_ref":base_ref,"dependency_count":len(nodes),"scan_errors":errors,"added":added,"removed":removed,"changed":changed,"findings":findings,"blocking_findings":bad}
    out.mkdir(parents=True,exist_ok=True);(out/"dependency-review.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");print(json.dumps({"status":status,"dependencies":len(nodes),"findings":len(findings)}));return int(status!="PASS")
if __name__=="__main__":raise SystemExit(main())
