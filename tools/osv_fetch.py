#!/usr/bin/env python3
import argparse, json, urllib.request
from pathlib import Path

ECO={"cargo":"crates.io","npm":"npm","python":"PyPI","go":"Go"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--graph",default="artifacts/dependency/dependency-graph.json")
    ap.add_argument("--raw-output",default="artifacts/dependency/osv-response.json")
    ap.add_argument("--advisory-output",default="security/advisories.json")
    ap.add_argument("--endpoint",default="https://api.osv.dev/v1/querybatch")
    args=ap.parse_args()
    graph=json.loads(Path(args.graph).read_text())
    queries=[]
    for n in graph.get("nodes",[]):
        if n.get("ecosystem") in ECO and n.get("name") and n.get("version"):
            queries.append({"package":{"name":n["name"],"ecosystem":ECO[n["ecosystem"]]},"version":n["version"]})
    queries=sorted(queries,key=lambda q:(q["package"]["ecosystem"],q["package"]["name"],q["version"]))
    req=urllib.request.Request(args.endpoint,data=json.dumps({"queries":queries}).encode(),headers={"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=30) as resp: raw=json.load(resp)
    Path(args.raw_output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.raw_output).write_text(json.dumps(raw,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"queries":len(queries),"raw_output":args.raw_output,"advisory_output":args.advisory_output},sort_keys=True))
if __name__=="__main__": main()
