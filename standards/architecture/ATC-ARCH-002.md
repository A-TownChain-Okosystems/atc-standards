---
standard:
  id: ATC-ARCH-002
  title: "KAI-OS Desktop Layer Architecture Standard"
  version: "0.1.1"
  status: draft
  category: architecture
  authority: "A-TownChain Ecosystems"
  owner: "Michael Wroblewski (Owner-Auftrag) / Standards Governance"
  created: "2026-11-17"
  updated: "2026-11-17"
  normative: false
  applies_to: "Desktop-Schicht des KAI-OS-Stacks; alle Repositories, die Desktop-, Sitzungs-, Anwendungs- oder Paketdienste beitragen"
  mandate: "Owner-Auftrag 17.11.2026 (Desktop-Zielbild, Windows-vergleichbare Bedienung bei eigener Architektur)"
  related: [ATC-ARCH-001, ATC-STD-000, ATC-STD-DESC-001, AD-008, KAI-CORE-RUNTIME-001]
  effective_date: null
  review_date: "2027-01-31"
  dependencies: [ATC-ARCH-001, ATC-STD-000, ATC-STD-DESC-001]
  requirements: [REQ-ARCH-201, REQ-ARCH-232]
  changelog: "0.1.0 (2026-11-17): Erster Entwurf nach Owner-Auftrag; DRAFT, nicht normativ. 0.1.1 (2026-11-17): DEC-1 als Begriffsordnung und DEC-2 als Anwendungsdomaene aufgenommen; weiterhin DRAFT."
---

# ATC-ARCH-002 — KAI-OS Desktop Layer Architecture Standard (v0.1.1, DRAFT)

> **Status:** DRAFT. Nicht normativ, nicht referenzierbar, nicht in der Registry
> als `approved` geführt. Verbindlichkeit entsteht ausschließlich durch
> Owner-Genehmigung nach ATC-STD-000 §9 (siehe SCR-0142).
> **Governance:** ATC-STD-000. **Struktur:** ATC-STD-DESC-001 §5.

## 1. Zweck

Dieser Standard legt fest, wie die benutzerseitige Desktop-Schicht des
KAI-OS-Stacks aufgebaut wird, damit ein Anwender das System ohne Kenntnisse
über Blockchain, Kernel oder KI bedienen kann: einschalten, anmelden,
Programme öffnen, im Netz arbeiten, Dateien verwalten, Anwendungen
installieren.

Der Zweck ist die **Einmaligkeit der Umsetzung**. Der Desktop ist der Ort, an
dem erfahrungsgemäß die meisten Parallelentwicklungen entstehen: zwei
Compositoren, zwei Rechtesysteme, zwei Paketmanager. Dieser Standard verhindert
das, bevor gebaut wird, nicht nachträglich.

## 2. Geltungsbereich

**Gilt für:**
- alle Komponenten, die dem Nutzer eine Oberfläche, Sitzung, Anwendungsausführung,
  Paketinstallation oder Wiederherstellung anbieten,
- alle Repositories, die solche Komponenten beitragen oder ihre Schnittstellen
  definieren,
- die Festlegung, wo eine neue Desktop-Funktion implementiert werden darf.

**Gilt nicht für:**
- Kernel-, Speicher-, Treiber- und Rechteverwaltung selbst (ATC-ARCH-001,
  GlobusOS, ShivaCore),
- Konsens-, VM- und Identitätssemantik (A-TownChain, ATC-VM, AD-008),
- die Frage, welche Produkte vermarktet werden. Naming ist eine
  Produktentscheidung, nicht Architektur (siehe § 5, DEC-1).

### 2.1 Einordnung in ATC-ARCH-001 (verbindliche Klarstellung)

ATC-ARCH-001 ist die einzige normative Architekturquelle. Dort gilt: KAI-OS ist
der **Architekturbegriff**, GlobusOS ist **das Betriebssystem**, ShivaCore ist
**der Kernel**. Daraus folgt für diesen Standard:

- Die Desktop-Schicht ist ein **Profil von GlobusOS**, kein eigenes
  Betriebssystem und kein eigenes System-Repository.
