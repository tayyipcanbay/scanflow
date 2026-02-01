/**
 * Quick test: Switch training focus to fat loss
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

async function switchToFatLoss() {
    console.log('🔥 Switching Training Focus to Fat Loss\n');

    const testUid = 'cJH6nr2IdVQ0OdCpcJz82BWzkGE3';

    try {
        // Get current state
        const userDoc = await db.collection('users').doc(testUid).get();
        const userData = userDoc.data();

        console.log('📊 Before:');
        console.log(`   Training Focus: ${userData.trainingPlan?.cycleFocus}`);
        console.log(`   Daily Calories: ${userData.nutritionPlan?.dailyCalories}\n`);

        // Test message
        const message = "I want to lose fat. Can you update my training and nutrition plan?";
        console.log(`💬 User: "${message}"\n`);

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
                            description: "New cycle focus for training plan (e.g., 'Fat Loss', 'Cutting Phase', 'Strength Phase', 'Hypertrophy', 'Deload')"
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

        console.log('\n🤖 AI Response:');
        console.log(textResponse);

        // Check for updates
        if (response.tool_calls && response.tool_calls.length > 0) {
            const toolCall = response.tool_calls[0];
            if (toolCall.function.name === "updateUserData") {
                const args = JSON.parse(toolCall.function.arguments);

                console.log('\n✅ AI Updates:');
                if (args.trainingPlanCycleFocus) {
                    console.log(`   Training Focus: ${args.trainingPlanCycleFocus}`);
                }
                if (args.nutritionPlanDailyCalories) {
                    console.log(`   Daily Calories: ${args.nutritionPlanDailyCalories}`);
                }
                if (args.goals) {
                    console.log(`   Goals: ${JSON.stringify(args.goals)}`);
                }
                console.log(`   Reason: ${args.reason}`);

                const updates = {};
                if (args.trainingPlanCycleFocus) {
                    updates["trainingPlan.cycleFocus"] = args.trainingPlanCycleFocus;
                }
                if (args.nutritionPlanDailyCalories) {
                    updates["nutritionPlan.dailyCalories"] = args.nutritionPlanDailyCalories;
                }
                if (args.goals) {
                    updates.goals = args.goals;
                }

                if (Object.keys(updates).length > 0) {
                    await db.collection("users").doc(testUid).update(updates);
                    console.log('\n   ✓ Applied to Firestore');
                }

                // Log interaction
                await db.collection("users").doc(testUid).update({
                    aiInteractionHistory: admin.firestore.FieldValue.arrayUnion({
                        timestamp: new Date().toISOString(),
                        userMessage: message,
                        aiResponse: textResponse,
                        updates: updates,
                        reason: args.reason
                    })
                });
            }
        }

        // Show final state
        const finalDoc = await db.collection('users').doc(testUid).get();
        const finalData = finalDoc.data();

        console.log('\n📊 After:');
        console.log(`   Training Focus: ${finalData.trainingPlan?.cycleFocus}`);
        console.log(`   Daily Calories: ${finalData.nutritionPlan?.dailyCalories}`);
        console.log(`   Goals: ${JSON.stringify(finalData.goals || [])}`);

        console.log('\n✅ Fat loss training update complete! 🎉');
        console.log(`\n🔗 View in Firestore: https://console.firebase.google.com/project/scanflow-app/firestore/data/~2Fusers~2F${testUid}`);

    } catch (error) {
        console.error('❌ Test failed:', error);
    } finally {
        process.exit(0);
    }
}

switchToFatLoss();
