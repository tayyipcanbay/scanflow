import { ScrollView, Text, View, TouchableOpacity, TextInput, Image } from "react-native";
import { useState, useEffect } from "react";
import { useLocalSearchParams, useRouter } from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { ScreenContainer } from "@/components/screen-container";
import { Card } from "@/components/ui/card";

interface SetData {
  setNumber: number;
  weight: string;
  reps: string;
  completed: boolean;
}

const exerciseData: Record<string, { name: string; muscleGroup: string; image: any; sets: number; targetReps: string }> = {
  "bench-press": {
    name: "Bench Press",
    muscleGroup: "Chest",
    image: require("@/assets/images/bench-press.png"),
    sets: 4,
    targetReps: "8-12",
  },
  "incline-press": {
    name: "Incline Bench Press",
    muscleGroup: "Upper Chest",
    image: require("@/assets/images/incline-press.png"),
    sets: 3,
    targetReps: "10-12",
  },
  "dumbbell-flys": {
    name: "Dumbbell Flys",
    muscleGroup: "Chest",
    image: require("@/assets/images/dumbbell-flys.png"),
    sets: 3,
    targetReps: "12-15",
  },
  "tricep-dips": {
    name: "Tricep Dips",
    muscleGroup: "Triceps",
    image: require("@/assets/images/tricep-dips.png"),
    sets: 3,
    targetReps: "10-15",
  },
  "tricep-pushdowns": {
    name: "Tricep Pushdowns",
    muscleGroup: "Triceps",
    image: require("@/assets/images/tricep-pushdowns.png"),
    sets: 3,
    targetReps: "12-15",
  },
  "squats": {
    name: "Barbell Squats",
    muscleGroup: "Legs",
    image: require("@/assets/images/squats.png"),
    sets: 4,
    targetReps: "8-12",
  },
  "leg-press": {
    name: "Leg Press",
    muscleGroup: "Legs",
    image: require("@/assets/images/leg-press.png"),
    sets: 3,
    targetReps: "10-12",
  },
  "leg-curls": {
    name: "Leg Curls",
    muscleGroup: "Hamstrings",
    image: require("@/assets/images/leg-curls.png"),
    sets: 3,
    targetReps: "12-15",
  },
  "calf-raises": {
    name: "Calf Raises",
    muscleGroup: "Calves",
    image: require("@/assets/images/calf-raises.png"),
    sets: 4,
    targetReps: "15-20",
  },
  "pull-ups": {
    name: "Pull-Ups",
    muscleGroup: "Back",
    image: require("@/assets/images/pull-ups.png"),
    sets: 4,
    targetReps: "8-12",
  },
  "barbell-rows": {
    name: "Barbell Rows",
    muscleGroup: "Back",
    image: require("@/assets/images/barbell-rows.png"),
    sets: 4,
    targetReps: "8-12",
  },
  "lat-pulldown": {
    name: "Lat Pulldown",
    muscleGroup: "Lats",
    image: require("@/assets/images/lat-pulldown.png"),
    sets: 3,
    targetReps: "10-12",
  },
  "bicep-curls": {
    name: "Bicep Curls",
    muscleGroup: "Biceps",
    image: require("@/assets/images/bicep-curls.png"),
    sets: 3,
    targetReps: "12-15",
  },
};

