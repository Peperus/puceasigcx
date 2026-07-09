import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export function Table({
  headers,
  children,
  className,
}: {
  headers: string[];
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("overflow-hidden rounded-puce-lg border border-ui-border bg-white", className)}>
      <div className="overflow-x-auto">
        <table className="min-w-full border-collapse text-left text-sm">
          <thead className="bg-ui-surface-muted text-xs font-bold uppercase text-ui-text-muted">
            <tr>
              {headers.map((header) => (
                <th className="px-4 py-3" key={header}>
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-ui-border">{children}</tbody>
        </table>
      </div>
    </div>
  );
}
