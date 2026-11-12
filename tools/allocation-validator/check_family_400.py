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
  ALLOC-14   Security-IDs liegen ausschliesslich im Allokationsfenster, das
             FAMILY-400.yaml **normativ** festlegt: vorbelegte Reservierung plus
             neues Vergabefenster. Der Pruefer bringt kein eigenes Fenster mit;
             fehlt die normative Angabe, ist das Gate FAIL (fail-closed).
             Die Ausnahmebehandlung wird nicht auf andere Kategorien ausgedehnt.
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
RESERVATIONS = os.path.join(ROOT, "registry", "allocation", "reservations.yaml")
EXCEPTIONS = os.path.join(ROOT, "registry", "allocation", "family-exceptions.yaml")

ID = re.compile(r"ATC-STD-4\d\d")


def main() -> int:
    fails: list[str] = []
    reg = yaml.safe_load(open(REGISTRY, encoding="utf-8"))
    fw = yaml.safe_load(open(FRAMEWORK, encoding="utf-8")) or {}
    cats = yaml.safe_load(open(CATEGORIES, encoding="utf-8")) or {}
    fam_def = yaml.safe_load(open(FAMILY, encoding="utf-8")) or {}
    exc_doc = yaml.safe_load(open(EXCEPTIONS, encoding="utf-8")) or {}
    resv = yaml.safe_load(open(RESERVATIONS, encoding="utf-8")) or {}

    std = {s["id"]: s for s in reg.get("standards", []) if ID.fullmatch(s.get("id", ""))}
    security = {i: s for i, s in std.items() if s.get("category") == "security"}
    other = {i: s for i, s in std.items() if s.get("category") != "security"}

    # Reservierte Security-IDs stehen bewusst nicht in der Registry (kein Dokument,
    # ATC-STD-000 kennt keinen Lifecycle-Stand `reserved`), sondern im
    # Reservierungsregister. Sie zaehlen zum Bestand der Familie.
    window = ((fam_def.get("allocation_window") or {}).get("new_allocation") or {}).get("range", "")
    pre_reserved = [
        str(x.get("id")) for x in ((fam_def.get("allocation_window") or {}).get("pre_reserved") or [])
    ]
    resv_ids = {
        str(x.get("id"))
        for x in (resv.get("standard_reservations") or [])
        if ID.fullmatch(str(x.get("id", ""))) and x.get("category") == "security"
    }
    if not pre_reserved:
        fails.append("ALLOC-14 FAMILY-400.yaml nennt keine vorbelegte Reservierung (normative Angabe fehlt)")
    for pid in pre_reserved:
        if pid not in resv_ids:
            fails.append(f"ALLOC-14 {pid} ist in FAMILY-400 vorbelegt, fehlt aber in reservations.yaml")
        if pid in std:
            fails.append(f"ALLOC-14 {pid} ist Reservierung, steht aber zusaetzlich in standards.yaml")
    for rid in sorted(resv_ids - set(pre_reserved)):
        fails.append(f"ALLOC-14 {rid} ist security-reserviert, aber nicht in FAMILY-400 vorbelegt")
    total = len(std) + len(pre_reserved)
    print(
        f"Familie 400 Bestand: {total} Slots = {len(std)} Standards "
        f"({len(security)} security, {len(other)} grandfatherte Ausnahmen) + "
        f"{len(pre_reserved)} Reservierung(en)"
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

    # ALLOC-14 — Allokationsfenster kommt aus FAMILY-400.yaml (normativ), nicht
    # aus diesem Pruefer. Vorbelegte Reservierung + neues Vergabefenster.
    allowed = set()
    m = re.fullmatch(r"ATC-STD-(4\d\d)\.\.(?:ATC-STD-)?(4\d\d)", window or "")
    if not m:
        fails.append(f"ALLOC-14 FAMILY-400.yaml new_allocation.range fehlt oder ist unlesbar ('{window}')")
    else:
        allowed = set(range(int(m.group(1)), int(m.group(2)) + 1))
    allowed |= {int(p.split("-")[-1]) for p in pre_reserved if ID.fullmatch(p)}
    for sid in sorted(set(security) | resv_ids):
        n = int(sid.split("-")[-1])
        if n not in allowed:
            fails.append(
                f"ALLOC-14 {sid} liegt ausserhalb des normativen Allokationsfensters "
                f"({window} plus vorbelegte Reservierung)"
            )
    for e in listed:
        if e.get("category") == "security":
            fails.append(f"ALLOC-14 {e.get('id')} ist Security und darf keine Ausnahme sein")
    print(
        f"ALLOC-14 Allokationsfenster (normativ): {len(security)} security-Standard(s) + "
        f"{len(pre_reserved)} Reservierung in {window or '?'}, "
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
        f"\nGate Familie 400: PASS — {total} Slots gedeckt ({len(std)} Standards + "
        f"{len(pre_reserved)} Reservierung), "
        f"{len(other)} grandfatherte Ausnahmen einzeln registriert, "
        f"Security-Allokation nur 411-419"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
