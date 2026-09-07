---
standard:
  id: ATC-STD-AI-DEV-012
  title: "ATC-STD-AI-DEV-012 — Multi-Agent Coordination Standard"
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

# ATC-STD-AI-DEV-012 — Multi-Agent Coordination Standard (v1.0.0, APPROVED)

> **Status:** APPROVED — Owner-Sammelfreigabe 07.09.2026 (ATC-STD-000 §9)
> **Reihe:** ATC-STD-AI-DEV-001…012 · **Basiert auf:** AI-DEV-001, AGENT_PROTOCOL (1-Agent-per-Repo)

## 1. Repo-Exklusivität

Pro Repository arbeitet zu jedem Zeitpunkt genau EIN Agent (1-Agent-per-Repo,
AgentAssignment-Registry). Repo-Wechsel nur wenn: alle Dateien vollständig,
Tests grün, gepusht, dokumentiert (AGENT_PROTOCOL-Regel).

## 2. Kommunikation über Artefakte

Agenten kommunizieren ausschließlich über maschinenlesbare Artefakte:
Task-Records (AI-DEV-004), Audit-Records (AI-DEV-009), Findings,
Commit-Trailer (AI-DEV-007). Keine Annahmen über internen Zustand anderer
Agenten; der Stand ist im Artefakt oder er existiert nicht.

## 3. Übergabe (Handover)

Übergabe nur bei übergabefähigem Task (AI-DEV-004 §5): vollständiger
Task-Record, aktuelle next_action, offene Annahmen registriert, history
lückenlos. Übernehmender Agent startet mit DISCOVERING (AI-DEV-003) und
vermerkt `handover_from: ATC-AI-…-NNN`.

## 4. Konfliktbehandlung

Bei parallelen Änderungen am gleichen Ziel (Verstoß gegen §1): Owner-
Eskalation (AI-DEV-011 §2), Findings S1, Auflösung durch den zuständigen
Agenten mit Sync-Record (BUG-004). Merge-Konflikte durch Regelverstoß
sind keine technischen Zufälle, sondern Governance-Verstöße.
