# Owner Decision Package — SCR-0095, SCR-0096, SCR-0139
Date: 2026-10-31
Repository: A-TownChain-Okosystems/atc-standards
Target: PR #120 — [Draft][SCR-0142] SCR registry implementation
Branch: governance/scr-registry-0142
Baseline PR head before this package: 0aa9472414c41a285b4a8f309bdf4ac250619c75
Base main: af98f5e3766db99f33497c1044b0521dea8c7593

## 0. Decision status and guardrails

This package records the available evidence and possible formal dispositions. A new Owner decision is not a prerequisite for technical evidence reconciliation, source mapping, or non-normative engineering improvements. This package does not itself record an Owner decision, allocate or reassign an SCR identifier, or modify normative standard metadata.

Evidence state for all three cases: historical scope/lifecycle remains unresolved. Technical reconciliation may continue; formal allocation, normative force, and SCR lifecycle remain unchanged until separately evidenced.

No SCR identity is marked ACCEPTED, CLOSED, REJECTED, SUPERSEDED, OBSOLETE, or FREE by this package. No ID is auto-allocated or recycled. No change-request file is fabricated. No normative flag or standard status is changed. PR #120 remains Draft; no merge is requested or performed.

This package supplements and refines the initial P1-A6 evidence inventory. In particular, the historical evidence shows multiple work items associated with SCR-0095 and SCR-0096. The evidence alone does not determine whether each identifier was intentionally used as an umbrella change request, whether one reference is erroneous, or whether the work should have been split. Do not treat the initial shorthand label "conflict" as an adjudicated outcome.

## 1. SCR-0095 — repository-file sweep vs Automated Repository Assurance

### 1.1 Evidence A — repository-file sweep / Hub PR #8

Source: A-TownChain-Okosystems/a-townchain-os-docs/REALITY_STATUS.md, commit 77ed5ed14cbed7375346211c2c9faa1a7299aa11, sections 39–40.

- Section 39 describes a 28-repository API tree scan and CONTRIBUTING.md additions in nine repositories.
- Section 40 records Hub PR #8 as SCR-0095, adding SECURITY.md, CONTRIBUTING.md, CODEOWNERS and STATUS.md to the .github Hub.
- GitHub PR: https://github.com/A-TownChain-Okosystems/.github/pull/8
- PR title: "SCR-0095: Hub-Artefakte ergaenzen (SECURITY/CONTRIBUTING/CODEOWNERS/STATUS)".
- PR state: closed; merged=true.
- PR head: 428c94891e63b1493dac3f588af17571340e27f8.
- Merge commit: caefa8c7315daceecb4ec8d02c47eb4df78e4027.
- PR body says the Owner approval was required because the Hub is PR-gated. The merge is proven; the exact human reviewer/approval identity should be verified from the PR review record if it is to be used as Owner-approval evidence.

### 1.2 Evidence B — Automated Repository Assurance

Source: A-TownChain-Okosystems/atc-standards commit 3eba30ef3253205de24e617389018b954672ee4e.

- Commit subject: "feat(SCR-0095): Automated Assurance — ATC-STD-030..043 (12 Standards) + GATE-SEC-001-Erweiterung".
- Commit message describes an Automated Repository Assurance system, including ATC-STD-030..039, ATC-STD-041 and ATC-STD-043, plus ATC-GATE-SEC-001.
- Commit signature verification: verified=false, reason=unsigned.
- ATC-STD-041 current document identifies Automated Assurance and SCR-0095 in its heading/changelog mapping.
- The commit's existence and content establish a historical reference, not cryptographic Owner attestation.

### 1.3 Related Owner approval evidence — bounded, not a SCR lifecycle decision

Source: atc-standards/approval/APPROVAL-DECISION-2026-09-11-001-Legacy-Restaurierung-25.md.

The approval record states that the Owner approved and put into effect 25 CANDIDATE standards from SCR-0093..0099 waves. Its explicit list includes ATC-STD-041 and ATC-STD-002, among other standards.

This is meaningful Owner approval evidence for the listed standards. It does not independently resolve whether the Hub-file sweep and Automated Assurance were:
- two work packages under one umbrella SCR-0095;
- separate changes incorrectly carrying the same SCR identity; or
- one canonical SCR with an ancillary implementation activity.

The approval record must not be stretched into a blanket closure decision for SCR-0095 itself.

### 1.4 Conflict / decision required

The source record associates SCR-0095 with at least two distinct work scopes:
A. repository-file/Hub artifact completion; and
B. Automated Repository Assurance / standards and gate changes.

