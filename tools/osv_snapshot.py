#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

SCHEMA="ATC-DEP-ADVISORY-1"
SEVERITIES={"critical","high","medium","low","unknown"}
ECO_MAP={"crates.io":"cargo","npm":"npm","PyPI":"python","Go":"go","cargo":"cargo","npmjs":"npm","pypi":"python","golang":"go"}

def normalize(raw):
    out=[]
    for item in raw if isinstance(raw,list) else raw.get("advisories",[]):
        aliases=item.get("aliases",[])
        aid=item.get("id") or (aliases[0] if aliases else None)
        affected=[]
        for a in item.get("affected",[]):
            eco=ECO_MAP.get(a.get("package",{}).get("ecosystem"),a.get("package",{}).get("ecosystem"))
            pkg=a.get("package",{}).get("name")
            if not eco or not pkg: continue
            events=[]
            for r in a.get("ranges",[]):
                for ev in r.get("events",[]): events.append({"introduced":ev.get("introduced"),"fixed":ev.get("fixed"),"last_affected":ev.get("last_affected")})
            affected.append({"ecosystem":eco,"package":pkg,"ranges":events,"versions":sorted(set(a.get("versions",[])))})
        sev="unknown"
        db=item.get("database_specific",{})
        rawsev=db.get("severity")
        if isinstance(rawsev,str) and rawsev.lower() in SEVERITIES: sev=rawsev.lower()
        elif item.get("severity"):
            sev=str(item["severity"][0].get("score","unknown")).lower()
        if aid and affected:
            out.append({"id":aid,"summary":item.get("summary",""),"severity":sev,"affected":affected,"aliases":sorted(set(aliases)),"modified":item.get("modified"),"published":item.get("published")})
    return sorted(out,key=lambda x:(x["id"],json.dumps(x,sort_keys=True)))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    ap.add_argument("--output",default="security/advisories.json")
    args=ap.parse_args()
    raw=json.loads(Path(args.input).read_text())
    advisories=normalize(raw)
    payload={"schema":SCHEMA,"source":{"format":"OSV","input_sha256":hashlib.sha256(Path(args.input).read_bytes()).hexdigest()},"advisories":advisories}
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"schema":SCHEMA,"advisories":len(advisories),"input_sha256":payload["source"]["input_sha256"]},sort_keys=True))
if __name__=="__main__": main()
