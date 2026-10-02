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

def test_spdx_sbom_module_imports():
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    import dependency_sbom
    assert callable(dependency_sbom.main)