Possible formal dispositions, only if a future lifecycle or allocation change is required:

- [ ] D1 — One umbrella SCR-0095 intentionally covered both scopes. Confirm the authoritative title, scope, acceptance criteria, and evidence set.
- [ ] D2 — SCR-0095 belongs to only one scope. Identify the authoritative scope and explicitly classify the other historical reference as misattributed; do not silently rewrite history.
- [ ] D3 — The work should have been split into separate SCRs. Owner must identify the historically valid identity for each part and authorize any required registry correction through the formal allocation process. The agent must not invent a new identifier.
- [ ] D4 — Other disposition, described by Owner: ______________________________

The PR review record is now directly verified: review ID 5178534325 is APPROVED by GitHub account A-TownChain; PR #8 was merged by that account, with signed merge commit caefa8c7315daceecb4ec8d02c47eb4df78e4027. This establishes implementation and review events for the Hub-file scope. It does not automatically close SCR-0095.

### 1.5 Owner decision record — intentionally blank

- Decision: ______________________________
- Canonical SCR-0095 title and scope: ______________________________
- Disposition of secondary scope: ______________________________
- Owner identity (human): ______________________________
- Decision timestamp (UTC): ______________________________
- Approval record / PR review / signed decision reference: ______________________________
- Lifecycle state authorized: ______________________________
- Conditions / residuals: ______________________________

Technical source mapping may proceed. SCR-0095 allocation remains UNRESOLVED; lifecycle and decision remain UNKNOWN.

## 2. SCR-0096 — scanner badge correction vs Standards Family ID architecture

### 2.1 Evidence A — scanner badge correction

Source: A-TownChain-Okosystems/a-townchain-os-docs/REALITY_STATUS.md, commit 77ed5ed14cbed7375346211c2c9faa1a7299aa11, section 41.

- The hardened organization compliance scanner reported atc-standards Badge=False.
- The documented fix added an ATC-COMPLIANCE badge as a generated template element.
- The source explicitly labels this fix SCR-0096.
- It reports the post-fix cross-registry test/validator as compliant and the follow-up sweep as 25/25 compliant.
- This is a historical implementation narrative; it is not a standalone SCR decision record.

### 2.2 Evidence B — Standards Family ID & Artifact Identifier Architecture

Source: atc-standards commit ea9050a39570deab79cd8eeac46d419a4abb80ec.

- Commit subject: "feat(SCR-0096): ATC-STD-002 Owner-Haertung + Registry-Architektur families/ + standards/".
- It describes numeric standards-family ranges, immutable IDs, no recycling, artifact identifier classes, traceability and registry architecture.
- Commit signature verification: verified=false, reason=unsigned.

Related commit: 49beb5c825876c01f8c69247b6e1c236a49cab15, also titled as SCR-0096 and describing ATC-STD-002 and ATC-STD-000 v1.3.0 changes. GitHub reports the commit as unsigned.

Current standard source: governance/ATC-STD-002.md.
- Current frontmatter: status=approved, normative=true.
- The document maps the family architecture to SCR-0096.
- The document describes family namespace reservations and the no-recycling rule.

### 2.3 Related Owner approval evidence — ATC-STD-002

Source: approval/APPROVAL-DECISION-2026-09-11-001-Legacy-Restaurierung-25.md.

The explicit 25-standard Owner approval list includes ATC-STD-002. This is bounded Owner approval evidence for ATC-STD-002 as a standard. It does not decide whether the scanner badge correction was:
- a separate subtask within SCR-0096;
- an unrelated change incorrectly labeled SCR-0096; or
- a valid umbrella scope of the same SCR.

### 2.4 Conflict / decision required

The source record associates SCR-0096 with two materially different scopes:
A. compliance scanner badge/template correction; and
B. Standards Family ID / Artifact Identifier Architecture (ATC-STD-002).

Owner must select and document one disposition:

- [ ] D1 — One umbrella SCR-0096 intentionally covered both scopes. Confirm title, scope, acceptance criteria, and evidence set.
- [ ] D2 — SCR-0096 belongs only to one scope. Identify the canonical scope and explicitly classify the other reference as misattributed.
- [ ] D3 — The work should have been split. Owner must identify the historical allocation and authorize any registry correction through the formal allocation process. No identifier may be invented by the agent.
- [ ] D4 — Other disposition, described by Owner: ______________________________

Owner must confirm whether ATC-STD-002's approval under SCR-0102 is the controlling approval for the standard, while SCR-0096 remains the originating change request, or provide a different authoritative chain.

