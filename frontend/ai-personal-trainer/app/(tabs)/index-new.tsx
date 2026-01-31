import { ScrollView, Text, View, TouchableOpacity, Image } from "react-native";
import { ScreenContainer } from "@/components/screen-container";
import { Card } from "@/components/ui/card";
import { ProgressBar } from "@/components/ui/progress-bar";
import { mockUserProfile, mockTodayWorkout, mockMacroGoals, mockMacroProgress } from "@/lib/mock-data";
import { LinearGradient } from "expo-linear-gradient";

export default function HomeScreen() {
  const today = new Date().toLocaleDateString("de-DE", { 
    weekday: "long", 
    day: "numeric", 
    month: "long", 
    year: "numeric" 
  });

  return (
    <View className="flex-1 bg-background">
      {/* Gradient Header */}
      <LinearGradient
        colors={['#8b5cf6', '#3b82f6']}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
        className="px-6 pt-12 pb-6"
      >
        <View className="flex-row items-center justify-between mb-6">
          <View>
            <Text className="text-white/80 text-sm">Welcome back,</Text>
            <Text className="text-white text-2xl font-bold">{mockUserProfile.name}</Text>
          </View>
          <View className="flex-row gap-3">
            <TouchableOpacity className="bg-white/20 backdrop-blur-sm p-2 rounded-full">
              <Text className="text-white text-lg">🔔</Text>
            </TouchableOpacity>
            <TouchableOpacity className="bg-white/20 backdrop-blur-sm p-2 rounded-full">
              <Text className="text-white text-lg">👤</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* AI Insight Card */}
        <Card className="bg-white/10 backdrop-blur-lg border-white/20 p-4">
          <View className="flex-row items-start gap-3">
            <View className="bg-white/20 p-2 rounded-lg">
              <Text className="text-white text-lg">✨</Text>
            </View>
            <View className="flex-1">
              <Text className="font-semibold text-white mb-1">Today's AI Insight</Text>
              <Text className="text-sm text-white/90">
                Great progress! You've lost 2.7kg since your last scan. Your muscle mass is increasing. Consider adding more protein today.
              </Text>
            </View>
          </View>
        </Card>
      </LinearGradient>

      {/* Content */}
      <ScrollView className="flex-1 px-6 -mt-4" contentContainerStyle={{ paddingBottom: 100 }}>
        {/* 3D Body Model */}
        <Card className="bg-gradient-to-br from-primary/20 to-secondary/20 border-primary/30 mb-6">
          <View className="items-center py-6 gap-4">
            <View className="w-full items-center">
              <Image
                source={require("@/assets/images/male-body-model.png")}
                style={{ width: 180, height: 320 }}
                resizeMode="contain"
              />
            </View>
            <View className="flex-row gap-6">
              <View className="items-center">
                <Text className="text-2xl font-bold text-foreground">
                  {mockUserProfile.currentScan.weight}
                </Text>
                <Text className="text-xs text-muted">kg</Text>
              </View>
              <View className="items-center">
                <Text className="text-2xl font-bold text-success">
                  {mockUserProfile.currentScan.muscleMass}
                </Text>
                <Text className="text-xs text-muted">kg Muscle</Text>
              </View>
              <View className="items-center">
                <Text className="text-2xl font-bold text-warning">
                  {mockUserProfile.currentScan.bodyFat}
                </Text>
                <Text className="text-xs text-muted">% Fat</Text>
              </View>
            </View>
          </View>
        </Card>

        {/* Quick Stats */}
        <View className="flex-row gap-3 mb-6">
          <Card className="flex-1 p-4 bg-gradient-to-br from-orange/10 to-error/10 border-orange/20">
            <View className="flex-row items-center gap-2 mb-2">
              <Text className="text-orange text-lg">🔥</Text>
              <Text className="text-sm text-foreground">Calories Today</Text>
            </View>
            <Text className="text-2xl font-bold text-foreground">1,847</Text>
            <Text className="text-xs text-muted mt-1">Goal: 2,200</Text>
            <ProgressBar value={1847} max={2200} showPercentage={false} className="mt-2" />
          </Card>

          <Card className="flex-1 p-4 bg-gradient-to-br from-green/10 to-success/10 border-green/20">
            <View className="flex-row items-center gap-2 mb-2">
              <Text className="text-green text-lg">⚡</Text>
              <Text className="text-sm text-foreground">Weekly Workouts</Text>
            </View>
            <Text className="text-2xl font-bold text-foreground">4/5</Text>
            <Text className="text-xs text-muted mt-1">Great streak!</Text>
            <ProgressBar value={4} max={5} showPercentage={false} className="mt-2" />
          </Card>
        </View>

        {/* Your Plans */}
        <Text className="font-semibold text-foreground mb-3 text-lg">Your Plans</Text>
        
        <Card className="p-4 mb-3">
          <View className="flex-row items-center gap-4">
            <View className="bg-primary/10 p-3 rounded-xl">
              <Text className="text-primary text-2xl">💪</Text>
            </View>
            <View className="flex-1">
              <Text className="font-semibold text-foreground">Training Plan</Text>
              <Text className="text-sm text-muted">Upper Body - Today</Text>
            </View>
            <Text className="text-muted">›</Text>
          </View>
        </Card>

        <Card className="p-4 mb-3">
          <View className="flex-row items-center gap-4">
            <View className="bg-green/10 p-3 rounded-xl">
              <Text className="text-green text-2xl">🍎</Text>
            </View>
            <View className="flex-1">
              <Text className="font-semibold text-foreground">Nutrition Plan</Text>
              <Text className="text-sm text-muted">High Protein - Week 4</Text>
            </View>
            <Text className="text-muted">›</Text>
          </View>
        </Card>

        <Card className="p-4 mb-6">
          <View className="flex-row items-center gap-4">
            <View className="bg-secondary/10 p-3 rounded-xl">
              <Text className="text-secondary text-2xl">📈</Text>
            </View>
            <View className="flex-1">
              <Text className="font-semibold text-foreground">Progress & Scans</Text>
              <Text className="text-sm text-muted">View transformation</Text>
            </View>
            <Text className="text-muted">›</Text>
          </View>
        </Card>

        {/* Next Scan CTA */}
        <Card className="p-5 bg-gradient-to-r from-primary to-secondary border-0 mb-6">
          <View className="flex-row items-center gap-4">
            <View className="bg-white/20 p-3 rounded-xl">
              <Text className="text-white text-2xl">📊</Text>
            </View>
            <View className="flex-1">
              <Text className="font-semibold text-white mb-1">Time for Your Next Scan</Text>
              <Text className="text-sm text-white/90">
                It's been 4 weeks. Update your data for better insights.
              </Text>
            </View>
          </View>
          <TouchableOpacity className="w-full mt-4 bg-white py-3 rounded-xl active:opacity-80">
            <Text className="text-primary text-center font-semibold">Schedule Scan</Text>
          </TouchableOpacity>
        </Card>
      </ScrollView>
    </View>
  );
}
