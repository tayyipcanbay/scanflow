/**
 * Quick test for training plan updates via AI chat
 */

// Load environment variables from .env file
require('dotenv/config');

const admin = require('firebase-admin');
const serviceAccount = require('../scanflow-app-firebase-adminsdk-fbsvc-9079de554e.json');
const OpenAI = require('openai');

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    projectId: 'scanflow-app'
});

const db = admin.firestore();

async function testTrainingPlanUpdate() {
    console.log('💪 Testing Training Plan Update via AI Chat\n');

    const testUid = 'cJH6nr2IdVQ0OdCpcJz82BWzkGE3';

    try {
        // Get current user data
        const userDoc = await db.collection('users').doc(testUid).get();
        const userData = userDoc.data();

        console.log('📊 Current Training Plan:');
        console.log('───────────────────────────────────────');
        console.log(`Focus: ${userData.trainingPlan?.cycleFocus || 'Not set'}`);
        console.log('═══════════════════════════════════════\n');

        // Test prompts that should trigger training plan updates
        const testPrompts = [
            "I want to switch to a strength-focused training plan",
            "I'm injured and need to focus on recovery for a while",
            "Can you change my training to prioritize muscle building?"
        ];

        for (let i = 0; i < testPrompts.length; i++) {
            const message = testPrompts[i];
            console.log(`💬 Test ${i + 1}: "${message}"`);
            console.log('───────────────────────────────────────');

            const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

            const systemPrompt = `You are a personal AI fitness coach for the Scanflow app. You have access to the user's complete fitness profile.

User Profile:
- Digital Twin: ${JSON.stringify(userData.digitalTwin || {})}
- Training Plan: ${JSON.stringify(userData.trainingPlan || {})}
- Nutrition Plan: ${JSON.stringify(userData.nutritionPlan || {})}
- Goals: ${JSON.stringify(userData.goals || [])}

Your role:
- Answer questions about their fitness journey
- Provide personalized advice based on their data
- Suggest adjustments to training/nutrition plans
- Motivate and support the user

When you recommend changes to their plan, use the updateUserData function. Only update fields when necessary.`;

            const tools = [{
                type: "function",
                function: {
                    name: "updateUserData",
                    description: "Update user's training or nutrition plan based on recommendations",
                    parameters: {
                        type: "object",
                        properties: {
                            trainingPlanCycleFocus: {
                                type: "string",
                                description: "New cycle focus for training plan (e.g., 'Strength Phase', 'Hypertrophy', 'Deload', 'Injury Recovery', 'Muscle Building')"
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
            }];

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

            console.log('🤖 AI Response:');
            console.log(textResponse);

            // Check for updates
            if (response.tool_calls && response.tool_calls.length > 0) {
                const toolCall = response.tool_calls[0];
                if (toolCall.function.name === "updateUserData") {
                    const args = JSON.parse(toolCall.function.arguments);

                    console.log('\n✅ AI is updating training plan:');
                    console.log(`   New Focus: ${args.trainingPlanCycleFocus || '(no change)'}`);
                    console.log(`   Reason: ${args.reason}`);

                    const updates = {};
                    if (args.trainingPlanCycleFocus) {
                        updates["trainingPlan.cycleFocus"] = args.trainingPlanCycleFocus;
                    }
                    if (args.goals) {
                        updates.goals = args.goals;
                    }

                    if (Object.keys(updates).length > 0) {
                        await db.collection("users").doc(testUid).update(updates);
                        console.log('   ✓ Applied to Firestore');
                    }
                }
            } else {
                console.log('\nℹ️  No training plan updates suggested by AI');
            }

            console.log('═══════════════════════════════════════\n');

            // Wait between requests
            if (i < testPrompts.length - 1) {
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
        }

        // Show final state
        const finalDoc = await db.collection('users').doc(testUid).get();
        const finalData = finalDoc.data();

        console.log('📊 Final Training Plan:');
        console.log('───────────────────────────────────────');
        console.log(`Focus: ${finalData.trainingPlan?.cycleFocus || 'Not set'}`);
        console.log(`Goals: ${JSON.stringify(finalData.goals || [])}`);
        console.log('═══════════════════════════════════════\n');

        console.log('✅ Training plan update test complete! 🎉');
        console.log(`\n🔗 View in Firestore: https://console.firebase.google.com/project/scanflow-app/firestore/data/~2Fusers~2F${testUid}`);

    } catch (error) {
        console.error('❌ Test failed:', error);
    } finally {
        process.exit(0);
    }
}

testTrainingPlanUpdate();
