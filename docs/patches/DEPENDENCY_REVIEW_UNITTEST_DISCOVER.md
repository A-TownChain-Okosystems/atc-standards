# Workflow-Korrektur: dependency-review.yml prüft nichts

**Status:** offen — Workflow-Änderung, benötigt `workflow`-Scope beim Push
**Betroffene Datei:** `.github/workflows/dependency-review.yml`
**Festgestellt:** 17.11.2026 bei der Reparatur des Dependency-Guards (PR #129)

## Befund

Zeile 25 ruft auf:

```yaml
run: python3 -m unittest discover -s tests -p "test_dependency_guard.py" -v
```

`tests/test_dependency_guard.py` enthält pytest-Funktionen (`def test_...`), keine
`unittest.TestCase`-Klassen. `unittest discover` findet darin keine Testklasse und
endet mit Erfolg, ohne einen Test auszuführen. Der Schritt ist damit grün, ohne zu
prüfen. Genau dieser Zustand hat verdeckt, dass sechs Tests rot waren.

Gegenprobe:

```
python3 -m unittest discover -s tests -p "test_dependency_guard.py" -v
Ran 0 tests in 0.000s
OK
```

## Korrektur

```yaml
- name: Tests (Dependency Guard)
  run: python3 -m unittest discover -s tests -p "test_dependency_guard.py" -v
```
ersetzen durch

```yaml
- name: Tests (Dependency Guard)
  run: python3 -m pytest -q --no-header tests/test_dependency_guard.py
```

`pytest` ist im Workflow bereits installiert. Nach der Änderung muss der Schritt
bei rotem Test rot werden; das ist die Abnahmebedingung, nicht der grüne Lauf.

## Grenze

Die Änderung liegt unter `.github/workflows/` und kann mit dem vorhandenen Token
nicht gepusht werden (`workflow`-Scope fehlt). Sie ist deshalb hier als
anwendungsfertige Anweisung abgelegt und nicht als Patch eingespielt.
