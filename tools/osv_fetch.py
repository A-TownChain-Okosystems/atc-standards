#!/usr/bin/env python3
import argparse, hashlib, json, urllib.request
from pathlib import Path
from osv_snapshot import normalize, validate

ECO={"cargo":"crates.io","npm":"npm","python":"PyPI","go":"Go"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--graph",default="artifacts/dependency/dependency-graph.json")
    ap.add_argument("--raw-output",default="artifacts/dependency/osv-response.json")
    ap.add_argument("--advisory-output",default="security/advisories.json")
    ap.add_argument("--endpoint",default="https://api.osv.dev/v1/querybatch")
    args=ap.parse_args()
    graph=json.loads(Path(args.graph).read_text())
    queries=sorted([
        {"package":{"name":n["name"],"ecosystem":ECO[n["ecosystem"]]},"version":n["version"]}
        for n in graph.get("nodes",[]) if n.get("ecosystem") in ECO and n.get("name") and n.get("version")
    ],key=lambda q:(q["package"]["ecosystem"],q["package"]["name"],q["version"]))
    body=json.dumps({"queries":queries},sort_keys=True,separators=(",",":")).encode()
    req=urllib.request.Request(args.endpoint,data=body,headers={"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=30) as resp:
        raw=json.load(resp)
    raw_bytes=(json.dumps(raw,sort_keys=True,separators=(",",":"))+"\n").encode()
    raw_sha=hashlib.sha256(raw_bytes).hexdigest()
    Path(args.raw_output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.raw_output).write_bytes(raw_bytes)
    advisories=[]
    for result in raw.get("results",[]):
        advisories.extend(result.get("vulns",[]))
    payload={"schema":"ATC-DEP-ADVISORY-1",
             "source":{"format":"OSV","endpoint":args.endpoint,"input_sha256":raw_sha,"raw_response_sha256":raw_sha},
             "advisories":normalize(advisories)}
    errors=validate(payload)
    if errors:
        raise SystemExit("invalid OSV snapshot: "+"; ".join(errors))
    Path(args.advisory_output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.advisory_output).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"queries":len(queries),"advisories":len(payload["advisories"]),"raw_response_sha256":raw_sha},sort_keys=True))

if __name__=="__main__": main()
