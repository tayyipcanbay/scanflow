import { ScrollView, Text, View, TouchableOpacity } from "react-native";
import { useState, useEffect } from "react";
import { ScreenContainer } from "@/components/screen-container";
import { Card } from "@/components/ui/card";
import AsyncStorage from "@react-native-async-storage/async-storage";

interface WorkoutExercise {
  id: string;
  name: string;
  sets: {
    weight: string;
    reps: string;
  }[];
}

interface WorkoutHistory {
  id: string;
  date: string;
  dayName: string;
  exercises: WorkoutExercise[];
  totalVolume: number;
}

export default function HistoryScreen() {
  const [workouts, setWorkouts] = useState<WorkoutHistory[]>([]);
  const [expandedWorkout, setExpandedWorkout] = useState<string | null>(null);

  useEffect(() => {
    loadWorkoutHistory();
  }, []);

  const loadWorkoutHistory = async () => {
    try {
      const historyJson = await AsyncStorage.getItem("workout_history");
      if (historyJson) {
        const history: WorkoutHistory[] = JSON.parse(historyJson);
        // Sort by date, newest first
        history.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
        setWorkouts(history);
      }
    } catch (error) {
      console.error("Error loading workout history:", error);
    }
  };

  const toggleWorkout = (id: string) => {
    setExpandedWorkout(expandedWorkout === id ? null : id);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  return (
    <ScreenContainer className="p-4">
      <ScrollView contentContainerStyle={{ flexGrow: 1, paddingBottom: 20 }}>
        <View className="flex-1 gap-6">
          {/* Header */}
          <View>
            <Text className="text-3xl font-bold text-foreground">Workout History</Text>
            <Text className="text-sm text-muted mt-1">
              {workouts.length} workout{workouts.length !== 1 ? "s" : ""} completed
            </Text>
          </View>

          {/* Workouts List */}
          {workouts.length === 0 ? (
            <Card>
              <View className="items-center py-8">
                <Text className="text-6xl mb-4">💪</Text>
                <Text className="text-lg font-semibold text-foreground mb-2">
                  No Workouts Yet
                </Text>
                <Text className="text-sm text-muted text-center">
                  Complete your first workout to see it here!
                </Text>
              </View>
            </Card>
          ) : (
            <View className="gap-3">
              {workouts.map((workout) => (
                <Card key={workout.id} className="p-0 overflow-hidden">
                  <TouchableOpacity
                    onPress={() => toggleWorkout(workout.id)}
                    className="p-4 active:opacity-70"
                  >
                    <View className="flex-row items-center justify-between">
                      <View className="flex-1">
                        <Text className="text-lg font-bold text-foreground">
                          {workout.dayName}
                        </Text>
                        <Text className="text-sm text-muted mt-1">
                          {formatDate(workout.date)}
                        </Text>
                      </View>
                      <View className="items-end">
                        <Text className="text-sm text-muted">Total Volume</Text>
                        <Text className="text-xl font-bold text-primary">
                          {workout.totalVolume.toLocaleString()} kg
                        </Text>
                      </View>
                    </View>

                    <View className="flex-row items-center gap-2 mt-3">
                      <Text className="text-xs text-muted">
                        {workout.exercises.length} exercise{workout.exercises.length !== 1 ? "s" : ""}
                      </Text>
                      <Text className="text-xs text-muted">•</Text>
                      <Text className="text-xs text-muted">
                        {workout.exercises.reduce((sum, ex) => sum + ex.sets.length, 0)} sets
                      </Text>
                      <View className="flex-1" />
                      <Text className="text-muted">
                        {expandedWorkout === workout.id ? "▲" : "▼"}
                      </Text>
                    </View>
                  </TouchableOpacity>

                  {/* Expanded Exercise Details */}
                  {expandedWorkout === workout.id && (
                    <View className="border-t border-border bg-surface/50 p-4">
                      {workout.exercises.map((exercise, idx) => (
                        <View key={idx} className="mb-4 last:mb-0">
                          <Text className="text-base font-semibold text-foreground mb-2">
                            {exercise.name}
                          </Text>
                          {exercise.sets.map((set, setIdx) => (
                            <View
                              key={setIdx}
                              className="flex-row items-center justify-between py-2 border-b border-border/50 last:border-b-0"
                            >
                              <Text className="text-sm text-muted">
                                Set {setIdx + 1}
                              </Text>
                              <Text className="text-sm text-foreground">
                                {set.weight} kg × {set.reps} reps
                              </Text>
                            </View>
                          ))}
                        </View>
                      ))}
                    </View>
                  )}
                </Card>
              ))}
            </View>
          )}
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}
