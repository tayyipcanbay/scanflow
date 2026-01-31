# Comprehensive API Specification

## 1. Onboarding & User Profile

### `AUTH TRIGGER: onUserCreate` (Automatic)
*   **Purpose**: Automatically triggers when User signs in with Google.
*   **Trigger**: `functions.auth.user().onCreate`
*   **Action**: 
    1.  Extracts `uid`, `email`, `displayName`, `photoURL` from Google Account.
    2.  Creates the `users/{uid}` document in Firestore with these basics.
    3.  Sets `onboardingStatus` to `pending_details`.

### `POST /functions/submitOnboardingDetails`
*   **Purpose**: Finish the profile setup (metrics/goals) AFTER the auto-creation.
*   **Request**:
    ```json
    {
      "dob": "1995-05-20",
      "gender": "male",
      "heightCm": 180,
      "goals": ["hypertrophy", "fat_loss"],
      "experienceLevel": "intermediate"
    }
    ```
*   **Response**: `{ "status": "success" }`
*   **Side Effect**: Updates `users/{uid}` with physical details.

### `POST /functions/processInitialScan`
*   **Purpose**: The "Magic Moment". Ingests the first 3D scan.
*   **Request**:
    ```json
    {
      "scanFileUrl": "gs://bucket/users/abc/scan1.obj", // OR raw JSON for MVP
      "manualMetrics": {
        "weight": 76.1
        // Other manual overrides if scan fails
      }
    }
    ```
*   **Response**:
    ```json
    {
      "digitalTwinId": "dt-001",
      "metrics": {
        "bodyFat": 18.5,
        "muscleMass": 42.1,
        "segmentalAnalysis": { "torsoFat": 12.0 }
      },
      "visualUrl": "https://.../heatmap_overlay.png" // Generated comparison
    }
    ```

---

## 2. Training Plan Lifecycle

### `POST /functions/generateTrainingPlan` (The "Brain")
*   **Purpose**: Generates the weekly schedule based on *current* Digital Twin state.
*   **Trigger**: Onboarding OR "Regenerate" button.
*   **Request**:
    ```json
    {
      "constraints": {
        "daysPerWeek": 4,
        "equipment": ["dumbbell", "barbell"],
        "durationMins": 60
      },
      "focusArea": "legs" // Optional override
    }
    ```
*   **Response (The Plan Object)**:
    ```json
    {
      "planId": "plan-week-1",
      "cycleFocus": "Hypertrophy Phase 1",
      "schedule": [
        {
          "day": "Monday",
          "type": "Push",
          "exercises": [
            { "name": "Bench Press", "sets": 3, "reps": "8-12", "rpe": 8 }
          ]
        },
        // ... rest of week
      ]
    }
    ```

### `POST /functions/logWorkoutFeedback` (The Loop)
*   **Purpose**: User tells AI how it went. Critical for updates.
*   **Request**:
    ```json
    {
      "planId": "plan-week-1",
      "dayIndex": 0,
      "difficultyRating": 4, // 1-5 (5 = too hard)
      "notes": "Knee hurt on squats"
    }
    ```
*   **System Action**: Triggers internal 'Plan Tweak' logic. If rating is 5 or pain reported, next leg day is automatically modified.

### `POST /functions/updateTrainingPlan` (Mid-Cycle Adjustment)
*   **Purpose**: AI modifies *future* days based on feedback.
*   **Request**: `{ "planId": "...", "reason": "User reported knee pain" }`
*   **Response**: Returns *modified* schedule for remaining days.

---

## 3. Nutrition Plan Lifecycle

### `POST /functions/generateNutritionPlan`
*   **Purpose**: Calculates Macros based on **BMR from 3D Scan** (Much more accurate than formula).
*   **Logic**: `BMR + Activity Level + Goal (Deficit/Surplus)`.
*   **Request**:
    ```json
    {
      "dietType": "vegan",
      "mealsPerDay": 3,
      "allergies": ["nuts"]
    }
    ```
*   **Response**:
    ```json
    {
      "dailyTargets": { "calories": 2400, "protein": 180, "carbs": 250, "fat": 70 },
      "mealSuggestions": [
        { "name": "Tofu Scramble", "macros": { "p": 30, "c": 10, "f": 15 } }
      ]
    }
    ```

### `POST /functions/updateNutritionPreferences`
*   **Scenario**: User switches from "Bulk" to "Cut".
*   **Request**: `{ "goal": "fat_loss" }`
*   **System Action**: Recalculates `dailyTargets` immediately.

---

### `POST /functions/logNutritionFeedback`
*   **Purpose**: User rates a meal or compliance for the day.
*   **Request**:
    ```json
    {
      "date": "2023-10-27",
      "mealTime": "Breakfast",
      "liked": false,
      "feedback": "Too much prep time",
      "ateOffPlan": true // "Cheat meal"
    }
    ```
*   **System Action**: 
    1.  AI learns preference (e.g., avoid high-prep time meals).
    2.  If `ateOffPlan` is true, AI adjusts *tomorrow's* calories (e.g., slight reduction) to balance weekly load.

### `POST /functions/regenerateMealSuggestions`
*   **Purpose**: "I don't like these options, give me new ones."
*   **Request**: `{ "mealTime": "Lunch", "excludeIngredients": ["avocado"] }`
*   **Response**: Returns 3 new `MealSuggestion` objects.

---

## 4. 3D Body Visualization Endpoints


### `GET /functions/getComparisonData`
*   **Purpose**: Returns the mesh diff for the 3D Viewer.
*   **Request**: `{ "scanIdA": "scan-jan", "scanIdB": "scan-feb" }`
*   **Response**:
    ```json
    {
      "meshUrlA": "...",
      "meshUrlB": "...",
      "heatMapConfig": {
        "bicep": "green", // grew
        "waist": "red"    // shrunk (good)
      },
      "textSummary": "You lost 2cm on your waist and gained 1cm on arms."
    }
    ```
