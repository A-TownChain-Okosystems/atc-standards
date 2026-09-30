#!/usr/bin/env python3
import argparse,os,re,sys,yaml
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))
SCHEMA=os.path.join(ROOT,"schemas","change-request.schema.yaml")
SHA=re.compile(r"^[0-9a-fA-F]{40}$")
AREAS={"ARCHITECTURE_SSOT","SPECIFICATION_CONTRACT","SOURCE_CODE","API","ABI_WIRE_FORMAT","STATE_STORAGE","SECURITY","TESTS","INTEGRATION","CI_CD","DOCUMENTATION","MIGRATION","COMPATIBILITY","RELEASE","AUDIT"}
LIFE={"UNANALYZED","ANALYZED","PLANNED","IMPLEMENTING","FIXED","RERUNNING","VERIFIED","CLOSED","REJECTED","FAILED","RESIDUAL"}
def extract(t):
 h=re.search(r"^##\s+Machine-readable Contract\s*$",t,re.M)
 if not h:return None
 fence=r"\x60\x60\x60"
 m=re.search(fence+r"yaml\s*\n(.*?)\n"+fence,t[h.end():],re.S)
 if not m:raise ValueError("missing YAML contract block")
 d=yaml.safe_load(m.group(1))
 if not isinstance(d,dict):raise ValueError("contract must be object")
 return d
def req(d,k,fields,e):
 x=d.get(k)
 if not isinstance(x,dict):e.append(k+" must be object");return
 for f in fields:
  if not isinstance(x.get(f),str) or not x[f].strip():e.append(k+"."+f+" required")
def validate(p):
 t=open(p,encoding="utf-8").read()
 try:d=extract(t)
 except Exception as x:return[str(x)]
 if d is None:return[]
 e=[]
 if d.get("schema_version")!=2:return["schema_version must be exactly 2"]
 s=yaml.safe_load(open(SCHEMA,encoding="utf-8"))
 e += ["missing top-level field: "+k for k in s.get("required",[]) if k not in d]
 if not re.fullmatch(r"SCR-[0-9]{4}",str(d.get("id",""))):e.append("id invalid")
 if not re.fullmatch(r"ATC-STD-[0-9]{3,}",str(d.get("affected_standard",""))):e.append("affected_standard invalid")
 for k in("proposed_change","motivation"):
  if not isinstance(d.get(k),str) or not d[k].strip():e.append(k+" required")
 if d.get("decision") not in{"ACCEPTED","REJECTED","PENDING"}:e.append("decision invalid")
 req(d,"purpose",["objective","problem_solved","system_benefit"],e)
 req(d,"rationale",["why","why_now","consequence_without_change","technical_rationale"],e)
 n=d.get("necessity")
 if not isinstance(n,dict):e.append("necessity must be object")
 else:
  if not isinstance(n.get("required"),bool):e.append("necessity.required boolean")
  if n.get("classification") not in{"MANDATORY","REQUIRED","CONDITIONAL","OPTIONAL","REJECTED"}:e.append("necessity.classification invalid")
  if not str(n.get("reason","")).strip():e.append("necessity.reason required")
 i=d.get("improvement")
 if not isinstance(i,dict) or not str(i.get("before","")).strip() or not str(i.get("after","")).strip():e.append("improvement before/after required")
 if not isinstance(i.get("dimensions"),dict) if isinstance(i,dict) else True:e.append("improvement.dimensions required")
 s=d.get("safety_security")
 for k in("security_impact","attack_surface_change","data_integrity","availability_reliability","new_failure_modes","rollback_recovery","residual_risk"):
  if not isinstance(s,dict) or not str(s.get(k,"")).strip():e.append("safety_security."+k+" required")
 if isinstance(s,dict) and s.get("safe") is True and not s.get("evidence"):e.append("safe=true requires evidence")
 rows=d.get("completeness",{}).get("matrix") if isinstance(d.get("completeness"),dict) else None
 if not isinstance(rows,list) or not rows:e.append("completeness.matrix required")
 else:
  seen=set()
  for r in rows:
   if not isinstance(r,dict) or r.get("area") not in AREAS:e.append("invalid completion area")
   elif r["area"] in seen:e.append("duplicate completion area: "+r["area"])
   else:seen.add(r["area"])
   if isinstance(r,dict) and r.get("status") in{"DONE","N_A"} and not str(r.get("evidence","")).strip():e.append("completed row needs evidence")
 ev=d.get("evidence_separation")
 if not isinstance(ev,dict):e.append("evidence_separation required")
 else:
  sets={k:{str(x).strip() for x in ev.get(k,[]) if str(x).strip()} for k in("error_evidence","finding_evidence","verification_evidence")}
  for a,b in(("error_evidence","finding_evidence"),("error_evidence","verification_evidence"),("finding_evidence","verification_evidence")):
   if sets[a]&sets[b]:e.append(a+" overlaps "+b)
 l=d.get("lifecycle")
 if not isinstance(l,dict) or l.get("status") not in LIFE:e.append("lifecycle.status invalid")
 else:
  if l.get("status")=="VERIFIED" and l.get("verification_state")!="VERIFIED":e.append("VERIFIED requires verification_state=VERIFIED")
  if l.get("status")!="VERIFIED" and l.get("verification_state")=="VERIFIED":e.append("non-VERIFIED state cannot claim verification")
  if l.get("status")=="FIXED" and l.get("implementation_state")!="IMPLEMENTED":e.append("FIXED requires IMPLEMENTED")
  if l.get("status")=="CLOSED" and not(l.get("implementation_state")=="IMPLEMENTED" and l.get("verification_state")=="VERIFIED" and l.get("closure_assessment")=="COMPLETE" and l.get("closure_decision")=="CLOSED"):e.append("CLOSED requires complete+implemented+verified")
  if l.get("status") in{"VERIFIED","CLOSED"} and (not ev.get("verification_evidence") or not SHA.fullmatch(str(ev.get("exact_sha","")).strip())):e.append("CI-relevant VERIFIED/CLOSED requires verification_evidence and exact_sha")
  if l.get("status")=="CLOSED":
   bad=[r.get("area") for r in rows if r.get("required") is True and r.get("status") not in{"DONE","N_A"}]
   if bad:e.append("CLOSED without complete Completion Matrix: "+",".join(sorted(bad)))
 x=d.get("existing_first")
 if not isinstance(x,dict) or x.get("performed") is not True or not str(x.get("ssot","")).strip() or not isinstance(x.get("existing_artifacts"),list):e.append("existing_first incomplete")
 return e
def main():
 ap=argparse.ArgumentParser();ap.add_argument("paths",nargs="*",default=["change-requests"]);a=ap.parse_args();ps=[]
 for p in a.paths:ps += [os.path.join(p,n) for n in os.listdir(p) if n.startswith("SCR-") and n.endswith(".md")] if os.path.isdir(p) else [p]
 bad=0
 for p in sorted(ps):
  e=validate(p)
  if e:bad+=1;print("SCR-VALIDATOR: FAIL — "+p);[print("  - "+x) for x in e]
  else:print("SCR-VALIDATOR: PASS — "+p)
 print("SCR-VALIDATOR RESULT: "+("PASS" if not bad else "FAIL"));return int(bool(bad))
if __name__=="__main__":sys.exit(main())
