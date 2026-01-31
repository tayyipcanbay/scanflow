import { initializeApp, getApps, getApp } from 'firebase/app';
import { getAuth, connectAuthEmulator } from 'firebase/auth';
import { getFirestore, connectFirestoreEmulator } from 'firebase/firestore';
import { getFunctions, connectFunctionsEmulator } from 'firebase/functions';

const firebaseConfig = {
  apiKey: "demo-key",
  authDomain: "demo-scanflow.firebaseapp.com",
  projectId: "demo-scanflow",
  storageBucket: "demo-scanflow.appspot.com",
};

// Initialize Firebase
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();

// Initialize services
const auth = getAuth(app);
const firestore = getFirestore(app);
const functions = getFunctions(app);

// Connect to emulators (only in development)
// IMPORTANT: Uncomment these lines when Firebase emulators are running locally
// if (__DEV__) {
//   try {
//     connectAuthEmulator(auth, "http://127.0.0.1:9099", { disableWarnings: true });
//     connectFirestoreEmulator(firestore, "127.0.0.1", 8080);
//     connectFunctionsEmulator(functions, "127.0.0.1", 5001);
//     console.log("✅ Connected to Firebase emulators");
//   } catch (error) {
//     console.warn("⚠️ Firebase emulators already connected or not available:", error);
//   }
// }
console.log("🔥 Firebase initialized (emulators disabled - enable in lib/firebase.ts when ready)");

export { app, auth, firestore, functions };
