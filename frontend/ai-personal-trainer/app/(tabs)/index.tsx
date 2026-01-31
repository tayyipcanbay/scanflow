import { ScrollView, Text, View, TouchableOpacity, Image } from "react-native";
import { useState } from "react";
import { useRouter } from "expo-router";
import { ScreenContainer } from "@/components/screen-container";
import { Card } from "@/components/ui/card";
import { ProgressBar } from "@/components/ui/progress-bar";
import { mockUserProfile, mockTodayWorkout, mockMacroGoals, mockMacroProgress } from "@/lib/mock-data";
import { LinearGradient } from "expo-linear-gradient";

export default function HomeScreen() {
  const router = useRouter();
  // Set today as Saturday, January 31, 2026
  const [currentDate, setCurrentDate] = useState(new Date(2026, 0, 31)); // Month is 0-indexed
  
  const today = new Date().toLocaleDateString("en-US", { 
    weekday: "long", 
    day: "numeric", 
    month: "long", 
    year: "numeric" 
  });

  // Calendar helper functions
  const getDaysInMonth = (date: Date) => {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
  };

  const getFirstDayOfMonth = (date: Date) => {
    return new Date(date.getFullYear(), date.getMonth(), 1).getDay();
  };

  const isTrainingDay = (date: Date) => {
    const day = date.getDay();
    // Monday = 1, Wednesday = 3, Friday = 5
    return day === 1 || day === 3 || day === 5;
  };

  const isToday = (day: number) => {
    const today = new Date(2026, 0, 31);
    return (
      day === today.getDate() &&
      currentDate.getMonth() === today.getMonth() &&
      currentDate.getFullYear() === today.getFullYear()
    );
  };

  const navigateMonth = (direction: 'prev' | 'next') => {
    setCurrentDate(prev => {
      const newDate = new Date(prev);
      if (direction === 'prev') {
        newDate.setMonth(newDate.getMonth() - 1);
      } else {
        newDate.setMonth(newDate.getMonth() + 1);
      }
      return newDate;
    });
  };

  const monthName = currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });

  return (
    <View className="flex-1 bg-background">
      {/* Gradient Header */}
      <LinearGradient
        colors={['#0F1F2A', '#3b82f6']}
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
      <ScrollView className="flex-1" contentContainerStyle={{ paddingBottom: 100 }}>
        {/* 3D Body Model */}
        <View className="mb-6">
          {/* Upper Card - 3D Model */}
          <Card className="bg-gradient-to-br from-primary/20 to-secondary/20 border-primary/30 rounded-b-none mb-0">
            <View className="items-center py-6">
              <Image
                source={require("@/assets/images/male-body-model.png")}
                style={{ width: 180, height: 320 }}
                resizeMode="contain"
              />
            </View>
          </Card>
          
          {/* Lower Card - Body Stats (Clickable) */}
          <TouchableOpacity 
            onPress={() => router.push('/progress')}
            activeOpacity={0.7}
          >
            <Card className="bg-gradient-to-br from-primary/20 to-secondary/20 border-primary/30 rounded-t-none border-t-0">
              <View className="gap-3 py-4">
                <Text className="text-center text-sm font-semibold text-foreground">Measurements</Text>
                <View className="flex-row gap-6 justify-center">
                <View className="items-center">
                  <Text className="text-2xl font-bold text-foreground">
                    {mockUserProfile.currentScan.weight}
                  </Text>
                  <Text className="text-xs text-muted">kg</Text>
                </View>
                <View className="items-center">
                  <Text className="text-2xl font-bold text-foreground">
                    {mockUserProfile.currentScan.muscleMass}
                  </Text>
                  <Text className="text-xs text-muted">kg Muscle</Text>
                </View>
                <View className="items-center">
                  <Text className="text-2xl font-bold text-foreground">
                    {mockUserProfile.currentScan.bodyFat}
                  </Text>
                  <Text className="text-xs text-muted">% Fat</Text>
                </View>
                </View>
              </View>
            </Card>
          </TouchableOpacity>
        </View>

        <View className="px-6">
        {/* Quick Stats */}
        <View className="flex-row gap-3 mb-6">
          <TouchableOpacity 
            className="flex-1" 
            onPress={() => router.push('/nutrition')}
            activeOpacity={0.7}
          >
            <Card className="flex-1 p-4 bg-gradient-to-br from-orange/10 to-error/10 border-orange/20">
            <View className="flex-row items-center gap-2 mb-2">
              <Text className="text-orange text-lg">🔥</Text>
              <Text className="text-sm text-foreground">Calories Today</Text>
            </View>
            <Text className="text-2xl font-bold text-foreground">1,847</Text>
            <Text className="text-xs text-muted mt-1">Goal: 2,200</Text>
            <ProgressBar value={1847} max={2200} showPercentage={false} customColor="#E9B44C" className="mt-2" />
          </Card>
          </TouchableOpacity>

          <TouchableOpacity 
            className="flex-1" 
            onPress={() => router.push('/training')}
            activeOpacity={0.7}
          >
            <Card className="flex-1 p-4 bg-gradient-to-br from-green/10 to-success/10 border-green/20">
            <View className="flex-row items-center gap-2 mb-2">
              <Text className="text-green text-lg">⚡</Text>
              <Text className="text-sm text-foreground">Weekly Workouts</Text>
            </View>
            <Text className="text-2xl font-bold text-foreground">4/5</Text>
            <Text className="text-xs text-muted mt-1">Great streak!</Text>
            <ProgressBar value={4} max={5} showPercentage={false} customColor="#E9B44C" className="mt-2" />
          </Card>
          </TouchableOpacity>
        </View>

        {/* 30-Day Training Calendar */}
        <Card className="p-0 mb-6 overflow-hidden bg-surface/50">
          {/* Calendar Header */}
          <View className="flex-row items-center justify-between px-4 py-3 bg-surface/80">
            <TouchableOpacity 
              className="w-10 h-10 items-center justify-center rounded-full active:bg-surface"
              onPress={() => navigateMonth('prev')}
            >
              <Text className="text-foreground text-xl">‹</Text>
            </TouchableOpacity>
            <Text className="text-base font-bold text-foreground uppercase">{monthName}</Text>
            <TouchableOpacity 
              className="w-10 h-10 items-center justify-center rounded-full active:bg-surface"
              onPress={() => navigateMonth('next')}
            >
              <Text className="text-foreground text-xl">›</Text>
            </TouchableOpacity>
          </View>

          <View className="px-4 py-4">
            {/* Weekday Labels */}
            <View className="flex-row justify-between mb-3">
              {['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'].map((day) => (
                <View key={day} className="w-11 items-center">
                  <Text className="text-xs font-semibold text-muted">{day}</Text>
                </View>
              ))}
            </View>

            {/* Calendar Grid */}
            <View className="gap-2">
              {(() => {
                const daysInMonth = getDaysInMonth(currentDate);
                const firstDay = getFirstDayOfMonth(currentDate);
                // Adjust for Monday start (0 = Sunday, 1 = Monday, etc.)
                const startOffset = firstDay === 0 ? 6 : firstDay - 1;
                const totalCells = Math.ceil((daysInMonth + startOffset) / 7) * 7;
                const weeks = Math.ceil(totalCells / 7);

                return Array.from({ length: weeks }).map((_, weekIndex) => (
                  <View key={weekIndex} className="flex-row justify-between">
                    {Array.from({ length: 7 }).map((_, dayIndex) => {
                      const cellIndex = weekIndex * 7 + dayIndex;
                      const dayNumber = cellIndex - startOffset + 1;
                      
                      if (cellIndex < startOffset || dayNumber > daysInMonth) {
                        return <View key={dayIndex} className="w-11 h-11" />;
                      }
                      
                      const dayDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), dayNumber);
                      const isTodayDay = isToday(dayNumber);
                      const isTraining = isTrainingDay(dayDate);
                      
                      return (
                        <TouchableOpacity
                          key={dayIndex}
                          className={`w-11 h-11 rounded-lg items-center justify-center ${
                            isTodayDay ? '' : isTraining ? 'bg-success/20' : 'bg-transparent'
                          }`}
                          style={{ backgroundColor: isTodayDay ? '#E9B44C' : undefined }}
                          activeOpacity={0.7}
                        >
                          <Text className={`text-sm font-semibold ${
                            isTodayDay ? 'text-white' : 'text-foreground'
                          }`}>
                            {dayNumber}
                          </Text>
                          {isTraining && !isTodayDay && (
                            <View className="absolute bottom-1">
                              <View className="w-1 h-1 rounded-full bg-success" />
                            </View>
                          )}
                        </TouchableOpacity>
                      );
                    })}
                  </View>
                ));
              })()}
            </View>
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
          <TouchableOpacity className="w-full mt-4 py-3 rounded-xl active:opacity-80" style={{ backgroundColor: '#E9B44C' }}>
            <Text className="text-primary text-center font-semibold">Schedule Scan</Text>
          </TouchableOpacity>
        </Card>
        </View>
      </ScrollView>
    </View>
  );
}
