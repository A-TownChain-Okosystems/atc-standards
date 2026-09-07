---
standard:
  id: ATC-STD-SC-016
  title: "ATC-STD-SC-016 — Oracle Contract Standard"
  version: "1.0.0"
  status: candidate
  category: sc
  authority: A-TownChain-Okosystems
  owner: Michael (Owner-Entwurf) / ATC-AI-ARCH-001 (Formalfassung)
  created: "2026-09-07"
  normative: true
  applies_to: "Alle Smart Contracts des A-TownChain-Oekosystems"
  supersedes: []
---

# ATC-STD-SC-016 — Oracle Contract Standard (v1.0.0, CANDIDATE)

> **Status:** CANDIDATE (v1.0.0) — Owner-Entwurf Michael 07.09.2026, Formalfassung
> durch ATC-AI-ARCH-001; Freigabe nach ATC-STD-000 §9 ausstehend (Todo #118).
> **Familie:** ATC Smart Contract Standards Framework (ATC-STD-SC-001..020).

## Abstract

Oracle-basierte Contracts definieren provider, update_frequency, max_staleness, deviation_threshold, fallback und emergency_behavior; veraltete oder manipulierte Daten werden nicht akzeptiert.

## Scope

Gilt fuer alle SC-ORACLE-Contracts und oracle-konsumierende Contracts (SC-DEFI).

## 1. Konfigurationspflicht (REQ-SC-045)

Oracle-konsumierende Contracts MUESSEN definieren: oracle.provider, update_frequency, max_staleness, deviation_threshold, fallback, emergency_behavior.

## 2. Datenvaliditaet (REQ-SC-046)

Ein Contract DARF KEINE veralteten (staleness > max_staleness) oder offensichtlich manipulierten (deviation > threshold) Daten akzeptieren; im Zweifel Fallback/Emergency-Verhalten.



## Anforderungs-Verzeichnis

| REQ-ID | Anforderung | Verbindlichkeit |
|---|---|---|
| REQ-SC-045 | Konfiguration (§1) | MUSS |
| REQ-SC-046 | Datenvaliditaet (§2) | MUSS |

## Compliance

Pruefung im Rahmen der SC-Compliance-Gates (ATC-STD-SC-001, SC-G0..G13):
kein Gate — kein Mainnet. Verstoege werden als Finding nach ATC-STD-BUG-001
dokumentiert. Registry-Pflichten nach ATC-STD-SC-019.

## Security Considerations

Oracle-Manipulation ist Top-Angriffsvektor fuer DeFi (siehe SC-003 §1).

## Changelog

| Version | Datum | Aenderung |
|---|---|---|
| 1.0.0 | 2026-09-07 | Initiale Fassung (Owner-Entwurf Michael, Formalfassung ATC-AI-ARCH-001) |

## References

- **NORMATIVE:** ATC-STD-000, ATC-STD-203, ATC-STD-204, ATC-STD-SC-001 (Familien-Hauptstandard), ATC-STD-SC-003 (Security)
- **INFORMATIVE:** ATC-AAS-001..025, AI-DEV-001..012, contracts/registry/
