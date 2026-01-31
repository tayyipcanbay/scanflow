import { ScrollView, Text, View, TouchableOpacity } from "react-native";
import { ScreenContainer } from "@/components/screen-container";
import { Card } from "@/components/ui/card";
import { mockUserProfile } from "@/lib/mock-data";

export default function ProfileScreen() {
  const menuItems = [
    { id: "1", title: "Personal Data", icon: "👤" },
    { id: "2", title: "Manage Goals", icon: "🎯" },
    { id: "3", title: "Connected Devices", icon: "📱" },
    { id: "4", title: "Notifications", icon: "🔔" },
    { id: "5", title: "App Settings", icon: "⚙️" },
    { id: "6", title: "Help & Support", icon: "❓" },
  ];

  return (
    <ScreenContainer className="p-4">
      <ScrollView contentContainerStyle={{ flexGrow: 1, paddingBottom: 20 }}>
        <View className="flex-1 gap-6">
          {/* Header */}
          <View className="gap-2">
            <Text className="text-3xl font-bold text-foreground">Profile</Text>
          </View>

          {/* Profile Card */}
          <Card className="bg-gradient-to-br from-primary/20 to-success/20 border-primary/30">
            <View className="items-center gap-4 py-4">
              <View className="w-24 h-24 bg-primary rounded-full items-center justify-center">
                <Text className="text-5xl">👨‍💼</Text>
              </View>
              <View className="items-center gap-1">
                <Text className="text-2xl font-bold text-foreground">
                  {mockUserProfile.name}
                </Text>
                <Text className="text-sm text-muted">
                  {mockUserProfile.experienceLevel}
                </Text>
              </View>
              <View className="bg-primary/30 px-4 py-2 rounded-full">
                <Text className="text-primary font-semibold text-sm">
                  Goal: {mockUserProfile.goal}
                </Text>
              </View>
            </View>
          </Card>

          {/* Stats Card */}
          <Card>
            <View className="gap-3">
              <Text className="text-lg font-bold text-foreground">Your Stats</Text>
              
              <View className="flex-row gap-3">
                <View className="flex-1 bg-border/20 p-3 rounded-lg items-center">
                  <Text className="text-2xl font-bold text-primary">3</Text>
                  <Text className="text-xs text-muted mt-1">Scans</Text>
                </View>
                <View className="flex-1 bg-border/20 p-3 rounded-lg items-center">
                  <Text className="text-2xl font-bold text-success">24</Text>
                  <Text className="text-xs text-muted mt-1">Workouts</Text>
                </View>
                <View className="flex-1 bg-border/20 p-3 rounded-lg items-center">
                  <Text className="text-2xl font-bold text-warning">76</Text>
                  <Text className="text-xs text-muted mt-1">Days</Text>
                </View>
              </View>
            </View>
          </Card>

          {/* Menu Items */}
          <View className="gap-2">
            {menuItems.map((item) => (
              <TouchableOpacity key={item.id} className="active:opacity-70">
                <Card>
                  <View className="flex-row items-center gap-3">
                    <View className="w-10 h-10 bg-primary/20 rounded-full items-center justify-center">
                      <Text className="text-xl">{item.icon}</Text>
                    </View>
                    <Text className="flex-1 text-base text-foreground font-medium">
                      {item.title}
                    </Text>
                    <Text className="text-muted text-lg">›</Text>
                  </View>
                </Card>
              </TouchableOpacity>
            ))}
          </View>

          {/* Logout Button */}
          <TouchableOpacity 
            className="border border-error py-4 rounded-xl active:opacity-70"
            style={{ marginTop: 8 }}
          >
            <Text className="text-error text-center font-semibold text-base">
              Logout
            </Text>
          </TouchableOpacity>

          {/* Version Info */}
          <View className="items-center py-4">
            <Text className="text-xs text-muted">AI Personal Trainer v1.0.0</Text>
          </View>
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}
