#!/usr/bin/env python3
import argparse, hashlib, json, re, urllib.request
from pathlib import Path
from osv_snapshot import normalize, validate

ECO={"cargo":"crates.io","npm":"npm","python":"PyPI","go":"Go"}

def cvss_severity(score):
    try:
        s=float(score)
    except (TypeError,ValueError):
        return None
    if 9.0 <= s <= 10.0: return "critical"
    if 7.0 <= s < 9.0: return "high"
    if 4.0 <= s < 7.0: return "medium"
    if 0.0 <= s < 4.0: return "low"
    return None

def normalize_severity(item):
    raw=(item.get("database_specific") or {}).get("severity")
    if isinstance(raw,str) and raw.lower() in {"critical","high","medium","low","unknown"}:
        return raw.lower()
    candidates=[]
    for entry in item.get("severity") or []:
        if not isinstance(entry,dict): continue
        score=entry.get("score")
        if isinstance(score,(int,float)):
            candidates.append(float(score))
            continue
        if isinstance(score,str):
            match=re.search(r"(?:CVSS:[^/]+/)?[^\s]+",score)
            if match:
                # CVSS vectors contain no base score; OSV may provide numeric strings.
                try: candidates.append(float(score))
                except ValueError: pass
    mapped=[cvss_severity(x) for x in candidates]
    order={"critical":4,"high":3,"medium":2,"low":1}
    return max((x for x in mapped if x),key=lambda x:order[x],default="unknown")

def normalize(raw):
    out=[]
    for item in raw if isinstance(raw,list) else raw.get("advisories",[]):
        if not isinstance(item,dict): continue
        aliases=item.get("aliases") or []
        aid=item.get("id") or (aliases[0] if aliases else None)
        affected=[]
        for a in item.get("affected") or []:
            package=a.get("package") or {}
            eco=ECO_MAP.get(package.get("ecosystem"),package.get("ecosystem"))
            pkg=package.get("name")
            if not eco or not pkg: continue
            ranges=[]
            for r in a.get("ranges") or []:
                if not isinstance(r,dict): continue
                events=[{"introduced":ev.get("introduced"),"fixed":ev.get("fixed"),"last_affected":ev.get("last_affected")}
                        for ev in r.get("events") or [] if isinstance(ev,dict)]
                if events: ranges.append({"type":r.get("type"),"events":events})
            affected.append({"ecosystem":eco,"package":pkg,"ranges":ranges,"versions":sorted(set(a.get("versions") or []))})
        if aid and affected:
            out.append({"id":aid,"summary":item.get("summary",""),"severity":normalize_severity(item),
                        "affected":affected,"aliases":sorted(set(aliases)),"modified":item.get("modified"),"published":item.get("published")})
    return sorted(out,key=lambda x:(x["id"],json.dumps(x,sort_keys=True)))

ECO_MAP={"crates.io":"cargo","npm":"npm","PyPI":"python","Go":"go","cargo":"cargo","npmjs":"npm","pypi":"python","golang":"go"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--graph",default="artifacts/dependency/dependency-graph.json")
    ap.add_argument("--raw-output",default="artifacts/dependency/osv-response.json")
    ap.add_argument("--advisory-output",default="security/advisories.json")
    ap.add_argument("--endpoint",default="https://api.osv.dev/v1/querybatch")
    args=ap.parse_args()
    graph=json.loads(Path(args.graph).read_text())
    queries=sorted([{"package":{"name":n["name"],"ecosystem":ECO[n["ecosystem"]]},"version":n["version"]}
                    for n in graph.get("nodes",[]) if n.get("ecosystem") in ECO and n.get("name") and n.get("version")],
                   key=lambda q:(q["package"]["ecosystem"],q["package"]["name"],q["version"]))
    body=json.dumps({"queries":queries},sort_keys=True,separators=(",",":")).encode()
    req=urllib.request.Request(args.endpoint,data=body,headers={"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=30) as resp: raw=json.load(resp)
    raw_bytes=(json.dumps(raw,sort_keys=True,separators=(",",":"))+"\n").encode()
    raw_sha=hashlib.sha256(raw_bytes).hexdigest()
    Path(args.raw_output).parent.mkdir(parents=True,exist_ok=True); Path(args.raw_output).write_bytes(raw_bytes)
    advisories=[]
    for result in raw.get("results",[]): advisories.extend(result.get("vulns",[]))
    payload={"schema":"ATC-DEP-ADVISORY-1",
             "source":{"format":"OSV","endpoint":args.endpoint,"input_sha256":raw_sha,"raw_response_sha256":raw_sha},
             "advisories":normalize(advisories)}
    errors=validate(payload)
    if errors: raise SystemExit("invalid OSV snapshot: "+"; ".join(errors))
    Path(args.advisory_output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.advisory_output).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"queries":len(queries),"advisories":len(payload["advisories"]),"raw_response_sha256":raw_sha},sort_keys=True))
if __name__=="__main__": main()
