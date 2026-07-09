import type { ButtonHTMLAttributes, ReactNode } from "react";
import { cn } from "@/lib/utils";

type ButtonVariant = "primary" | "secondary" | "outline" | "ghost" | "danger";

const variants: Record<ButtonVariant, string> = {
  primary: "bg-puce-blue text-white hover:bg-puce-blue-dark",
  secondary: "bg-puce-turquoise text-ui-text hover:bg-puce-sky",
  outline: "border border-ui-border bg-white text-puce-blue hover:border-puce-blue",
  ghost: "text-puce-blue hover:bg-puce-blue-soft",
  danger: "bg-status-danger text-white hover:bg-red-800",
};

export function Button({
  children,
  className,
  variant = "primary",
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
  variant?: ButtonVariant;
}) {
  return (
    <button
      className={cn(
        "inline-flex min-h-[42px] items-center justify-center gap-2 rounded-puce-sm px-4 text-sm font-bold transition-colors disabled:cursor-not-allowed disabled:opacity-60",
        variants[variant],
        className,
      )}
      {...props}
    >
      {children}
    </button>
  );
}
