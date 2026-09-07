---
standard:
  id: ATC-AAS-015
  title: "ATC-AAS-015 — Agent Git Standard"
  version: "1.0.0"
  status: approved
  category: aas
  authority: A-TownChain Ecosystems
  owner: ShivaCoreDev
  created: "2026-09-07"
  updated: "2026-09-07"
  normative: true
  supersedes: []
  superseded_by: null
---

# ATC-AAS-015 — Agent Git Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Operationen (normativ)

branch · commit · push · pull request · review · merge · tag · release.
Force-Push auf main/review-Zweigen verboten (AI-DEV-007 §7); Merge nur
über das Merge-Gate (AI-DEV-007 §6); Tags/Releases unveränderlich
(ATC-STD-000 §34, SCR-0003 Option B).

## 2. Commit-Typen

feat · fix · refactor · docs · test · security · build · ci · chore

Format & Trailer unverändert AI-DEV-007 §1: `ATC-TASK-NNNN: <type>: <desc>`
plus Trailer-Block (Agent-ID, Task-ID, Finding-ID, Action-ID, AI-Role,
Validation).

## 3. SCR-0006 — Erweiterung des Typ-Sets (angenommen 07.09.2026)

AI-DEV-007 §1 normierte feat|fix|docs|test|refactor|chore|spec; dieser
Standard ergänzt `security`, `build`, `ci`, `refactor` (teils neu). Da
AI-DEV-007 approved und unveränderlich ist (ATC-STD-000 §30), wird die
Typ-Set-Vereinheitlichung über SCR-0006 formal nachgezogen; bis dahin
sind beide Sets per AI-DEV-007 v1.0.1 vereinheitlicht (SCR-0006 ACCEPTED, 07.09.2026).

## 4. Pflichtbezug

Jeder Commit trägt Task- oder Requirement-Bezug (Trailer); Commits ohne
Bezug sind nur für rein menschliche Änderungen zulässig.
