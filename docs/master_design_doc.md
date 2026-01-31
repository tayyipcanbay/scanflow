# Master Design Document: Modular AI Fitness Platform

**Version:** 1.0 (Hackathon MVP)
**Status:** Ready for Development
**Tech Stack:** Flutter + Firebase + Vertex AI (Gemini)

---

## 1. Executive Summary
**Vision:** A "one-in-all" personalized health platform driven by **3D Body Scanning data**.
Unlike generic apps, our platform creates a "Digital Twin" of the user. We use this precise data (segmental fat/muscle) to generate hyper-personalized training and nutrition plans via AI.

**Core Innovation:** **"Modular Availability"**.
The app is a shell. Users "install" features (Modules) relevant to them.
*   *Want a run tracker?* Install the Strava Module.
*   *Want meal plans?* Install the Nutrition Module.
*   *Want just the workout?* Keep it simple.

---

## 2. User Scenarios (The "Why")

### Scenario A: The "New Resolution" (Onboarding)
*   **User**: "I have 12 weeks to get lean for summer."
*   **Input**: 3D Scan shows High Body Fat (25%), Low Muscle.
*   **System Action**: AI generates a **Hypertrophy + Deficit** plan.
*   **System Action**: AI generates a **Hypertrophy + Deficit** plan.
*   **User View**: 3D Mesh overlay showing "Target Areas". DASHBOARD highlights difference between current vs goal mesh.

### Scenario B: The "Hybrid Athlete" (Extensibility)
*   **User**: Decides to run a marathon. Enables **"Endurance Module"**.
*   **System Action**: AI sees the new module. It **reduces leg volume** in the gym plan to prevent overtraining.
*   **User View**: Dashboard now shows "Weekly KM" alongside "Weight".

### Scenario C: The "Plateau" (The AI Advantage)
*   **User**: "Scale weight isn't moving! I'm failing."
*   **Input**: New 3D Scan shows Weight is same, but **Muscle +1kg, Fat -1kg**.
*   **System Action**: AI detects "Recomposition".
*   **Feedback**: "You ARE making progress. Do not drop calories." (Prevents user from quitting).

---

## 3. Technical Architecture (The "How")

### High-Level Stack
*   **App Framework**: Flutter (Cross-platform).
*   **Backend**: Firebase (Auth, Firestore, Functions).
*   **Backend**: Firebase (Auth, Firestore, Functions).
*   **AI Engine**: Google Vertex AI (Gemini Pro).
*   **Visualization**: Flutter 3D Controller (Mesh Rendering .obj/.glb).

### The "Modular" Pattern
We do not build a monolithic app. We build a **Module Registry**.

```dart
// Every feature (Internal or External) follows this contract
abstract class BaseModule {
  String get id;             // e.g., "strava_integration"
  ModuleType get type;       // INTERNAL_CORE or EXTERNAL
  Widget buildDashboard();   // UI Component
  void onNewScanningData(DigitalTwin data); // React to 3D scans
}
```

### Data Flow
1.  **Ingest**: User uploads 3D Scan (JSON for MVP, API later).
2.  **Process**: `DigitalTwin` object updated in Firestore.
3.  **React**: Active Modules receive the update.
4.  **Generate**: AI Trainer (Module A) calls Gemini -> Updates Plan.
5.  **Sync**: Strava (Module B) checks runs -> Updates Plan Recovery.

---

## 4. MVP Scope (Hackathon)

### Included (Phase 1)
*   **Shell App**: Login, Module Store UI.
*   **Core Module**: 3D Data Ingester (Mock Data).
*   **AI Module**: Generates text-based plan from data.
*   **AI Module**: Generates text-based plan from data.
*   **Dashboard**: Visualizes the 3D metrics.
*   **3D Viewer**: Rendering strict mesh files (.obj) to show muscle/fat visual changes (Heatmap style).

### Deferred (Phase 2)
*   Real-time 3D Scanner SDK integration (using Mock for now).
*   Live Strava API connection (Architecture is ready, implementation deferred).

---

## 5. Future Proofing: External Integrations
We have validated the feasibility of adding external apps (like Strava/Apple Health).
*   **Method**: `ExternalIntegrationModule` interface.
*   **Mechanism**: OAuth 2.0 flow -> Token exchange -> Data Normalization.
*   **Result**: External data acts as just another "Signal" for the AI Trainer.
