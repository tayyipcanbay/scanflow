import { View, Text } from "react-native";
import { cn } from "@/lib/utils";

export interface ProgressBarProps {
  value: number;
  max: number;
  label?: string;
  showPercentage?: boolean;
  color?: "primary" | "success" | "warning" | "error";
  customColor?: string;
  className?: string;
}

export function ProgressBar({
  value,
  max,
  label,
  showPercentage = true,
  color = "primary",
  customColor,
  className,
}: ProgressBarProps) {
  const percentage = Math.min((value / max) * 100, 100);
  
  const colorClasses = {
    primary: "bg-primary",
    success: "bg-success",
    warning: "bg-warning",
    error: "bg-error",
  };

  return (
    <View className={cn("gap-1", className)}>
      {label && (
        <View className="flex-row justify-between items-center">
          <Text className="text-sm text-foreground font-medium">{label}</Text>
          {showPercentage && (
            <Text className="text-sm text-muted">
              {value}/{max}
            </Text>
          )}
        </View>
      )}
      <View className="h-2 bg-border rounded-full overflow-hidden">
        <View
          className={cn("h-full rounded-full", !customColor && colorClasses[color])}
          style={{ width: `${percentage}%`, backgroundColor: customColor }}
        />
      </View>
    </View>
  );
}
