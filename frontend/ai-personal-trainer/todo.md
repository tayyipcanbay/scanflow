# AI Personal Trainer - TODO

## Branding
- [x] App-Logo generieren
- [x] Logo in alle erforderlichen Positionen kopieren
- [x] App-Namen und Branding in app.config.ts aktualisieren

## Onboarding Flow
- [ ] Welcome Screen erstellen
- [ ] Goals Screen erstellen
- [ ] Experience Screen erstellen
- [ ] Onboarding-Navigation implementieren

## Tab Navigation
- [x] Home Tab implementieren
- [x] Training Tab implementieren
- [x] Progress Tab implementieren
- [x] Nutrition Tab implementieren
- [x] Profile Tab implementieren
- [x] Tab-Icons in icon-symbol.tsx hinzufügen

## Home Screen
- [x] Begrüßungs-Header mit Namen und Datum
- [x] Heutiges Training Card mit Vorschau
- [x] Ernährungs-Card mit Makronährstoff-Zielen
- [x] Motivations-Widget
- [x] Bodyscan Call-to-Action

## Training Screen
- [x] Wochenübersicht der Trainingstage
- [x] Liste der heutigen Übungen
- [x] Übungsdetails mit Sätzen und Wiederholungen
- [x] Abhaken-Funktion für abgeschlossene Übungen
- [ ] Navigation zu Workout Detail Screen

## Progress Screen
- [x] Vereinfachtes Körpermodell-Visual
- [x] Liniendiagramm für Gewichtsverlauf
- [x] Liniendiagramm für Körperfettanteil
- [x] Liniendiagramm für Muskelmasse
- [x] Scan-Timeline mit allen bisherigen Scans
- [x] Vergleichs-Widget (erster vs. aktueller Scan)

## Nutrition Screen
- [x] Makronährstoff-Ziele mit Fortschrittsbalken
- [x] Mahlzeiten-Vorschläge für den Tag
- [x] Einfaches Mahlzeiten-Tracking Interface
- [x] AI-Begründung für Ernährungsempfehlungen

## Profile Screen
- [x] Profilbild und Name anzeigen
- [x] Persönliche Daten bearbeiten
- [x] Ziele verwalten
- [x] Einstellungen (Benachrichtigungen, Theme)
- [x] Logout-Funktion

## Scan Upload Screen
- [ ] PDF-Upload Interface
- [ ] Foto-Upload von Scan-Bericht
- [ ] Upload-Fortschrittsanzeige
- [ ] Erfolgsbestätigung nach Datenextraktion

## AI Insights Screen
- [ ] Liste der AI-Empfehlungen
- [ ] Begründungen für jede Empfehlung
- [ ] Feedback-Funktion für Empfehlungen
- [ ] Links zu wissenschaftlichen Quellen

## Workout Detail Screen
- [ ] Detailansicht einer Trainingseinheit
- [ ] Übungsanleitungen mit Animationen/Bildern
- [ ] Set- und Wiederholungs-Tracking
- [ ] Timer für Pausen zwischen Sätzen

## Datenmodell & State Management
- [x] AsyncStorage Setup für lokale Datenpersistenz
- [x] User Profile Datenstruktur
- [x] Body Scan Datenstruktur
- [x] Training Plan Datenstruktur
- [x] Nutrition Plan Datenstruktur
- [x] Mock-Daten für MVP erstellen

## Styling & Theme
- [x] Dark Mode Theme in theme.config.js anpassen
- [x] Farbpalette implementieren (Cyan Primary, Success Green)
- [x] Wiederverwendbare UI-Komponenten erstellen (Card, Button, ProgressBar)
- [x] Typografie-Styles definieren

## Testing & Finalisierung
- [x] Alle User Flows testen
- [x] Responsive Design für verschiedene Bildschirmgrößen prüfen
- [x] Performance-Optimierung
- [x] Checkpoint erstellen

## UI Design Änderungen
- [x] 3D-Modell eines männlichen Dummy-Menschen generieren
- [x] 3D-Modell oben auf dem Home Screen integrieren
- [x] UI Layout anpassen für 3D-Modell-Darstellung

