---
standard:
  id: ATC-STD-MAINT-000
  title: "ATC-STD-MAINT-000 — Maintenance Governance Standard (Parent Standard)"
  version: "1.0.0"
  status: draft
  category: maint
  authority: A-TownChain Ecosystems
  owner: "Michael (Owner-Entwurf)"
  created: "2026-09-14"
  updated: "2026-09-14"
  normative: true
  supersedes: []
  superseded_by: null
  effective_date: "pending §9-Freigabe"
  review_date: null
  applies_to: "Gesamtes A-TownChain-Oekosystem als uebergeordnete Ecosystem-Governance-Capability (OS, Kernel, Blockchain, VM/Runtime, AI, Standards, Infrastruktur, Repositories — auch Repos ausserhalb KAI-OS)"
  license: "Copyright (c) 2026 Michael Wroblewski"
---

# ATC-STD-MAINT-000 — Maintenance Governance Standard (Parent Standard, v1.0.0 DRAFT)

> **Status:** DRAFT — wartet auf §9-Freigabe (ATC-STD-000). Parent Standard der
> Querschnittsfamilie ATC-STD-MAINT-000..024; MAINT-001..024 erben die Mandatory Baseline
> dieses Standards. Die spezialisierten Standards duplizieren keine technischen Anforderungen
> dieses Standards — sie konkretisieren sie.

## §1 Scope

Geltungsbereich: Maintenance des gesamten A-TownChain-Oekosystems als **uebergeordnete
Ecosystem-Governance-Capability** — nicht als Teil von KAI-OS selbst. Dies ist strategisch:
Dieselbe Maintenance-Infrastruktur kann spaeter auch fuer Repositories ausserhalb von KAI-OS
verwendet werden. Die Familie gilt fuer alle Schichten (Aurora AI, GlobusOS, ShivaCore, ATC-VM,
A-TownChain, ATCLang, Hardware/Firmware), alle Repositories und alle Releases.

## §2 Normativsprache und Terminologie (normativ)

Die Schluesselwoerter **MUST / MUST NOT** (verbindlich), **SHOULD / SHOULD NOT** (empfohlen)
und **MAY** (optional) sind im Sinne von ATC-STD-000 zu lesen; REQ-Eintraege tragen ihre
Pflichtstufe explizit. Informative Abschnitte sind gekennzeichnet.

Begriffe (normativ): **Maintenance** (praeventive, korrektive, adaptive und sicherheitskritische
Pflege) · **Maintenance Capability** (die Faehigkeit einer Komponente, betrieben gepflegt zu
werden: Metriken, Tests, Upgrade-Pfad, Rollback, Observability) · **Maintenance Readiness**
(Vollstaendigkeit der required-Felder vor Release) · **Maintenance Engine** (automatisierte
Detection, Klassifikations-Vorschlaege, Gates, Remediation) · **Evidence Record** (maschinenlesbarer
Nachweis, MAINT-019) · **Verified State** (Zustand nach vollstaendiger Evidence in CI nachweisbar).

## §3 Maintenance Principles (normativ)

P1 Maintenance deckt den gesamten Lifecycle ab (praeventiv, korrektiv, adaptiv,
sicherheitskritisch) — nicht nur Post-Release.
P2 **Maintenance Capability ist eine Release-Voraussetzung** (§7) — Maintenance-from-Development.
P3 Klassifikation vor Bearbeitung: M0-M3 ab Anlage, im Zweifel die hoehere Klasse (MAINT-001).
P4 Einheitlicher Lifecycle: 13 Phasen DETECT..CLOSE, GSEPF-kompatibel (MAINT-002).
P5 No Evidence, No Trust: kein CLOSE ohne vollstaendigen Record (MAINT-019).
P6 Schichtgrenzen des KAI-OS-Stacks sind Maintenance-Grenzen; Kompatibilitaetsnachweis pflichtig (MAINT-009 als Muster).
P7 Separation of Duties fuer M2/M3 (§7.4).
P8 KPIs werden generiert, nie handgezahlt (§9).
P9 Automatisierung mit Eskalationsgrenzen: M0 Automate, M1 Review, M2/M3 Escalate — nie autonom (MAINT-020).
P10 Ecosystem-weite Wiederverwendbarkeit: Die Maintenance-Infrastruktur ist von KAI-OS unabhaengig einsetzbar.