- Ein Produktname für den ausgelieferten Desktop (etwa „KAI-OS Desktop
  Edition") ist zulässig, solange er als Profil eines GlobusOS-Systems
  ausgeliefert und dokumentiert wird.
- Es entsteht **keine zweite Kernel-, VM- oder Rechteimplementierung**.

## 3. Begriffe und Definitionen

| Begriff | Definition |
|---|---|
| Desktop-Schicht | Gesamtheit der Dienste und Oberflächen zwischen Kernel/ShivaCore und Anwendung |
| Profil | Auslieferungsvariante von GlobusOS mit festgelegter Dienst- und Paketauswahl |
| D0 Display | Compositor und Display-Protokoll; alleiniger Inhaber des Ausgabegraphen |
| D1 Session | Anmeldung, Sitzungsidentität, Sitzungswechsel, Sperren |
| D2 Shell | Desktop, Startmenü, Taskleiste, Benachrichtigungen, Einstellungen, Shortcut-Register |
| D3 Storage UX | Dateiverwaltung, Datenträger, verschlüsselte Bereiche, Papierkorb, Suche |
| D4 Runtime | Anwendungsausführung, Sandbox, Capability-Vermittlung |
| D5 Pakete | Installation, Signaturprüfung, Aktualisierung, Rücknahme |
| D6 Kompatibilität | isolierte Fremdausführung (Linux, Web); keine Rechteausweitung |
| D7 Assistenz | lokale KI-Oberfläche (Aurora), Sprach- und Automatisierungszugang |
| Capability | nicht fälschbares Rechtetoken, ausgestellt durch ShivaCore |
| Portal | vermittelter Zugriff auf Datei, Bildschirm, Zwischenablage, Mikrofon, Standort, Kamera |
| Authority-SSOT | alleinige Quelle für Rechteentscheidungen: ShivaCore |
| Conformance-Nachweis | prüfbarer Beleg, dass eine Komponente die COM-Kriterien erfüllt |


### 3.1 Verbindliche Begriffsordnung (DEC-1, entschieden am 17.11.2026)

Die folgende Zuordnung ist verbindlich. Sie bildet die Regelung aus
ATC-ARCH-001 ab und aendert sie nicht.

| Begriff | Rolle in der Architektur | Regel |
|---|---|---|
| KAI | fuehrende Bezeichnung der Gesamtarchitektur | BEG-1 |
| KAI-OS | gueltiger Alias derselben Gesamtarchitektur | BEG-2 |
| GlobusOS | das einzige Betriebssystem innerhalb der Architektur | BEG-3 |
| ShivaCore | der einzige Kernel | BEG-4 |
| ATC-VM | die virtuelle Maschine | BEG-5 |
| A-TownChain | die Blockchain | BEG-6 |

**BEG-1** — KAI MUSS als fuehrende Bezeichnung der Gesamtarchitektur verwendet
werden.

**BEG-2** — KAI-OS ist ein gueltiger Alias derselben Gesamtarchitektur. KAI-OS
DARF NICHT als eigenstaendiges Betriebssystem neben GlobusOS definiert werden;
eine solche Definition widerspricht ATC-ARCH-001.

**BEG-3** — GlobusOS ist das einzige Betriebssystem innerhalb der Architektur.
Ein zweites Betriebssystem DARF NICHT entstehen, auch nicht unter dem Namen
KAI-OS.

**BEG-4** — ShivaCore ist der einzige Kernel. Ein zweiter Kernel DARF NICHT
entstehen.

**BEG-5** — ATC-VM ist die virtuelle Maschine der Architektur. Eine zweite
VM-Implementierung DARF NICHT entstehen.

**BEG-6** — A-TownChain ist die Blockchain der Architektur.

Die Begriffsordnung gilt fuer alle Standards, Dokumente und Repository-Texte.
Sie entfaltet keine normative Wirkung, solange dieser Standard den Status DRAFT
hat.

## 4. Normative Anforderungen

Legende: MUSS = verpflichtend, DARF NICHT = verboten, SOLLTE = begründet abweichbar.

### 4.1 Einmaligkeit und Einordnung

**REQ-ARCH-201** — Die Desktop-Schicht MUSS als Profil von GlobusOS
ausgeliefert werden. Ein eigenständiges Betriebssystem oder ein eigener
Kernel-Derivat für den Desktop DARF NICHT entstehen.

**REQ-ARCH-202** — Je Desktop-Komponente DARF es genau eine produktive
Implementierung geben. Die Zuordnung in § 7 ist verbindlich; ein zweites
Produkt mit gleicher Funktion DARF NICHT parallel betrieben werden.

**REQ-ARCH-203** — Eine neue Desktop-Funktion MUSS im zugeordneten Repository
implementiert werden. Existiert keine Zuordnung, ist sie vor der Umsetzung per
SCR zu klären.

**REQ-ARCH-204** — Desktop-Komponenten DÜRFEN keine Konsens-, VM- oder
Kernel-Semantik definieren (AD-008). Sie konsumieren diese ausschließlich über
Schnittstellen.

### 4.2 Schichten und Abhängigkeiten

**REQ-ARCH-205** — Die Schichten D0 bis D7 MÜSSEN eingehalten werden.
Abhängigkeiten dürfen ausschließlich abwärts verlaufen (D7 → D0). Eine
Aufwärtsabhängigkeit, etwa Shell → Runtime, ist unzulässig; gemeinsame
Funktionen gehören in die untere Schicht.

**REQ-ARCH-206** — Jede Komponente MUSS ihre Abhängigkeiten deklarieren
(Modul- und Prozessgrenzen) und ohne optionale Nachbarkomponenten startfähig
sein.

**REQ-ARCH-207** — Der Compositor (D0) ist alleiniger Inhaber des
Display-Graphen. Anwendungen DÜRFEN NICHT direkt auf Scanout, Framebuffer oder
GPU-Kontext zugreifen; sie liefern Puffer an D0.

**REQ-ARCH-208** — Der Input-Dienst MUSS alle Eingaben vermitteln. Anwendungen
DÜRFEN NICHT auf Rohgeräte für Tastatur, Maus oder Touch zugreifen. Globale
Tastenkürzel werden zentral beim Shell-Dienst registriert.

**REQ-ARCH-209** — Der Sitzungsdienst (D1) ist alleinige Quelle der
Sitzungsidentität. Ein Sitzungswechsel oder Sperren MUSS alle
Capability-Tokens der Sitzung ungültig machen.

**REQ-ARCH-210** — Der Sitzungsdienst MUSS mindestens zwei Anmeldewege
unterstützen: lokales Konto und dezentrale Identität (DID/Wallet). Beide Wege
MÜSSEN ohne Netzverbindung funktionieren, sofern die Identität lokal vorliegt.

### 4.3 Schnittstellen und IPC

**REQ-ARCH-211** — Jede IPC-Schnittstelle MUSS ein versioniertes Schema
besitzen mit: `schema_id`, `version` (SemVer), erforderliche Capability,
Fehlerklassifikation und Audit-Ereignis. Ein Schema ohne Capability-Bezug ist
unzulässig.

**REQ-ARCH-212** — Inkompatible Schemaänderungen MÜSSEN eine neue
Major-Version erhalten und ein Migrationsfenster benennen.

**REQ-ARCH-213** — Zugriff gilt als verboten, solange er nicht ausdrücklich
erlaubt ist (Default Deny). Jede Nachricht MUSS einer Capability zugeordnet
sein.

**REQ-ARCH-214** — Sensible Ressourcen (Dateien, Bildschirm, Zwischenablage,
Mikrofon, Kamera, Standort) MÜSSEN über Portale vermittelt werden. Stille
Berechtigungen sind unzulässig; die Nutzerentscheidung MUSS sichtbar und
widerrufbar sein.

**REQ-ARCH-215** — Rechteentscheidungen trifft ShivaCore. Die Desktop-Schicht
DARF keinen eigenen Rechtespeicher und keine parallele Policy-Engine führen.

### 4.4 Sandbox und Sicherheit

**REQ-ARCH-216** — Jede Anwendung MUSS in einer eigenen Sandbox mit minimalem
Capability-Set laufen. Eine Anwendung DARF NICHT Rechte einer anderen erben.

**REQ-ARCH-217** — Die Installation von Anwendungen und Updates MUSS
signaturgeprüft erfolgen. Bei Prüf- oder Kettenfehler gilt Fail-Closed.

**REQ-ARCH-218** — Schlüssel DÜRFEN die Keyring-Grenze NICHT verlassen. Kein
Desktop-Dienst und keine Anwendung hält private Schlüssel im eigenen
Prozessspeicher.

**REQ-ARCH-219** — Jede sicherheitsrelevante Nutzerentscheidung (Installation,
Rechteerteilung, Update, Wiederherstellung) MUSS auditierbar protokolliert
werden, mit Zeitpunkt, Subjekt, Objekt und Ergebnis.

### 4.5 Anwendungen und Kompatibilität

**REQ-ARCH-220** — Es werden drei Anwendungskategorien unterstützt:
native Anwendungen (Rust, mit nativer Integration), kompatible Anwendungen
über eine abgegrenzte Kompatibilitätsschicht, Web-Anwendungen über den
Browser. Windows-Kompatibilität ist nicht Teil dieser Architektur.

**REQ-ARCH-221** — Eine Kompatibilitätsschicht MUSS das Capability-Mapping
explizit deklarieren und DARF keine Kernel-Rechte erweitern. Sie ist
abschaltbar und darf den Systemstart nicht blockieren.

**REQ-ARCH-222** — Der Browser ist eine Sandbox-Anwendung wie jede andere. Er
DARF keine Sonderrechte auf Dateisystem oder Prozessraum erhalten.

### 4.6 Pakete, Updates, Wiederherstellung

**REQ-ARCH-223** — Installation, Aktualisierung und Rücknahme MÜSSEN über einen
Paketdienst mit signierten Manifesten laufen. Direkte Manipulation des
Systembaums durch Anwendungen ist unzulässig.

**REQ-ARCH-224** — Updates MÜSSEN atomar sein und auf die vorherige Generation
zurückrollen können. Ein fehlgeschlagenes Update DARF das System nicht
unstartbar machen.

**REQ-ARCH-225** — Wiederherstellung MUSS ohne Netzverbindung möglich sein. Ein
Werksprofil MUSS getrennt von Nutzdaten wiederherstellbar sein.

**REQ-ARCH-226** — Ausgelieferte Desktop-Binaries MÜSSEN reproduzierbar baubar
sein, mit nachweisbarer Übereinstimmung zwischen Quelle, Build und Auslieferung.

### 4.7 Bedienbarkeit und Assistenz

**REQ-ARCH-227** — Ein Anwender MUSS ohne Fachkenntnis über Blockchain, Kernel
oder KI alle Grundaufgaben erledigen können. Keine Kernaufgabe darf eine
Kenntnis dieser Schichten voraussetzen.

**REQ-ARCH-228** — Barrierefreiheit MUSS als Systemdienst bereitstehen
(Bildschirmausgabe, Skalierung, Kontrast, Tastaturnavigation) und von jeder
Shell-Komponente genutzt werden.

**REQ-ARCH-229** — Alle sichtbaren Texte MÜSSEN aus Ressourcen stammen.
Hartkodierte Nutzertexte sind unzulässig.

**REQ-ARCH-230** — Die KI-Assistenz ist Dienst, nicht Rechteinhaber. Sie handelt
ausschließlich über Portale und Capabilities, und jede von ihr ausgelöste
Aktion MUSS auditierbar sein.

**REQ-ARCH-231** — Telemetrie ist standardmäßig aus, lokal zuerst, und nur mit
nachvollziehbarer Zustimmung aktiv.

**REQ-ARCH-232** — Kein Statuswechsel einer Desktop-Komponente auf ACTIVE ohne
vollständigen Conformance-Nachweis nach § 8.

## 5. Rollen und Verantwortlichkeiten

| Rolle | Träger | Verantwortung |
|---|---|---|
| Owner | Michael Wroblewski | Genehmigung, Naming (DEC-1), Kompatibilitätsumfang (DEC-3) |
| Standards Authority | atc-standards | Pflege dieses Standards, SCR-Verfahren |
| Architecture Reviewer | ArchitectAgent | Prüfung gegen ATC-ARCH-001 und AD-008 |
| Component Owner | je Repository (siehe § 7) | Umsetzung, Conformance-Nachweis |
| Security Authority | ShivaCore | Rechteentscheidungen, Sandbox-Policy |
| Auditor | GovernanceAgent | Prüfung der COM-Kriterien, Evidenz |

## 6. Prozesse und Verfahren

1. **Neue Desktop-Funktion:** Zuordnung nach § 7 prüfen, bei Lücke SCR
   anlegen, erst danach implementieren.
2. **Neue Komponente:** Schema, Capability-Bedarf, Fehlerklassen und
   Audit-Ereignisse vor dem ersten Commit festlegen.
3. **Schnittstellenänderung:** Major-Version bei Inkompatibilität, Ankündigung,
   Migrationsfenster.
4. **Freigabe:** Statuswechsel nur über § 8, mit Evidenz im Standard-Repository.
5. **Konfliktfall:** Bei zwei Implementierungen derselben Funktion entscheidet
   der Owner; die nicht gewählte wird stillgelegt, nicht geduldet.

## 7. Schnittstellen, Abhängigkeiten und Zuordnung

| Schicht | Komponente | Verantwortliches Repository | Status |
|---|---|---|---|
| D0 | Compositor, Display-Protokoll | globus-os | geplant |
| D0 | Grafiktreiber, GPU-Speicher | globus-os | teilweise vorhanden |
| D1 | Session, Login, Sperren | globus-os | geplant |
| D1 | Identität, DID, Wallet-Anbindung | a-townchain | teilweise vorhanden |
| D2 | Shell: Desktop, Startmenü, Taskleiste, Benachrichtigungen | globus-os | geplant |
| D2 | Einstellungen | globus-os | geplant |
| D3 | Dateiverwaltung, Datenträger, Suche | globus-os | teilweise vorhanden (VFS) |
| D3 | Verschlüsselte Bereiche | atc-shivacore, globus-os | geplant |
| D4 | Runtime und Sandbox | globus-os | teilweise vorhanden (service_space) |
| D4 | Rechtevermittlung | atc-shivacore | vorhanden (Authority-SSOT) |
| D5 | Paketdienst, Signaturen, Rollback | globus-os, atcpkg | geplant |
| D5 | Marktplatz-Oberfläche | atc-marketplace | geplant |
| D6 | Linux-Kompatibilität | noch offen (DEC-3) | nicht entschieden |
| D6 | Browser (Web) | globus-os | geplant |
| D7 | Lokale KI-Oberfläche | aurora-ai | teilweise vorhanden |
| alle | Normative Vorgaben | atc-standards | vorhanden |

Der Browser ist gemäß REQ-ARCH-222 eine gewöhnliche Sandbox-Anwendung. Ein
Produktname für ihn ist frei, begründet aber keine Sonderrechte.


### 7.1 Anwendungsdomaene Genesis Engine (DEC-2, entschieden am 17.11.2026)

Genesis Engine ist eine **Anwendungsdomaene** und eine eigenstaendige
KAI-Technologiedomaene. Verbindlich gilt:

**ZUO-1** — Genesis Engine ist keine Unterkomponente von GlobusOS. Die
Klassifikation als Anwendungsdomaene DARF keine hierarchische Unterordnung
innerhalb von GlobusOS erzeugen.

**ZUO-2** — Genesis Engine ist kein Bestandteil von Aurora AI.

**ZUO-3** — Genesis Engine ist keine Unterfunktion von ATC-VM oder
A-TownChain.

**ZUO-4** — Die Anwendungsdomaene umfasst KI-gestuetzte Spieleentwicklung,
Softwareprogrammierung und Entwicklungswerkzeuge.

Begruendung: Genesis Engine stellt Entwicklungs- und Anwendungsfunktionen
bereit, keine Betriebssystem-Systemdomaene wie Kernel, Speicherverwaltung oder
Treibersystem. Eine Systemdomaene waere eine siebte Kernkomponente und
widerspraeche ATC-ARCH-001.

## 8. Compliance und Pruefungen

| ID | Prüfkriterium | Methode |
|---|---|---|
| COM-ARCH-201 | Genau eine Implementierung je Komponente nach § 7 | Repo-Audit, Matrix |
| COM-ARCH-202 | Jede IPC-Schnittstelle hat Version, Capability und Audit-Ereignis | Schema-Validierung |
| COM-ARCH-203 | Kein Anwendungszugriff auf Rohgeräte, Scanout oder Fremdspeicher | Code- und Rechteaudit |
| COM-ARCH-204 | Keine Rechteentscheidung außerhalb ShivaCore | Policy-Audit |
| COM-ARCH-205 | Keine Konsens-, VM- oder Kernel-Semantik in Desktop-Komponenten | Architektur-Review gegen AD-008 |
| COM-ARCH-206 | Signaturprüfung vor Installation; Fail-Closed nachgewiesen | Negativtests |
| COM-ARCH-207 | Update-Rollback praktisch nachgewiesen | Wiederherstellungstest |
| COM-ARCH-208 | Reproduzierbarer Build mit Hash-Vergleich | Build-Evidenz |
| COM-ARCH-209 | Grundaufgaben ohne Fachkenntnis durchführbar | Usability-Testprotokoll |
| COM-ARCH-210 | Barrierefreiheitsdienst vorhanden und genutzt | Funktions- und Codeaudit |

Ein Statuswechsel auf ACTIVE setzt voraus, dass alle zehn Kriterien mit
gebundenem Commit und reproduzierbarem Nachweis belegt sind.

## 9. Ausnahmen

Ausnahmen MÜSSEN per SCR beantragt, begründet, befristet und mit
Auslaufdatum versehen werden. Unbefristete Ausnahmen sind unzulässig.
Ausnahmen von REQ-ARCH-201, 215 und 218 sind nicht möglich.

## 10. Versionierung

SemVer. 0.x gilt als Entwurf und ist nicht referenzierbar. 1.0.0 setzt
Owner-Genehmigung nach ATC-STD-000 §9 und vollständige COM-Evidenz für den
Freigabeumfang voraus.

## 11. Änderungsmanagement

Änderungen laufen über SCR. Bei Änderungen an § 2.1, § 4.1 oder § 8 ist ein
Architecture Review gegen ATC-ARCH-001 zwingend. Dieses Dokument darf nicht
dazu benutzt werden, ATC-ARCH-001 zu überschreiben.

## 12. Referenzen

**NORMATIVE**
- ATC-ARCH-001 — KAI-OS System Architecture Standard
- ATC-STD-000 — Standards Governance
- ATC-STD-DESC-001 — Standard Description Standard
- AD-008 — Language & Execution Boundary

**INFORMATIVE**
- KAI-CORE-RUNTIME-001 — Core Runtime Track
- SCR-0129 — Standalone First, Ecosystem Second (PROPOSED)
- SCR-0142 — Antrag zu diesem Standard (PROPOSED)

## 13. Changelog

| Version | Datum | Änderung |
|---|---|---|
| 0.1.0 | 2026-11-17 | Erster Entwurf nach Owner-Auftrag. DRAFT, nicht normativ. |
| 0.1.1 | 2026-11-17 | DEC-1 (Begriffsordnung, § 3.1) und DEC-2 (Anwendungsdomaene, § 7.1) nach Owner-Entscheidung aufgenommen. DRAFT bleibt bestehen; keine neue Standard-ID, keine Umbenennung, keine Aenderung der Architekturhierarchie. |

## 14. Offene Entscheidungen

### 14.1 Entschieden am 17.11.2026 (Owner)

| ID | Entscheidung | Verbindliche Fassung |
|---|---|---|
| DEC-1 | **Begriffstabelle** | KAI fuehrend, KAI-OS Alias derselben Gesamtarchitektur, GlobusOS einziges Betriebssystem, ShivaCore einziger Kernel, ATC-VM die VM, A-TownChain die Blockchain; normative Fassung in § 3.1. Status bleibt DRAFT bis zum regulaeren Freigabeverfahren. |
| DEC-2 | **Anwendungsdomaene** | Genesis Engine ist eigenstaendige KAI-Technologiedomaene, keine Unterkomponente von GlobusOS, kein Bestandteil von Aurora AI, keine Unterfunktion von ATC-VM oder A-TownChain; Umfang: KI-gestuetzte Spieleentwicklung, Softwareprogrammierung, Entwicklungswerkzeuge; normative Fassung in § 7.1. |

Beide Entscheidungen sind in den Entwurf uebernommen. Der Standard bleibt
`draft` und `normative: false`, bis das Freigabeverfahren nach ATC-STD-000
abgeschlossen ist.

### 14.2 Offen

| ID | Frage | Empfehlung | Blockiert |
|---|---|---|---|
| DEC-3 | Umfang der Linux-Kompatibilitätsschicht | Eng begrenzt, abschaltbar, kein Rechte-Mapping über Portale hinaus | D6 |
| DEC-4 | Update-Kanal und Vertrauenskette (eigene Signatur, DID-basiert, beides) | Beides, mit Offline-Verifikation | D5 |
