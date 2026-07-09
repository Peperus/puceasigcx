import type { ReactNode } from "react";
import type { AcademicResult, AcademicStatus } from "@/types/academic";
import { cn } from "@/lib/utils";

type BadgeTone = "info" | "success" | "warning" | "danger" | "neutral";

const toneClasses: Record<BadgeTone, string> = {
  info: "bg-status-info-soft text-status-info",
  success: "bg-status-success-soft text-status-success",
  warning: "bg-status-warning-soft text-status-warning",
  danger: "bg-status-danger-soft text-status-danger",
  neutral: "bg-ui-surface-muted text-ui-text-muted",
};

const statusTone: Record<AcademicStatus | AcademicResult, BadgeTone> = {
  draft: "neutral",
  pending: "warning",
  pending_review: "warning",
  review: "info",
  approved: "success",
  observed: "warning",
  rejected: "danger",
  closed: "neutral",
  archived: "neutral",
  correction: "warning",
  signed: "success",
  failed: "danger",
  recovery: "warning",
  ungraded: "neutral",
  risk: "danger",
};

const statusLabel: Record<AcademicStatus | AcademicResult, string> = {
  draft: "Borrador",
  pending: "Pendiente",
  pending_review: "Pendiente",
  review: "En revision",
  approved: "Aprobado",
  observed: "Observado",
  rejected: "Rechazado",
  closed: "Cerrado",
  archived: "Archivado",
  correction: "Requiere correccion",
  signed: "Firmado",
  failed: "Reprobado",
  recovery: "Recuperacion",
  ungraded: "Sin calificar",
  risk: "En riesgo",
};

export function Badge({
  children,
  className,
  tone = "neutral",
}: {
  children: ReactNode;
  className?: string;
  tone?: BadgeTone;
}) {
  return (
    <span
      className={cn(
        "inline-flex min-h-6 items-center rounded-puce-sm px-2.5 text-xs font-bold",
        toneClasses[tone],
        className,
      )}
    >
      {children}
    </span>
  );
}

export function StatusBadge({ status }: { status: AcademicStatus | AcademicResult }) {
  return <Badge tone={statusTone[status]}>{statusLabel[status]}</Badge>;
}
