import type { DashboardMetric } from "@/types/academic";
import { Card } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/badge";

export function MetricCard({ metric }: { metric: DashboardMetric }) {
  return (
    <Card>
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm font-bold text-ui-text-muted">{metric.label}</p>
          <p className="mt-2 text-3xl font-black text-puce-blue">{metric.value}</p>
        </div>
        {metric.status ? <StatusBadge status={metric.status} /> : null}
      </div>
      <p className="mt-4 text-sm leading-6 text-ui-text-muted">{metric.detail}</p>
    </Card>
  );
}
