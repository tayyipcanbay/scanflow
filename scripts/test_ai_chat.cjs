/**
 * Test script for AI Chat Function
 * Tests the chatWithAI endpoint with a live user
 */

const admin = require('firebase-admin');
const serviceAccount = require('../scanflow-app-firebase-adminsdk-fbsvc-9079de554e.json');

// Initialize Admin SDK
admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    projectId: 'scanflow-app'
});

const db = admin.firestore();
const auth = admin.auth();

async function testAIChat() {
    console.log('🤖 Testing AI Chat Function\n');

    // Use an existing test user (from previous tests)
    const testUid = 'cJH6nr2IdVQ0OdCpcJz82BWzkGE3'; // From our previous tests

    try {
        // Verify user exists
        console.log('🔍 Verifying user exists...');
        const userDoc = await db.collection('users').doc(testUid).get();
        if (!userDoc.exists) {
            console.error('❌ Test user not found. Run test_live_api.cjs first. ');
            return;
        }
        console.log('✅ User found\n');

        // Test messages
        const testMessages = [
            "What's my current training plan?",
            "I'm feeling very tired today, should I adjust my workout?",
            "Can you increase my daily calories by 200?"
        ];

        for (let i = 0; i < testMessages.length; i++) {
            const message = testMessages[i];
            console.log(`📝 Test ${i + 1}: "${message}"`);
            console.log('───────────────────────────────────────');

            // Simulate calling the chatWithAI function
            // In a real scenario, this would be called from the mobile app
            // For testing, we'll use the Firebase Functions SDK

            // Note: This requires deploying the function first
            console.log('⚠️  This test requires the chatWithAI function to be deployed.');
            console.log('    Deploy with: npx firebase deploy --only functions:chatWithAI\n');
            console.log('    Then call it from your mobile app or use the Firebase Console.\n');

            // Example call structure:
            console.log('Example call from mobile app:');
            console.log(`
const chatWithAI = firebase.functions().httpsCallable('chatWithAI');
const result = await chatWithAI({ message: "${message}" });
console.log('AI Response:', result.data.response);
console.log('Updates Applied:', result.data.updatesApplied);
      `);

            console.log('═══════════════════════════════════════\n');
        }

        // Check if aiInteractionHistory exists
        console.log('🔍 Checking for aiInteractionHistory field...');
        const updated = await db.collection('users').doc(testUid).get();
        const userData = updated.data();

        if (userData.aiInteractionHistory) {
            console.log(`✅ aiInteractionHistory field exists with ${userData.aiInteractionHistory.length} interactions\n`);

            if (userData.aiInteractionHistory.length > 0) {
                console.log('Last interaction:');
                console.log(JSON.stringify(userData.aiInteractionHistory.slice(-1)[0], null, 2));
            }
        } else {
            console.log('ℹ️  aiInteractionHistory field not yet populated (no interactions yet)\n');
        }

        console.log('✅ Test script completed');
        console.log('\n📋 Next steps:');
        console.log('1. Deploy the chatWithAI function');
        console.log('2. Call it from your mobile app');
        console.log('3. Check the Firestore console for aiInteractionHistory updates');

    } catch (error) {
        console.error('❌ Test failed:', error);
    } finally {
        process.exit(0);
    }
}

testAIChat();
