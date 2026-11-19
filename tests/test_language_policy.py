import pathlib
import subprocess
import sys

def test_language_policy_passes():
    root = pathlib.Path(__file__).parents[1]
    result = subprocess.run(
        [sys.executable, str(root / "tools/atc-language-validator/check_language_policy.py"), str(root)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
