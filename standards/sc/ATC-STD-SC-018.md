---
standard:
  id: ATC-STD-SC-018
  title: "ATC-STD-SC-018 — Mining Contract Standard"
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

# ATC-STD-SC-018 — Mining Contract Standard (v1.0.0, CANDIDATE)

> **Status:** CANDIDATE (v1.0.0) — Owner-Entwurf Michael 07.09.2026, Formalfassung
> durch ATC-AI-ARCH-001; Freigabe nach ATC-STD-000 §9 ausstehend (Todo #118).
> **Familie:** ATC Smart Contract Standards Framework (ATC-STD-SC-001..020).

## Abstract

Anforderungen fuer Mining-Reward-Contracts: Emissionsplan, Schwierigkeits-/Block-Reward-Regeln, Claim-Mechanismen und Events fuer Emissions- und Reward-Verteilung (Verzahnung MinerWatcherGPT).

## Scope

Gilt fuer alle SC-MINING-Contracts (atc-mining, ATC-Kernkonsensus PoW/PoS).

## 1. Emissionsplan (REQ-SC-050)

Mining-Contracts MUESSEN einen dokumentierten Emissionsplan haben (Invariant: minedSupply <= maxSupply; halbierungs-/epochenbasierte Regeln explizit).

## 2. Reward-Verteilung (REQ-SC-051)

Claim- und Verteilungsmechanismen MUessen gegen Replay und Double-Claim gesichert sein (SC-003).

## 3. Monitoring (REQ-SC-052)

Block-Reward- und Claim-Events sind Event-pflichtig (SC-008) fuer MinerWatcherGPT-Monitoring.



## Anforderungs-Verzeichnis

| REQ-ID | Anforderung | Verbindlichkeit |
|---|---|---|
| REQ-SC-050 | Emissionsplan (§1) | MUSS |
| REQ-SC-051 | Double-Claim-Schutz (§2) | MUSS |
| REQ-SC-052 | Monitoring-Events (§3) | MUSS |

## Compliance

Pruefung im Rahmen der SC-Compliance-Gates (ATC-STD-SC-001, SC-G0..G13):
kein Gate — kein Mainnet. Verstoege werden als Finding nach ATC-STD-BUG-001
dokumentiert. Registry-Pflichten nach ATC-STD-SC-019.

## Security Considerations

Emissionsfehler sind irreversibel (Immutabilitaet SC-007) — Invariant-Tests Pflicht.

## Changelog

| Version | Datum | Aenderung |
|---|---|---|
| 1.0.0 | 2026-09-07 | Initiale Fassung (Owner-Entwurf Michael, Formalfassung ATC-AI-ARCH-001) |

## References

- **NORMATIVE:** ATC-STD-000, ATC-STD-203, ATC-STD-204, ATC-STD-SC-001 (Familien-Hauptstandard), ATC-STD-SC-004 (Testing)
- **INFORMATIVE:** ATC-AAS-001..025, AI-DEV-001..012, contracts/registry/
