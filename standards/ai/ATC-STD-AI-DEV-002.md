---
standard:
  id: ATC-STD-AI-DEV-002
  title: "ATC-STD-AI-DEV-002 — Agent Capabilities & Permissions Standard"
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

# ATC-STD-AI-DEV-002 — Agent Capabilities & Permissions Standard (v1.0.0, APPROVED)

> **Status:** APPROVED — Owner-Sammelfreigabe 07.09.2026 (ATC-STD-000 §9)
> **Reihe:** ATC-STD-AI-DEV-001…012 · **Basiert auf:** AI-DEV-001 §3 (Capability-Matrix)

## 1. Capability-Matrix

`capabilities.yaml` ist normativ: Jede Fähigkeit ist benannt, versioniert und
ausschließlich in deklarierter Form ausübbar. Nicht deklarierte Fähigkeit =
nicht vorhanden. Änderungen der Matrix erfordern Manifest-Versionierung
(`agent.version` bump) und Owner-Benachrichtigung bei sicherheitsrelevanten
Erweiterungen.

## 2. Permission-Modell (Least Privilege)

`permissions.yaml` deklariert je Repository: read/write/merge/delete/release.
Defaults: read=true, write je Repo-Notwendigkeit, merge/delete/release=false.
Eskalation (z.B. merge-Recht) nur über dokumentierten Owner-Auftrag mit
Befristung; nach Ablauf automatische Rückstufung.

## 3. Restriktions-Invarianten

Nicht entfernbar, unabhängig von Konfiguration: `no_production_deployment`,
`no_secret_access`, `no_direct_main_merge` (Ausnahme: dokumentierte
Owner-Ausnahme gemäß SCR-0003 Option B mit Commit-Nachweis).

## 4. Verstoßbehandlung

Handeln außerhalb der Matrix = Governance-Verstoß; sofortiges Anhalten,
Dokumentation als Finding (F-NNN) und BLOCKED-Status des Tasks. Keine
Rückwirkungsbereinigung ohne Audit-Record (AI-DEV-009 §3).
