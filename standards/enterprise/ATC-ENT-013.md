---
standard:
  id: ATC-ENT-013
  title: "ATC-ENT-013 — KPI & Performance Standard"
  version: "1.0.0"
  status: approved
  category: enterprise
  authority: A-TownChain Ecosystems
  owner: ShivaCoreDev
  created: "2026-09-07"
  updated: "2026-09-07"
  normative: true
  supersedes: []
  superseded_by: null
---

# ATC-ENT-013 — KPI & Performance Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. KPI-Familien (kanonisch)

**Engineering:** Deployment Frequency · Lead Time · Change Failure Rate ·
Mean Time to Recovery · Test Coverage · Open Bugs · Critical Findings.
**Security:** Critical Vulnerabilities · Patch Time · Security Incidents ·
Failed Security Gates.
**AI:** Agent Success Rate · Human Intervention Rate · Failed Tasks ·
Unauthorized Actions · Token/Compute Cost · Verification Rate.
**Blockchain:** Node Availability · Block Finality · Transaction
Throughput · Failed Transactions · Validator Health · Network Latency.

## 2. Erhebung

Automatisiert aus Audit-Records (ENT-014), CI-Artefakten und System-
Metriken; Agenten-KPIs unverändert aus AAS-021. Erhebung als Workflow
(monatlich, ENT-012 §4), Report an Owner (E3/E4).

## 3. Schwellen

Kritische KPI-Überschreitungen (z.B. Critical Findings > 0,
Unauthorized Actions > 0) triggern Eskalation (ENT-007) und ggf.
Risiko-Registry-Eintrag (ENT-011 §1).