### 2.5 Owner decision record — intentionally blank

- Decision: ______________________________
- Canonical SCR-0096 title and scope: ______________________________
- Disposition of secondary scope: ______________________________
- Relationship between SCR-0096 and SCR-0102 approval: ______________________________
- Owner identity (human): ______________________________
- Decision timestamp (UTC): ______________________________
- Approval record / signed decision reference: ______________________________
- Lifecycle state authorized: ______________________________
- Conditions / residuals: ______________________________

Technical source mapping may proceed. SCR-0096 allocation remains UNRESOLVED; lifecycle and decision remain UNKNOWN.

## 3. SCR-0139 — status=approved while normative=false

### 3.1 Evidence

Source: standards/ai-gov/ATC-AI-GOV-AUTH-001.md (current main).

Frontmatter:
- id: ATC-AI-GOV-AUTH-001
- version: 1.0.0
- status: approved
- owner: "Michael (Owner-Spezifikation 07.10.)"
- normative: false
- created/updated: 2026-10-07

Document heading/body:
- Describes the document as "APPROVED".
- Calls it an Owner specification dated 07.10.2026.
- Describes a technical authorization/automation order and explicitly distinguishes it from a classical personal power of attorney.
- Maps the document to SCR-0139 and references a machine-readable implementation hub.

Historical source commit:
- bceec03d7acd5bbaad42da10bbc2c75affd39f2f.
- Commit message identifies a SCR-0139 naming-conformance change and references the generator/registry chain.
- GitHub signature verification: verified=false, reason=unsigned.
- The commit proves a source revision and SCR reference, not a signed Owner decision establishing normative status.

No canonical standalone change-request file change-requests/SCR-0139.md was found on the reviewed main branch. No separate signed approval artifact specifically deciding the normative force of SCR-0139 was identified in the reviewed evidence set.

### 3.2 Exact semantic issue

The fields may represent different dimensions:
- status=approved may mean editorial/Owner acceptance of the specification;
- normative=false means the document is not currently an enforceable normative standard.

That interpretation is plausible but is not assumed to be true without Owner confirmation. Conversely, changing normative to true based only on the word APPROVED would be unsafe.

### 3.3 Evidence-led technical interpretation and optional formal dispositions

Owner must select and document one disposition:

- [ ] D1 — APPROVED + normative=false is intentional. Confirm that "approved" means accepted as a non-normative Owner specification, identify its intended authority, and confirm which normative standards/gates remain controlling.
- [ ] D2 — The document is intended to be normative. Identify the governing approval record, effective date, scope, and required normative change process. No metadata change is made by this package.
- [ ] D3 — "approved" is an incorrect lifecycle label. Specify the correct status (e.g. candidate/draft) and the evidence required for a later approval.
- [ ] D4 — Other disposition, described by Owner: ______________________________

The current fields can be read consistently without changing them: `status: approved` describes the document's editorial/acceptance state, while `normative: false` means it is not an enforceable normative standard. This is the recommended technical interpretation, not a new formal lifecycle decision. Standard status and SCR lifecycle remain separate.

### 3.4 Owner decision record — intentionally blank

- Decision: ______________________________
- Meaning of status=approved: ______________________________
- Intended normative force: ______________________________
- Governing approval / ADR / decision reference: ______________________________
- Effective date (if applicable): ______________________________
- Controlling standards/gates during transition: ______________________________
- SCR-0139 lifecycle state: ______________________________
- Owner identity (human): ______________________________
- Decision timestamp (UTC): ______________________________
- Conditions / residuals: ______________________________

Technical use of the existing non-normative specification and its machine-readable configuration may continue within existing authority boundaries. SCR-0139 lifecycle remains UNKNOWN.

## 4. Cross-case decision protocol

For each case, the Owner decision must:
1. Identify the exact SCR identity and authoritative scope.
2. Identify source files, repositories, immutable commit SHAs, PRs, and relevant review/approval records.
3. Distinguish implementation evidence from Owner authorization and normative approval.
4. State the SCR lifecycle decision independently from the lifecycle/normativity of any standard.
5. Identify supersession, split, grouping, or misattribution explicitly; no silent history rewrite.
6. State effective date and residual conditions where applicable.
7. Be preserved as a human-authored approval record with traceable identity and timestamp.

The agent may update technical source mappings when the source evidence is directly verified and the change does not assert new allocation, Owner authority, normative force, acceptance/rejection, supersession, or closure. Those formal state transitions require attributable authorization. Every registry change must preserve original evidence and pass relevant positive/negative tests and CI gates.

