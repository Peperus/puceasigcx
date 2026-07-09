import Link from "next/link";
import { FileQuestion } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-ui-background px-4">
      <div className="max-w-md rounded-puce-lg border border-ui-border bg-white p-6 text-center shadow-puce-md">
        <FileQuestion className="mx-auto text-puce-blue" size={40} />
        <h1 className="mt-4 text-2xl font-black text-puce-blue">Pagina no encontrada</h1>
        <p className="mt-3 text-sm leading-6 text-ui-text-muted">El recurso solicitado no existe en el prototipo navegable.</p>
        <Link href="/dashboard">
          <Button className="mt-6">Volver al inicio</Button>
        </Link>
      </div>
    </main>
  );
}
