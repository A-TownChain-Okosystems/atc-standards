---
standard:
  id: ATC-AAS-009
  title: "ATC-AAS-009 — Agent Change Standard"
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

# ATC-AAS-009 — Agent Change Standard (v1.0.0, APPROVED)

> **Status:** APPROVED (Owner-Sammelfreigabe 07.09.2026, ATC-STD-000 §9) — normativ in Kraft

## 1. Änderungsdokumentation (Pflicht je Änderung, im PR-Body)

```
WHAT     — was wurde geändert
WHY      — warum war es notwendig (reason mit REQ-/Standard-Bezug)
WHERE    — welche Dateien
IMPACT   — welche Systeme betroffen (Dependency-Check ATC-STD-204)
TEST     — welche Tests/Validierungen (mit CI-Run-Referenz, AAS-010)
RISK     — welche Risiken bestehen (Restrisiken, bekannte Grenzen)
ROLLBACK — wie wird zurückgenommen (git revert …, Migrationshinweise)
```

## 2. Regeln

- Jedes der 7 Felder ist auszufüllen; „n/a" ist eine gültige, aber
  dokumentierte Aussage.
- RISK bei Blockchain-Kernkomponenten (Consensus/Crypto/State/Tokens)
  verpflichtet zur Human-Approval-Kennzeichnung (AAS-017).
- ROLLBACK ist für MERGE-fähige PRs zwingend konkret (kein „siehe oben").
