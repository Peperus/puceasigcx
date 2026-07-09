"use client";

import { ErrorState } from "@/components/feedback/error-state";

export default function ErrorPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-ui-background px-4">
      <div className="w-full max-w-xl">
        <ErrorState title="Error general" description="Pagina de error general preparada para fallos de render o integracion futura." />
      </div>
    </main>
  );
}
