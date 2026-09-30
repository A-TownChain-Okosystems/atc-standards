---
standard:
  id: ATC-STD-MAINT-019
  title: "ATC-STD-MAINT-019 — Maintenance Evidence Standard"
  version: "1.0.0"
  status: approved
  category: maint
  authority: A-TownChain Ecosystems
  owner: ShivaCoreDev
  created: "2026-09-14"
  updated: "2026-09-30"
  normative: true
  supersedes: []
  superseded_by: null
  effective_date: "2026-09-14"
  review_date: null
  applies_to: "Alle Maintenance-Aufgaben des Oekosystems (Nachweis- und Audit-Evidence)"
  license: "Copyright (c) 2026 Michael Wroblewski"
---

# ATC-STD-MAINT-019 — Maintenance Evidence Standard (v1.0.0, APPROVED)

> **Status:** APPROVED — §9-Freigabe erteilt per Sammelfreigabe SCR-0124 (Owner-Direktive 14.09.2026). Dach: ATC-STD-MAINT-000 ·
> Klassifikation: MAINT-001 · Lifecycle: MAINT-002 · Evidence: MAINT-019.

## Abstract

Verbindliches maschinenlesbares Evidence-Schema fuer Maintenance-Aufgaben (No Evidence, No Trust). P0-Governance-Standard.

## §1 Verbindliches Record-Schema (MAINT-Records, ID-Schema MAINT-YYYY-NNNN)

```yaml
maintenance:
  id: MAINT-2026-0001
  classification: M1
  component: atc-node
  detected: 2026-09-13
  reason: dependency_update
  change:
    before: "x.y.z"
    after: "x.y.z+1"
  validation:
    unit_tests: PASS
    integration_tests: PASS
    security_scan: PASS
    compatibility: PASS
    performance: PASS
  rollback:
    available: true
    tested: true
  evidence:
    commit: "<sha>"
    pull_request: "<url/id>"
    test_report: "<ref>"
    audit_report: "<ref>"
  status: CLOSED
```

## §2 Regeln (normativ)

1. Kein CLOSE ohne vollstaendigen Record (alle validation-Felder bearbeitet, Evidence-Referenzen gesetzt).
2. 'Update durchgefuehrt' ist KEIN gueltiger Abschluss.
3. Records werden maschinenlesbar im Repo (`docs/maintenance/`) oder Registry gefuehrt und sind auditierbar.
4. Maschinenlesbare Schemas (MAINT-000 §20.1 Machine-Readable Conformance):
   - `schemas/maintenance/maintenance-record.schema.json` — Maintenance Record.
   - `schemas/maintenance/maintenance-evidence.schema.json` — bestehendes konsolidiertes Evidence-Envelope.
   - `schemas/maintenance/workflow-evidence.schema.json` — spezialisierter Workflow-/Job-Evidence-Layer nach SCR-0129.
5. M2/M3 zusaetzlich: SoD-Vermerk (Implementer/Validator/Auditor) und Security- bzw. Emergency-Report.
6. Evidence Completeness ist KPI (Anteil vollstaendiger Records, generiert).

## §3 Workflow-/Job-Evidence-Layer (SCR-0129)

Der Workflow-/Job-Layer ist die technische Auspraegung des bestehenden MAINT-019-Evidence-Modells. Er erzeugt keinen parallelen Evidence-Standard.

Die normative Traceability-Kette lautet:

`Workflow → Run → Job → Step → Result / Exit Code → Finding → Architecture Contract → Root Cause → Minimal Fix → Commit → Exact-SHA Rerun → Verification`

### 3.1 Workflow

Ein Evidence-Record MUSS, soweit der CI-Lauf diese Daten liefert, Workflow, Workflow-ID oder Workflow-Datei, Repository, Trigger, Pull-Request/Branch und den erwarteten Ziel-SHA enthalten.

### 3.2 Run

Ein Run MUSS Run-ID, Status, getesteten SHA, Checkout-Ref, Exact-SHA-Status und Evidence-Status enthalten.

`tested_sha` und `expected_sha` sind getrennte Felder. Ein frueherer PASS-Lauf darf keinen spaeteren Commit verifizieren.

