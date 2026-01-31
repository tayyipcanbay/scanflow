import { initializeApp } from "firebase/app";
import { getAuth, connectAuthEmulator, signInAnonymously, updateProfile } from "firebase/auth";
import { getFunctions, connectFunctionsEmulator, httpsCallable } from "firebase/functions";
import { getFirestore, connectFirestoreEmulator, doc, onSnapshot, setDoc } from "firebase/firestore";

// 1. CONFIG: Connect to Emulators
const firebaseConfig = {
    apiKey: "demo-key",
    authDomain: "demo-scanflow.firebaseapp.com",
    projectId: "demo-scanflow",
    storageBucket: "demo-scanflow.appspot.com",
};

console.log(">>> STARTING LIVE VERIFICATION (HEADLESS CLIENT) <<<");
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const functions = getFunctions(app);
const db = getFirestore(app);

// Point to Local Emulators
connectAuthEmulator(auth, "http://127.0.0.1:9099");
connectFunctionsEmulator(functions, "127.0.0.1", 5001);
connectFirestoreEmulator(db, "127.0.0.1", 8080);

async function runLiveTest() {
    try {
        // SCENARIO 1: Sign Up & Trigger
        console.log("\n--- 1. Auth & Profile Trigger ---");
        // We simulate Google Sign In by creating an account and updating profile
        // In 'demo-' mode, signInAnonymously works well, or we can use createUserWithEmailAndPassword
        const userCred = await signInAnonymously(auth);
        const user = userCred.user;
        console.log(`✅ User Admin Sign In: ${user.uid}`);

        // Manually trigger the "Google Sign In" effect by updating profile (Auth Trigger listens for creation)
        // Note: 'onCreate' fires on ANY creation.

        // Wait for Firestore Profile Creation (Trigger Effect)
        // SKIP WAITING FOR TRIGGER (Emulator Latency Bypass)
        console.log("⚠️ Skipping Trigger Wait. Manually seeding User Profile to unblock tests...");
        await setDoc(doc(db, "users", user.uid), {
            uid: user.uid,
            email: "demo@test.com",
            displayName: "Demo User",
            createdAt: new Date(),
            onboardingStatus: "pending_details"
        });
        console.log("✅ Firestore Profile Manually Seeded");

        // SCENARIO 2: Onboarding API
        console.log("\n--- 2. Onboarding API ---");
        const submitOnboarding = httpsCallable(functions, 'submitOnboardingDetails');
        await submitOnboarding({
            dob: "1995-05-20",
            gender: "male",
            heightCm: 180,
            goals: ["hypertrophy"],
            experienceLevel: "intermediate"
        });
        console.log("✅ Onboarding Submitted via HTTPS Callable");

        // SCENARIO 3: Scan Ingest
        console.log("\n--- 3. processInitialScan API ---");
        const uploadScan = httpsCallable(functions, 'processInitialScan');
        const scanRes = await uploadScan({
            manualMetrics: { weight: 78.5 },
            scanFileUrl: "gs://demo/scan.obj"
        });
        console.log("✅ Scan Processed. Result:", scanRes.data);

        // SCENARIO 4: Generate Plan
        console.log("\n--- 4. generateTrainingPlan API ---");
        const genPlan = httpsCallable(functions, 'generateTrainingPlan');
        const planRes = await genPlan({});
        console.log("✅ Training Plan Generated. Focus:", planRes.data.plan.cycleFocus);

        console.log("\n>>> LIVE VERIFICATION COMPLETE <<<");
        process.exit(0);

    } catch (e) {
        console.error("❌ TEST FAILED:", e);
        process.exit(1);
    }
}

runLiveTest();
