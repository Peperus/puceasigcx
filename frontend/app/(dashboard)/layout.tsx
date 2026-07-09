import type { ReactNode } from "react";
import { Suspense } from "react";
import { AppShell } from "@/components/layout/app-shell";
import { LoadingState } from "@/components/feedback/loading-state";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <Suspense
      fallback={
        <main className="min-h-screen bg-ui-background p-6">
          <LoadingState label="Preparando navegacion por rol" />
        </main>
      }
    >
      <AppShell>{children}</AppShell>
    </Suspense>
  );
}
