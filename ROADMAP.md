# ROADMAP — atc-standards

## Q3/2026 (laufend)

1. **ATC-STD-000 in Kraft:** Owner-Approval -> APPROVED -> STABLE (wartet auf
   Entscheidung; Paket liegt seit 07.09. bereit).
2. **SCR-Klaerung:** SCR-0001 (ID-Allokation) + SCR-0004 (Rollenmodell)
   nach STABLE; SCR-0003 Option A/B (Branch-Absicherung) jederzeit.
3. **Co-Approval 201/202/203:** Kurze Review-Passagen + Owner-Sammelapproval.

## Danach (Standards-Ausbau je Bedarf)

4. **100er-Bereich (Architecture):** Erste Architektur-Standards nach
   ID-Allokationsregel (SCR-0001) — Kandidaten: Kernel-/Service-Space-Architektur
   (Querverweis AD-012/028), Chain-Architektur (Chain-ID 658467).
5. **400er-Bereich (Security):** Security-Basistandard (Secret-Handling,
   Release-Gates) — Verallgemeinerung aus ATC-STD-203 + Issue #69-Ergebnissen.
6. **800er-Bereich (OS/Runtime):** ATS-Serie (ATS-1000…1007) perspektivisch in
   die STD-Registry-Nomenklatur ueberfuehren (Alias-Mapping, keine Renumbering-
   Pflicht; Legacy-Nummern bleiben gueltig).
7. **Registry-Automation:** atc-std-validator um Registry-Sync-Pruefung
   (Header == Registry je Standard) erweitern; ggf. Version-Sync gegen
   versions.yaml.

## Regel

Neue Standards nur nach Bedarf aus Bauhierarchie L0-L7 (AD-026) und
Lauffaehigkeits-Roadmap M1-M8 (AD-027) — Standards folgen der Baulogik,
nicht umgekehrt.
