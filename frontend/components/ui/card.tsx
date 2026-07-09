import type { HTMLAttributes, ReactNode } from "react";
import { cn } from "@/lib/utils";

export function Card({
  children,
  className,
  ...props
}: HTMLAttributes<HTMLDivElement> & { children: ReactNode }) {
  return (
    <div
      className={cn("rounded-puce-lg border border-ui-border bg-white p-5 shadow-puce-xs", className)}
      {...props}
    >
      {children}
    </div>
  );
}
