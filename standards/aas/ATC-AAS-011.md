---
standard:
  id: ATC-AAS-011
  title: "ATC-AAS-011 — Agent Verification Standard"
  version: "1.0.0"
  status: candidate
  category: aas
  authority: A-TownChain Ecosystems
  owner: ShivaCoreDev
  created: "2026-09-07"
  updated: "2026-09-07"
  normative: true
  supersedes: []
  superseded_by: null
---

# ATC-AAS-011 — Agent Verification Standard (v1.0.0, CANDIDATE)

> **Status:** CANDIDATE · **Priorität:** P0 · **Erweitert:** ATC-STD-AI-DEV-008 (Testing & Validation)

## 1. Verifikationsebenen

L1 Syntax (Lint/Compile) · L2 Unit Tests · L3 Integration Tests ·
L4 System Validation (End-to-End, Devnet-basiert, ATC-STD-NET-001).

Je Änderung gilt die höchste anwendbare Ebene als Mindest-Validierung;
L-Angabe ist Teil des Evidenzblocks (AAS-010).

## 2. Zusatz-Dimensionen für Blockchain-Kernkomponenten

Security · Consensus · Cryptography · State Transition · Economic Rules ·
Compatibility.

Betroffene Komponenten (atc-blockchain, atc-algorithm, atc-vm, a-townchain,
atc-contracts, atc-zkp) DÜRFEN nur mit Prüfung aller zutreffenden
Zusatz-Dimensionen als COMPLETED abgeschlossen werden (Findings bei
Abweichung, Human-Approval-Pflicht AAS-017).

## 3. Verifikationsmatrix

`verification: {level: L1..L4, dimensions: [...], result, evidence}` je Task
(AI-DEV-008 §1).
