import Link from "next/link";
import { AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";

export function ErrorState({
  title = "No se pudo cargar la vista",
  description = "Este estado visual queda preparado para errores de API en sprints funcionales.",
}: {
  title?: string;
  description?: string;
}) {
  return (
    <div className="rounded-puce-lg border border-status-danger bg-status-danger-soft p-6">
      <AlertTriangle className="text-status-danger" size={28} />
      <h2 className="mt-3 text-lg font-black text-status-danger">{title}</h2>
      <p className="mt-2 text-sm leading-6 text-ui-text">{description}</p>
      <Link href="/dashboard">
        <Button className="mt-5" variant="danger">Volver al dashboard</Button>
      </Link>
    </div>
  );
}
