# AGENTS.md — atc-standards (AI-DEV-001 §6 / AAS-005)

## Identität

Zuständiger Agent: ATC-AI-ARCH-001 (Aurora #1, Superagent) — 1-Agent-per-Repo.
Identitäts-Manifest: AGENT_MANIFEST.md (Repo-Wurzel) + .github/ai/agent.yaml
(Repo-Manifest, AAS-025).

## Pflicht-Workflow (AAS-008)

DISCOVER → UNDERSTAND → PLAN → IMPLEMENT → TEST → AUDIT → DOCUMENT →
REVIEW → COMMIT → PR → HUMAN APPROVAL → MERGE.

## Verbindliche Standards — ALLE 81 (Vollmandat)

Der Agent MUSS sämtliche Standards der Registry einhalten UND umsetzen
(Voll-Compliance-Mandat, siehe AGENT_MANIFEST.md): Verfassung ATC-STD-000
(insb. §9 Struktur, §10 REQ-IDs, §19-33 SCR, §30 Immutabilität, §37
ID-Allokation) · AI-DEV-001..012 · ATC-AAS-001..025 · ATC-ENT-001..015 ·
ATC-STD-100/201-204/300 · BUG-001..004 · NET-001..008 · ZKP-001..010.
Maschinenlesbar: .github/ai/agent.yaml (required_standards = alle 81);
CI-Gate: check_agent_manifest.py (A1-A4). Neue APPROVED-Standards sind
automatisch verbindlich (dynamische Bindung, Registry = SSOT).

## Kernregeln

- Registry-First: Kein Standard ohne standards.yaml-Eintrag; IDs via §37.
- Änderungen an APPROVED-Standards nur via SCR (§30).
- Jeder Agenten-Task erhält AUD-Record (.github/ai/audit/, AI-DEV-009).
- Commits: AI-DEV-007 v1.0.1 (Typ-Set feat/fix/docs/test/refactor/
  security/build/ci/chore/spec) mit Task-Bezug; Übergang Inline-Tag →
  Trailer bis 07.10.2026 (#112).
- CI MUSS grün sein: validate_all.py (81/81), Mutationssuite (12/12),
  Repo-Audit R3 (Gate PASS) — Ergebnisse sind Evidenz (AAS-010).
- Findings nach BUG-001 mit Severity S0-S4 (BUG-002).
