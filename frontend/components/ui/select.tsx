import type { SelectHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export function Select({ className, children, ...props }: SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select
      className={cn(
        "min-h-[42px] w-full rounded-puce-sm border border-ui-border bg-white px-3 text-sm font-medium text-ui-text",
        "focus:border-puce-turquoise focus:outline-none disabled:bg-ui-surface-muted",
        className,
      )}
      {...props}
    >
      {children}
    </select>
  );
}
