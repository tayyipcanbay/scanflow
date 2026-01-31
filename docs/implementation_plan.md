# Implementation Plan: Modular AI Fitness Platform (MVP)

## Goal
Build a functional MVP for a modular health platform where users can enable/disable features. The core value is AI-driven plans based on 3D body data.

## Technology Stack (Hackathon Optimized)
- **Frontend**: Flutter (Cross-platform, Widget-based modularity).
- **Backend/Data**: Firebase (Google Ecosystem).
    - **Authentication**: Firebase Auth (**Google Sign-In Only**).
    - **Database**: Cloud Firestore (NoSQL for flexible generic module data).
    - **Storage**: Cloud Storage (for 3D model files).
- **AI/Logic**: Google Vertex AI (Gemini Models) for generating plans.

## Proposed Architecture

### 1. Extensible Module Architecture (The "Ecosystem")
The core innovation is the `Module` interface, designed to allow future 3rd-party integrations (like Strava) with the same ease as internal features.

#### The `Module` Interface Protocol
Every feature (Internal or External) implements this contract:
*   `String id` (Unique identifier)
*   `String manifestUrl` (For dynamic loading - future proofing)
*   `Widget buildWidget(BuildContext context)` ( The UI component)
*   `Future<void> onDataUpdate(DigitalTwin data)` (Reactivity: Modules react to new body scans)
*   `ModuleType type` (INTERNAL_CORE, EXTERNAL_INTEGRATION)

#### Module Registry
A central service that manages the lifecycle of these modules:
*   **Discovery**: Finds available modules (hardcoded list for MVP, API call in future).
*   **Activation**: User toggles enable/disable specific modules.
*   **Event Bus**: Broadcasts Body Scan updates to all active modules.

### 2. Core Data: "The Digital Twin"
We need a schema to store the 3D data.
*   **JSON Structure** (derived from user example):
    ```json
    {
      "weight_kg": 76.1,
      "bmi": 23.4,
      "bmr_kcal": 1877,
      "body_water_l": 51.1,
      "visceral_fat_level": 12,
      "body_fat_percent": 8.3,
      "muscle_mass_kg": 40.7,
      "fat_free_mass_kg": 69.8,
      "segmental_fat": { "torso": 2.7, "left_arm": 0.1, "right_arm": 0.1, "left_leg": 1.1, "right_leg": 1.1 },
      "segmental_lean": { "torso": 32.6, "left_arm": 4.3, "right_arm": 4.4, "left_leg": 10.8, "right_leg": 10.9 }
    }
    ```
*   **Input Method (MVP)**: Load this JSON structure from a local asset file to simulate the API response.
*   **Future Integration**: this data will eventually come from an external 3D Scanning SDK (e.g., Nano/Banuba/etc).

### 3. Key Modules (MVP Scope)

#### A. Dashboard Module (Core)
- Visualization of the user's current status (Avatar/Stats).
- Access to the Module Store.

#### B. AI Trainer Module
- **Input**: "Digital Twin" data + User Goals.
- **Process**: Call Gemini with structured prompt.
- **Output**: Weekly Training Schedule.

#### C. Nutrition Module
- **Input**: BMR (Calc from 3D data) + Preferences.
- **Process**: Call Gemini.
- **Output**: Daily Macro goals + Meal suggestions.

## Implementation Steps

## Implementation Steps (Backend First Strategy)

### Phase 1: Backend & Data Layer (Immediate Focus)
1.  **Project Init**: Setup Firebase project (Firestore, Functions, Auth).
2.  **Database Schema**: Deploy Firestore Security Rules to enforce `data_schema.md`.
3.  **API Logic**: Implement Cloud Functions defined in `api_spec.md`.
    *   `createUserProfile`
    *   `processInitialScan`
    *   `generateTrainingPlan` (Gemini Stub)
    *   `generateNutritionPlan` (Gemini Stub)

### Phase 2: API Testing & Validation
1.  **Test Script**: Create a local script (Node/Python) to hit all endpoints.
2.  **Validation**: Verify Firestore documents are created correctly after API calls.
3.  **Refinement**: Adjust JSON payloads based on test results.

### Phase 3: Frontend Module Construction
1.  **Shell**: Flutter Project + Firebase Auth.
2.  **Modules**: Build UI Widgets for Dashboard/Training/Nutrition.
3.  **Integration**: Connect UI to the (tested) Cloud Functions.

## Verification Plan

## Verification Plan

### Backend Verification (Pre-release)
*   **Unit Tests**: Jest/Mocha tests for Cloud Functions logic.
*   **Integration Script**: A `test_endpoints.py` script that runs the full user flow:
    1.  Create User -> Check DB.
    2.  Upload Mock Scan -> Check DB `digitalTwin`.
    3.  Generate Plan -> Check DB `plans`.

### Frontend Verification
- Run on iOS Simulator / Android Emulator.
- Verify "Switching off" a module removes it from the UI.
- Verify sending mock 3D data results in a personalized plan response from Gemini.
