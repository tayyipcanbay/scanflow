import AsyncStorage from "@react-native-async-storage/async-storage";

export interface WorkoutExercise {
  id: string;
  name: string;
  sets: {
    weight: string;
    reps: string;
  }[];
}

export interface WorkoutHistory {
  id: string;
  date: string;
  dayName: string;
  exercises: WorkoutExercise[];
  totalVolume: number;
}

/**
 * Save a completed workout to history
 */
export async function saveWorkoutToHistory(
  dayName: string,
  exercises: WorkoutExercise[]
): Promise<void> {
  try {
    // Calculate total volume (weight × reps for all sets)
    const totalVolume = exercises.reduce((total, exercise) => {
      const exerciseVolume = exercise.sets.reduce((sum, set) => {
        const weight = parseFloat(set.weight) || 0;
        const reps = parseFloat(set.reps) || 0;
        return sum + weight * reps;
      }, 0);
      return total + exerciseVolume;
    }, 0);

    const workout: WorkoutHistory = {
      id: `workout_${Date.now()}`,
      date: new Date().toISOString(),
      dayName,
      exercises,
      totalVolume: Math.round(totalVolume),
    };

    // Load existing history
    const historyJson = await AsyncStorage.getItem("workout_history");
    const history: WorkoutHistory[] = historyJson ? JSON.parse(historyJson) : [];

    // Add new workout
    history.push(workout);

    // Save updated history
    await AsyncStorage.setItem("workout_history", JSON.stringify(history));
  } catch (error) {
    console.error("Error saving workout to history:", error);
    throw error;
  }
}

/**
 * Get workout data for a specific exercise from AsyncStorage
 */
export async function getExerciseWorkoutData(
  exerciseId: string
): Promise<{ weight: string; reps: string }[] | null> {
  try {
    const dataJson = await AsyncStorage.getItem(`exercise_${exerciseId}_data`);
    return dataJson ? JSON.parse(dataJson) : null;
  } catch (error) {
    console.error("Error loading exercise workout data:", error);
    return null;
  }
}
