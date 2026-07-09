import type { RoleCode } from "@/config/roles";
import { roleLabels } from "@/config/roles";
import { dashboardMetrics, moduleRows } from "@/lib/mock-data";
import { MetricCard } from "@/components/dashboard/metric-card";
import { PageHeader } from "@/components/prototypes/page-header";
import { Card } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/badge";
import { Alert } from "@/components/ui/alert";

export function DashboardPage({ role }: { role: RoleCode }) {
  return (
    <>
      <PageHeader
        title={`Dashboard ${roleLabels[role]}`}
        description="Vista prototipo con indicadores sinteticos por rol. No consume API ni representa datos institucionales reales."
      />
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {dashboardMetrics[role].map((metric) => (
          <MetricCard key={metric.label} metric={metric} />
        ))}
      </div>
      <div className="mt-6 grid gap-4 lg:grid-cols-[1fr_0.7fr]">
        <Card>
          <h2 className="text-lg font-black text-puce-blue">Actividad reciente</h2>
          <div className="mt-4 space-y-3">
            {moduleRows.slice(0, 4).map((row) => (
              <div className="flex items-center justify-between gap-3 rounded-puce-md bg-ui-surface-muted p-3" key={row.id}>
                <div>
                  <p className="font-bold">{row.primary}</p>
                  <p className="text-sm text-ui-text-muted">{row.secondary}</p>
                </div>
                <StatusBadge status={row.status} />
              </div>
            ))}
          </div>
        </Card>
        <Alert tone="warning">
          El selector de rol es temporal para Sprint 0.5. En Sprint 1 debe alimentarse desde el perfil autenticado devuelto por la API.
        </Alert>
      </div>
    </>
  );
}
