#!/usr/bin/env python3
"""S-19 Mutationstest-Suite: Header-Drift MUSS zuverlaessig erkannt werden.

Erzeugt aus echten Standards gezielte Mutanten und prueft, dass der
Validator jeden Drift-Fall korrekt klassifiziert (FAIL) und keine
False Positives produziert (PASS).
CI-ungebunden lauffaehig: python3 tests/test_s19_mutation.py
Exit-Code 0 = alle Faelle bestanden.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
VALIDATOR = os.path.join(HERE, "..", "atc_std_validator.py")
BUG1 = os.path.join(HERE, "..", "..", "..", "standards", "bug", "ATC-STD-BUG-001.md")
STD202 = os.path.join(HERE, "..", "..", "..", "standards", "repository", "ATC-STD-202.md")

def run_validator(text):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(text)
        path = f.name
    try:
        out = subprocess.run([sys.executable, VALIDATOR, path],
                             capture_output=True, text=True).stdout
        m = re.search(r"\[(PASS|FAIL|WARN)\] S-19: (.*)", out)
        return (m.group(1), m.group(2)) if m else ("?", "keine S-19-Ausgabe: " + out[:120])
    finally:
        os.unlink(path)

def main():
    bug = open(BUG1, encoding="utf-8").read()
    s202 = open(STD202, encoding="utf-8").read()

    kopf_status = re.search(r"> \*\*Status:\*\* \w+", bug).group(0)
    titel = re.search(r"^# ATC-STD-BUG-001[^\n]*", bug, re.M).group(0)

    klassisch = ("---\nstandard:\n  id: ATC-STD-BUG-001\n  version: \"1.0.0\"\n"
                 "  status: candidate\n---\n\n# Titel (v1.0.0, CANDIDATE)\n\n"
                 "> **Version:** 1.0.0 (FORMAL)\n> **Status:** CANDIDATE\n\n---\n\n## Abstract\n")

    faelle = [
        # (Label, Text, erwartetes S-19-Ergebnis)
        ("M1: Titel-Version manipuliert",
         bug.replace(titel, "# ATC-STD-BUG-001 — Bug Finding Standard (v7.7.7, CANDIDATE)", 1), "FAIL"),
        ("M2: Titel-Status NORMATIV statt candidate",
         bug.replace(titel, "# ATC-STD-BUG-001 — Bug Finding Standard (v1.0.0, NORMATIV)", 1), "FAIL"),
        ("M3: Kopf-Statuszeile manipuliert",
         bug.replace(kopf_status, "> **Status:** APPROVED", 1), "FAIL"),
        ("M4: Frontmatter-Status abweichend",
         bug.replace("status: candidate", "status: approved", 1), "FAIL"),
        ("M5: Kopf-Statuszeile geloescht",
         re.sub(r"^> \*\*Status:\*\*.*\n", "", bug, count=1, flags=re.M), "WARN"),
        ("M6: BUG-001 unveraendert", bug, "PASS"),
        ("M7: STD-202 unveraendert (Statuszeilen-Version)", s202, "PASS"),
        ("M8: STD-202 Statuszeilen-Version manipuliert",
         re.sub(r"(> \*\*Status:\*\* [A-Z]+ \(v)\d+\.\d+\.\d+(\))", r"\g<1>9.9.9\g<2>", s202, count=1), "FAIL"),
        ("M9: Beispielblock tief im Dokument (kein False Positive)",
         bug + "\n\n> **Version:** 0.0.1 (nur Beispiel, weit unterhalb des Kopfs)\n", "PASS"),
        ("M10: klassisches Frontmatter, konsistenter Kopf", klassisch, "PASS"),
        ("M11: klassisches Frontmatter, Kopf-Drift",
         klassisch.replace("> **Version:** 1.0.0", "> **Version:** 2.0.0", 1), "FAIL"),
        ("M12: klassisches Frontmatter, Titel-Status-Drift",
         klassisch.replace("(v1.0.0, CANDIDATE)", "(v1.0.0, APPROVED)", 1), "FAIL"),
    ]

    fehl = 0
    print(f"S-19 Mutationstest-Suite: {len(faelle)} Faelle\n" + "=" * 70)
    for label, text, expect in faelle:
        got, msg = run_validator(text)
        ok = got == expect
        print(f"[{'OK     ' if ok else 'FEHLER '}] {label:46s} erwartet={expect:5s} ist={got}")
        if not ok:
            print(f"          -> {msg}")
            fehl += 1
    print("=" * 70)
    print(f"Ergebnis: {len(faelle) - fehl}/{len(faelle)} bestanden")
    sys.exit(1 if fehl else 0)

if __name__ == "__main__":
    main()
