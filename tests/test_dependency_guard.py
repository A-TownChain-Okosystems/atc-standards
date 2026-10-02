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
