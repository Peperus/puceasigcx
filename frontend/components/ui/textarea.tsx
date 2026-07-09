import type { TextareaHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export function Textarea({ className, ...props }: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      className={cn(
        "min-h-28 w-full rounded-puce-sm border border-ui-border bg-white px-3 py-2 text-sm text-ui-text placeholder:text-ui-text-subtle",
        "focus:border-puce-turquoise focus:outline-none disabled:bg-ui-surface-muted",
        className,
      )}
      {...props}
    />
  );
}
