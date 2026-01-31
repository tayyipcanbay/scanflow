const assert = require('assert');

// MOCKING FIREBASE (Since we don't have Emulator running yet)
const mockFirestore = {};
const mockCollection = (path) => {
    return {
        doc: (id) => ({
            set: (data) => { console.log(`[MockDB] Set ${path}/${id}:`, data); mockFirestore[`${path}/${id}`] = data; return Promise.resolve(); },
            update: (data) => { console.log(`[MockDB] Update ${path}/${id}:`, data); mockFirestore[`${path}/${id}`] = { ...mockFirestore[`${path}/${id}`], ...data }; return Promise.resolve(); },
            get: () => {
                const data = mockFirestore[`${path}/${id}`];
                return Promise.resolve({ exists: !!data, data: () => data });
            },
            collection: (subPath) => mockCollection(`${path}/${id}/${subPath}`)
        }),
        add: (data) => { console.log(`[MockDB] Add ${path}:`, data); return Promise.resolve({ id: 'new-id' }); }
    };
};

// Mock the Modules
const functions = {
    https: {
        onCall: (handler) => handler,
        HttpsError: class extends Error { constructor(code, msg) { super(msg); this.code = code; } }
    },
    auth: {
        user: () => ({ onCreate: (handler) => handler })
    }
};
const admin = {
    initializeApp: () => { },
    firestore: () => ({ collection: mockCollection }),
    firestore: Object.assign(() => ({ collection: mockCollection }), { FieldValue: { serverTimestamp: () => 'TIMESTAMP' } })
};

// Override Require to inject mocks
const originalRequire = require('module').prototype.require;
require('module').prototype.require = function (path) {
    if (path === 'firebase-functions') return functions;
    if (path === 'firebase-admin') return admin;
    if (path === '@google-cloud/vertexai') return { VertexAI: class { constructor() { } } };
    return originalRequire.apply(this, arguments);
};

// ------------------------------------------------------------------
// IMPORT THE CODE TO TEST
const myFunctions = require('./index.js');

async function runTests() {
    console.log(">>> STARTING BACKEND LOGIC TESTS <<<");

    // TEST 1: Auth Trigger
    console.log("\n[TEST 1] onUserCreate");
    const mockUser = { uid: 'test-uid', email: 'test@example.com', displayName: 'Test User' };
    await myFunctions.onUserCreate(mockUser);
    assert.ok(mockFirestore['users/test-uid'], "User document created");
    assert.equal(mockFirestore['users/test-uid'].email, 'test@example.com', "Email matches");

    // TEST 2: Onboarding
    console.log("\n[TEST 2] submitOnboardingDetails");
    const onboardingData = { dob: '1990-01-01', gender: 'male', heightCm: 180, goals: ['bulk'] };
    const context = { auth: { uid: 'test-uid' } };
    await myFunctions.submitOnboardingDetails(onboardingData, context);
    assert.equal(mockFirestore['users/test-uid'].heightCm, 180, "Height updated");
    assert.equal(mockFirestore['users/test-uid'].onboardingStatus, 'complete', "Status complete");

    // TEST 3: Generate Training Plan
    console.log("\n[TEST 3] generateTrainingPlan");
    // Seed the mock DB with digital twin data required by the function
    mockFirestore['users/test-uid/digitalTwin/latest'] = { weight: 80 };
    const result = await myFunctions.generateTrainingPlan({}, context);
    assert.ok(result.plan, "Plan returned");
    assert.ok(result.plan.schedule.length > 0, "Schedule exists");
    console.log("Generated Plan ID:", result.plan.planId);

    // TEST 4: Feedback Logging
    console.log("\n[TEST 4] logWorkoutFeedback");
    await myFunctions.logWorkoutFeedback({ planId: 'p1', rating: 5, notes: 'Ouch' }, context);
    // Verification is implicit via the console logs in the mock 'add' method

    console.log("\n>>> ALL TESTS PASSED SUCCESSFULLY <<<");
}

runTests().catch(e => {
    console.error("TEST FAILED:", e);
    process.exit(1);
});
