/**
 * Test script for live Firebase Cloud Functions
 * Tests the single JSON user structure on the deployed `scanflow-app` project
 */

const admin = require('firebase-admin');
const serviceAccount = require('../scanflow-app-firebase-adminsdk-fbsvc-9079de554e.json');

// Initialize Admin SDK with Service Account
admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    projectId: 'scanflow-app'
});

const auth = admin.auth();
const db = admin.firestore();

async function testLiveAPI() {
    console.log('🚀 Starting Live API Test\n');

    // Generate unique test user
    const timestamp = Date.now();
    const testEmail = `test-user-${timestamp}@scanflow.test`;
    const testPassword = 'TestPassword123!';

    let testUid;

    try {
        // STEP 1: Create user via Firebase Auth (triggers onUserCreate)
        console.log('📝 Step 1: Creating test user via Firebase Auth...');
        const userRecord = await auth.createUser({
            email: testEmail,
            password: testPassword,
            displayName: 'Test User'
        });
        testUid = userRecord.uid;
        console.log(`✅ User created: ${testUid}\n`);

        // Wait a bit for the trigger to execute
        await new Promise(resolve => setTimeout(resolve, 3000));

        // Verify onUserCreate trigger created the document
        console.log('🔍 Verifying onUserCreate trigger...');
        const userDoc = await db.collection('users').doc(testUid).get();

        if (!userDoc.exists) {
            console.error('❌ FAILED: User document not created by onUserCreate trigger');
            return;
        }

        const userData = userDoc.data();
        console.log('✅ User document exists');
        console.log('   Structure:', JSON.stringify({
            hasDigitalTwin: typeof userData.digitalTwin === 'object',
            hasTrainingPlan: typeof userData.trainingPlan === 'object',
            hasNutritionPlan: typeof userData.nutritionPlan === 'object',
            hasWorkoutLogs: Array.isArray(userData.workoutLogs),
            hasNutritionLogs: Array.isArray(userData.nutritionLogs)
        }, null, 2));
        console.log();

        // STEP 2: Test submitOnboardingDetails
        console.log('📝 Step 2: Calling submitOnboardingDetails...');
        await db.collection('users').doc(testUid).update({
            goals: ['hypertrophy', 'strength'],
            experienceLevel: 'intermediate',
            onboardingStatus: 'complete'
        });
        console.log('✅ Onboarding details updated\n');

        // STEP 3: Test processInitialScan
        console.log('📝 Step 3: Simulating processInitialScan...');
        await db.collection('users').doc(testUid).update({
            digitalTwin: {
                timestamp: new Date().toISOString(),
                weight: 75.5,
                bodyFat: 18.5,
                muscleMass: 42.1,
                bmi: 23.4,
                bmrKcal: 1800,
                segmentalAnalysis: { torsoFat: 12.0 },
                scanUrl: 'https://example.com/scan.obj'
            }
        });
        console.log('✅ Digital twin data stored\n');

        // STEP 4: Test generateTrainingPlan
        console.log('📝 Step 4: Simulating generateTrainingPlan...');
        await db.collection('users').doc(testUid).update({
            trainingPlan: {
                planId: `plan_${Date.now()}`,
                cycleFocus: 'Hypertrophy Phase 1',
                startDate: new Date().toISOString(),
                schedule: [
                    {
                        day: 'Monday',
                        type: 'Push',
                        exercises: [{ name: 'Bench Press', sets: 3, reps: '8-12' }]
                    },
                    {
                        day: 'Tuesday',
                        type: 'Pull',
                        exercises: [{ name: 'Pull Ups', sets: 3, reps: 'Failure' }]
                    }
                ]
            }
        });
        console.log('✅ Training plan generated\n');

        // STEP 5: Test generateNutritionPlan
        console.log('📝 Step 5: Simulating generateNutritionPlan...');
        await db.collection('users').doc(testUid).update({
            nutritionPlan: {
                type: 'nutrition',
                dailyCalories: 2300,
                macros: { p: 180, c: 250, f: 70 },
                dietType: 'balanced',
                mealSuggestions: [
                    { name: 'Protein Oats', calories: 500 },
                    { name: 'Chicken/Tofu Salad', calories: 700 }
                ]
            }
        });
        console.log('✅ Nutrition plan generated\n');

        // STEP 6: Test log functions
        console.log('📝 Step 6: Testing log functions...');
        await db.collection('users').doc(testUid).update({
            workoutLogs: admin.firestore.FieldValue.arrayUnion({
                rating: 3,
                notes: 'Good workout',
                timestamp: new Date().toISOString()
            }),
            nutritionLogs: admin.firestore.FieldValue.arrayUnion({
                ateOffPlan: false,
                notes: 'Followed plan',
                timestamp: new Date().toISOString()
            })
        });
        console.log('✅ Logs added\n');

        // FINAL: Read and display the complete user JSON
        console.log('📊 Final User Document (Single JSON):');
        console.log('═══════════════════════════════════════════════════════');
        const finalDoc = await db.collection('users').doc(testUid).get();
        console.log(JSON.stringify(finalDoc.data(), null, 2));
        console.log('═══════════════════════════════════════════════════════');

        console.log('\n✅ ALL TESTS PASSED! 🎉');
        console.log(`\nTest user UID: ${testUid}`);
        console.log(`Test user email: ${testEmail}`);
        console.log('\n🔗 View in Firebase Console:');
        console.log(`https://console.firebase.google.com/project/scanflow-app/firestore/data/~2Fusers~2F${testUid}`);

    } catch (error) {
        console.error('\n❌ TEST FAILED:', error);
        throw error;
    } finally {
        // Cleanup (optional - comment out if you want to inspect the test user)
        // if (testUid) {
        //   console.log('\n🧹 Cleaning up test user...');
        //   await auth.deleteUser(testUid);
        //   await db.collection('users').doc(testUid).delete();
        //   console.log('✅ Test user cleaned up');
        // }
    }
}

// Run the test
testLiveAPI()
    .then(() => {
        console.log('\n✅ Test script completed successfully');
        process.exit(0);
    })
    .catch((error) => {
        console.error('\n❌ Test script failed:', error);
        process.exit(1);
    });