## §4 Rollen und RACI (normativ)

Rollen: **Owner** (Governance-Freigabe, §9, Emergency-Eskalation) · **Maintainer**
(Bereichsverantwortung je MAINT-Standard/Repository) · **Implementer** · **Validator** ·
**Auditor** · **Release Authority**.

| Phase (MAINT-002) | Owner | Maintainer | Implementer | Validator | Auditor | Release Authority |
|---|---|---|---|---|---|---|
| DETECT / ASSESS | I | A | R | C | I | — |
| CLASSIFY / PLAN | I | A/R | C | C | I | — |
| APPROVE (M0/M1) | I | A | — | C | — | R |
| APPROVE (M2) | C | A | — | C | C | R |
| APPROVE (M3 Emergency) | A | C | — | C | C | R |
| IMPLEMENT / TEST | I | C | A/R | I | — | — |
| VALIDATE (M2/M3) | I | C | — | A/R | C | — |
| DEPLOY / MONITOR | I | C | R | — | — | A |
| EVIDENCE / CLOSE | I | A | R | C | R (Audit) | I |

R=Responsible, A=Accountable, C=Consulted, I=Informed.

## §5 Klassifikation M0-M3 (Uebersicht — normative Details: MAINT-001)

M0-Routine (regulaerer Zyklus) · M1-Operational (priorisiert) · M2-Security (darf
Release-Zyklen vorlagern) · M3-Critical (Emergency-Pfad §32, uebersteuert normale Zyklen).

## §6 Lifecycle (Uebersicht — normative Details: MAINT-002)

DETECT → ASSESS → CLASSIFY → PLAN → APPROVE → IMPLEMENT → TEST → VALIDATE → DEPLOY →
MONITOR → EVIDENCE → CLOSE.

## §7 Governance und Gates

### §7.1 Zentraler Grundsatz (normativ, verbindlich)

> **A system MUST NOT be released to a lifecycle state requiring operational support unless
> its required maintenance capabilities are implemented, validated, documented, and evidenced.**

(Deutsche Fassung: Ein System DARF NICHT in einen Lifecycle-Zustand mit Betriebsunterstuetzung
released werden, solange seine erforderlichen Maintenance-Faehigkeiten nicht implementiert,
validiert, dokumentiert und nachgewiesen sind.) Damit wird verhindert, dass z.B. ein neues
KAI-OS-Release zwar funktioniert, aber keinen getesteten Upgrade-, Rollback-, Monitoring- oder
Recovery-Pfad besitzt.

### §7.2 Maintenance Readiness Gate (normativ)

```
RELEASE CANDIDATE
        │
        ▼
┌─────────────────────┐
│ Maintenance Readiness│
│        Gate          │
└──────────┬──────────┘
        │
   ┌────┴────┐
 FAIL       PASS
   │         │
   ▼         ▼
 BLOCK     RELEASE
             │
             ▼
          OBSERVE
             │
             ▼
          EVIDENCE
             │
             ▼
       VERIFIED STATE
```

Mindestanforderungen (alle required): `maintenance_owner`, `maintenance_documentation`,
`dependency_inventory`, `security_process`, `test_suite`, `rollback_strategy`,
`compatibility_strategy`, `monitoring`, `evidence_collection`, `lifecycle_status`.
Zusaetzlich fuer M2/M3-Releases (alle required): `independent_validation`, `security_review`,
`rollback_test`, `incident_record`, `audit_evidence`. Maschinenlesbar:
`schemas/maintenance/maintenance-readiness.schema.json`; geprueft durch den
Maintenance-Conformance-Workflow (§12).

### §7.3 Klassifikations-Gates

M0 → Standard Review · M1 → Operational Review · M2 → Security Review · M3 → Emergency
Governance (ATC-STD-000 §32).

### §7.4 Separation of Duties (normativ)

```
Implementer ≠ Validator ≠ Auditor
Release Authority ≠ Implementer (bei besonders kritischen Aenderungen)
```

## §8 Exceptions (normativ)