## Modulares System (Master Design Document)
- [x] Module Store Screen erstellen
- [x] Modul-Karten mit Install/Uninstall Funktion
- [ ] BaseModule Interface definieren
- [ ] Core Module: AI Trainer implementieren
- [ ] Core Module: 3D Data Ingester implementieren
- [ ] Optional Module: Strava Integration (UI only)
- [ ] Optional Module: Nutrition Module (UI only)
- [x] Dashboard: Digital Twin Visualisierung verbessern
- [x] AI Feedback: Recomposition Detection
- [ ] Module Registry System implementieren

## UI Design Update (Figma Basis)
- [x] Gradient Header (Purple to Blue) implementieren
- [x] AI Insight Card im Header hinzufügen
- [x] Quick Stats Cards (Calories, Weekly Workouts) erstellen
- [ ] Body Weight Trend Chart implementieren
- [ ] Bottom Navigation mit Icons neu gestalten
- [ ] Card-basiertes Layout für alle Screens
- [x] Farbschema auf Purple/Blue Gradient umstellen

## Navigation & Localization Updates
- [x] Quick Stats Cards mit Screens verknüpfen (Calories → Nutrition, Workouts → Training)
- [x] "index-" Tab aus der Navigation entfernen
- [x] Alle Texte auf Englisch umstellen

## Exercise Detail Screen
- [x] Exercise Detail Screen erstellen mit Bild und Set-Tracking
- [x] Gewicht und Reps pro Satz eingeben können
- [x] Navigation vom Training Screen zum Detail Screen
- [x] Übungsbilder für alle Exercises hinzufügen (Bench Press, Incline Press, Dumbbell Flys, Tricep Dips, Tricep Pushdowns)
- [ ] Set-Daten persistent speichern

## Bug Fixes
- [x] Exercise Detail Screen Error beheben

## UX Improvements - Navigation & Auto-Completion
- [x] Gesamtes Exercise Card navigiert zum Detail Screen (außer Kreis-Button)
- [x] Sätze werden automatisch abgehakt wenn Gewicht und Reps eingetragen sind
- [x] Übung wird automatisch abgehakt wenn alle Sätze komplett sind
- [x] State-Synchronisation zwischen Detail Screen und Training Screen

## Home Screen - 30-Day Training Calendar
- [x] Entferne "Your Plans" Bereich mit den 3 Plan-Cards
- [x] Erstelle 30-Tage-Kalender Komponente
- [x] Füge Trainings-Symbole für geplante Trainingstage hinzu
- [x] Zeige aktuellen Tag hervorgehoben an

## Training Schedule Design Improvements
- [x] Füge Monat/Jahr-Header mit Navigation (Pfeile links/rechts) hinzu
- [x] Füge Wochentags-Labels (MON, TUE, WED, THU, FRI, SAT, SUN) hinzu
- [x] Verbessere Kalender-Layout: 7 Spalten (eine pro Wochentag)
- [x] Dunkleres, eleganteres Design mit Hintergrundbild-Effekt

## Functional Calendar Implementation
- [x] Implement month/year state management
- [x] Add working left/right navigation arrows
- [x] Calculate correct first day of month and day-of-week alignment
- [x] Display correct number of days per month
- [x] Set today as Saturday, January 31, 2026
- [x] Calculate training days based on actual weekdays (Mon/Wed/Fri)

## Firebase Backend Refactor
- [x] Remove TRPC, Drizzle, MySQL dependencies from package.json
- [x] Remove server/ directory and backend logic
- [x] Install Firebase SDK (firebase package)
- [x] Create Firebase configuration with emulator settings
- [x] Set up Firebase Context Provider in app/_layout.tsx
- [x] Implement Firebase Auth with anonymous sign-in
- [x] Create useAuth hook for Firebase authentication
- [ ] Refactor Home Screen to use Firestore (users/{uid})
- [ ] Refactor Progress Screen to use Firestore (users/{uid}/digitalTwin/latest)
- [ ] Refactor Training Screen to use Firestore (users/{uid}/plans/latest_training)
- [ ] Create Cloud Functions integration (submitOnboardingDetails, processInitialScan, generateTrainingPlan, logWorkoutFeedback)
- [ ] Replace AsyncStorage workout completion with Firestore
- [ ] Test Firebase emulator connections
- [ ] Update authentication flow in Profile Screen

