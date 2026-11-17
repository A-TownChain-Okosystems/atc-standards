# Approval Decision — ATC-STD-000 v1.3.1

Dieses Dokument haelt **drei getrennte Dinge** fest, die nicht vermischt werden
duerfen: den Owner-Entscheid (Freigabe), den formalen Review-Erlass und den
Nachweisstand. Der Merge-Commit und die Verifikation werden ausserhalb dieses
Dokuments gefuehrt und hier nur referenziert.

## 1. Entscheid (Owner)

- **Datum:** 2026-11-17, 09:06 Ortszeit (Europe/Berlin)
- **Entscheider:** Michael Wroblewski (Owner, genau 1 nach §14.1)
- **Gegenstand:** SCR-0143 Option A — klarstellende Zeile in ATC-STD-000 §9
- **Woertlich:** „SCR-0143 / Option A: Ja – die klarstellende Zeile in
  `ATC-STD-000 §9` mit Version 1.3.1 umsetzen. Die Aenderung bleibt eine
  Klarstellung, keine neue Anforderung und keine Abschwaechung bestehender
  Governance-Regeln. `SCR-0143` bleibt bis zur ordnungsgemaessen Umsetzung und
  Freigabe im vorgesehenen Status. Merge, Approval und Verification sind
  getrennt zu dokumentieren."
- **Wirkung:** ATC-STD-000 v1.3.1 traegt in §9 die Klarstellung, dass die
  Genehmigung §18 regelt und historische Verweise auf §9 diese Stelle meinen.
  Kein Anforderungstext wird geaendert, keine Freigabe vom 07.09.2026 wird
  umgedeutet.

## 2. Review-Erlass (Owner-Mandat, §14.1 Regel 3)

Der Owner hat den Gegenstand ausdruecklich als Klarstellung eingeordnet. Damit
greift die Erlass-Regel fuer einfache Aenderungen: die Review-Kette wird auf
**einen** Review-Typ reduziert, naemlich Technical Review. Security Review und
Architecture Review entfallen fuer diese Aenderung, weil kein Anforderungs-,
Security- oder Schichtinhalt beruehrt wird. Der Erlass ist hiermit im
Approval-Paket vermerkt, wie §14.1 Regel 3 es verlangt.

## 3. Technical Review (§15)

Ergebnis: **PASS**.

| Pruefpunkt | Befund |
|---|---|
| Technische Konsistenz | Die Zeile steht in §9 (Standard Structure) und verweist auf §18; kein Widerspruch zu §14 bis §17 |
| Vollstaendigkeit | Ein Satz plus Hinweis auf §30; keine offene Formulierung |
| Requirement-Qualitaet | Keine neue Anforderung, kein neues REQ, keine Nummer belegt |
| Terminologie | „Genehmigung", „Freigabegrundlage", „Bestandsdokumente" konsistent mit §14.1 und §18 |
| Testbarkeit | Pruefbar ueber `registry_view_gate.py` und R11 (Sunset-Check) |
| Versionierung | 1.3.0 → 1.3.1, Patch-Sprung fuer Klarstellung, Changelog-Eintrag vorhanden |
| Kompatibilitaet | Kein Bestandsdokument wird geaendert; §30 bleibt gewahrt |

Die Zeichnung erfolgt durch den Autor. Eine unabhaengige Reviewer-Zeichnung wird
nicht beansprucht; der Owner hat die Formanforderung mit dem Erlass nach §14.1
Regel 3 reduziert.

## 4. Merge (getrennt gefuehrt)

- **Status:** ausstehend. Der Merge-Commit ist zum Zeitpunkt dieses Dokuments
  nicht bekannt und wird hier nicht vorweggenommen.
- **Nachweisort:** PR im Repository `atc-standards`; nach dem Merge ist der
  Merge-Commit in SCR-0143 §7.3 einzutragen.

## 5. Verifikation (getrennt gefuehrt)

Unabhaengig vom Merge erhoben:

| Pruefung | Ergebnis |
|---|---|
| `tools/consistency/registry_view_gate.py` | PASS, Anker auf Registry-Blob 018ba34f57a8b9ccbe69c6e6db549319a47c4f31 |
| `tools/consistency/check_cross_registry.py` R11 | Sunset v1.3.0, Registry v1.3.1 — geprueft |
| `tools/repo_registry_check.py` | OK, 33/33 Eintraege |
| `pytest tests tools` | 60/60 |
| Dokument ↔ Metadaten ↔ Registry | 1.3.1 durchgaengig |

Die Verifikation belegt, dass Dokument, Metadaten und Registry gleichlautend
sind. Sie belegt **nicht** den Merge; das ist ein eigener Nachweis.

## 6. Vorher gueltig

v1.3.0 APPROVED (APPROVAL-DECISION-2026-09-11-000-v1.3.0.md). §30-Immutabilitaet
gilt fuer v1.3.0 fort; der Inhalt von v1.3.1 unterscheidet sich ausschliesslich
durch die Klarstellung in §9 und den Changelog-Eintrag.