## 5. Current disposition

| Identity | Source evidence | Conflict status | Owner decision | Registry action |
|---|---|---|---|---|
| SCR-0095 | REALITY_STATUS §§39–40; approved/merged .github PR #8; signed merge commit; unsigned Automated Assurance commit; ATC-STD-041; bounded SCR-0102 approval context | Two work scopes; ATC-STD-041 effectiveness conflict | Not required for technical mapping | Preserve separate evidence relationships; no lifecycle change |
| SCR-0096 | REALITY_STATUS §41; two unsigned ATC-STD-002 architecture commits; bounded SCR-0102 approval context | Badge correction and family architecture remain distinct scopes | Not required for technical mapping | Preserve separate evidence relationships; no lifecycle change |
| SCR-0139 | ATC-AI-GOV-AUTH-001; unsigned machine-readable config and naming commits | approved + normative=false is technically coherent; SCR lifecycle not evidenced | Not required for technical mapping | Preserve normative=false; lifecycle UNKNOWN |

No formal lifecycle decision is made by this report. The three entries remain unresolved in allocation/lifecycle fields, while technical evidence mapping and non-normative improvements can proceed independently.



## Technical evidence update — 2026-10-31

The registry now contains multiple typed evidence relationships for SCR-0095, SCR-0096 and SCR-0139. This materially improves the decision basis and means further technical analysis does not need to wait for an Owner decision.

The new evidence map distinguishes:
- SCR-0095: Automated Assurance source commit; merged .github PR #8 for Hub repository files; signed REALITY_STATUS corroboration; bounded approval context for ATC-STD-041; and the ATC-STD-041 frontmatter/body effectiveness conflict.
- SCR-0096: scanner badge correction documented in signed REALITY_STATUS §41; two unsigned commits describing ATC-STD-002 family architecture; bounded approval context for ATC-STD-002.
- SCR-0139: Automation Authority standard; machine-readable .github configuration commit; naming/generator provenance commit; approved-versus-normative=false distinction.

These evidence relationships do not predetermine the Owner's final lifecycle or scope decision. They also do not create a blanket Owner dependency for technical work. The registry continues to preserve UNKNOWN lifecycle and decision values and UNRESOLVED allocation status. No identifier was allocated, no standard status was modified, and no SCR was closed or rejected.

The prior decision options remain available as one possible governance resolution, but they are not prerequisites for continued evidence reconciliation, technical recommendations or non-normative improvements. Any eventual formal lifecycle, allocation, normative or supersession change must still be supported by attributable evidence and the applicable authorization.


## 6. Evidence-led recommended dispositions — 2026-10-31

These are technical recommendations, not Owner decisions and not SCR lifecycle transitions.

### SCR-0095
- Preserve the Hub-file sweep and Automated Repository Assurance as two separately typed historical work scopes under the existing SCR-0095 identity.
- Treat PR #8 as verified implementation evidence for the Hub-file scope: review ID `5178534325` is APPROVED by GitHub account `A-TownChain`; the PR merged at `2026-09-11T12:27:40Z`; merge commit `caefa8c7315daceecb4ec8d02c47eb4df78e4027` has a valid GitHub signature.
- Do not infer SCR closure from the PR merge. Keep Automated Assurance commit `3eba30e...` classified as unsigned historical provenance.
- Preserve the ATC-STD-041 status/effectiveness discrepancy: frontmatter `approved` / `normative: true` / `effective_date: null`, while the body says it is not effective until §9 release.

### SCR-0096
- Preserve scanner badge correction and Standards Family ID architecture as separate evidence scopes.
- Keep the two ATC-STD-002 architecture commits explicitly unsigned; the approval record's inclusion of ATC-STD-002 is bounded standard-approval context, not SCR-0096 lifecycle closure.
- Do not split or reallocate the historical identity without direct allocation evidence.

### SCR-0139
- Preserve `status: approved` and `normative: false` as separate dimensions. Recommended reading: accepted specification document, not an enforceable normative standard.
- Continue technical use of the machine-readable configuration only within already-established authority and security boundaries.
- Do not promote normative status or close SCR-0139 based on unsigned commits or the document heading.

### Common disposition
- Keep `allocation_status: UNRESOLVED`, `lifecycle_status: UNKNOWN`, and `decision: UNKNOWN` where the historical allocation/lifecycle is not proven.
- Do not let the absence of those formal decisions block source reconciliation, evidence-quality improvements, tests, or non-normative technical work.
- Revisit formal status only if new attributable evidence or a concrete product/governance need warrants it.