1. **Emergency (M3):** beschleunigter, aber vollstaendiger Lifecycle (MAINT-021); §32 bleibt
   verbindlich; EVIDENCE wird nachdokumentiert, nie ausgelassen.
2. **Dokumentierte Ausnahme:** Eine Abweichung von diesem Standard ist nur befristet, mit
   Begruendung, Ersatzmassnahme und Owner-Freigabe moeglich. Ausnahmen duerfen NIE die
   Evidence-Pflicht (P5) oder die SoD-Pflicht fuer M3 (§7.4) umgehen.
3. **M0-Konsolidierung:** Fuer M0 duerfen Lifecycle-Phasen zusammengefasst dokumentiert werden,
   solange die Evidence vollstaendig ist (MAINT-002 §3).

## §9 Metriken (verbindliche KPIs — Details: MAINT-019/020)

MTTA · MTTD · MTTR · MTBF · Patch Latency · Dependency Freshness · Technical Debt ·
Maintenance Backlog · Rollback Success Rate · Regression Rate · Evidence Completeness ·
Recovery Readiness. Generiert, nie handgezahlt.

## §10 Compliance-Regeln (normativ)

1. **Mandatory Baseline / Vererbung:** MAINT-001..024 erben diesen Standard als verbindliche
   Baseline; im Konflikt gilt MAINT-000. Spezialstandards konkretisieren, sie duplizieren nicht.
2. **Drei-Stufen-Compliance** (wie R12): formal (Standards/Registry konsistent) ·
   implementation (Mechanismen gebaut) · production (im Betrieb nachgewiesen). Nur
   CI-nachweisbare Zustaende sind zitierbar (CLAIMED != PASS).
3. **Kernprofil:** ATC-STD-000, ATC-STD-201/202/203, ATC-STD-ENG-001.
4. **Nichtkonformitaet:** Readiness-Gate-FAIL blockiert das Release; fehlende Evidence verhindert
   CLOSE (P5); Verstoesse gegen SoD machen die Freigabe ungueltig.

## §11 Beziehungen zu anderen ATC-Standards (normativ)

| Standard | Beziehung |
|---|---|
| ATC-STD-000 | Meta-Governance, §9-Freigabe, §32-Emergency (M3) |
| ATC-STD-ENG-001 | Engineering-Disziplin; MAINT ist spezialisierter Lifecycle innerhalb von GSEPF |
| ATC-STD-REPO-MAINT-001 | SSOT Repository-Pflegezyklus (MAINT-011 bindet nur) |
| ATC-STD-UPDATE-001 | SSOT Update-Durchfuehrung (MAINT-017 bindet nur) |
| ATC-STD-COMPAT-001 | SSOT Kompatibilitaetspruefung (MAINT-016 bindet nur) |
| ATC-STD-BUG-001..004 / ERR-* | Findings-/Fehler-Lifecycle; MAINT klassifiziert zusaetzlich M0-M3 |
| ATC-STD-AI-DEV-001..012 | Agenten-Governance; Maintenance-Automation unterliegt ihr (MAINT-020) |
| ATC-STD-IMPLEMENTATION-000 | Implementierungs-Matrix/Abdeckung; MAINT-Eintraege specification_only |

## §12 Machine-readable Conformance (normativ)

```
standards/maintenance/ATC-STD-MAINT-000..024.md   (normative Dokumente)
registry/standards/ATC-STD-MAINT-000..024.yaml    (per-Standard-Conformance-Metadaten)
schemas/maintenance/
  maintenance-record.schema.json                  (Evidence-Record, MAINT-019)
  maintenance-readiness.schema.json              (Readiness-Gate, §7)
  maintenance-evidence.schema.json               (Evidence-Envelope, MAINT-019)
.github/workflows/maintenance-conformance.yml    (CI-Gate)
```

Der Conformance-Workflow prueft maschinenlesbar u.a.: MAINTENANCE.md · dependency inventory ·
security scanning · SBOM · tests · rollback strategy · compatibility strategy · monitoring ·
evidence · lifecycle metadata → **MAINTENANCE READY**.

## §13 Zielarchitektur und strategische Positionierung (normativ)

