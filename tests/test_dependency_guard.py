import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_dependency_policy_schema():
    p=json.loads((ROOT/'security/dependency-policy.json').read_text())
    assert p['schema']=='ATC-DEP-POLICY-1'
    assert 'critical' in p['block_severities']

def test_dependency_advisory_schema():
    p=json.loads((ROOT/'security/advisories.json').read_text())
    assert p['schema']=='ATC-DEP-ADVISORY-1'

def test_base_head_diff_detects_add_remove_and_upgrade():
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    import dependency_guard as dg
    base=[{"ecosystem":"cargo","name":"foo","version":"1.0.0"},{"ecosystem":"cargo","name":"bar","version":"1.0.0"}]
    head=[{"ecosystem":"cargo","name":"foo","version":"1.1.0"},{"ecosystem":"cargo","name":"baz","version":"2.0.0"}]
    added,removed,changed=dg.compare_nodes(base,head)
    assert [x["name"] for x in added] == ["baz"]
    assert [x["name"] for x in removed] == ["bar"]
    assert len(changed)==1
    assert changed[0]["from"]["version"]=="1.0.0"
    assert changed[0]["to"]["version"]=="1.1.0"

def test_osv_semver_range_is_conservative():
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    import dependency_guard as dg
    events=[{"introduced":"0"},{"fixed":"1.2.0"}]
    assert dg.range_match("1.1.9",events,"cargo")== (True,"range")
    assert dg.range_match("1.2.0",events,"cargo")== (False,"range")
    assert dg.range_match("not-semver",events,"cargo")[1]=="unsupported"

def test_osv_advisory_exact_match():
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    import dependency_guard as dg
    ad={"id":"GHSA-test","affected":[{"ecosystem":"npm","package":"foo","versions":["1.0.0"],"ranges":[]}]}
    assert dg.advisory_matches({"ecosystem":"npm","name":"foo","version":"1.0.0"},ad)==(True,"exact")

def test_osv_snapshot_normalization():
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    import osv_snapshot
    raw=[{"id":"GHSA-test","aliases":["CVE-2099-0001"],"affected":[{"package":{"ecosystem":"npm","name":"foo"},"versions":["1.0.0"],"ranges":[]}]}]
    out=osv_snapshot.normalize(raw)
    assert out[0]["id"]=="GHSA-test"
    assert out[0]["affected"][0]["ecosystem"]=="npm"
    assert out[0]["affected"][0]["package"]=="foo"

def test_spdx_sbom_module_imports():
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    import dependency_sbom
    assert callable(dependency_sbom.main)
