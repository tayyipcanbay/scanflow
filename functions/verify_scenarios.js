const assert = require('assert');
// Moved require('./index.js') to after mock injection

// ----------------------------------------------------------
// MOCKING INFRASTRUCTURE (Re-used for Scenario consistency)
// ----------------------------------------------------------
const mockFirestore = {};
const mockCollection = (path) => ({
    doc: (id) => ({
        set: (data) => { mockFirestore[`${path}/${id}`] = data; return Promise.resolve(); },
        update: (data) => {
            const docKey = `${path}/${id}`;
            if (!mockFirestore[docKey]) mockFirestore[docKey] = {};

            // Handle increment specifically before Object.assign overwrites it
            if (data.dailyCalories && typeof data.dailyCalories === 'object') {
                // Assume it's an increment for this test case
                const currentVal = mockFirestore[docKey].dailyCalories || 0;
                // Manually apply the -200 logic (since mock increment returns {val: -200})
                const newVal = currentVal + data.dailyCalories.val;

                // Assign result directly, bypassing Object.assign for this field
                mockFirestore[docKey].dailyCalories = newVal;

                // Remove from data to prevent Object.assign from overwriting it with the object
                const { dailyCalories, ...rest } = data;
                Object.assign(mockFirestore[docKey], rest);
            } else {
                Object.assign(mockFirestore[docKey], data);
            }
            return Promise.resolve();
        },
        get: () => {
            const data = mockFirestore[`${path}/${id}`];
            return Promise.resolve({ exists: !!data, data: () => data });
        },
        collection: (subPath) => mockCollection(`${path}/${id}/${subPath}`)
    }),
    add: (data) => { return Promise.resolve({ id: 'new-id' }); }
});

const functions = {
    https: { onCall: (h) => h, HttpsError: class extends Error { } },
    auth: { user: () => ({ onCreate: (h) => h }) }
};
const admin = {
    initializeApp: () => { },
    firestore: Object.assign(() => ({ collection: mockCollection }), { FieldValue: { serverTimestamp: () => 'TIMESTAMP', increment: (n) => ({ val: n }) } })
};

// Inject Mocks
const originalRequire = require('module').prototype.require;
require('module').prototype.require = function (path) {
    if (path === 'firebase-functions') return functions;
    if (path === 'firebase-admin') return admin;
    if (path === '@google-cloud/vertexai') return { VertexAI: class { } };
    return originalRequire.call(this, path);
};
const myFunctions = require('./index.js');
// ----------------------------------------------------------

async function runScenarios() {
    console.log(">>> RUNNING USER SCENARIOS (API ONLY) <<<");

    const uid = "scenario-user-1";
    const context = { auth: { uid } };

    // SCENARIO 1: The "New Resolution"
    console.log("\n--- SCENARIO 1: Onboarding & First Plan ---");

    // 1. Auth Trigger
    await myFunctions.onUserCreate({ uid, email: "jim@gym.com" });
    assert.equal(mockFirestore[`users/${uid}`].email, "jim@gym.com");
    console.log("✅ User Created via Google Auth");

    // 2. Onboarding Details
    await myFunctions.submitOnboardingDetails({ goals: ["hypertrophy"], experienceLevel: "beginner" }, context);
    console.log("✅ Onboarding Details Submitted");

    // 3. Scan Upload
    await myFunctions.processInitialScan({ manualMetrics: { weight: 80 } }, context);
    assert.equal(mockFirestore[`users/${uid}/digitalTwin/latest`].weight, 80);
    console.log("✅ 3D Scan Processed (Digital Twin Created)");

    // 4. Generate Plans
    const trainRes = await myFunctions.generateTrainingPlan({}, context);
    assert.equal(trainRes.plan.cycleFocus, "Hypertrophy Phase 1");
    console.log("✅ Training Plan Generated: " + trainRes.plan.cycleFocus);

    const nutrRes = await myFunctions.generateNutritionPlan({ dietType: "vegan" }, context);
    assert.equal(nutrRes.plan.dietType, "vegan");
    console.log("✅ Nutrition Plan Generated: " + nutrRes.plan.dailyCalories + "kcal");


    // SCENARIO 2: The "Hybrid Athlete" (Goal Change)
    console.log("\n--- SCENARIO 2: Changing Goals (Endurance) ---");

    // User changes goal
    await myFunctions.submitOnboardingDetails({ goals: ["endurance"] }, context);

    // User Regenerates Plan
    const hybridRes = await myFunctions.generateTrainingPlan({}, context);
    assert.equal(hybridRes.plan.cycleFocus, "Hybrid Athlete (Run + Lift)");
    console.log("✅ Plan Adapted to New Goal: " + hybridRes.plan.cycleFocus);


    // SCENARIO 3: Feedback Loop (Injury)
    console.log("\n--- SCENARIO 3: Feedback & Adaptation ---");

    const feedbackRes = await myFunctions.logWorkoutFeedback({ rating: 5, notes: "Knee hurts" }, context);
    assert.equal(feedbackRes.planUpdated, true);

    // Check DB for update
    const updatedPlan = mockFirestore[`users/${uid}/plans/latest_training`];
    assert.equal(updatedPlan.cycleFocus, "Injury Recovery / Deload");
    console.log("✅ High Pain Logged -> Plan Switched to: " + updatedPlan.cycleFocus);


    // SCENARIO 4: Nutrition Feedback (Cheat Meal)
    console.log("\n--- SCENARIO 4: Nutrition Adjustment ---");

    const initialCals = mockFirestore[`users/${uid}/plans/latest_nutrition`].dailyCalories;
    await myFunctions.logNutritionFeedback({ ateOffPlan: true }, context);

    const newCals = mockFirestore[`users/${uid}/plans/latest_nutrition`].dailyCalories;
    console.log(`✅ Cheat Meal Logged. Calories adjusted: ${initialCals} -> ${newCals}`);
    assert.ok(newCals < initialCals);

    console.log("\n>>> ALL SCENARIOS VERIFIED SUCCESSFULLY <<<");
}

runScenarios().catch(e => { console.error(e); process.exit(1); });