```
ATC ECOSYSTEM GOVERNANCE
        │
   ┌────┼────────────┐
   ▼    ▼            ▼
ATC Standards  GSEPF  Release Governance
   │    │            │
   └────┼────────────┘
        ▼
Maintenance Governance
        ▼
Maintenance Engine
        │
   ┌────┼────────────┐
   ▼    ▼            ▼
KAI-OS/OS  A-TownChain  Aurora AI
(ShivaCore, (ATC-VM, Node,  (Models, Registry,
GlobusOS,   P2P, ...)    Inference)
Drivers)
   │    │            │
   └────┼────────────┘
        ▼
    Evidence
        ▼
  VERIFIED STATE
```

Strategischer Vorteil: Dieselbe Maintenance-Infrastruktur ist spaeter auch fuer Repositories
ausserhalb von KAI-OS wiederverwendbar (P10). ATC-STD-MAINT-* ist damit eine echte
Enterprise-/Platform-Standardfamilie, keine KAI-OS-spezifische Spezifikation.

## REQ-Matrix (normativ)

| REQ | Anforderung | Pflicht |
|---|---|---|
| REQ-MAINT-000-001 | Familienstruktur 000-024 (8 Gruppen, §1/SCR-0120), ab 025 frei via SCR | MUST |
| REQ-MAINT-000-002 | MAINT-001..024 erben diesen Standard als Mandatory Baseline; im Konflikt gilt MAINT-000 | MUST |
| REQ-MAINT-000-003 | A system MUST NOT be released to a lifecycle state requiring operational support unless its required maintenance capabilities are implemented, validated, documented, and evidenced (§7.1) | MUST |
| REQ-MAINT-000-004 | Kein Release ohne vollstaendige maintenance_readiness; FAIL = BLOCK (§7.2) | MUST |
| REQ-MAINT-000-005 | M2/M3-Releases erfordern zusaetzlich vollstaendige critical_maintenance (§7.2) | MUST |
| REQ-MAINT-000-006 | Separation of Duties (Implementer ≠ Validator ≠ Auditor; Release Authority ≠ Implementer) fuer M2/M3 | MUST |
| REQ-MAINT-000-007 | Der 13-Phasen-Lifecycle ist fuer alle Maintenance-Aufgaben verbindlich; kein CLOSE ohne Evidence | MUST |
| REQ-MAINT-000-008 | Schichtgrenzen des KAI-OS-Stacks sind Maintenance-Grenzen; Kompatibilitaetsnachweis pflichtig | MUST |
| REQ-MAINT-000-009 | KPIs werden generiert, nicht handgeschrieben | MUST |
| REQ-MAINT-000-010 | Kritische Repositories besitzen MAINTENANCE.md + docs/maintenance/ | MUST |
| REQ-MAINT-000-011 | Exceptions nur befristet mit Owner-Freigabe; nie Umgehung von Evidence-Pflicht oder M3-SoD (§8) | MUST |
| REQ-MAINT-000-012 | Machine-readable Conformance (§12): Standards-Verzeichnis, registry/standards/-YAMLs, JSON-Schemas, Conformance-Workflow | MUST |
| REQ-MAINT-000-013 | Maintenance ist uebergeordnete Ecosystem-Governance-Capability, wiederverwendbar ausserhalb KAI-OS (P10) | MUST |
| REQ-MAINT-000-014 | P0-Standards werden vor P1/P2 implementiert (Prioritaeten SCR-0120 v3) | MUST |

## Implementierungsstatus (ehrlich, SCR-0080-Doktrin)

**SPECIFICATION_ONLY (Conformance-Struktur angelegt).** Die machine-readable Struktur (§12:
schemas, registry/standards/, Conformance-Workflow) ist in diesem PR angelegt; Readiness-Gate,
Maintenance Engine, Evidence-Records und MAINTENANCE.md-Rollout in den Produktiv-Repos sind
NICHT implementiert. CLAIMED != PASS.

## Compliance

Kernprofil: ATC-STD-000, ATC-STD-201/202/203, ATC-STD-ENG-001. Parent der Querschnittfamilie;
REPO-MAINT-001/UPDATE-001/COMPAT-001/BUG/ERR bleiben SSOT ihrer Durchfuehrungsdomaenen.
