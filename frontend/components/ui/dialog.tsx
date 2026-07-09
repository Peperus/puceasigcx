import type { ReactNode } from "react";
import { X } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Dialog({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: ReactNode;
}) {
  return (
    <div className="rounded-puce-lg border border-ui-border bg-white p-5 shadow-puce-md">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-lg font-black text-puce-blue">{title}</h2>
          <p className="mt-1 text-sm text-ui-text-muted">{description}</p>
        </div>
        <Button aria-label="Cerrar modal de prototipo" className="h-9 min-h-9 w-9 px-0" variant="ghost">
          <X size={16} />
        </Button>
      </div>
      <div className="mt-5">{children}</div>
    </div>
  );
}
