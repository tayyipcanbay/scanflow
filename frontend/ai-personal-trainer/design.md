# AI Personal Trainer – Mobile App Design

## Design-Philosophie

Die App folgt den **Apple Human Interface Guidelines** und orientiert sich an modernen iOS Health & Fitness Apps. Das Design ist für **mobile Portrait-Orientierung (9:16)** und **einhändige Bedienung** optimiert. Der Fokus liegt auf Klarheit, Motivation und datengestützter Transparenz.

## Zielgruppen

Die App richtet sich an zwei primäre Personas:

**Der ambitionierte Anfänger (Alex, 28)** ist ein Software-Entwickler, der nach einer längeren inaktiven Phase wieder fit werden möchte. Er sucht einen klaren, datengestützten Weg zu mehr Fitness und einem gesünderen Lebensstil. Seine größten Herausforderungen sind Unsicherheit bei der Übungsausführung, fehlendes Wissen über Trainingsplanung und die Angst vor Verletzungen. Die App bietet ihm strukturierte Pläne mit verständlichen Erklärungen und baut Vertrauen durch transparente AI-Empfehlungen auf.

**Die datengetriebene Optimiererin (Sarah, 35)** ist eine Marketing-Managerin, die bereits sportlich aktiv ist und ihre Leistung auf das nächste Level heben möchte. Sie liebt es, ihre Fortschritte zu tracken und zu analysieren. Ihre Herausforderungen sind Stagnation im Training und die Schwierigkeit, die letzten Prozent an Leistung herauszuholen. Die App bietet ihr präzise Körperdaten-Analysen und personalisierte Empfehlungen, die über allgemeine Ratschläge hinausgehen.

## Core User Journey

Die Nutzererfahrung gliedert sich in vier Hauptphasen:

**Onboarding:** Der Nutzer wird durch eine kurze, ansprechende Einführung in die App geführt. Die App erklärt die Vorteile der 3D-Bodyscan-Integration und fragt grundlegende Informationen ab (Fitnessziele, Erfahrungslevel, Präferenzen). Der Nutzer erhält eine Anleitung zur Verbindung mit dem 3D-Bodyscanner im Fitnessstudio.

**Erster Bodyscan & Datenupload:** Nach dem ersten Scan im Fitnessstudio ermöglicht die App den Upload des PDF-Berichts. Die KI extrahiert automatisch die relevanten Körperdaten (Gewicht, Körperfettanteil, Muskelmasse, Körpermaße) und analysiert diese.

**Generierung des KI-Plans:** Basierend auf den Scandaten und den Nutzerzielen erstellt die KI einen personalisierten Trainings- und Ernährungsplan. Jede Empfehlung wird mit einer verständlichen Begründung versehen, um Vertrauen aufzubauen.

**Laufendes Tracking & Anpassung:** Der Nutzer trackt seine Trainingseinheiten und Mahlzeiten in der App. Regelmäßige Re-Scans (alle 4-6 Wochen) aktualisieren die Körperdaten, und die KI passt den Plan kontinuierlich an die Fortschritte an.

## Screen-Liste und Funktionalität

### Onboarding Flow (3 Screens)
- **Welcome Screen:** Begrüßung mit Hero-Visual und Hauptvorteil der App
- **Goals Screen:** Auswahl des Hauptziels (Muskelaufbau, Fettabbau, Fitness verbessern)
- **Experience Screen:** Auswahl des Erfahrungslevels (Anfänger, Fortgeschritten, Experte)

### Main App (Tab-Navigation)

#### Home Screen
Der zentrale Hub der App zeigt die heutigen Aufgaben und motivierende Einblicke. Oben befindet sich eine Begrüßung mit dem Namen des Nutzers und dem aktuellen Datum. Eine große Karte zeigt das heutige Training mit einer Vorschau der Übungen und einem "Start Workout"-Button. Darunter folgt eine Ernährungskarte mit den heutigen Makronährstoff-Zielen und einem Fortschrittsbalken. Ein Motivations-Widget zeigt eine inspirierende Nachricht basierend auf den letzten Fortschritten. Am unteren Rand befindet sich ein Call-to-Action für den nächsten Bodyscan.

#### Training Screen
Detaillierte Ansicht des aktuellen Trainingsplans. Eine Wochenübersicht zeigt die geplanten Trainingstage. Für das heutige Training werden alle Übungen mit Namen, Muskelgruppe, Sätzen und Wiederholungen aufgelistet. Jede Übung kann angeklickt werden, um eine Anleitung mit Animation oder Video zu sehen. Nach Abschluss einer Übung kann der Nutzer diese abhaken.

#### Progress Screen
Visualisierung der Körperdaten-Entwicklung über die Zeit. Ein 3D-Körpermodell (vereinfacht) zeigt die aktuelle Körperkomposition. Darunter befinden sich Liniendiagramme für Gewicht, Körperfettanteil und Muskelmasse über die letzten Scans. Eine Timeline zeigt alle bisherigen Scans mit Datum. Ein Vergleichs-Widget zeigt die Veränderung seit dem ersten Scan.

#### Nutrition Screen
Übersicht über die Ernährungsempfehlungen. Oben werden die täglichen Makronährstoff-Ziele (Protein, Kohlenhydrate, Fette) mit Fortschrittsbalken angezeigt. Darunter folgen Mahlzeiten-Vorschläge für den Tag. Ein einfaches Tracking-Interface ermöglicht das Hinzufügen von Mahlzeiten. Die KI-Begründung erklärt, warum diese Nährstoffverteilung empfohlen wird.

