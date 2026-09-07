---
standard:
  id: ATC-AAS-002
  title: "ATC-AAS-002 — Agent Capability Standard"
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

# ATC-AAS-002 — Agent Capability Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Deklarationskategorien (kanonisch)

`capabilities.yaml` deklariert je Kategorie TRUE/FALSE + ggf. Detail-Einschränkung:
Repository lesen · Code schreiben · Tests ausführen · Issues erstellen ·
Pull Requests erstellen · Dokumentation ändern · Releases vorbereiten ·
CI/CD ausführen · Infrastruktur verändern · Secrets verwenden ·
Blockchain-Deployments · Smart Contracts · Datenbankzugriff.

## 2. Kernregel

**Nicht deklarierte Fähigkeiten gelten als nicht vorhanden.** (AI-DEV-002 §1,
hier als konkrete Kategorie-Taxonomie verbindlich.)

## 3. Erweiterungen

Neue Kategorien nur über Ergänzung dieses Standards (SCR, ATC-STD-000 §30)
— eine einzelne Agent-Konfiguration darf keine privaten neuen Kategorien
erfinden.
