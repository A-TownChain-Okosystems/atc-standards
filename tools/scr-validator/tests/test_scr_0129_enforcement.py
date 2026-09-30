#!/usr/bin/env python3
import copy,os,tempfile,yaml,sys
HERE=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.insert(0,HERE)
from validate_scr import validate
BASE={
"schema_version":2,"id":"SCR-9999","affected_standard":"ATC-STD-999","proposed_change":"x","motivation":"x","decision":"PENDING",
"purpose":{"objective":"x","problem_solved":"x","system_benefit":"x"},
"necessity":{"required":True,"classification":"REQUIRED","reason":"x"},
"rationale":{"why":"x","why_now":"x","consequence_without_change":"x","technical_rationale":"x"},
"improvement":{"before":"x","after":"x","dimensions":{"correctness":{"status":"IMPROVED","evidence":"x"}}},
"safety_security":{"security_impact":"x","attack_surface_change":"x","data_integrity":"x","availability_reliability":"x","new_failure_modes":"x","rollback_recovery":"x","residual_risk":"x","safe":False},
"completeness":{"matrix":[{"area":a,"required":False,"status":"N_A","evidence":"not applicable"} for a in ["ARCHITECTURE_SSOT","SPECIFICATION_CONTRACT","SOURCE_CODE","API","ABI_WIRE_FORMAT","STATE_STORAGE","SECURITY","TESTS","INTEGRATION","CI_CD","DOCUMENTATION","MIGRATION","COMPATIBILITY","RELEASE","AUDIT"]]},
"evidence_separation":{"error_evidence":["log-1"],"finding_evidence":["finding-1"],"verification_evidence":["verify-1"],"exact_sha":"0123456789abcdef0123456789abcdef01234567"},
"lifecycle":{"status":"IMPLEMENTING","implementation_state":"IN_PROGRESS","verification_state":"NOT_VERIFIED","closure_assessment":"OPEN","closure_decision":"OPEN"},
"existing_first":{"performed":True,"ssot":"ATC-STD-999","existing_artifacts":["tools/atc-std-validator"],"reuse_extend_consolidate_decision":"extend"}}
def run(d):
 fence=chr(96)*3
 text="# SCR-9999\n\n## Machine-readable Contract\n\n"+fence+"yaml\n"+yaml.safe_dump(d,sort_keys=False)+fence+"\n"
 f=tempfile.NamedTemporaryFile("w",suffix=".md",delete=False,encoding="utf-8");f.write(text);f.close()
 try:return validate(f.name)
 finally:os.unlink(f.name)
def fail(d,label):
 if not run(d):return
 raise SystemExit("NEGATIVE TEST FAILED: "+label)
def main():
 if run(BASE):raise SystemExit("BASE fixture must pass")
 d=copy.deepcopy(BASE);d["schema_version"]=1;fail(d,"schema_version")
 d=copy.deepcopy(BASE);d["evidence_separation"]["finding_evidence"]=["log-1"];fail(d,"evidence separation")
 d=copy.deepcopy(BASE);d["lifecycle"]["status"]="FIXED";d["lifecycle"]["verification_state"]="VERIFIED";fail(d,"FIXED != VERIFIED")
 d=copy.deepcopy(BASE);d["lifecycle"]["status"]="VERIFIED";d["lifecycle"]["verification_state"]="VERIFIED";d["evidence_separation"]["exact_sha"]="";fail(d,"VERIFIED exact SHA")
 d=copy.deepcopy(BASE);d["lifecycle"]={"status":"CLOSED","implementation_state":"IMPLEMENTED","verification_state":"VERIFIED","closure_assessment":"COMPLETE","closure_decision":"CLOSED"};d["completeness"]["matrix"][0]["required"]=True;d["completeness"]["matrix"][0]["status"]="OPEN";fail(d,"CLOSED incomplete")
 print("SCR-0129 negative tests: PASS")
if __name__=="__main__":main()
