# Changelog — atc-standards

## [1.2.0] — 2026-09-07 (AD-032)
- Wiki-Konsolidierung II: 6 weitere Standards aus dem Docs-Hub uebernommen —
  ats/ATS_STANDARDS.md (ATS-1000…1007 ShivaOS Kernel/Stack, vollstaendige
  283-Zeilen-Fassung), atc/ATC_STANDARDS.md (ATC-0001…0008 Core-Protokolle,
  vollstaendige 233-Zeilen-Fassung mit ATC-9000-Sektion),
  atc/ATC_TOKEN_STANDARD.md (ATC-001/8300/9000/9900-Referenz),
  licensing/ATVM_LICENSE_GATE_SPEC.md, licensing/IP_LICENSE_DASHBOARD_SPEC.md,
  licensing/SMART_CONTRACT_RICHTLINIE.md (BaFin-Richtlinie)
- README-Struktur und Std.-Zaehler aktualisiert (115 Dokumente)


## [1.1.0] — 2026-09-07 (AD-031)
- ATC-STD-REPO-001 v1.0.0 FORMALE SPEZIFIKATION: MUST/SHOULD/MAY (RFC 2119),
  Compliance-Matrix R0-R4 (M-01…M-16), Validator-Regeln V-01…V-16
- ATC-STD-REPO-002 v1.0.1: Ownership-Standard, Lifecycle-Uebergangsregeln,
  Security-Klassifizierung S0-S4, zentraler Dependency Graph, Repository-Registry
- ATC-STD-REPO-003 v1.0.1: Branching, Conventional Commits, PR-Standard,
  Release-Gates GATE-01…GATE-10, Dependency Policy, Third-Party, API-Stability,
  Breaking Changes, Reproducible Builds, Artifact Management, Health Score
- registry/: repositories.yaml (23 Repos mit R- und S-Klassen), teams.yaml,
  dependencies.yaml (L0-L7-Graph)
- schemas/: 4 Metadaten-Schemas; templates/: Repository-/PR-/CI-Vorlagen
- tools/atc-repo-audit v0.1.0: lauffaehiger Validator (stdlib-only), GATE: PASS/NO-GO
- Self-Compliance: .atc/-Metadaten, CODEOWNERS, Governance-CI (Auditor prueft sich selbst)


## [1.0.0] — 2026-09-07 (AD-030)
- Initial-Bestand: 109 Standard-Dokumente aus dem Docs-Hub ueberfuehrt
  (ATC-01…99 inkl. ATC-LIC + ATC_ECOSYSTEM_STANDARDS, ATS-LIC, OVERVIEW,
  STANDARDS_REGISTRY)
- Governance-Standards ATC-STD-REPO-001/002/003 (AD-029, 07.09.2026)
- .atc-Referenzimplementierungen (registry.atc + 4 Standards-Vertraege,
  aus atc-contracts modules/atc-standards-refs)
- Repo ist SPEC-Typ R3 gemaess eigener Klassifizierung (self-compliant)
