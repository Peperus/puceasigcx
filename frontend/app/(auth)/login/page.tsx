import { AuthCard } from "@/components/prototypes/auth-card";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function LoginPage() {
  return (
    <AuthCard
      title="Iniciar sesion"
      description="Formulario visual con validaciones minimas de cliente pendientes de reemplazo por autenticacion JWT."
    >
      <form className="space-y-4">
        <div>
          <Label htmlFor="email">Correo institucional</Label>
          <Input className="mt-2" id="email" placeholder="usuario@institucion.example" type="email" />
        </div>
        <div>
          <Label htmlFor="password">Contrasena</Label>
          <Input className="mt-2" id="password" placeholder="Minimo 8 caracteres" type="password" />
        </div>
        <label className="flex items-center gap-2 text-sm text-ui-text-muted">
          <Checkbox />
          Recordar este dispositivo en el prototipo
        </label>
        <Button className="w-full" type="button">Validar acceso</Button>
      </form>
    </AuthCard>
  );
}
