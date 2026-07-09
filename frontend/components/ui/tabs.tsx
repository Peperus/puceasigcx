import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export function Tabs({
  tabs,
  active,
  children,
}: {
  tabs: string[];
  active: string;
  children?: ReactNode;
}) {
  return (
    <div>
      <div className="flex flex-wrap gap-2 border-b border-ui-border">
        {tabs.map((tab) => (
          <button
            className={cn(
              "min-h-10 border-b-2 px-3 text-sm font-bold",
              tab === active
                ? "border-puce-turquoise text-puce-blue"
                : "border-transparent text-ui-text-muted hover:text-puce-blue",
            )}
            key={tab}
            type="button"
          >
            {tab}
          </button>
        ))}
      </div>
      {children ? <div className="mt-5">{children}</div> : null}
    </div>
  );
}