export default function ExerciseDetailScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const exercise = exerciseData[id || "bench-press"];

  const [sets, setSets] = useState<SetData[]>(
    Array.from({ length: exercise.sets }, (_, i) => ({
      setNumber: i + 1,
      weight: "",
      reps: "",
      completed: false,
    }))
  );

  const updateSet = (index: number, field: "weight" | "reps", value: string) => {
    setSets((prev) =>
      prev.map((set, i) => {
        if (i === index) {
          const updatedSet = { ...set, [field]: value };
          // Auto-complete set if both weight and reps are filled
          if (updatedSet.weight && updatedSet.reps) {
            updatedSet.completed = true;
          }
          return updatedSet;
        }
        return set;
      })
    );
  };

  const toggleSetComplete = (index: number) => {
    setSets((prev) =>
      prev.map((set, i) =>
        i === index ? { ...set, completed: !set.completed } : set
      )
    );
  };

  const allSetsCompleted = sets.every((set) => set.completed);

  const addSet = () => {
    setSets((prev) => [
      ...prev,
      {
        setNumber: prev.length + 1,
        weight: "",
        reps: "",
        completed: false,
      },
    ]);
  };

  const removeSet = () => {
    if (sets.length > 1) {
      setSets((prev) => prev.slice(0, -1));
    }
  };

  // Auto-mark exercise as completed when all sets are done
  useEffect(() => {
    const markExerciseComplete = async () => {
      if (allSetsCompleted && sets.length > 0) {
        try {
          await AsyncStorage.setItem(`exercise_${id}_completed`, "true");
          // Save workout data (weight and reps for each set)
          const workoutData = sets.map(set => ({
            weight: set.weight,
            reps: set.reps,
          }));
          await AsyncStorage.setItem(`exercise_${id}_data`, JSON.stringify(workoutData));
        } catch (error) {
          console.error("Error saving exercise completion:", error);
        }
      }
    };
    markExerciseComplete();
  }, [allSetsCompleted, id, sets]);

  return (
    <ScreenContainer className="p-4">
      <ScrollView contentContainerStyle={{ flexGrow: 1, paddingBottom: 20 }}>
        <View className="flex-1 gap-6">
          {/* Header */}
          <View className="flex-row items-center gap-3">
            <TouchableOpacity
              onPress={() => router.back()}
              className="w-10 h-10 items-center justify-center rounded-full bg-surface active:opacity-70"
            >
              <Text className="text-foreground text-xl">←</Text>
            </TouchableOpacity>
            <View className="flex-1">
              <Text className="text-2xl font-bold text-foreground">{exercise.name}</Text>
              <Text className="text-sm text-muted">{exercise.muscleGroup}</Text>
            </View>
          </View>

          {/* Exercise Image */}
          <Card className="p-4 items-center">
            <Image
              source={exercise.image}
              style={{ width: 300, height: 300 }}
              resizeMode="contain"
            />
          </Card>

          {/* Target Info */}
          <Card>
            <View className="flex-row justify-between items-center">
              <View>
                <Text className="text-sm text-muted">Target Sets</Text>
                <Text className="text-xl font-bold text-foreground">{exercise.sets}</Text>
              </View>
              <View>
                <Text className="text-sm text-muted">Target Reps</Text>
                <Text className="text-xl font-bold text-foreground">{exercise.targetReps}</Text>
              </View>
            </View>
          </Card>

          {/* Sets Tracking */}
          <View className="gap-3">
            <View className="flex-row items-center justify-between">
              <Text className="text-lg font-bold text-foreground">Track Your Sets</Text>
              <View className="flex-row gap-2">
                <TouchableOpacity
                  onPress={removeSet}
                  className="px-3 py-2 rounded-lg active:opacity-70"
                  disabled={sets.length <= 1}
                  style={{ backgroundColor: '#0F1F2A', opacity: sets.length <= 1 ? 0.3 : 1 }}
                >
                  <Text className="text-white text-xs font-semibold">Remove Set</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  onPress={addSet}
                  className="px-3 py-2 rounded-lg active:opacity-70"
                  style={{ backgroundColor: '#E9B44C' }}
                >
                  <Text className="text-primary text-xs font-semibold">Add Set</Text>
                </TouchableOpacity>
              </View>
            </View>

            {sets.map((set, index) => (
              <Card key={index} className={set.completed ? "opacity-60" : ""}>
                <View className="gap-3">
                  <View className="flex-row items-center justify-between">
                    <Text className="text-base font-semibold text-foreground">
                      Set {set.setNumber}
                    </Text>
                    <TouchableOpacity
                      onPress={() => toggleSetComplete(index)}
                      className="active:opacity-70"
                    >
                      <View
                        className={`w-6 h-6 rounded-full border-2 items-center justify-center $\{
                          set.completed
                            ? "bg-success border-success"
                            : "border-border"
                        }`}
                      >
                        {set.completed && (
                          <Text className="text-background text-xs font-bold">✓</Text>
                        )}
                      </View>
                    </TouchableOpacity>
                  </View>

                  <View className="flex-row gap-3">
                    <View className="flex-1">
                      <Text className="text-xs text-muted mb-2">Weight (kg)</Text>
                      <TextInput
                        value={set.weight}
                        onChangeText={(value) => updateSet(index, "weight", value)}
                        keyboardType="numeric"
                        placeholder="0"
                        placeholderTextColor="#687076"
                        className="bg-surface border border-border rounded-lg px-4 py-3 text-foreground"
                      />
                    </View>
                    <View className="flex-1">
                      <Text className="text-xs text-muted mb-2">Reps</Text>
                      <TextInput
                        value={set.reps}
                        onChangeText={(value) => updateSet(index, "reps", value)}
                        keyboardType="numeric"
                        placeholder="0"
                        placeholderTextColor="#687076"
                        className="bg-surface border border-border rounded-lg px-4 py-3 text-foreground"
                      />
                    </View>
                  </View>
                </View>
              </Card>
            ))}
          </View>

          {/* Complete Exercise Button */}
          {allSetsCompleted && (
            <TouchableOpacity
              onPress={() => router.back()}
              className="bg-success py-4 rounded-xl active:opacity-80"
            >
              <Text className="text-background text-center font-bold text-base">
                Complete Exercise
              </Text>
            </TouchableOpacity>
          )}
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}
