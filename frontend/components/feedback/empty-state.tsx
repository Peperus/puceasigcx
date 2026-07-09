import { Inbox } from "lucide-react";
import { Button } from "@/components/ui/button";

export function EmptyState({
  title = "No hay registros",
  description = "Cuando existan datos reales o mock para esta vista, apareceran aqui.",
}: {
  title?: string;
  description?: string;
}) {
  return (
    <div className="rounded-puce-lg border border-dashed border-ui-border bg-white p-8 text-center">
      <Inbox className="mx-auto text-puce-blue" size={32} />
      <h2 className="mt-4 text-lg font-black text-puce-blue">{title}</h2>
      <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-ui-text-muted">{description}</p>
      <Button className="mt-5" variant="outline">Crear registro mock</Button>
    </div>
  );
}
