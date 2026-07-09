import { auditRows } from "@/lib/mock-data";
import { PageHeader } from "@/components/prototypes/page-header";
import { Alert } from "@/components/ui/alert";
import { Card } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/badge";

export default function AuditPage() {
  return (
    <>
      <PageHeader title="Auditoria y trazabilidad" description="Prototipo para acciones criticas: notas, silabos, matricula, roles y cierres academicos." />
      <div className="grid gap-4 lg:grid-cols-[1fr_0.6fr]">
        <Card>
          <h2 className="text-lg font-black text-puce-blue">Eventos mock</h2>
          <div className="mt-4 space-y-3">
            {auditRows.map((row) => (
              <div className="flex items-center justify-between gap-3 rounded-puce-md border border-ui-border p-3" key={row}>
                <span className="text-sm font-medium">{row}</span>
                <StatusBadge status="closed" />
              </div>
            ))}
          </div>
        </Card>
        <Alert tone="danger">Toda correccion de nota cerrada debe exigir permiso especial y justificacion auditable en backend.</Alert>
      </div>
    </>
  );
}
