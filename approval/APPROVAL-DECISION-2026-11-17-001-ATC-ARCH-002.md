---
title: "Freigabe ATC-ARCH-002 v1.0.0 (Owner, 17.11.2026)"
standard: ATC-ARCH-002
version: "1.0.0"
authority: "Michael Wroblewski (Owner)"
date: "2026-11-17"
---

# Freigabe ATC-ARCH-002 v1.0.0 (Owner, 17.11.2026)

## 1. Gegenstand

Standard `ATC-ARCH-002 — KAI-OS Desktop Layer Architecture Standard`, Fassung
1.0.0 (vorher 0.1.3, DRAFT).

## 2. Entscheid

Der Owner hat am 17.11.2026 die Freigabe erteilt. Wortlaut: **„Genehmigt“**.
Damit ist der Standard nach ATC-STD-000 § 18 APPROVED und normativ.

## 3. Prüfkette vor der Freigabe

| Prüfung | Ergebnis | Ort |
|---|---|---|
| Technical Review | PASS, keine kritischen Findings (T-3 offen, nicht kritisch) | Standard § 15 |
| Security Review | PASS, keine kritischen Findings (S-1, S-2 dokumentiert) | Standard § 16 |
| Architecture Review | PASS, keine kritischen Findings (A-1 dokumentiert) | Standard § 17 |

Die Bedingung aus ATC-STD-000 § 18 — drei Reviews PASS und keine offenen
kritischen Findings — ist erfüllt.

## 4. Wirkung

- `status`: draft → **approved**
- `normative`: false → **true**
- `version`: 0.1.3 → **1.0.0**
- `effective_date`: 2026-11-17
- Einfrieren nach ATC-STD-000 § 30 ab Merge dieser Fassung.

## 5. Was diese Freigabe nicht umfasst

**ACTIVE ist nicht erklärt.** Die Kriterien COM-ARCH-201 bis 210 aus § 8 sind
nicht durchgängig mit gebundenem Commit und reproduzierbarem Nachweis belegt.
Bekannt offen: keine Implementierung der Signaturprüfung (COM-ARCH-206), kein
praktischer Rollback-Nachweis (COM-ARCH-207), keine COM-Evidenz für 201 bis 205
und 208 bis 210. Die Desktop-Schicht ist nach der Gap-Analyse zu 7 von 32
Anforderungen gedeckt, 13 teilweise, 12 nicht.

Die Freigabe macht die Architektur verbindlich; sie behauptet keine
Implementierung. Ein Statuswechsel auf ACTIVE bleibt an die zehn Nachweise
gebunden.

## 6. Nicht kritische Punkte aus den Reviews (in dieser Fassung geschlossen)

| ID | Punkt | Erledigt durch |
|---|---|---|
| T-3 | § 12 führte SCR-0142/0143 nicht als Referenz | § 12 nachgeführt, SCR-0142 als ACCEPTED |
| S-1 | Höchstalter des Trust-Store war nicht normiert | **UVK-5** in § 4.6.1: Fail-Closed oberhalb `trust_store_max_age`, Standard 30 Tage |
| A-1 | D0–D7 waren nicht ausdrücklich als Binnengliederung benannt | Klarstellung im Vorspann von § 7 |

Mit diesen drei Punkten sind alle Befunde aus § 15 bis § 17 geschlossen; es bleiben keine
offenen Findings, auch keine nicht kritischen.

## 7. Nachweise

- Standard: `standards/architecture/ATC-ARCH-002.md` (v1.0.0)
- Registry: `registry/standards.yaml` (id ATC-ARCH-002, status approved, normative true)
- Change Request: `change-requests/SCR-0142.md`
