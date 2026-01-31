import { ScrollView, Text, View, TouchableOpacity } from "react-native";
import { useState } from "react";
import { ScreenContainer } from "@/components/screen-container";
import { Card } from "@/components/ui/card";

interface Module {
  id: string;
  name: string;
  description: string;
  type: "CORE" | "OPTIONAL";
  icon: string;
  installed: boolean;
}

export default function ModulesScreen() {
  const [modules, setModules] = useState<Module[]>([
    {
      id: "ai_trainer",
      name: "AI Trainer",
      description: "Generates personalized training plans based on your 3D scan data",
      type: "CORE",
      icon: "🤖",
      installed: true,
    },
    {
      id: "body_scanner",
      name: "3D Body Scanner",
      description: "Import and analyze 3D body scan data for precise body composition",
      type: "CORE",
      icon: "📊",
      installed: true,
    },
    {
      id: "nutrition",
      name: "Nutrition Module",
      description: "Personalized nutrition plans and macro tracking",
      type: "OPTIONAL",
      icon: "🍎",
      installed: true,
    },
    {
      id: "strava",
      name: "Strava Integration",
      description: "Sync your runs and rides for better recovery planning",
      type: "OPTIONAL",
      icon: "🏃",
      installed: false,
    },
    {
      id: "sleep",
      name: "Sleep Tracker",
      description: "Monitor your sleep and optimize your recovery",
      type: "OPTIONAL",
      icon: "😴",
      installed: false,
    },
    {
      id: "wearable",
      name: "Wearable Sync",
      description: "Connect your smartwatch for heart rate and activity data",
      type: "OPTIONAL",
      icon: "⌚",
      installed: false,
    },
  ]);

  const toggleModule = (id: string) => {
    setModules((prev) =>
      prev.map((mod) =>
        mod.id === id && mod.type === "OPTIONAL"
          ? { ...mod, installed: !mod.installed }
          : mod
      )
    );
  };

  const coreModules = modules.filter((m) => m.type === "CORE");
  const optionalModules = modules.filter((m) => m.type === "OPTIONAL");

  return (
    <ScreenContainer className="p-4">
      <ScrollView contentContainerStyle={{ flexGrow: 1, paddingBottom: 20 }}>
        <View className="flex-1 gap-6">
          {/* Header */}
          <View className="gap-2">
            <Text className="text-3xl font-bold text-foreground">Module Store</Text>
            <Text className="text-sm text-muted">
              Extend your app with additional features
            </Text>
          </View>

          {/* Info Card */}
          <Card className="bg-primary/10 border-primary/30">
            <View className="gap-2">
              <View className="flex-row items-center gap-2">
                <Text className="text-2xl">💡</Text>
                <Text className="text-base font-bold text-foreground">Modular System</Text>
              </View>
              <Text className="text-sm text-foreground leading-relaxed">
                This app is a shell. Install only the modules you need. Each module
                responds to your 3D scan data and adapts automatically.
              </Text>
            </View>
          </Card>

          {/* Core Modules */}
          <View className="gap-3">
            <Text className="text-lg font-bold text-foreground">Core Modules</Text>
            <Text className="text-sm text-muted">
              These modules are essential and cannot be uninstalled
            </Text>

            {coreModules.map((module) => (
              <Card key={module.id} className="bg-surface border-primary/50">
                <View className="flex-row items-center gap-3">
                  <View className="w-12 h-12 bg-primary/20 rounded-xl items-center justify-center">
                    <Text className="text-2xl">{module.icon}</Text>
                  </View>
                  <View className="flex-1">
                    <Text className="text-base font-semibold text-foreground">
                      {module.name}
                    </Text>
                    <Text className="text-sm text-muted mt-1">{module.description}</Text>
                  </View>
                  <View className="bg-success/20 px-3 py-1 rounded-full">
                    <Text className="text-success text-xs font-bold">Active</Text>
                  </View>
                </View>
              </Card>
            ))}
          </View>

          {/* Optional Modules */}
          <View className="gap-3">
            <Text className="text-lg font-bold text-foreground">Optional Modules</Text>
            <Text className="text-sm text-muted">
              Extend your app with additional features
            </Text>

            {optionalModules.map((module) => (
              <Card key={module.id}>
                <View className="gap-3">
                  <View className="flex-row items-center gap-3">
                    <View className="w-12 h-12 bg-border/30 rounded-xl items-center justify-center">
                      <Text className="text-2xl">{module.icon}</Text>
                    </View>
                    <View className="flex-1">
                      <Text className="text-base font-semibold text-foreground">
                        {module.name}
                      </Text>
                      <Text className="text-sm text-muted mt-1">{module.description}</Text>
                    </View>
                  </View>

                  <TouchableOpacity
                    onPress={() => toggleModule(module.id)}
                    className="py-3 rounded-xl active:opacity-80"
                    style={{
                      backgroundColor: module.installed ? 'transparent' : '#E9B44C',
                      borderWidth: module.installed ? 1 : 0,
                      borderColor: module.installed ? '#ef4444' : 'transparent'
                    }}
                  >
                    <Text
                      className={`text-center font-semibold text-sm ${
                        module.installed ? "text-error" : "text-background"
                      }`}
                    >
                      {module.installed ? "Uninstall" : "Install"}
                    </Text>
                  </TouchableOpacity>
                </View>
              </Card>
            ))}
          </View>
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}
