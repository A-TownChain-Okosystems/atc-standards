---
standard:
  id: ATC-AAS-014
  title: "ATC-AAS-014 — Agent Security Standard"
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

# ATC-AAS-014 — Agent Security Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Geschützte Klassen (niemals durch Agenten in Code/Logs/Issues/Commits/PRs)

API Keys · Tokens · SSH Keys · Wallet Keys · Private Keys ·
Environment-Variable-Werte (nur Namen referenzieren) · Credentials.

**Grundregel: Secrets dürfen niemals vom Agenten in Code, Logs, Issues,
Commits oder PRs geschrieben werden.** (Invariant `no_secret_access`,
AI-DEV-002 §3.)

## 2. Umgebungssicherheit

`environment` im Identity-Manifest (AAS-001) deklariert: Sandbox-Typ,
Netzzugriff (allowlist), erlaubte Kommandoausführung. Nicht deklarierte
Netzwerkziele/Kommandos sind verboten.

## 3. Umgang mit Secret-Fund

Findet ein Agent ein exponiertes Secret: KEIN Kopieren/Zitieren, sofort
Finding S0 (AI-DEV-005), Owner-Eskalation (AI-DEV-011 §2), Task BLOCKED
bis Bereinigung. Rotation ist Owner-Aktion.

## 4. Konsum

Benötigt eine Agentenarbeit ein Secret (z.B. Deploy), erfolgt der Zugriff
ausschließlich über vom Owner verwaltete Secret-Stores — der Agent
referenziert nur den Namen.
