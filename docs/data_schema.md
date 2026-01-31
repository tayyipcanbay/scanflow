# Database Schema Reference (Firestore)

This document serves as the Single Source of Truth for the data model. All API endpoints read/write to these structures.

## 1. Top-Level Collection: `users`
**Document ID**: `uid` (from Firebase Auth)

| Field | Type | Description |
| :--- | :--- | :--- |
| `uid` | String | Primary Key (matches Auth ID). |
| `email` | String | User's email address. |
| `displayName` | String | User's full name. |
| `dob` | Timestamp | Date of Birth (Age calc). |
| `gender` | String | `male`, `female`, `other` (affects 3D base model). |
| `heightCm` | Number | Height in centimeters. |
| `createdAt` | Timestamp | Account creation date. |
| `role` | String | `user`, `admin`, `tester`. |

### Sub-Object: `preferences`
| Field | Type | Description |
| :--- | :--- | :--- |
| `units` | String | `metric` or `imperial`. |
| `language` | String | UI Language code (e.g., `en`). |
| `darkMode` | Boolean | Theme preference. |

### Sub-Object: `goals`
| Field | Type | Description |
| :--- | :--- | :--- |
| `primaryGoal` | String | `hypertrophy`, `fat_loss`, `endurance`, `strength`. |
| `targetWeightKg` | Number | Desired weight (optional). |
| `daysPerWeek` | Number | Preferred workout frequency (e.g., 4). |
| `workoutDurationMins` | Number | Preferred session length (e.g., 60). |
| `equipment` | Array<String> | `["dumbbell", "barbell", "bodyweight"]`. |

---

## 2. Sub-Collection: `users/{uid}/digitalTwin`
**Document ID**: `current` (The latest state) or `history_{timestamp}`

| Field | Type | Description |
| :--- | :--- | :--- |
| `scanId` | String | Reference to the Scan file used. |
| `timestamp` | Timestamp | When this data was recorded. |
| `weightKg` | Number | Total body weight. |
| `bmi` | Number | Body Mass Index. |
| `bmrKcal` | Number | Basal Metabolic Rate (scan-derived). |
| `bodyFatPercent` | Number | Total Body Fat %. |
| `muscleMassKg` | Number | Total Skeletal Muscle Mass. |
| `visceralFatLevel` | Number | Visceral Fat Rating (1-20+). |
| `bodyWaterL` | Number | Total Body Water in Liters. |
| `meshUrl` | String | **(Visual)** URL to the `.obj` file in Storage. |

### Sub-Object: `segmentalAnalysis` (The "Strict 3D" Data)
| Field | Type | Description |
| :--- | :--- | :--- |
| `torsoFatKg` | Number | Fat mass in torso. |
| `leftArmFatKg` | Number | Fat mass in left arm. |
| `rightArmFatKg` | Number | Fat mass in right arm. |
| `leftLegFatKg` | Number | Fat mass in left leg. |
| `rightLegFatKg` | Number | Fat mass in right leg. |
| `torsoLeanKg` | Number | Lean mass in torso. |
| `leftArmLeanKg` | Number | Lean mass in left arm. |
| `rightArmLeanKg` | Number | Lean mass in right arm. |
| `leftLegLeanKg` | Number | Lean mass in left leg. |
| `rightLegLeanKg` | Number | Lean mass in right leg. |

### Sub-Object: `measurements` (Circumferences)
| Field | Type | Description |
| :--- | :--- | :--- |
| `chestCm` | Number | Chest circumference. |
| `waistCm` | Number | Waist circumference. |
| `hipsCm` | Number | Hips circumference. |
| `thighRightCm` | Number | Right thigh circumference. |
| `bicepRightCm` | Number | Right bicep circumference. |

---

## 3. Sub-Collection: `users/{uid}/plans`
**Document ID**: `latest_training` OR `latest_nutrition`