## Firebase Timeout Error Fix
- [x] Investigate "6000ms timeout exceeded" error
- [x] Fix Firebase emulator connection configuration
- [x] Handle emulator connection errors gracefully
- [x] Test Firebase initialization without emulators

## Training Screen - Multi-Day Schedule
- [x] Add training data for all days (Monday Chest, Wednesday Legs, Friday Back)
- [x] Implement day selector to switch between training days
- [x] Connect calendar with training schedule to show actual dates
- [x] Display date for each training day (e.g., "Monday, Feb 3")
- [x] Update week overview to be clickable

## Exercise Images - Leg and Back Exercises
- [x] Generate anatomical image for Squats
- [x] Generate anatomical image for Leg Press
- [x] Generate anatomical image for Leg Curls
- [x] Generate anatomical image for Calf Raises
- [x] Generate anatomical image for Pull-Ups
- [x] Generate anatomical image for Barbell Rows
- [x] Generate anatomical image for Lat Pulldown
- [x] Generate anatomical image for Bicep Curls
- [x] Update exercise detail screen with new images

## Workout History View
- [x] Create workout history screen/tab
- [x] Design workout history data structure in AsyncStorage
- [x] Display past workouts with dates and exercise names
- [x] Show weights and reps for each exercise in history
- [x] Calculate and display total volume per workout
- [x] Add navigation from Training screen to History view
- [x] Save workout data when all exercises are completed
- [x] Sort workouts by date (newest first)

## Bug Fix - Firebase Timeout
- [x] Remove Firebase initialization to prevent timeout errors
- [x] Clean up Firebase-related code and dependencies

## Exercise Image Sizing Fix
- [x] Make all exercise images uniform size
- [x] Center exercise images in detail screen

## Color Theme Update
- [x] Replace purple color (#A855F7) with dark blue #0F1F2A throughout app

## UI Color Updates
- [x] Change bottom button color to #E9B44C
- [x] Update kg Muscle and % Fat text colors to match kg weight color

## Tab Bar Color Update
- [x] Change tab bar active button color to #E9B44C

## Exercise Detail - Set Management
- [x] Add "Add Set" button next to "Track Your Sets" heading
- [x] Add "Remove Set" button next to "Track Your Sets" heading
- [x] Implement functionality to dynamically add new set fields
- [x] Implement functionality to remove existing set fields

## Remove Set Button Design Update
- [x] Update Remove Set button to match Add Set button design
- [x] Change background color to #0F1F2A
- [x] Change text color to white for contrast

## Home Screen - 3D Model Section Redesign
- [x] Split 3D model section into two connected cards
- [x] Upper card contains 3D model only
- [x] Lower card contains body stats (kg, kg Muscle, % Fat)
- [x] Make lower card clickable to navigate to Progress screen

## UI Color and Headline Updates
- [x] Add "Measurements" headline to body stats card on home screen
- [x] Change selected weekday buttons (Monday, Wednesday, Friday) to #E9B44C
- [x] Change completed exercise checkbox color to #E9B44C

## Home Screen Layout and Color Updates
- [x] Align 3D model card flush with blue header gradient
- [x] Change Calories today progress bar color to #E9B44C
- [x] Change Weekly workouts progress bar color to #E9B44C
- [x] Change current day calendar box border to #E9B44C

## Home Screen Scroll Behavior Fix
- [x] Fix scrolling so content cards stay below blue header
- [x] Prevent cards from scrolling over the header gradient

## Progress Screen Redesign
- [x] Add side-by-side 3D model comparison (start scan left, current scan right)
- [x] Create weight progress graph over time
- [x] Create muscle mass progress graph over time
- [x] Create body fat percentage progress graph over time
- [x] Display data from first scan to current scan

## Button Colors and Translation
- [x] Change Modules screen buttons to #E9B44C (Strava, Sleep Tracker, Wearable Sync)
- [x] Change "Mahlzeit Hinzufügen" button in Nutrition to #E9B44C
- [x] Translate all German text to English throughout the app
