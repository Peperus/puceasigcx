import type { InputHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export function Checkbox({ className, ...props }: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={cn(
        "h-4 w-4 rounded border-ui-border text-puce-blue accent-puce-blue",
        className,
      )}
      type="checkbox"
      {...props}
    />
  );
}
