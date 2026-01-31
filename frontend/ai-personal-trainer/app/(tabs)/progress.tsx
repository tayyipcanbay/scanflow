import { ScrollView, Text, View, Image, Dimensions } from "react-native";
import { ScreenContainer } from "@/components/screen-container";
import { Card } from "@/components/ui/card";
import { mockBodyScans, mockUserProfile } from "@/lib/mock-data";
import { LineChart } from "react-native-chart-kit";

export default function ProgressScreen() {
  const currentScan = mockUserProfile.currentScan;
  const firstScan = mockUserProfile.firstScan;
  const screenWidth = Dimensions.get("window").width;

  const weightChange = currentScan.weight - firstScan.weight;
  const bodyFatChange = currentScan.bodyFat - firstScan.bodyFat;
  const muscleMassChange = currentScan.muscleMass - firstScan.muscleMass;

  const formatChange = (value: number, unit: string) => {
    const sign = value > 0 ? "+" : "";
    return `${sign}${value.toFixed(1)} ${unit}`;
  };

  // Prepare chart data from mockBodyScans
  const sortedScans = [...mockBodyScans].sort((a, b) => 
    new Date(a.date).getTime() - new Date(b.date).getTime()
  );

  const chartConfig = {
    backgroundGradientFrom: "#1E2022",
    backgroundGradientTo: "#1E2022",
    color: (opacity = 1) => `rgba(233, 180, 76, ${opacity})`,
    strokeWidth: 2,
    barPercentage: 0.5,
    useShadowColorFromDataset: false,
    decimalPlaces: 1,
  };

  const weightData = {
    labels: sortedScans.map((scan, index) => 
      index === 0 ? "Start" : index === sortedScans.length - 1 ? "Now" : ""
    ),
    datasets: [
      {
        data: sortedScans.map(scan => scan.weight),
        color: (opacity = 1) => `rgba(233, 180, 76, ${opacity})`,
        strokeWidth: 3,
      },
    ],
  };

  const muscleMassData = {
    labels: sortedScans.map((scan, index) => 
      index === 0 ? "Start" : index === sortedScans.length - 1 ? "Now" : ""
    ),
    datasets: [
      {
        data: sortedScans.map(scan => scan.muscleMass),
        color: (opacity = 1) => `rgba(233, 180, 76, ${opacity})`,
        strokeWidth: 3,
      },
    ],
  };

  const bodyFatData = {
    labels: sortedScans.map((scan, index) => 
      index === 0 ? "Start" : index === sortedScans.length - 1 ? "Now" : ""
    ),
    datasets: [
      {
        data: sortedScans.map(scan => scan.bodyFat),
        color: (opacity = 1) => `rgba(233, 180, 76, ${opacity})`,
        strokeWidth: 3,
      },
    ],
  };

  return (
    <ScreenContainer className="p-4">
      <ScrollView contentContainerStyle={{ flexGrow: 1, paddingBottom: 20 }}>
        <View className="flex-1 gap-6">
          {/* Header */}
          <View className="gap-2">
            <Text className="text-3xl font-bold text-foreground">Progress</Text>
            <Text className="text-sm text-muted">
              Since {new Date(firstScan.date).toLocaleDateString("en-US")}
            </Text>
          </View>

          {/* 3D Model Comparison */}
          <Card className="bg-gradient-to-br from-primary/20 to-secondary/20 border-primary/30">
            <View className="py-6">
              <Text className="text-center text-lg font-bold text-foreground mb-4">
                Body Transformation
              </Text>
              <View className="flex-row justify-around items-center">
                {/* Start Scan */}
                <View className="items-center flex-1">
                  <Text className="text-xs text-muted mb-2">Start</Text>
                  <Image
                    source={require("@/assets/images/male-body-model.png")}
                    style={{ width: 120, height: 200, opacity: 0.6 }}
                    resizeMode="contain"
                  />
                  <View className="mt-2 gap-1">
                    <Text className="text-center text-sm font-semibold text-foreground">
                      {firstScan.weight} kg
                    </Text>
                    <Text className="text-center text-xs text-muted">
                      {firstScan.muscleMass} kg muscle
                    </Text>
                    <Text className="text-center text-xs text-muted">
                      {firstScan.bodyFat}% fat
                    </Text>
                  </View>
                </View>

                {/* Arrow */}
                <View className="px-2">
                  <Text className="text-2xl" style={{ color: '#E9B44C' }}>→</Text>
                </View>

                {/* Current Scan */}
                <View className="items-center flex-1">
                  <Text className="text-xs text-muted mb-2">Current</Text>
                  <Image
                    source={require("@/assets/images/male-body-model.png")}
                    style={{ width: 120, height: 200 }}
                    resizeMode="contain"
                  />
                  <View className="mt-2 gap-1">
                    <Text className="text-center text-sm font-semibold text-foreground">
                      {currentScan.weight} kg
                    </Text>
                    <Text className="text-center text-xs text-muted">
                      {currentScan.muscleMass} kg muscle
                    </Text>
                    <Text className="text-center text-xs text-muted">
                      {currentScan.bodyFat}% fat
                    </Text>
                  </View>
                </View>
              </View>

              {/* Change Summary */}
              <View className="mt-6 pt-4 border-t border-border/30">
                <View className="flex-row justify-around">
                  <View className="items-center">
                    <Text
                      className={`text-lg font-bold ${
                        weightChange < 0 ? "text-success" : "text-warning"
                      }`}
                    >
                      {formatChange(weightChange, "kg")}
                    </Text>
                    <Text className="text-xs text-muted">Weight</Text>
                  </View>
                  <View className="items-center">
                    <Text
                      className={`text-lg font-bold ${
                        muscleMassChange > 0 ? "text-success" : "text-error"
                      }`}
                    >
                      {formatChange(muscleMassChange, "kg")}
                    </Text>
                    <Text className="text-xs text-muted">Muscle</Text>
                  </View>
                  <View className="items-center">
                    <Text
                      className={`text-lg font-bold ${
                        bodyFatChange < 0 ? "text-success" : "text-error"
                      }`}
                    >
                      {formatChange(bodyFatChange, "%")}
                    </Text>
                    <Text className="text-xs text-muted">Body Fat</Text>
                  </View>
                </View>
              </View>
            </View>
          </Card>

          {/* Weight Progress Graph */}
          <Card>
            <View className="gap-3">
              <Text className="text-lg font-bold text-foreground">Weight Progress</Text>
              <LineChart
                data={weightData}
                width={screenWidth - 80}
                height={200}
                chartConfig={chartConfig}
                bezier
                style={{
                  marginVertical: 8,
                  borderRadius: 16,
                }}
                withInnerLines={false}
                withOuterLines={true}
                withVerticalLabels={true}
                withHorizontalLabels={true}
                fromZero={false}
              />
              <View className="flex-row justify-between">
                <Text className="text-xs text-muted">
                  Start: {firstScan.weight} kg
                </Text>
                <Text className="text-xs text-muted">
                  Current: {currentScan.weight} kg
                </Text>
              </View>
            </View>
          </Card>

          {/* Muscle Mass Progress Graph */}
          <Card>
            <View className="gap-3">
              <Text className="text-lg font-bold text-foreground">Muscle Mass Progress</Text>
              <LineChart
                data={muscleMassData}
                width={screenWidth - 80}
                height={200}
                chartConfig={chartConfig}
                bezier
                style={{
                  marginVertical: 8,
                  borderRadius: 16,
                }}
                withInnerLines={false}
                withOuterLines={true}
                withVerticalLabels={true}
                withHorizontalLabels={true}
                fromZero={false}
              />
              <View className="flex-row justify-between">
                <Text className="text-xs text-muted">
                  Start: {firstScan.muscleMass} kg
                </Text>
                <Text className="text-xs text-muted">
                  Current: {currentScan.muscleMass} kg
                </Text>
              </View>
            </View>
          </Card>

          {/* Body Fat Progress Graph */}
          <Card>
            <View className="gap-3">
              <Text className="text-lg font-bold text-foreground">Body Fat Progress</Text>
              <LineChart
                data={bodyFatData}
                width={screenWidth - 80}
                height={200}
                chartConfig={chartConfig}
                bezier
                style={{
                  marginVertical: 8,
                  borderRadius: 16,
                }}
                withInnerLines={false}
                withOuterLines={true}
                withVerticalLabels={true}
                withHorizontalLabels={true}
                fromZero={false}
              />
              <View className="flex-row justify-between">
                <Text className="text-xs text-muted">
                  Start: {firstScan.bodyFat}%
                </Text>
                <Text className="text-xs text-muted">
                  Current: {currentScan.bodyFat}%
                </Text>
              </View>
            </View>
          </Card>
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}
