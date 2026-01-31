import { ScrollView, Text, View, TouchableOpacity } from "react-native";
import { useState, useEffect } from "react";
import { useRouter } from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useFocusEffect } from "@react-navigation/native";
import { useCallback } from "react";
import { ScreenContainer } from "@/components/screen-container";
import { Card } from "@/components/ui/card";
import { mockWeekWorkouts, type Exercise, type Workout } from "@/lib/mock-data";
import { saveWorkoutToHistory, getExerciseWorkoutData, type WorkoutExercise } from "@/lib/workout-history";

// Helper function to get next training day date
function getNextTrainingDayDate(dayName: string): string {
  const today = new Date(2026, 0, 31); // Saturday, Jan 31, 2026
  const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const targetDayIndex = daysOfWeek.indexOf(dayName);
  const currentDayIndex = today.getDay();
  
  let daysUntilTarget = targetDayIndex - currentDayIndex;
  if (daysUntilTarget <= 0) {
    daysUntilTarget += 7; // Next week
  }
  
  const targetDate = new Date(today);
  targetDate.setDate(today.getDate() + daysUntilTarget);
  
  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  return `${dayName}, ${monthNames[targetDate.getMonth()]} ${targetDate.getDate()}`;
}

export default function TrainingScreen() {
  const router = useRouter();
  const [selectedWorkoutIndex, setSelectedWorkoutIndex] = useState(0);
  const [exercises, setExercises] = useState<Exercise[]>(mockWeekWorkouts[0].exercises);

  // Load exercise completion status from AsyncStorage
  const loadExerciseStatus = useCallback(async () => {
    try {
      const currentWorkout = mockWeekWorkouts[selectedWorkoutIndex];
      const updatedExercises = await Promise.all(
        currentWorkout.exercises.map(async (exercise) => {
          const completed = await AsyncStorage.getItem(`exercise_${exercise.id}_completed`);
          return { ...exercise, completed: completed === "true" };
        })
      );
      setExercises(updatedExercises);
    } catch (error) {
      console.error("Error loading exercise status:", error);
    }
  }, [selectedWorkoutIndex]);

  // Reload status when screen comes into focus or workout changes
  useFocusEffect(
    useCallback(() => {
      loadExerciseStatus();
    }, [loadExerciseStatus])
  );

  useEffect(() => {
    loadExerciseStatus();
  }, [selectedWorkoutIndex, loadExerciseStatus]);

  const toggleExercise = async (id: string) => {
    setExercises(prev => {
      const updated = prev.map(ex => {
        if (ex.id === id) {
          const newCompleted = !ex.completed;
          // Update AsyncStorage
          AsyncStorage.setItem(`exercise_${id}_completed`, newCompleted.toString()).catch(err =>
            console.error("Error saving exercise status:", err)
          );
          return { ...ex, completed: newCompleted };
        }
        return ex;
      });
      return updated;
    });
  };

  const completedCount = exercises.filter(ex => ex.completed).length;
  const totalCount = exercises.length;
  const currentWorkout = mockWeekWorkouts[selectedWorkoutIndex];

  const handleCompleteWorkout = async () => {
    try {
      // Collect workout data for all exercises
      const workoutExercises: WorkoutExercise[] = await Promise.all(
        exercises.map(async (exercise) => {
          const sets = await getExerciseWorkoutData(exercise.id);
          return {
            id: exercise.id,
            name: exercise.name,
            sets: sets || [],
          };
        })
      );

      // Save to history
      await saveWorkoutToHistory(currentWorkout.day, workoutExercises);

      // Clear completion status for next workout
      await Promise.all(
        exercises.map(ex => AsyncStorage.removeItem(`exercise_${ex.id}_completed`))
      );
      await Promise.all(
        exercises.map(ex => AsyncStorage.removeItem(`exercise_${ex.id}_data`))
      );

      // Reload exercises
      await loadExerciseStatus();

      // Show success message (optional: add a toast/alert here)
      alert("Workout completed and saved to history!");
    } catch (error) {
      console.error("Error completing workout:", error);
      alert("Failed to save workout. Please try again.");
    }
  };

  return (
    <ScreenContainer className="p-4">
      <ScrollView contentContainerStyle={{ flexGrow: 1, paddingBottom: 20 }}>
        <View className="flex-1 gap-6">
          {/* Header */}
          <View className="gap-2">
            <Text className="text-3xl font-bold text-foreground">Training</Text>
            <Text className="text-sm text-muted">
              {completedCount} of {totalCount} exercises completed
            </Text>
          </View>

          {/* Week Overview - Clickable Days */}
          <View className="gap-3">
            <Text className="text-base font-semibold text-foreground">This Week</Text>
            <View className="flex-row gap-2">
              {mockWeekWorkouts.map((workout, index) => (
                <TouchableOpacity
                  key={workout.id}
                  onPress={() => setSelectedWorkoutIndex(index)}
                  className={`flex-1 p-3 rounded-xl ${
                    index === selectedWorkoutIndex ? "" : "bg-surface border border-border"
                  }`}
                  style={{ backgroundColor: index === selectedWorkoutIndex ? '#E9B44C' : undefined }}
                >
                  <Text
                    className={`text-xs font-semibold ${
                      index === selectedWorkoutIndex ? "text-background" : "text-muted"
                    }`}
                  >
                    {workout.day}
                  </Text>
                  <Text
                    className={`text-base font-bold mt-1 ${
                      index === selectedWorkoutIndex ? "text-background" : "text-foreground"
                    }`}
                  >
                    {workout.exercises[0].muscleGroup}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* Selected Day Header with Date */}
          <View className="bg-surface rounded-xl p-4 border border-border">
            <Text className="text-sm text-muted">Training Day</Text>
            <Text className="text-2xl font-bold text-foreground mt-1">
              {getNextTrainingDayDate(currentWorkout.day)}
            </Text>
            <Text className="text-sm text-muted mt-1">
              {currentWorkout.exercises.length} exercises · {currentWorkout.exercises[0].muscleGroup} Focus
            </Text>
          </View>

          {/* Today's Exercises */}
          <View className="gap-3">
            <Text className="text-base font-semibold text-foreground">Exercises</Text>
            
            {exercises.map((exercise) => (
              <Card key={exercise.id} className={exercise.completed ? "opacity-60" : ""}>
                <TouchableOpacity
                  onPress={() => router.push(`/exercise/${exercise.id}`)}
                  className="flex-row items-center gap-3 flex-1 active:opacity-70"
                >
                    {/* Checkbox */}
                    <TouchableOpacity
                      onPress={(e) => {
                        e.stopPropagation();
                        toggleExercise(exercise.id);
                      }}
                      className="active:opacity-70"
                    >
                      <View
                        className={`w-6 h-6 rounded-full border-2 items-center justify-center ${
                          exercise.completed
                            ? "border-[#E9B44C]"
                            : "border-border"
                        }`}
                        style={{ backgroundColor: exercise.completed ? '#E9B44C' : 'transparent' }}
                      >
                        {exercise.completed && (
                          <Text className="text-background text-xs font-bold">✓</Text>
                        )}
                      </View>
                    </TouchableOpacity>

                    {/* Exercise Info */}
                    <View className="flex-1">
                      <Text
                        className={`text-base font-semibold ${
                          exercise.completed ? "line-through text-muted" : "text-foreground"
                        }`}
                      >
                        {exercise.name}
                      </Text>
                      <Text className="text-sm text-muted mt-1">
                        {exercise.muscleGroup} · {exercise.sets} sets × {exercise.reps} reps
                      </Text>
                    </View>

                    {/* Arrow */}
                    <Text className="text-muted text-lg">›</Text>
                </TouchableOpacity>
              </Card>
            ))}
          </View>

          {/* Complete Workout Button */}
          {completedCount === totalCount && totalCount > 0 && (
            <TouchableOpacity
              onPress={handleCompleteWorkout}
              className="bg-success py-4 rounded-xl active:opacity-80"
            >
              <Text className="text-background text-center font-bold text-base">
                Complete Workout & Save to History
              </Text>
            </TouchableOpacity>
          )}
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}
