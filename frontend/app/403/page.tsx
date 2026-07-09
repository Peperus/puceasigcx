import Link from "next/link";
import { ShieldAlert } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function ForbiddenPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-ui-background px-4">
      <div className="max-w-md rounded-puce-lg border border-ui-border bg-white p-6 text-center shadow-puce-md">
        <ShieldAlert className="mx-auto text-status-danger" size={40} />
        <h1 className="mt-4 text-2xl font-black text-puce-blue">Acceso no autorizado</h1>
        <p className="mt-3 text-sm leading-6 text-ui-text-muted">Esta pagina representa el estado 403 para permisos insuficientes.</p>
        <Link href="/dashboard">
          <Button className="mt-6">Volver al inicio</Button>
        </Link>
      </div>
    </main>
  );
}