### Document: Training Plan
| Field | Type | Description |
| :--- | :--- | :--- |
| `type` | String | `training`. |
| `startDate` | Timestamp | When this cycle began. |
| `cycleDurationWeeks` | Number | Length of mesocycle (e.g., 4, 8, 12). |
| `cycleFocus` | String | Name of the phase (e.g., "Hypertrophy Phase 1"). |
| `status` | String | `active`, `completed`, `archived`. |

#### Sub-Collection: `weeks` -> `days` (Structure)
Stored as nested arrays or sub-collections depending on query needs. For MVP, nested Array in the Plan document:

```json
"schedule": [
  {
    "dayIndex": 0, // 0 = Monday
    "dayName": "Monday",
    "workoutType": "Push",
    "completed": false,
    "rating": null, // User feedback 1-5
    "feedbackText": null,
    "exercises": [
      {
        "name": "Bench Press",
        "sets": 3,
        "reps": "8-12",
        "rpe": 8,
        "restSec": 90,
        "videoUrl": "https://..."
      }
    ]
  }
]
```

### Document: Nutrition Plan
| Field | Type | Description |
| :--- | :--- | :--- |
| `type` | String | `nutrition`. |
| `dailyCalories` | Number | Target Calories (e.g., 2400). |
| `macros` | Map | `{ "p": 180, "c": 250, "f": 70 }`. |
| `dietType` | String | `vegan`, `paleo`, `balanced`. |
| `mealsPerDay` | Number | e.g., 3. |
| `allergies` | Array<String> | Excluded ingredients. |

#### Field: `mealSuggestions` (Array)
```json
[
  {
    "mealTime": "Breakfast",
    "options": [
      { "name": "Oats & Whey", "calories": 450, "recipeId": "rec-123" }
    ]
  }
]
```

---

---

## 4. Sub-Collection: `users/{uid}/nutritionLogs`
**Document ID**: `YYYY-MM-DD` (e.g., `2023-10-27`)

| Field | Type | Description |
| :--- | :--- | :--- |
| `date` | String | Date string. |
| `caloriesConsumed` | Number | User estimated intake. |
| `ateOffPlan` | Boolean | Did they cheat? |
| `dailyFeedback` | String | Free text notes. |
| `meals` | Array | List of specific feedback per meal. |

### Sub-Object: `meals` Item
```json
{
  "mealTime": "Breakfast",
  "liked": false,
  "issue": "Too much prep"
}
```

## 5. Sub-Collection: `users/{uid}/workoutLogs`
**Document ID**: `planId_dayIndex` (e.g., `plan-week1_0`)

| Field | Type | Description |
| :--- | :--- | :--- |
| `completedAt` | Timestamp | When they finished. |
| `durationMins` | Number | Actual time taken. |
| `rpe` | Number | Rate of Perceived Exertion (1-10). |
| `painReported` | Boolean | Specific injury flag. |
| `notes` | String | "Knee hurt during squats". |

---

## 6. Sub-Collection: `users/{uid}/modules`
**Document ID**: `moduleId` (e.g., `strava`, `nutrition_tracker`)

| Field | Type | Description |
| :--- | :--- | :--- |
| `enabled` | Boolean | Is this module active for the user? |
| `installedAt` | Timestamp | Date added. |
| `settings` | Map | Module-specific config (freeform JSON). |
| `lastSync` | Timestamp | Last time external data was pulled. |
| `accessToken` | String | (Encrypted) OAuth token for integrations. |

---

## 5. Top-Level Collection: `scans` (Raw Metadata)
**Document ID**: `scanId` (UUID)

| Field | Type | Description |
| :--- | :--- | :--- |
| `uid` | String | User who owns the scan. |
| `fileUrl` | String | Storage path to `.obj`. |
| `processed` | Boolean | Has the cloud function finished analyzing it? |
| `deviceInfo` | String | Scanner Device ID / SDK Version. |
