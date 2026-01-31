# Appendix: Strava Module Specification

This document assesses the feasibility and design for a **Strava Integration Module**.

## Feasibility Rating: Medium complexity
*   **Difficulty**: 3/5
*   **Primary Challenge**: OAuth 2.0 authentication flow (requires setting up a redirect URL).
*   **Architecture Fit**: Excellent (Fits perfectly into `ExternalIntegrationModule`).

## Implementation Strategy

### 1. The Protocol
This module will implement the `ExternalIntegrationModule` interface.
*   **ID**: `strava_integration_v1`
*   **Display Name**: "Connect Strava"

### 2. Authentication Flow (User Experience)
1.  User clicks "Enable" in the Module Store.
2.  App opens a secure web view to `www.strava.com/oauth/authorize`.
3.  User logs in and grants permission.
4.  Strava redirects back to app schema `scanflow://callback`.
5.  App extracts `access_token` and stores it securely.

### 3. Data Mapping (The "Intelligence")
We ingest Strava activities to modify the **Workout Plan**.

| Strava Activity | Metric | Action on AI Plan |
| :--- | :--- | :--- |
| **Run** (Cardio) | Distance > 5km | **Reduce Leg Volume** in gym plan (Recovery focus). |
| **Swim** | Duration > 30m | Mark "Active Recovery" day complete. |
| **Weight Training** | Suffer Score | Reduce intensity of next AI workout. |

### 4. Code Structure (Draft)
```dart
class StravaModule extends BaseModule {
  Future<void> onSync() async {
     // 1. Fetch last 3 activities
     var activities = await stravaApi.getActivities(after: lastSync);
     
     // 2. Normalize
     var load = calculateLoad(activities);
     
     // 3. Update Global State
     globalState.tweakRecovery(load);
  }
}
```

## Conclusion
Implementing this is standard engineering work. The architecture supports it fully without changing the core core app.
