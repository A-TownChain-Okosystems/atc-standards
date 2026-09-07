# Approval Process — Freigabeverfahren (operationalisiert)

Geltung: ATC-STD-000 §13-18 (Review Chain, Approval, Stable). Dieses Dokument
beschreibt den Ablauf vom CANDIDATE zum STABLE-Standard.

## Ablauf

```
Standard (status: candidate)
    |
    v
Review-Paket (approval/): Snapshot + 3 Reviews + Requirement-Matrix
    |
    v
APPROVAL-DECISION.md dem Owner vorgelegt
    |
    +-- APPROVE        -> Status: approved -> stable (Registry + Header + Changelog synchron)
    +-- REQUEST CHANGES -> Status: draft (Findings als SCR/Revision vor Freigabe)
    +-- REJECT         -> Neuentwurf
```

## Pflichten je Entscheidung

- **APPROVE:** Owner-Vermerk (Datum) in APPROVAL-DECISION.md; Statuswechsel
  approved dann stable dokumentiert im Changelog; Registry-Zeile synchron;
  Immutabilitaet ab jetzt (ATC-STD-000 §29) — Aenderungen nur noch via SCR.
- **REQUEST CHANGES:** Befundliste mit vorher/nachher-Status; Rueckkehr an
  draft; erneute Review-Chain nach Revision.
- **REJECT:** Begruendung; Standard verbleibt je nach Sachlage auf draft oder
  wird retired.

## Approval-Zustand im Repo

- ATC-STD-000 v1.0.0: CANDIDATE seit 07.09.2026 — Approval BLOCKED, wartet auf
  Owner-Entscheidung (approval/APPROVAL-DECISION.md).
- ATC-STD-201/202/203: draft/proposed — Co-Approval-Empfehlung im
  ATC-STD-000-Paket; eigene kurze Review-Passagen vor Approval.

## Rollen (bis SCR-0004 entschieden ist)

- **Owner (ShivaCoreDev):** Alleinige Approval-Entscheidung + SCR-Decision.
- **Agent (Aurora):** Autor, Reviewer in der Kette (Technical/Security/
  Architecture), Executor von Umsetzungen — nie Approver.
- **Zukuenftig (SCR-0004):** Reviewer/Maintainer-Rollen mit definierten
  Schreibrechten je Registry-Domain.
