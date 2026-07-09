import type { ReactNode } from "react";
import Link from "next/link";
import { ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";

export function AuthCard({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: ReactNode;
}) {
  return (
    <main className="grid min-h-screen bg-ui-background lg:grid-cols-[0.95fr_1.05fr]">
      <section className="hidden bg-puce-blue px-10 py-12 text-white lg:flex lg:flex-col lg:justify-between">
        <div>
          <div className="text-sm font-bold uppercase text-puce-blue-soft">PUCEASIG</div>
          <h1 className="mt-6 max-w-xl text-4xl font-black leading-tight">Sistema academico institucional</h1>
          <p className="mt-4 max-w-lg text-sm leading-6 text-blue-50">
            Prototipos visuales para autenticacion, roles y experiencia base. La autenticacion JWT real se implementara en Sprint 1.
          </p>
        </div>
        <div className="rounded-puce-lg border border-white/20 p-5">
          <ShieldCheck size={28} />
          <p className="mt-3 text-sm leading-6 text-blue-50">Sin credenciales reales, sin datos personales y sin conexion al backend productivo.</p>
        </div>
      </section>
      <section className="flex items-center justify-center px-4 py-10">
        <div className="w-full max-w-md rounded-puce-lg border border-ui-border bg-white p-6 shadow-puce-md">
          <p className="text-sm font-bold uppercase text-puce-turquoise-dark">Acceso institucional</p>
          <h2 className="mt-2 text-2xl font-black text-puce-blue">{title}</h2>
          <p className="mt-3 text-sm leading-6 text-ui-text-muted">{description}</p>
          <div className="mt-6">{children}</div>
          <div className="mt-6 flex flex-wrap gap-3 border-t border-ui-border pt-5">
            <Link href="/dashboard">
              <Button variant="outline">Entrar al prototipo</Button>
            </Link>
            <Link className="inline-flex min-h-[42px] items-center text-sm font-bold text-puce-blue" href="/recuperar">
              Recuperar acceso
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
