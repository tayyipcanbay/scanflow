# Frontend Refactor Instructions (React Native + Firebase)

I need you to refactor this React Native (Expo) project to work with a pre-existing Firebase Backend that has already been built and verified.

**Goal**: Remove the current TRPC/Drizzle/SQL backend logic and replace it with direct Firebase SDK calls to my Firestore database and Cloud Functions.

## 1. The Tech Stack Change
*   **REMOVE**: trpc, drizzle-orm, mysql2, and the local `server/` logic.
*   **INSTALL**: `firebase` (The JS SDK).
*   **KEEP**: Expo Router, NativeWind (Tailwind), React Query (if acceptable for Firebase, otherwise use direct listeners).

## 2. Firebase Configuration
Initialize the Firebase App in `app/_layout.tsx` (or similar root) with this config:
```javascript
const firebaseConfig = {
    apiKey: "demo-key",
    authDomain: "demo-scanflow.firebaseapp.com",
    projectId: "demo-scanflow",
    storageBucket: "demo-scanflow.appspot.com",
};
// IMPORTANT: For now, connect to local emulators:
// auth().useEmulator("http://127.0.0.1:9099");
// firestore().useEmulator("127.0.0.1", 8080);
// functions().useEmulator("127.0.0.1", 5001);
```

## 3. Authentication Refactor
*   Replace the current login logic with **Firebase Auth**.
*   **Method**: `signInAnonymously()` (for MVP) or Google Sign In.
*   **Trigger**: The backend listens for account creation and automatically creates a user document in Firestore. You do NOT need to manually create the user profile record in the DB, just sign them in via Auth.

## 4. Data Integration Points (The Schema)
Refactor the UI screens to bind to these Firestore paths:

### A. User Profile (Dashboard)
*   **Path**: `users/{uid}`
*   **Fields**: `displayName`, `goals` (Array), `onboardingStatus`.

### B. 3D Scan Data (Progress Screen)
*   **Path**: `users/{uid}/digitalTwin/latest`
*   **Fields**: `weight` (number), `bodyFat` (number), `muscleMass` (number).

### C. Training Plan (Calendar/Workout Screen)
*   **Path**: `users/{uid}/plans/latest_training`
*   **Fields**: 
    *   `cycleFocus` (String, e.g., "Hypertrophy")
    *   `schedule` (Array of objects: `{ day: "Monday", exercises: [...] }`)

## 5. API Actions (Cloud Functions)
Replace any "Save" or "Submit" buttons to call these **HTTPS Callable** Cloud Functions:
1.  `submitOnboardingDetails(data)`: Updates user profile.
2.  `processInitialScan(data)`: Uploads scan metrics.
3.  `generateTrainingPlan()`: Triggers the AI agent to build a workout.
4.  `logWorkoutFeedback(data)`: Sends user feedback.

**Execution Order**:
Please start by stripping out the SQL dependencies and setting up the Firebase Context provider.
