export interface BodyScan {
  id: string;
  date: string;
  weight: number;
  bodyFat: number;
  muscleMass: number;
  measurements: {
    chest: number;
    waist: number;
    hips: number;
    arms: number;
    thighs: number;
  };
}

export interface Exercise {
  id: string;
  name: string;
  muscleGroup: string;
  sets: number;
  reps: string;
  completed: boolean;
}

export interface Workout {
  id: string;
  day: string;
  exercises: Exercise[];
}

export interface MacroGoals {
  protein: number;
  carbs: number;
  fats: number;
  calories: number;
}

export interface MacroProgress {
  protein: number;
  carbs: number;
  fats: number;
  calories: number;
}

export interface UserProfile {
  name: string;
  goal: string;
  experienceLevel: string;
  currentScan: BodyScan;
  firstScan: BodyScan;
}

// Mock Data
export const mockUserProfile: UserProfile = {
  name: "Alex",
  goal: "Muskelaufbau",
  experienceLevel: "Anfänger",
  currentScan: {
    id: "scan-3",
    date: "2026-01-15",
    weight: 78.5,
    bodyFat: 18.2,
    muscleMass: 36.8,
    measurements: {
      chest: 98,
      waist: 82,
      hips: 95,
      arms: 34,
      thighs: 56,
    },
  },
  firstScan: {
    id: "scan-1",
    date: "2025-11-01",
    weight: 82.0,
    bodyFat: 22.5,
    muscleMass: 33.2,
    measurements: {
      chest: 96,
      waist: 88,
      hips: 98,
      arms: 32,
      thighs: 58,
    },
  },
};

export const mockBodyScans: BodyScan[] = [
  {
    id: "scan-1",
    date: "2025-11-01",
    weight: 82.0,
    bodyFat: 22.5,
    muscleMass: 33.2,
    measurements: {
      chest: 96,
      waist: 88,
      hips: 98,
      arms: 32,
      thighs: 58,
    },
  },
  {
    id: "scan-2",
    date: "2025-12-15",
    weight: 80.2,
    bodyFat: 20.1,
    muscleMass: 35.0,
    measurements: {
      chest: 97,
      waist: 85,
      hips: 96,
      arms: 33,
      thighs: 57,
    },
  },
  {
    id: "scan-3",
    date: "2026-01-15",
    weight: 78.5,
    bodyFat: 18.2,
    muscleMass: 36.8,
    measurements: {
      chest: 98,
      waist: 82,
      hips: 95,
      arms: 34,
      thighs: 56,
    },
  },
];

export const mockTodayWorkout: Workout = {
  id: "workout-1",
  day: "Montag",
  exercises: [
    {
      id: "bench-press",
      name: "Bench Press",
      muscleGroup: "Chest",
      sets: 4,
      reps: "8-12",
      completed: false,
    },
    {
      id: "incline-press",
      name: "Incline Bench Press",
      muscleGroup: "Upper Chest",
      sets: 3,
      reps: "10-12",
      completed: false,
    },
    {
      id: "dumbbell-flys",
      name: "Dumbbell Flys",
      muscleGroup: "Chest",
      sets: 3,
      reps: "12-15",
      completed: false,
    },
    {
      id: "tricep-dips",
      name: "Tricep Dips",
      muscleGroup: "Triceps",
      sets: 3,
      reps: "10-15",
      completed: false,
    },
    {
      id: "tricep-pushdowns",
      name: "Tricep Pushdowns",
      muscleGroup: "Triceps",
      sets: 3,
      reps: "12-15",
      completed: false,
    },
  ],
};

