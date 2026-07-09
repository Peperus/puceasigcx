import type { ReactNode } from "react";
import { AlertCircle, CheckCircle2, Info, TriangleAlert } from "lucide-react";
import { cn } from "@/lib/utils";

const tones = {
  info: { icon: Info, className: "border-status-info bg-status-info-soft text-status-info" },
  success: { icon: CheckCircle2, className: "border-status-success bg-status-success-soft text-status-success" },
  warning: { icon: TriangleAlert, className: "border-status-warning bg-status-warning-soft text-status-warning" },
  danger: { icon: AlertCircle, className: "border-status-danger bg-status-danger-soft text-status-danger" },
} as const;

export function Alert({
  children,
  tone = "info",
}: {
  children: ReactNode;
  tone?: keyof typeof tones;
}) {
  const Icon = tones[tone].icon;

  return (
    <div className={cn("flex gap-3 rounded-puce-md border p-4 text-sm font-medium", tones[tone].className)}>
      <Icon className="mt-0.5 shrink-0" size={18} />
      <div>{children}</div>
    </div>
  );
}
