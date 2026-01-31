# ScanFlow Backend (Firebase Cloud Functions)

This directory contains the server-less backend logic for the ScanFlow AI Fitness Platform.

## 📂 Structure
*   `index.js`: **Production Code**. Contains all API endpoints (Auth, AI Training, Nutrition, Feedback).
*   `verify_scenarios.js`: **Integration Tests**. Simulate full user stories (Onboarding -> Hybrid Athlete -> Injury).
*   `test_logic.js`: **Unit Tests**. Isolated tests for individual functions.

## 🚀 How to Run Tests (No Cloud Required)
We use a mock-injection strategy to test logic without needing a live Firebase project.

```bash
# 1. Install dependencies
cd functions
npm install

# 2. Run the Full Scenario Verification
node verify_scenarios.js
```

You should see output confirming:
- User Creation
- Plan Generation (Training & Nutrition)
- Feedback Loops (Injury & Cheat Meals)

## ☁️ How to Deploy (When Ready)
1.  Install Firebase CLI: `npm install -g firebase-tools`
2.  Login: `firebase login`
3.  Deploy:
    ```bash
    firebase deploy --only functions
    ```

## 🛠 Adding New Modules
To add a new module (e.g., Sleep Tracker):
1.  Define the Schema in `../docs/data_schema.md`.
2.  Add a new export in `index.js` (e.g., `exports.syncSleepData`).
3.  Add a test case in `verify_scenarios.js`.
