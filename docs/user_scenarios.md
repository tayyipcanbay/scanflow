# User Standard Scenarios

This document outlines the key interactions between the User and the Platform, serving as the basis for the AI Prompt Engineering and UI Workflows.

## Scenario 1: The "New Resolution" (Onboarding)
**User Input**:
*   **Goal**: "I want to get lean for summer. I have 12 weeks."
*   **Preferences**: "Vegetarian, workout 4 days/week."
*   **3D Data (Mock)**: High Body Fat (25%), Low Muscle.
*   **Modules Selected**: Core Dashboard, Nutrition, Basic Training.

**System Output**:
*   **Plan**: Hypertrophy focus with caloric deficit.
*   **Nutrition**: High protein vegetarian meal plan.
*   **Module UI**: Shows basic "Calories Burned" and "Workout Streak".

---

## Scenario 2: The "Hybrid Athlete" (Module Interaction)
**User Input**:
*   **Action**: User enables the **"Endurance/Strava" Module**.
*   **Goal Update**: "I want to run my first half-marathon."
*   **3D Data**: Moderate composition.

**System Output**:
*   **Plan Adjustment**: The AI re-balances the existing lifting plan.
    *   *Before*: 4 days heavy lifting.
    *   *After*: 2 days lifting (maintenance), 3 days running (intervals/long runs).
*   **UI Update**: Dashboard now shows "Weekly KM" alongside "Weight".

---

## Scenario 3: The "Plateau" (Progress Update)
**User Input**:
*   **Action**: User uploads a NEW 3D Scan (Month 2).
*   **Data Change**: Weight stayed same, but Body Fat -2%, Muscle +1kg (Recomp).
*   **User Feedback**: "I feel like I'm not losing weight."

**System Output**:
*   **AI Insight**: "You ARE making progress! You are recomposing (losing fat, gaining muscle)."
*   **Plan Update**: Maintain current intensity, do not drop calories further (avoiding crash).
*   **Notification**: Motivation message explaining the "Scale Weight" vs "Body Composition" difference.

---

## Scenario 4: The "Injury/Constraint" (Feedback Loop)
**User Input**:
*   **Feedback**: "My knee hurts when submitting data." or "I only have 30 mins now."

**System Output**:
*   **Plan Update**: Replace high-impact legs (Squats) with low-impact (Cycling/Swimming) or shorten sessions to HIT.
