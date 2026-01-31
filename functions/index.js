const functions = require("firebase-functions/v1");
const admin = require("firebase-admin");
const { VertexAI } = require("@google-cloud/vertexai");
const { FieldValue } = require("firebase-admin/firestore");

admin.initializeApp();
const db = admin.firestore();

// ----------------------------------------------------
// 1. AUTH TRIGGERS
// ----------------------------------------------------

exports.onUserCreate = functions.auth.user().onCreate(async (user) => {
  const { uid, email, displayName, photoURL } = user;
  await db.collection("users").doc(uid).set({
    uid,
    email,
    displayName: displayName || "New User",
    photoURL: photoURL || null,
    createdAt: FieldValue.serverTimestamp(),
    onboardingStatus: "pending_details",
    role: "user",
    // Initialize sub-structures for Single JSON architecture
    digitalTwin: {},
    trainingPlan: {},
    nutritionPlan: {},
    workoutLogs: [],
    nutritionLogs: []
  });
  console.log(`[Auth] User profile and single-json structure created for ${uid}`);
  return null;
});

// ----------------------------------------------------
// 2. ONBOARDING & DATA
// ----------------------------------------------------

exports.submitOnboardingDetails = functions.https.onCall(async (data, context) => {
  try {
    if (!context.auth) throw new functions.https.HttpsError("unauthenticated", "User must be logged in");
    const { uid } = context.auth;
    await db.collection("users").doc(uid).update({
      ...data,
      onboardingStatus: "complete",
      updatedAt: FieldValue.serverTimestamp()
    });
    return { status: "success", message: "Profile updated" };
  } catch (e) {
    console.error("submitOnboardingDetails Error:", e);
    throw new functions.https.HttpsError("internal", e.message);
  }
});

exports.processInitialScan = functions.https.onCall(async (data, context) => {
  if (!context.auth) throw new functions.https.HttpsError("unauthenticated", "User must be logged in");
  const { uid } = context.auth;
  const { scanFileUrl, manualMetrics } = data; // Emulated input

  // MOCK LOGIC: In real app, this would download .obj and process it.
  // For MVP, we trust manualMetrics or return a standard "Digital Twin"

  const digitalTwin = {
    timestamp: new Date().toISOString(), // Use ISO string for JSON compat inside object
    weight: manualMetrics?.weight || 75.0,
    bodyFat: 18.5,
    muscleMass: 42.1,
    bmi: 23.4,
    bmrKcal: 1800, // Derived
    segmentalAnalysis: { torsoFat: 12.0 },
    scanUrl: scanFileUrl
  };

  await db.collection("users").doc(uid).update({
    digitalTwin
  });
  return { status: "success", digitalTwin };
});

// ----------------------------------------------------
// 3. AI PLAN GENERATION (TRAINING)
// ----------------------------------------------------

exports.generateTrainingPlan = functions.https.onCall(async (data, context) => {
  if (!context.auth) throw new functions.https.HttpsError("unauthenticated", "User must be logged in");
  const { uid } = context.auth;

  // Logic: Check if User has specific modules or goals
  const userDoc = await db.collection("users").doc(uid).get();
  const userData = userDoc.data();
  const goals = userData?.goals || [];

  const mockPlan = {
    planId: `plan_${Date.now()}`,
    cycleFocus: goals.includes("endurance") ? "Hybrid Athlete (Run + Lift)" : "Hypertrophy Phase 1",
    startDate: new Date().toISOString(),
    schedule: [
      {
        day: "Monday",
        type: "Push",
        exercises: [{ name: "Bench Press", sets: 3, reps: "8-12" }]
      },
      {
        day: "Tuesday",
        type: "Pull",
        exercises: [{ name: "Pull Ups", sets: 3, reps: "Failure" }]
      }
    ]
  };

  await db.collection("users").doc(uid).update({
    trainingPlan: mockPlan
  });
  return { status: "success", plan: mockPlan };
});

// ----------------------------------------------------
// 4. AI PLAN GENERATION (NUTRITION)
// ----------------------------------------------------

exports.generateNutritionPlan = functions.https.onCall(async (data, context) => {
  if (!context.auth) throw new functions.https.HttpsError("unauthenticated", "User must be logged in");
  const { uid } = context.auth;
  const { dietType } = data;

  // Fetch BMR from Digital Twin in the same doc
  const userDoc = await db.collection("users").doc(uid).get();
  const userData = userDoc.data();
  // Safe access to nested BMR
  const bmr = userData?.digitalTwin?.bmrKcal || 2000;

  const targetCalories = bmr + 500; // Default surplus

  const nutritionPlan = {
    type: "nutrition",
    dailyCalories: targetCalories,
    macros: { p: 180, c: 250, f: 70 },
    dietType: dietType || "balanced",
    mealSuggestions: [
      { name: "Protein Oats", calories: 500 },
      { name: "Chicken/Tofu Salad", calories: 700 }
    ]
  };

  await db.collection("users").doc(uid).update({
    nutritionPlan
  });
  return { status: "success", plan: nutritionPlan };
});

// ----------------------------------------------------
// 5. FEEDBACK LOOPS
// ----------------------------------------------------

exports.logWorkoutFeedback = functions.https.onCall(async (data, context) => {
  if (!context.auth) throw new functions.https.HttpsError("unauthenticated", "User must be logged in");
  const { uid } = context.auth;
  const { rating, notes } = data;

  await db.collection("users").doc(uid).update({
    workoutLogs: FieldValue.arrayUnion({
      ...data,
      timestamp: new Date().toISOString()
    })
  });

  if (rating >= 5) {
    console.log(`[AI Logic] High pain reported. Adjusting future plan...`);
    // SIMULATION: Update the plan to "Deload"
    // We update the nested trainingPlan fields using dot notation
    await db.collection("users").doc(uid).update({
      "trainingPlan.cycleFocus": "Injury Recovery / Deload",
      "trainingPlan.schedule.0.type": "Mobility & Stretch"
    });
    return { status: "logged", planUpdated: true, message: "Plan adapted for recovery." };
  }

  return { status: "logged", planUpdated: false };
});


exports.logNutritionFeedback = functions.https.onCall(async (data, context) => {
  if (!context.auth) throw new functions.https.HttpsError("unauthenticated", "User must be logged in");
  const { uid } = context.auth;
  const { ateOffPlan } = data;

  await db.collection("users").doc(uid).update({
    nutritionLogs: FieldValue.arrayUnion({
      ...data,
      timestamp: new Date().toISOString()
    })
  });

  if (ateOffPlan) {
    // SIMULATION: Reduce tomorrow's calories
    await db.collection("users").doc(uid).update({
      "nutritionPlan.dailyCalories": FieldValue.increment(-200)
    });
    return { status: "logged", planUpdated: true, message: "Calories adjusted for tomorrow." };
  }

  return { status: "logged", planUpdated: false };
});
