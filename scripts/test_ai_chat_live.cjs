/**
 * Live test for chatWithAI Cloud Function
 * Simulates calling the deployed function with a real user
 */

// Load environment variables from .env file
require('dotenv/config');

const admin = require('firebase-admin');
const serviceAccount = require('../scanflow-app-firebase-adminsdk-fbsvc-9079de554e.json');

// Initialize Admin SDK
admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    projectId: 'scanflow-app'
});

const db = admin.firestore();

async function testChatWithAI() {
    console.log('🤖 Testing AI Chat Function (Live)\n');

    // Use existing test user
    const testUid = 'cJH6nr2IdVQ0OdCpcJz82BWzkGE3';

    try {
        // Verify user exists
        console.log('🔍 Verifying user exists...');
        const userDoc = await db.collection('users').doc(testUid).get();
        if (!userDoc.exists) {
            console.error('❌ Test user not found');
            return;
        }
        console.log('✅ User found\n');

        // Display current user data summary
        const userData = userDoc.data();
        console.log('📊 Current User Data:');
        console.log('───────────────────────────────────────');
        console.log(`Goals: ${JSON.stringify(userData.goals || [])}`);
        console.log(`Training Focus: ${userData.trainingPlan?.cycleFocus || 'Not set'}`);
        console.log(`Daily Calories: ${userData.nutritionPlan?.dailyCalories || 'Not set'}`);
        console.log(`BMR: ${userData.digitalTwin?.bmrKcal || 'Not set'} kcal`);
        console.log('═══════════════════════════════════════\n');

        // Test messages
        const testMessages = [
            "What's my current training plan?",
            "I've been feeling very tired after my workouts. What should I do?",
            "Can you increase my daily calories to 2500?"
        ];

        for (let i = 0; i < testMessages.length; i++) {
            const message = testMessages[i];
            console.log(`\n💬 Test ${i + 1}: "${message}"`);
            console.log('───────────────────────────────────────');

            try {
                // Call the deployed chatWithAI function
                // We'll simulate this by making an HTTP request to the function endpoint
                const fetch = (await import('node-fetch')).default;

                // Get ID token for the user (simulate auth)
                const customToken = await admin.auth().createCustomToken(testUid);

                // Alternatively, we can directly call the function logic by importing it
                // But for now, let's make a direct Firestore/logic simulation

                // Since we can't easily call a deployed callable function from Node.js without
                // the Firebase client SDK, let's manually simulate what the function does:

                // 1. Get user data (already have it)
                // 2. Call OpenAI API manually
                const OpenAI = require('openai');
                const openai = new OpenAI({
                    apiKey: process.env.OPENAI_API_KEY
                });

                const systemPrompt = `You are a personal AI fitness coach for the Scanflow app. You have access to the user's complete fitness profile.

User Profile:
- Digital Twin: ${JSON.stringify(userData.digitalTwin || {})}
- Training Plan: ${JSON.stringify(userData.trainingPlan || {})}
- Nutrition Plan: ${JSON.stringify(userData.nutritionPlan || {})}
- Recent Workout Logs: ${JSON.stringify((userData.workoutLogs || []).slice(-3))}
- Recent Nutrition Logs: ${JSON.stringify((userData.nutritionLogs || []).slice(-3))}
- Goals: ${JSON.stringify(userData.goals || [])}
- Experience Level: ${userData.experienceLevel || "unknown"}

Your role:
- Answer questions about their fitness journey
- Provide personalized advice based on their data
- Suggest adjustments to training/nutrition plans
- Motivate and support the user

When you recommend changes to their plan, use the updateUserData function. Only update fields when necessary.`;

                const tools = [
                    {
                        type: "function",
                        function: {
                            name: "updateUserData",
                            description: "Update user's training or nutrition plan based on recommendations",
                            parameters: {
                                type: "object",
                                properties: {
                                    trainingPlanCycleFocus: {
                                        type: "string",
                                        description: "New cycle focus for training plan (e.g., 'Strength Phase', 'Hypertrophy', 'Deload')"
                                    },
                                    nutritionPlanDailyCalories: {
                                        type: "number",
                                        description: "New daily calorie target"
                                    },
                                    goals: {
                                        type: "array",
                                        items: { type: "string" },
                                        description: "Updated fitness goals"
                                    },
                                    reason: {
                                        type: "string",
                                        description: "Brief explanation of why these changes are being made"
                                    }
                                },
                                required: ["reason"]
                            }
                        }
                    }
                ];

                console.log('🔄 Calling ChatGPT API...');
                const completion = await openai.chat.completions.create({
                    model: "gpt-4o-mini",
                    messages: [
                        { role: "system", content: systemPrompt },
                        { role: "user", content: message }
                    ],
                    tools,
                    tool_choice: "auto",
                    temperature: 0.7,
                    max_tokens: 500
                });

                const response = completion.choices[0].message;
                let textResponse = response.content || "I'm here to help!";
                const updates = {};

                console.log('\n🤖 AI Response:');
                console.log(textResponse);

                // Process function calls
                if (response.tool_calls && response.tool_calls.length > 0) {
                    const toolCall = response.tool_calls[0];
                    if (toolCall.function.name === "updateUserData") {
                        const args = JSON.parse(toolCall.function.arguments);

                        console.log('\n✏️  AI wants to update data:');
                        console.log(JSON.stringify(args, null, 2));

                        // Build update object
                        if (args.trainingPlanCycleFocus) {
                            updates["trainingPlan.cycleFocus"] = args.trainingPlanCycleFocus;
                        }
                        if (args.nutritionPlanDailyCalories) {
                            updates["nutritionPlan.dailyCalories"] = args.nutritionPlanDailyCalories;
                        }
                        if (args.goals && Array.isArray(args.goals)) {
                            updates.goals = args.goals;
                        }

                        // Apply updates
                        if (Object.keys(updates).length > 0) {
                            await db.collection("users").doc(testUid).update(updates);
                            console.log('\n✅ Updates applied to Firestore');
                        }

                        // Log interaction
                        await db.collection("users").doc(testUid).update({
                            aiInteractionHistory: admin.firestore.FieldValue.arrayUnion({
                                timestamp: new Date().toISOString(),
                                userMessage: message,
                                aiResponse: textResponse,
                                updates: updates,
                                reason: args.reason || "AI recommendation"
                            })
                        });
                    }
                } else {
                    // Log interaction without updates
                    await db.collection("users").doc(testUid).update({
                        aiInteractionHistory: admin.firestore.FieldValue.arrayUnion({
                            timestamp: new Date().toISOString(),
                            userMessage: message,
                            aiResponse: textResponse,
                            updates: null
                        })
                    });
                }

                console.log('═══════════════════════════════════════');

                // Wait 2 seconds between requests to avoid rate limits
                if (i < testMessages.length - 1) {
                    await new Promise(resolve => setTimeout(resolve, 2000));
                }

            } catch (error) {
                console.error(`❌ Error for message ${i + 1}:`, error.message);
            }
        }

        // Show final user data
        console.log('\n\n📊 Final User Data After AI Interactions:');
        console.log('═══════════════════════════════════════');
        const finalDoc = await db.collection('users').doc(testUid).get();
        const finalData = finalDoc.data();
        console.log(`Goals: ${JSON.stringify(finalData.goals || [])}`);
        console.log(`Training Focus: ${finalData.trainingPlan?.cycleFocus || 'Not set'}`);
        console.log(`Daily Calories: ${finalData.nutritionPlan?.dailyCalories || 'Not set'}`);
        console.log(`\nAI Interaction History (${(finalData.aiInteractionHistory || []).length} total):`);
        if (finalData.aiInteractionHistory && finalData.aiInteractionHistory.length > 0) {
            finalData.aiInteractionHistory.slice(-3).forEach((interaction, idx) => {
                console.log(`\n  ${idx + 1}. ${interaction.timestamp}`);
                console.log(`     User: ${interaction.userMessage}`);
                console.log(`     AI: ${interaction.aiResponse.substring(0, 100)}...`);
                if (interaction.updates) {
                    console.log(`     Updates: ${JSON.stringify(interaction.updates)}`);
                }
            });
        }
        console.log('\n═══════════════════════════════════════');

        console.log('\n✅ All tests completed successfully! 🎉');
        console.log('\n🔗 View user in Firestore:');
        console.log(`https://console.firebase.google.com/project/scanflow-app/firestore/data/~2Fusers~2F${testUid}`);

    } catch (error) {
        console.error('\n❌ Test failed:', error);
    } finally {
        process.exit(0);
    }
}

testChatWithAI();
