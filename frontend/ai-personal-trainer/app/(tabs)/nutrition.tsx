import { ScrollView, Text, View, TouchableOpacity } from "react-native";
import { ScreenContainer } from "@/components/screen-container";
import { Card } from "@/components/ui/card";
import { ProgressBar } from "@/components/ui/progress-bar";
import { mockMacroGoals, mockMacroProgress, mockMealSuggestions } from "@/lib/mock-data";

export default function NutritionScreen() {
  return (
    <ScreenContainer className="p-4">
      <ScrollView contentContainerStyle={{ flexGrow: 1, paddingBottom: 20 }}>
        <View className="flex-1 gap-6">
          {/* Header */}
          <View className="gap-2">
            <Text className="text-3xl font-bold text-foreground">Nutrition</Text>
            <Text className="text-sm text-muted">Your daily nutrition goals</Text>
          </View>

          {/* Macro Goals Card */}
          <Card>
            <View className="gap-3">
              <Text className="text-lg font-bold text-foreground">Macros Today</Text>
              
              <View className="gap-2">
                <ProgressBar
                  value={mockMacroProgress.protein}
                  max={mockMacroGoals.protein}
                  label="Protein"
                  color="primary"
                />
                <ProgressBar
                  value={mockMacroProgress.carbs}
                  max={mockMacroGoals.carbs}
                  label="Carbs"
                  color="warning"
                />
                <ProgressBar
                  value={mockMacroProgress.fats}
                  max={mockMacroGoals.fats}
                  label="Fats"
                  color="success"
                />
              </View>

              <View className="bg-primary/10 p-4 rounded-lg border border-primary/30" style={{ marginTop: 8 }}>
                <View className="flex-row justify-between items-center">
                  <Text className="text-sm text-foreground font-semibold">Calories</Text>
                  <Text className="text-lg font-bold text-primary">
                    {mockMacroProgress.calories} / {mockMacroGoals.calories}
                  </Text>
                </View>
                <View className="mt-2 h-2 bg-border/30 rounded-full overflow-hidden">
                  <View
                    className="h-full bg-primary rounded-full"
                    style={{ width: `${(mockMacroProgress.calories / mockMacroGoals.calories) * 100}%` }}
                  />
                </View>
              </View>
            </View>
          </Card>

          {/* AI Recommendation */}
          <Card className="bg-primary/10 border-primary/30">
            <View className="gap-2">
              <View className="flex-row items-center gap-2">
                <View className="bg-primary w-8 h-8 rounded-full items-center justify-center">
                  <Text className="text-background font-bold text-sm">AI</Text>
                </View>
                <Text className="text-base font-bold text-foreground">Recommendation</Text>
              </View>
              
              <Text className="text-sm text-foreground leading-relaxed">
                Your protein intake is optimal for muscle building. Make sure to distribute the remaining 55g of protein evenly throughout the day. You should consume carbohydrates especially around your training.
              </Text>
            </View>
          </Card>

          {/* Meal Suggestions */}
          <View className="gap-3">
            <Text className="text-base font-semibold text-foreground">Meal Suggestions</Text>
            
            {mockMealSuggestions.map((meal) => (
              <Card key={meal.id}>
                <View className="gap-2">
                  <View className="flex-row justify-between items-start">
                    <View className="flex-1">
                      <Text className="text-base font-semibold text-foreground">
                        {meal.name}
                      </Text>
                      <Text className="text-sm text-muted mt-1">
                        {meal.description}
                      </Text>
                    </View>
                    <View className="bg-primary/20 px-2 py-1 rounded-lg">
                      <Text className="text-primary text-xs font-bold">
                        {meal.calories} kcal
                      </Text>
                    </View>
                  </View>

                  <View className="flex-row gap-3 mt-2">
                    <View className="flex-1 bg-border/20 p-2 rounded-lg">
                      <Text className="text-xs text-muted">Protein</Text>
                      <Text className="text-sm font-bold text-primary">{meal.protein}g</Text>
                    </View>
                    <View className="flex-1 bg-border/20 p-2 rounded-lg">
                      <Text className="text-xs text-muted">Carbs</Text>
                      <Text className="text-sm font-bold text-warning">{meal.carbs}g</Text>
                    </View>
                    <View className="flex-1 bg-border/20 p-2 rounded-lg">
                      <Text className="text-xs text-muted">Fats</Text>
                      <Text className="text-sm font-bold text-success">{meal.fats}g</Text>
                    </View>
                  </View>
                </View>
              </Card>
            ))}
          </View>

          {/* Add Meal Button */}
          <TouchableOpacity className="py-4 rounded-xl active:opacity-80" style={{ backgroundColor: '#E9B44C' }}>
            <Text className="text-background text-center font-bold text-base">
              Add Meal
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}
