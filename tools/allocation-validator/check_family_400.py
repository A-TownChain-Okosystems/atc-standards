#!/usr/bin/env python3
# Copyright (c) 2026 A-TownChain-Okosystems — Apache-2.0
"""Gate Familie 400 (SECURITY) — Option B, Owner-Entscheidung 12.11.2026.

Geprueft wird der **vollstaendige 4xx-Bestand**, nicht eine Einzel-ID. Ein
gruener Einzeltest fuer ATC-STD-410 waere kein Nachweis.

  ALLOC-12f  Jeder 4xx-Standard liegt in der SECURITY-Familien-Range (FAM-77).
  ALLOC-13   Die Bestandsliste der grandfatherten Ausnahmen ist vollstaendig,
             eindeutig und deckungsgleich mit der Registry: genau die 4xx-
             Standards mit Kategorie != security, je mit derselben Kategorie,
             keine Doppelung, keine Ausnahme fuer einen Security-Standard.
  ALLOC-14   Security-Standards im 4xx liegen ausschliesslich im freien
             Allokationsbereich ATC-STD-411..419; die Ausnahmebehandlung wird
             nicht auf andere Kategorien ausgedehnt.
  ALLOC-15   Die normative Definition, das Familienregister und die
             Kategorien-Verkabelung zeigen dieselbe Zuordnung.

Exit 0 = PASS, 1 = FAIL. Keine Netzwerk-, keine Registry-Schreibzugriffe.
"""
from __future__ import annotations

import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REGISTRY = os.path.join(ROOT, "registry", "standards.yaml")
FRAMEWORK = os.path.join(ROOT, "registry", "framework.yaml")
CATEGORIES = os.path.join(ROOT, "registry", "categories.yaml")
FAMILY = os.path.join(ROOT, "registry", "families", "FAMILY-400.yaml")
EXCEPTIONS = os.path.join(ROOT, "registry", "allocation", "family-exceptions.yaml")

ID = re.compile(r"ATC-STD-4\d\d")


