---
standard:
  id: ATC-COMP-503
  title: "Worker Specification (Ausfuehrung, Sandbox, Runtime-Pinning, Timeout und strukturierter Ausfuehrungsrecord)"
  version: "0.1.0"
  status: draft
  category: compute
  authority: A-TownChain-Okosystems
  owner: "Michael (Owner-Entwurf via SCR-0071)"
  created: "2026-11-15"
  updated: "2026-11-15"
  normative: false
  supersedes: null
  superseded_by: null
  effective_date: null
  review_date: null
  license: "Copyright (c) 2026 Michael Wroblewski"
  applies_to: "Compute-Schicht und angrenzende Signatur- und Nachweispfade"
  registration: SCR-0142
  source_repository: atc-compute
  source_path: docs/specs/ATC-COMP-503-WORKER.md
  source_commit: 89d833edf338085d6141b0c703ebf92a0db83a5e
  source_version: 0.1.0-DRAFT
  source_status: SPEC-DRAFT
---

# ATC-COMP-503 — Worker Specification

> **Diese Datei ist ein Registrierungsnachweis, keine Spezifikation.**
> Der normative Inhalt liegt in `atc-compute`, Datei `docs/specs/ATC-COMP-503-WORKER.md`, Stand
> `89d833edf3` (Version `0.1.0-DRAFT`, Status `SPEC-DRAFT`). Hier steht
> ausschliesslich der Identitaets- und Nachweisbezug der Registry.
>
> **Registrierung ist keine normative Freigabe** (Owner-Auflage 15.11.2026).
> Der Status bleibt `draft`; die Version `0.1.0` ist die Lifecycle-Normalform
> von `0.1.0-DRAFT` und keine Aufwertung. Es gibt keine Implementierungs-,
> Test- oder CI-Evidence zu diesem Eintrag.

## 1. Gegenstand

Ausfuehrung, Sandbox, Runtime-Pinning, Timeout und strukturierter Ausfuehrungsrecord.

## 2. Kanonische Quelle

| Feld | Wert |
| --- | --- |
| Repository | `atc-compute` |
| Pfad | `docs/specs/ATC-COMP-503-WORKER.md` |
| Commit | `89d833edf338085d6141b0c703ebf92a0db83a5e` |
| Quellversion | `0.1.0-DRAFT` |
| Quellstatus | `SPEC-DRAFT` (normativ erst nach Spec-Freeze) |
| Mandat der Erzeugung | SCR-0071 (10.09.2026, Spezifikations-Backlog) |
| Registrierung | SCR-0142 (15.11.2026) |

## 3. Was diese Registrierung nicht tut

- Sie aendert keinen Wortlaut der Quelle.
- Sie stuft nichts hoch: kein `candidate`, kein `approved`, kein `VERIFIED`.
- Sie fuehrt keine zweite Fassung des Textes. Aenderungen erfolgen in der Quelle
  und werden hier nur nachgezogen; die Registry bleibt SSOT der Identitaet,
  nicht des Textes.
- Sie behauptet keine Umsetzung. Der Implementierungsstatus ist
  `specification_only`.

## 4. Aenderungsweg

Aenderungen an Version, Status oder Fundstelle nur ueber SCR (ATC-STD-000 §20,
ATC-STD-002 §2) mit Nachzug von `registry/standards.yaml`,
`registry/standard-implementation.yaml` und den generierten Views.
