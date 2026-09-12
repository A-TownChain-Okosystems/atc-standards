#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Standard-ID Allocation Gate (P1-A2, Allocation-SSOT-Drift-Check).

Prueft, dass registry/allocation/allocation-status.yaml mit den SSOTs
uebereinstimmt:
  - registry/standards.yaml  (Bestands-SSOT: ALLOCATED)
  - registry/framework.yaml (VERWEIST-Slots + FAM-Ranges: RESERVED)

Regeln:
  ALLOC-01  Jede Registry-3xx-ID muss als ALLOCATED gefuehrt werden.
  ALLOC-02  Jede als ALLOCATED gefuehrte ID muss in der Registry existieren.
  ALLOC-03  Jeder VERWEIST-/FAM-Range-Slot muss als RESERVED gefuehrt werden.
  ALLOC-04  Jede als RESERVED gefuehrte ID muss einen VERWEIST-/FAM-Beleg haben.
  ALLOC-05  FREE-Slots muessen numerisch unbeeobachtet sein (weder Registry noch Verweis).
  ALLOC-06  counts muessen stimmen (allocated/reserved/free = 100 je Familie).
  ALLOC-07  rule_free_is_not_allocatable muss auf true stehen.
  ALLOC-08  Jede ID in reservations.yaml muss in allocation-status als RESERVED stehen.

Exit 0 = PASS, 1 = FAIL (Drift). Neue ID-Vergabe ohne Aktualisierung beider
Seiten laesst das Gate anschlagen — 'ID nicht gefunden' wird nie 'ID ist frei'."""
import argparse
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML erforderlich: pip install pyyaml")


def fail(msg):
    print(f"  FAIL  {msg}")
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", type=int, default=300)
    ap.add_argument("--registry", default="registry/standards.yaml")
    ap.add_argument("--framework", default="registry/framework.yaml")
    ap.add_argument("--status", default="registry/allocation/allocation-status.yaml")
    ap.add_argument("--reservations", default="registry/allocation/reservations.yaml")
    args = ap.parse_args()
    b = str(args.family)[0]

    reg = yaml.safe_load(open(args.registry, encoding="utf-8"))
    fw_raw = open(args.framework, encoding="utf-8").read()
    status = yaml.safe_load(open(args.status, encoding="utf-8"))

    lo, hi = args.family, args.family + 99
    all_ids = [f"ATC-STD-{n}" for n in range(lo, hi + 1)]
    allocated = {s["id"] for s in reg.get("standards", [])
                 if re.fullmatch(rf"ATC-STD-{b}\d\d", s["id"])}
    reserved = set()
    for m in re.finditer(
            rf"- id: (ATC-STD-{b}\d\d)\s*\n\s*title: [^\n]*\n\s*status: VERWEIST",
            fw_raw):
        reserved.add(m.group(1))
    for m in re.finditer(r"range: (ATC-STD-(\d+)\.\.ATC-STD-(\d+))", fw_raw):
        for n in range(int(m.group(2)), int(m.group(3)) + 1):
            if lo <= n <= hi:
                reserved.add(f"ATC-STD-{n}")

    alloc_sec = status["allocation"]
    st_alloc = {f"ATC-STD-{k}" for k in status.get("allocated", {})}
    st_res = {f"ATC-STD-{k}" for k in status.get("reserved", {})}
    st_free = {f"ATC-STD-{n}" for n in _free_ids(status)}
    counts = alloc_sec["counts"]

    errs = 0
    print(f"Allocation-Gate Familie {args.family}: Registry {len(allocated)} | "
          f"Verweise {len(reserved)} | Status-Datei {len(st_alloc)}/{len(st_res)}/{len(st_free)}")
    errs += fail_count(allocated - st_alloc, "ALLOC-01 Registry-ID fehlt als ALLOCATED", errs)
    for x in st_alloc - allocated:
        errs += fail(f"ALLOC-02 als ALLOCATED gefuehrt, aber nicht in Registry: {x}")
    for x in reserved - st_res:
        errs += fail(f"ALLOC-03 VERWEIST-/FAM-Slot fehlt als RESERVED: {x}")
    for x in st_res - reserved:
        errs += fail(f"ALLOC-04 als RESERVED gefuehrt ohne Verweis-Beleg: {x}")
    for x in st_free & (allocated | reserved):
        errs += fail(f"ALLOC-05 als FREE gefuehrt, aber belegt: {x}")
    if counts.get("allocated") != len(st_alloc):
        errs += fail(f"ALLOC-06a counts.allocated falsch ({counts.get('allocated')} != {len(st_alloc)})")
    if counts.get("reserved") != len(st_res):
        errs += fail(f"ALLOC-06b counts.reserved falsch ({counts.get('reserved')} != {len(st_res)})")
    if counts.get("free_numerically_unobserved") != len(st_free):
        errs += fail(f"ALLOC-06c counts.free falsch ({counts.get('free_numerically_unobserved')} != {len(st_free)})")
    if len(st_alloc) + len(st_res) + len(st_free) != 100:
        errs += fail(f"ALLOC-06d Familie nicht vollstaendig abgebildet "
                     f"({len(st_alloc)}+{len(st_res)}+{len(st_free)} != 100)")
    if alloc_sec.get("rule_free_is_not_allocatable") is not True:
        errs += fail("ALLOC-07 rule_free_is_not_allocatable != true")

    try:
        resv = yaml.safe_load(open(args.reservations, encoding="utf-8"))
        for r in resv.get("reservations", []):
            rid = r.get("id", "")
            if rid.startswith("ATC-STD-") and rid not in st_res:
                errs += fail(f"ALLOC-08 {rid} in reservations.yaml, aber nicht RESERVED in allocation-status")
    except FileNotFoundError:
        errs += fail("ALLOC-08 reservations.yaml nicht gefunden")

    if errs:
        print(f"Ergebnis: FAIL — {errs} Allocation-Drift-Funde. Registry-Update oder "
              f"allocation-status.yaml-Update erforderlich.")
        sys.exit(1)
    print("Ergebnis: PASS — allocation-status konsistent mit Registry + Framework.")


def fail_count(missing, msg, _):
    n = 0
    for x in sorted(missing):
        fail(f"{msg}: {x}")
        n += 1
    return n


def _free_ids(status):
    """Parst ids wie '305, 315-319, 336-339' in eine Liste von Slot-Nummern."""
    ids = []
    raw = status.get("free_numerically_unobserved", {}).get("ids", [])
    parts = [str(p).strip() for p in raw] if isinstance(raw, list) \
        else [p.strip() for p in str(raw).split(",")]
    for part in parts:
        if not part:
            continue
        m = re.fullmatch(r"(\d+)-(\d+)", part)
        if m:
            ids.extend(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.isdigit():
            ids.append(int(part))
        else:
            raise ValueError(f"Ungueltiger FREE-Slot: {part!r}")
    return ids


if __name__ == "__main__":
    main()
