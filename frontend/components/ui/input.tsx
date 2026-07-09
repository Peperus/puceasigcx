import type { InputHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export function Input({ className, ...props }: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={cn(
        "min-h-[42px] w-full rounded-puce-sm border border-ui-border bg-white px-3 text-sm text-ui-text placeholder:text-ui-text-subtle",
        "focus:border-puce-turquoise focus:outline-none disabled:bg-ui-surface-muted",
        className,
      )}
      {...props}
    />
  );
}