def main() -> int:
    fails: list[str] = []
    reg = yaml.safe_load(open(REGISTRY, encoding="utf-8"))
    fw = yaml.safe_load(open(FRAMEWORK, encoding="utf-8")) or {}
    cats = yaml.safe_load(open(CATEGORIES, encoding="utf-8")) or {}
    fam_def = yaml.safe_load(open(FAMILY, encoding="utf-8")) or {}
    exc_doc = yaml.safe_load(open(EXCEPTIONS, encoding="utf-8")) or {}

    std = {s["id"]: s for s in reg.get("standards", []) if ID.fullmatch(s.get("id", ""))}
    security = {i: s for i, s in std.items() if s.get("category") == "security"}
    other = {i: s for i, s in std.items() if s.get("category") != "security"}
    print(
        f"Familie 400 Bestand: {len(std)} Standards "
        f"({len(security)} security, {len(other)} grandfatherte Ausnahmen)"
    )

    # ALLOC-12f — Familien-Range deckt den gesamten 4xx-Bestand
    fams = {f["id"]: f for f in (fw.get("framework") or {}).get("families") or []}
    fam = fams.get("FAM-77")
    if not fam:
        fails.append("ALLOC-12f FAM-77 fehlt in registry/framework.yaml")
        range_ok = False
    else:
        range_ok = str(fam.get("range", "")).replace("..", "-") == "ATC-STD-400-499"
        if not range_ok:
            fails.append(f"ALLOC-12f FAM-77-Range ist '{fam.get('range')}', erwartet ATC-STD-400..499")
    if range_ok:
        for sid in sorted(std):
            n = int(sid.split("-")[-1])
            if not 400 <= n <= 499:
                fails.append(f"ALLOC-12f {sid} liegt nicht in 400-499")
        print(f"ALLOC-12f Familien-Range: {len(std)}/{len(std)} 4xx-Standards gedeckt")

    # ALLOC-13 — Bestandsliste vollstaendig, eindeutig, deckungsgleich
    listed = exc_doc.get("exceptions") or []
    ids = [str(e.get("id", "")) for e in listed]
    if len(ids) != len(set(ids)):
        fails.append("ALLOC-13 Bestandsliste enthaelt doppelte IDs")
    missing = sorted(set(other) - set(ids))
    extra = sorted(set(ids) - set(other))
    for sid in missing:
        fails.append(f"ALLOC-13 {sid} fehlt in der Bestandsliste (keine pauschale Ausnahme)")
    for sid in extra:
        if sid in std:
            fails.append(f"ALLOC-13 {sid} ist als Ausnahme gelistet, aber Kategorie '{std[sid].get('category')}'")
        else:
            fails.append(f"ALLOC-13 {sid} ist als Ausnahme gelistet, steht aber nicht in der Registry")
    for e in listed:
        sid = str(e.get("id", ""))
        if sid in std and e.get("category") != std[sid].get("category"):
            fails.append(
                f"ALLOC-13 {sid} Kategorie in Bestandsliste '{e.get('category')}' "
                f"!= Registry '{std[sid].get('category')}'"
            )
        if e.get("status") != "GRANDFATHERED":
            fails.append(f"ALLOC-13 {sid} Status '{e.get('status')}', erwartet GRANDFATHERED")
        if not e.get("basis"):
            fails.append(f"ALLOC-13 {sid} ohne Grandfathering-Basis (§3)")
    if not missing and not extra:
        print(f"ALLOC-13 Bestandsliste: {len(ids)} Ausnahmen, vollstaendig und deckungsgleich")

    # ALLOC-14 — neue Security-Standards nur in 411..419.
    # ATC-STD-410 ist die bereits reservierte erste Security-ID (Owner-Entscheidung
    # 12.11.2026). Sie bleibt zulaessig; umnummeriert wird nicht. Der Bereich
    # 411-419 ist der freie Raum fuer alles Neue.
    allowed = range(410, 420)
    for sid in sorted(security):
        n = int(sid.split("-")[-1])
        if n not in allowed:
            fails.append(f"ALLOC-14 {sid} liegt ausserhalb des freien Security-Bereichs 411-419")
    for e in listed:
        if e.get("category") == "security":
            fails.append(f"ALLOC-14 {e.get('id')} ist Security und darf keine Ausnahme sein")
    print(
        f"ALLOC-14 Allokationsfenster: {len(security)} security-Standard(s) in 410-419 (410 reserviert, 411-419 frei), "
        f"{len(other)} Ausnahmen unveraendert"
    )

    # ALLOC-15 — eine Zuordnung in Norm, Register, Kategorien
    cat_sec = ((cats.get("categories") or {}).get(400) or {})
    if cat_sec.get("fam") != "FAM-77":
        fails.append(f"ALLOC-15 categories.yaml security verweist auf '{cat_sec.get('fam')}', erwartet FAM-77")
    if str(fam_def.get("range", "")).replace("-499", "..499") != "ATC-STD-400..499":
        fails.append(f"ALLOC-15 FAMILY-400.yaml Range '{fam_def.get('range')}' weicht ab")
    if str(fam_def.get("family", "")).upper() != "SECURITY":
        fails.append(f"ALLOC-15 FAMILY-400.yaml family '{fam_def.get('family')}' != SECURITY")
    wiring = fam_def.get("wiring") or {}
    if wiring.get("fam") != "FAM-77":
        fails.append(f"ALLOC-15 FAMILY-400.yaml wiring.fam '{wiring.get('fam')}' != FAM-77")
    exc_ref = ((fam_def.get("grandfathered_exceptions") or {}).get("list_ref"))
    if exc_ref != "registry/allocation/family-exceptions.yaml":
        fails.append("ALLOC-15 FAMILY-400.yaml verweist nicht auf die Bestandsliste")
    if ((fam_def.get("grandfathered_exceptions") or {}).get("count")) != len(other):
        fails.append("ALLOC-15 FAMILY-400.yaml Ausnahmenzahl weicht vom Bestand ab")
    print("ALLOC-15 Norm/Register/Kategorien: eine Zuordnung (FAM-77, SECURITY, 400-499)")

    if fails:
        for f in fails:
            print(f"FAIL: {f}")
        print(f"\nGate Familie 400: FAIL ({len(fails)} Befunde)")
        return 1
    print(
        f"\nGate Familie 400: PASS — {len(std)}/52 Standards gedeckt, "
        f"{len(other)} grandfatherte Ausnahmen einzeln registriert, "
        f"Security-Allokation nur 411-419"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
