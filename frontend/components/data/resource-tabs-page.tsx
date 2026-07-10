"use client";

import { useState } from "react";
import { ResourcePage, type ResourceConfig } from "@/components/data/resource-page";
import { Button } from "@/components/ui/button";

export function ResourceTabsPage({ tabs }: { tabs: { id: string; label: string; config: ResourceConfig }[] }) {
  const [active, setActive] = useState(tabs[0]?.id ?? "");
  const current = tabs.find((tab) => tab.id === active) ?? tabs[0];

  return (
    <div>
      <div className="mb-4 flex flex-wrap gap-2">
        {tabs.map((tab) => (
          <Button
            key={tab.id}
            onClick={() => setActive(tab.id)}
            type="button"
            variant={tab.id === current.id ? "primary" : "outline"}
          >
            {tab.label}
          </Button>
        ))}
      </div>
      <ResourcePage config={current.config} />
    </div>
  );
}
