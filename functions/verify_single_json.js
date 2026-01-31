const assert = require('assert');

// ----------------------------------------------------------
// MOCKING INFRASTRUCTURE
// ----------------------------------------------------------
const mockFirestore = {};

const mockCollection = (path) => ({
    doc: (id) => ({
        set: (data) => {
            mockFirestore[`${path}/${id}`] = JSON.parse(JSON.stringify(data)); // Deep copy to simulate DB storage
            return Promise.resolve();
        },
        update: (data) => {
            const docKey = `${path}/${id}`;
            if (!mockFirestore[docKey]) mockFirestore[docKey] = {};
            const doc = mockFirestore[docKey];

            for (const [key, value] of Object.entries(data)) {
                // Determine target object and property key
                let target = doc;
                let prop = key;

                if (key.includes('.')) {
                    const parts = key.split('.');
                    prop = parts.pop();
                    for (const part of parts) {
                        if (!target[part]) target[part] = {};
                        target = target[part];
                    }
                }

                // Apply update based on value type
                if (value && value._isArrayUnion) {
                    if (!Array.isArray(target[prop])) target[prop] = [];
                    target[prop].push(value.element);
                }
                else if (value && value._isIncrement) {
                    const current = typeof target[prop] === 'number' ? target[prop] : 0;
                    target[prop] = current + value.amount;
                }
                else {
                    target[prop] = value;
                }
            }
            return Promise.resolve();
        },
        get: () => {
            const data = mockFirestore[`${path}/${id}`];
            return Promise.resolve({ exists: !!data, data: () => data });
        }
    })
});

const mockFieldValue = {
    serverTimestamp: () => 'TIMESTAMP',
    arrayUnion: (element) => ({ _isArrayUnion: true, element }),
    increment: (amount) => ({ _isIncrement: true, amount })
};

const functions = {
    https: { onCall: (h) => h, HttpsError: class extends Error { } },
    auth: { user: () => ({ onCreate: (h) => h }) }
};
const admin = {
    initializeApp: () => { },
    firestore: Object.assign(() => ({ collection: mockCollection }), { FieldValue: mockFieldValue })
};

// Inject Mocks
const originalRequire = require('module').prototype.require;
require('module').prototype.require = function (path) {
    if (path === 'firebase-functions') return functions;
    if (path === 'firebase-admin') return admin;
    if (path === 'firebase-admin/firestore') return { FieldValue: mockFieldValue };
    if (path === '@google-cloud/vertexai') return { VertexAI: class { } };
    return originalRequire.call(this, path);
};
const myFunctions = require('./index.js');

// ----------------------------------------------------------
// VERIFICATION Logic
// ----------------------------------------------------------

async function runVerification() {
    console.log(">>> RUNNING VERIFICATION FOR SINGLE JSON <<<");

    const uid = "single-json-user";
    const context = { auth: { uid } };

    // 1. Auth Trigger - User Creation
    console.log("\n[1] User Creation");
    await myFunctions.onUserCreate({ uid, email: "single@json.com" });
    const userDoc = mockFirestore[`users/${uid}`];

    assert.deepEqual(userDoc.digitalTwin, {}, "digitalTwin should be empty obj");
    assert.deepEqual(userDoc.trainingPlan, {}, "trainingPlan should be empty obj");
    assert.deepEqual(userDoc.workoutLogs, [], "workoutLogs should be empty array");
    console.log("✅ User created with Single JSON structure initiated.");

    // 2. Initial Scan
    console.log("\n[2] Process Initial Scan");
    await myFunctions.processInitialScan({ manualMetrics: { weight: 70 } }, context);
    assert.equal(mockFirestore[`users/${uid}`].digitalTwin.weight, 70, "Weight matches");
    console.log("✅ digitalTwin updated in root doc.");

    // 3. Generate Training Plan
    console.log("\n[3] Generate Training Plan");
    await myFunctions.generateTrainingPlan({}, context);
    assert.ok(mockFirestore[`users/${uid}`].trainingPlan.planId, "Plan ID exists");
    console.log("✅ trainingPlan updated in root doc.");

    // 4. Generate Nutrition Plan
    console.log("\n[4] Generate Nutrition Plan");
    await myFunctions.generateNutritionPlan({ dietType: "keto" }, context);
    assert.equal(mockFirestore[`users/${uid}`].nutritionPlan.dietType, "keto");
    console.log("✅ nutritionPlan updated in root doc.");

    // 5. Log Feedback (ArrayUnion)
    console.log("\n[5] Log Workout Feedback");
    await myFunctions.logWorkoutFeedback({ rating: 3, notes: "Ok" }, context);

    const logs = mockFirestore[`users/${uid}`].workoutLogs;
    console.log("DEBUG: workoutLogs type:", typeof logs);
    console.log("DEBUG: workoutLogs content:", JSON.stringify(logs, null, 2));

    if (Array.isArray(logs)) {
        console.log("DEBUG: workoutLogs length:", logs.length);
    } else {
        console.log("DEBUG: workoutLogs is NOT an array!");
    }

    assert.equal(mockFirestore[`users/${uid}`].workoutLogs.length, 1);
    assert.equal(mockFirestore[`users/${uid}`].workoutLogs[0].rating, 3);
    console.log("✅ Workout log appended to array.");

    // 6. Feedback Trigger Logic (High Pain -> Deload)
    console.log("\n[6] Log High Pain Feedback (Trigger logic)");
    await myFunctions.logWorkoutFeedback({ rating: 5, notes: "Pain" }, context);
    assert.equal(mockFirestore[`users/${uid}`].workoutLogs.length, 2);
    assert.equal(mockFirestore[`users/${uid}`].trainingPlan.cycleFocus, "Injury Recovery / Deload");
    console.log("✅ Plan adjusted via dot notation update.");

    // 7. Nutrition Log & Calorie Adjustment
    console.log("\n[7] Log Nutrition Feedback & Adjust");
    const initialCals = mockFirestore[`users/${uid}`].nutritionPlan.dailyCalories;
    await myFunctions.logNutritionFeedback({ ateOffPlan: true }, context);
    const newCals = mockFirestore[`users/${uid}`].nutritionPlan.dailyCalories;
    assert.equal(newCals, initialCals - 200, "Calories should decrease by 200");
    console.log(`✅ Calories adjusted: ${initialCals} -> ${newCals}`);

    console.log("\n>>> VERIFICATION SUCCESSFUL <<<");
}

runVerification().catch(e => { console.error(e); process.exit(1); });
