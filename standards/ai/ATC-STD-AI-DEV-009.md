---
standard:
  id: ATC-STD-AI-DEV-009
  title: "ATC-STD-AI-DEV-009 — AI Audit Trail Standard"
  version: "1.0.0"
  status: approved
  category: ai-dev
  authority: A-TownChain Ecosystems
  owner: ShivaCoreDev
  created: "2026-09-07"
  updated: "2026-09-07"
  normative: true
  supersedes: []
  superseded_by: null
---

# ATC-STD-AI-DEV-009 — AI Audit Trail Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (v1.0.0) — Owner-Freigabe 07.09.2026 (ATC-STD-000 §9); normativ in Kraft · **Reihe:** ATC-STD-AI-DEV-001…012
> **Autoren:** Michael Wroblewski (Owner), Aurora (Superagent)
> **Kernprinzip:** Jede abgeschlossene Agentenarbeit hinterlässt einen
> unveränderlichen, maschinenlesbaren Audit-Record. Der Audit Trail ist das
> Gedächtnis der Organisation — er überlebt Repos, Agenten und Sessions.
> **Referenzen:** ATC-STD-AI-DEV-001 (§13), ATC-STD-AI-DEV-004 (§7 Completion), naming-conventions `auditRecordId` (AUD-NNN)

---

## Abstract

AI-DEV-009 normiert Struktur, Ablage, Unveränderlichkeit und Auswertbarkeit von
Audit-Records. Ein Audit-Record ist die zusammenfassende Antwort auf: Wer hat
was, warum, worauf gestützt, wie verifiziert — und was ist als Nächstes zu tun?

## 1. Audit-Record (Pflichtstruktur)

ID: `AUD-NNN` (naming-conventions `auditRecordId`, fortlaufend, nie wiederverwendet).
Ablage kanonisch im Repository des Auftrags: `.github/ai/audit/AUD-NNN.yaml`
(Vorlage: `templates/ai/audit-record.template.yaml`).

```yaml
audit:
  id: AUD-031
  task_id: ATC-TASK-00427
  agent: {id: ATC-AI-DEV-001, version: "1.0.0"}
  started: "2026-09-07T19:00:00Z"
  completed: "2026-09-07T19:42:00Z"
  sources: [repository, issue, standard, architecture, tests, ci_cd]
  findings: [F-001]
  actions: [ACT-001, ACT-002, ACT-003, ACT-004]
  validation:
    tests: PASS            # mit CI-Run-Referenz
    lint: PASS
    build: PASS
    security: PASS
    ci_run: "#1234"
  documentation: {status: COMPLETE, references: [docs/parser.md]}
  next_action: ACT-005     # oder null bei Abschluss
  human_review: {required: true, requested: true}
  consistency:            # AI-DEV-001 §12 Konsistenzmatrix
    code: updated
    specification: consistent
    standard: consistent
    wiki: checked
    architecture: checked
    tests: updated
    roadmap: checked
```

Pflichtfelder: alle oben genannten. `next_action` darf nur null sein, wenn der
Task COMPLETED und kein Folge-Auftrag existiert.

## 2. Anlagezeitpunkt

Ein Audit-Record wird angelegt:
- spätestens bei `COMPLETED` oder `CANCELLED` eines Tasks (AI-DEV-004 §7),
- zusätzlich bei jedem `BLOCKED`, der menschliche Entscheidung erfordert,
- bei Übergaben (Handover, AI-DEV-004 §5).

## 3. Unveränderlichkeit (Append-Only)

- Audit-Records werden NIE geändert oder gelöscht.
- Korrekturen erfolgen ausschließlich durch einen Folgercord, der den
  Vorgänger referenziert (`corrects: AUD-031`).
- Audit-Records überleben Archivierung/Migration eines Repos und sind bei
  Repository-Ausgründungen mitzunehmen (keine Informationen dürfen verloren
  gehen).

## 4. Auswertbarkeit (Machine Readability)

- Struktur strikt nach §1; YAML-validierbar gegen die Vorlage.
- Jede Referenz ist eine gültige ID aus naming-conventions: Task
  (ATC-TASK-NNNN), Finding (F-NNN), Action (ACT-NNN), Annahme
  (ASSUMPTION-ANNN), CI-Run.
- `validation.*` MUSS einen nachvollziehbaren CI-Run referenzieren; "PASS ohne
  Run" ist ungültig.

## 5. Blockierende Konsistenzprüfung

Ist ein Eintrag der Konsistenzmatrix nicht `updated`/`consistent`/`checked`,
ist der Status `BLOCKED` — niemals `COMPLETED` (AI-DEV-001 §12). Der
Audit-Record dokumentiert die Abweichung und die geforderte Nacharbeit.

## 6. Verbotene Muster

- Nachträgliche "Bereinigung" von Audit-Records.
- Audit-Record ohne Task-Referenz.
- COMPLETED ohne Audit-Record (Merge-Gate AI-DEV-007 §6 verweigert).
- Paralleldokumentation außerhalb `.github/ai/audit/` als "Ersatz".

## 7. Aufbewahrung

Unbegrenzt. Audit-Records sind Historiendokumentation im Sinne von
ATC-STD-203 und unterliegen keinem Aufräumprozess.