### 3.3 Job und Step

Jeder relevante Job MUSS Job-ID, Name, Ergebnis, Exit-Code und Steps enthalten. Fehlerhafte Steps MUESSEN eine technische Fehlermeldung referenzierbar machen.

### 3.4 Finding und Architecture Contract

Ein Finding MUSS von der technischen CI-Meldung bis zur Architekturwirkung nachvollziehbar sein. P0/P1-relevante Architekturverletzungen MUESSEN, soweit anwendbar, SSOT, erwarteten Contract, aktuelle Implementierung, konkrete Verletzung und Severity dokumentieren.

### 3.5 Remediation

Eine Remediation MUSS Minimal Fix, Commit-SHA, geaenderte Dateien und Validierung dokumentieren.

Gate-Abschwaechungen, Allowlist-Tricks, Warnungsunterdrueckung und kosmetische Touch-Commits sind keine gueltige Remediation.

### 3.6 Rerun und Verification

Verbindliche Lifecycle-Kette:

`UNANALYZED → ANALYZED → FIXED → RERUNNING → VERIFIED | RESIDUAL`

`VERIFIED` ist nur zulaessig, wenn:
- der getestete SHA exakt dem zu verifizierenden erwarteten SHA entspricht;
- der Checkout-Ref kein PR-Merge-Ref `refs/pull/<n>/merge` bzw. `refs/remotes/pull/<n>/merge` ist;
- alle erforderlichen Jobs PASS mit Exit-Code 0 sind;
- alle erforderlichen Gates PASS sind;
- keine RESIDUAL-Findings im verifizierten Scope verbleiben.

## §4 Exact-SHA Contract (normativ)

1. PR-Merge-Refs sind nicht automatisch Exact-SHA-Evidence.
2. `refs/pull/<n>/merge` und `refs/remotes/pull/<n>/merge` duerfen nicht als Exact-SHA-Nachweis fuer den PR-Head akzeptiert werden.
3. Ein Run auf einem Merge-Commit kann nur Evidence fuer genau diesen Merge-Commit sein.
4. Ein PR-Head benoetigt einen Lauf, der den tatsaechlichen PR-Head-SHA testet.
5. Ein Evidence-Record mit `VERIFIED` ohne nachgewiesene SHA-Bindung MUSS vom Validator abgelehnt werden.

## §5 Implementierung / Enforcement

Die SCR-0129-Implementierung umfasst:

- `schemas/maintenance/workflow-evidence.schema.json`;
- `tools/maintenance/validate_workflow_evidence.py`;
- positive und negative Exact-SHA-Tests;
- CI-Ausfuehrung des Validators.

Der Validator ist fail-closed. Tool-Existenz allein ist kein Implementierungsnachweis; die CI-Ausfuehrung und ihr realer Lauf sind Teil der Evidence.

## REQ-Matrix (normativ)

| REQ | Anforderung | Pflicht |
|---|---|---|
| REQ-MAINT-072 | Jede Maintenance-Aufgabe schliesst mit Record im §1-Schema | MUST |
| REQ-MAINT-073 | Kein CLOSE ohne vollstaendige validation- und evidence-Felder | MUST |
| REQ-MAINT-074 | M2/M3-Records enthalten SoD-Vermerke | MUST |
| REQ-MAINT-075 | Records sind maschinenlesbar gespeichert und auditierbar | MUST |

## Implementierungsstatus

**SCR-0129 IMPLEMENTATION ON BRANCH — REVIEW PENDING.**

Die technische Implementierung liegt auf dem SCR-0129-Branch vor. Die normative Aenderung an diesem APPROVED-Standard ist bis zur vorgesehenen Freigabe nicht als auf `main` wirksam zu betrachten. Mainline-Evidence darf daher erst nach Review/Freigabe und anschliessendem Exact-SHA-CI-Lauf als VERIFIED gelten.

## Compliance

Dach: ATC-STD-MAINT-000; Kernprofil: ATC-STD-000, ATC-STD-201/202/203, ATC-STD-ENG-001.