#### Profile Screen
Verwaltung des Nutzerprofils und der Einstellungen. Profilbild und Name werden oben angezeigt. Darunter befinden sich Abschnitte für persönliche Daten, Ziele, verbundene Geräte (Bodyscanner), Benachrichtigungen und App-Einstellungen. Ein Logout-Button befindet sich am unteren Rand.

### Zusätzliche Screens

#### Scan Upload Screen
Interface zum Hochladen des PDF-Berichts vom Bodyscanner. Der Nutzer kann ein Foto des Berichts machen oder eine PDF-Datei auswählen. Die App zeigt einen Upload-Fortschritt und bestätigt die erfolgreiche Extraktion der Daten.

#### AI Insights Screen
Detaillierte Ansicht der KI-Empfehlungen. Jede Empfehlung wird mit einer verständlichen Begründung und optionalen Links zu wissenschaftlichen Quellen versehen. Der Nutzer kann Feedback geben (z.B. "Diese Übung fühlt sich nicht gut an").

#### Workout Detail Screen
Detailansicht einer einzelnen Trainingseinheit mit allen Übungen, Anleitungen und der Möglichkeit, Sets und Wiederholungen zu tracken.

## UI-Stil und Farbpalette

Das Design verwendet einen **Dark Mode als Basis**, um die Konzentration auf die Inhalte zu lenken und eine hochwertige Anmutung zu erzeugen. Die Farbpalette ist clean und modern:

- **Background:** Dunkles Anthrazit (#151718)
- **Surface:** Leicht aufgehelltes Grau (#1e2022) für Karten und erhöhte Flächen
- **Foreground:** Helles Weiß (#ECEDEE) für primären Text
- **Muted:** Gedämpftes Grau (#9BA1A6) für sekundären Text
- **Primary/Accent:** Elektrisches Cyan (#0a7ea4) für Call-to-Actions und Hervorhebungen
- **Success:** Leuchtendes Grün (#4ADE80) für Fortschritte und positive Feedback
- **Warning:** Warmes Gelb (#FBBF24) für Warnungen
- **Error:** Kräftiges Rot (#F87171) für Fehler

Die **Typografie** nutzt eine klare, gut lesbare serifenlose Schriftart (SF Pro auf iOS, Roboto auf Android). Verschiedene Schriftstärken schaffen Hierarchie: Bold für Überschriften, Regular für Fließtext, Light für sekundäre Informationen. Große, plakative Zahlen werden für wichtige Metriken verwendet.

Der **Ton** ist motivierend, unterstützend und datengestützt. Die App spricht den Nutzer als kompetenter Partner auf Augenhöhe an, ohne belehrend oder militärisch zu wirken.

## Datenvisualisierung

Die Visualisierung fokussiert sich auf **Trends statt rohe Zahlen**. Einfache Liniendiagramme zeigen den Verlauf von Muskelmasse, Körperfettanteil und Gewicht über die Zeit. Ein vereinfachtes 3D-Körpermodell visualisiert die aktuelle Körperkomposition und verändert sich subtil im Laufe der Zeit, um den Fortschritt zu zeigen.

**Progress Bars** werden für alle wichtigen Ziele verwendet (wöchentliches Trainingsvolumen, Proteinzufuhr, Wasserzufuhr), um ein Gefühl von Gamification und Erreichbarkeit zu vermitteln. Farbcodierung hilft bei der schnellen Erfassung: Grün für erreichte Ziele, Gelb für in Bearbeitung, Rot für verpasste Ziele.

## AI-Transparenz und Vertrauensbildung

Jede KI-Empfehlung wird mit einer **kurzen, verständlichen Begründung** versehen. Beispiel: "Basierend auf deinem letzten Scan hat deine Muskelmasse am Oberkörper um 2% zugenommen. Wir erhöhen daher das Volumen für Brust- und Rückenübungen, um dieses Momentum zu nutzen."

Bei Ernährungsempfehlungen werden **Links zu wissenschaftlichen Quellen** oder kurzen Erklärtexten angeboten. Der Nutzer hat die Möglichkeit, **Feedback zu den Plänen zu geben** (z.B. "Diese Übung fühlt sich nicht gut an"), worauf die KI lernen und reagieren kann.

## MVP-Fokus für Hackathon

Der MVP konzentriert sich auf die **Kernfunktionalität**: PDF-Upload und -Extraktion, Erstellung eines initialen Trainingsplans, Tracking von Workouts und Visualisierung der Körperdaten.

**Vereinfachungen für den MVP:**
- Der Ernährungsplan ist zunächst eine Liste von Empfehlungen und Makronährstoffzielen, kein detailliertes Mahlzeiten-Tracking
- Falls die PDF-Extraktion zu aufwändig ist, können die wichtigsten Daten (Gewicht, Körperfett, Muskelmasse) manuell eingegeben werden
- Keine Integration von Wearables oder anderen Diensten im MVP
- Vereinfachtes 3D-Körpermodell (2D-Silhouette mit Farbcodierung für Muskelgruppen)

**Wow-Faktor:**
- Automatische PDF-Extraktion der Bodyscan-Daten
- Personalisierte AI-Empfehlungen mit transparenten Begründungen
- Visueller Fortschritt durch Körpermodell-Visualisierung
- Clean, modernes Design mit starkem Fokus auf Usability
