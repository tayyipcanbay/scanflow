import { View, type ViewProps } from "react-native";
import { cn } from "@/lib/utils";

export interface CardProps extends ViewProps {
  className?: string;
}

export function Card({ children, className, ...props }: CardProps) {
  return (
    <View
      className={cn(
        "bg-surface rounded-2xl p-4 border border-border shadow-sm",
        className
      )}
      {...props}
    >
      {children}
    </View>
  );
}
