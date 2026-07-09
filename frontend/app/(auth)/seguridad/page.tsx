import { AuthCard } from "@/components/prototypes/auth-card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";

export default function SecurityQuestionsPage() {
  return (
    <AuthCard
      title="Validacion de seguridad"
      description="Referencia funcional futura para preguntas de seguridad, sin almacenar respuestas en el repositorio."
    >
      <form className="space-y-4">
        <div>
          <Label htmlFor="question">Pregunta</Label>
          <Select className="mt-2" id="question">
            <option>Seleccione una pregunta configurada</option>
            <option>Pregunta demo 1</option>
            <option>Pregunta demo 2</option>
          </Select>
        </div>
        <div>
          <Label htmlFor="answer">Respuesta</Label>
          <Input className="mt-2" id="answer" placeholder="Respuesta temporal de prototipo" />
        </div>
        <Button className="w-full" type="button">Continuar</Button>
      </form>
    </AuthCard>
  );
}