export const mockWeekWorkouts: Workout[] = [
  {
    id: "workout-1",
    day: "Monday",
    exercises: [
      {
        id: "bench-press",
        name: "Bench Press",
        muscleGroup: "Chest",
        sets: 4,
        reps: "8-12",
        completed: false,
      },
      {
        id: "incline-press",
        name: "Incline Bench Press",
        muscleGroup: "Upper Chest",
        sets: 3,
        reps: "10-12",
        completed: false,
      },
      {
        id: "dumbbell-flys",
        name: "Dumbbell Flys",
        muscleGroup: "Chest",
        sets: 3,
        reps: "12-15",
        completed: false,
      },
      {
        id: "tricep-dips",
        name: "Tricep Dips",
        muscleGroup: "Triceps",
        sets: 3,
        reps: "10-15",
        completed: false,
      },
      {
        id: "tricep-pushdowns",
        name: "Tricep Pushdowns",
        muscleGroup: "Triceps",
        sets: 3,
        reps: "12-15",
        completed: false,
      },
    ],
  },
  {
    id: "workout-2",
    day: "Wednesday",
    exercises: [
      {
        id: "squats",
        name: "Barbell Squats",
        muscleGroup: "Legs",
        sets: 4,
        reps: "8-10",
        completed: false,
      },
      {
        id: "leg-press",
        name: "Leg Press",
        muscleGroup: "Legs",
        sets: 3,
        reps: "10-12",
        completed: false,
      },
      {
        id: "leg-curls",
        name: "Leg Curls",
        muscleGroup: "Hamstrings",
        sets: 3,
        reps: "12-15",
        completed: false,
      },
      {
        id: "calf-raises",
        name: "Calf Raises",
        muscleGroup: "Calves",
        sets: 4,
        reps: "15-20",
        completed: false,
      },
    ],
  },
  {
    id: "workout-3",
    day: "Friday",
    exercises: [
      {
        id: "pull-ups",
        name: "Pull-Ups",
        muscleGroup: "Back",
        sets: 4,
        reps: "8-10",
        completed: false,
      },
      {
        id: "barbell-rows",
        name: "Barbell Rows",
        muscleGroup: "Back",
        sets: 3,
        reps: "10-12",
        completed: false,
      },
      {
        id: "lat-pulldown",
        name: "Lat Pulldown",
        muscleGroup: "Lats",
        sets: 3,
        reps: "12-15",
        completed: false,
      },
      {
        id: "bicep-curls",
        name: "Bicep Curls",
        muscleGroup: "Biceps",
        sets: 3,
        reps: "12-15",
        completed: false,
      },
    ],
  },
];

export const mockMacroGoals: MacroGoals = {
  protein: 150,
  carbs: 250,
  fats: 70,
  calories: 2400,
};

export const mockMacroProgress: MacroProgress = {
  protein: 95,
  carbs: 180,
  fats: 45,
  calories: 1680,
};

export const mockAIInsight = "Basierend auf deinem letzten Scan hat deine Muskelmasse am Oberkörper um 2% zugenommen. Wir erhöhen daher das Volumen für Brust- und Rückenübungen, um dieses Momentum zu nutzen. Dein Körperfettanteil ist ebenfalls gesunken, was zeigt, dass deine Ernährung gut funktioniert.";

export const mockMealSuggestions = [
  {
    id: "meal-1",
    name: "Frühstück",
    description: "Haferflocken mit Beeren und Proteinpulver",
    protein: 35,
    carbs: 60,
    fats: 12,
    calories: 480,
  },
  {
    id: "meal-2",
    name: "Mittagessen",
    description: "Hähnchenbrust mit Reis und Gemüse",
    protein: 45,
    carbs: 80,
    fats: 15,
    calories: 620,
  },
  {
    id: "meal-3",
    name: "Abendessen",
    description: "Lachs mit Süßkartoffeln und Brokkoli",
    protein: 40,
    carbs: 70,
    fats: 25,
    calories: 680,
  },
  {
    id: "meal-4",
    name: "Snack",
    description: "Griechischer Joghurt mit Nüssen",
    protein: 30,
    carbs: 40,
    fats: 18,
    calories: 420,
  },
];
