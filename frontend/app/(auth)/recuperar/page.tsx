import Link from "next/link";
import { AuthCard } from "@/components/prototypes/auth-card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function RecoverPage() {
  return (
    <AuthCard
      title="Recuperar contrasena"
      description="Pantalla de referencia para solicitar recuperacion segura sin enviar correos reales desde el prototipo."
    >
      <form className="space-y-4">
        <div>
          <Label htmlFor="recover-email">Correo institucional</Label>
          <Input className="mt-2" id="recover-email" placeholder="usuario@institucion.example" type="email" />
          <p className="mt-2 text-xs text-ui-text-muted">El mensaje real se conectara al servicio definido en Sprint 1.</p>
        </div>
        <Button className="w-full" type="button">Enviar instrucciones</Button>
        <Link className="block text-center text-sm font-bold text-puce-blue" href="/seguridad">
          Validar preguntas de seguridad
        </Link>
      </form>
    </AuthCard>
  );
}
