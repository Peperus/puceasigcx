import { Upload } from "lucide-react";
import { PageHeader } from "@/components/prototypes/page-header";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { StatusBadge } from "@/components/ui/badge";

export default function SignedSyllabusUploadPage() {
  return (
    <>
      <PageHeader title="Carga de silabo aprobado" description="Prototipo para adjuntar PDF firmado y registrar estado de aprobacion sin guardar archivos en Git." />
      <div className="grid gap-4 lg:grid-cols-[1fr_360px]">
        <Card>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <Label htmlFor="signed-course">Curso</Label>
              <Select className="mt-2" id="signed-course">
                <option>Investigacion aplicada - Paralelo A</option>
                <option>Metodologia demo - Paralelo B</option>
              </Select>
            </div>
            <div>
              <Label htmlFor="signed-status">Estado</Label>
              <Select className="mt-2" id="signed-status">
                <option>Aprobado por coordinacion</option>
                <option>Aprobado por direccion academica</option>
                <option>Firmado/cargado</option>
              </Select>
            </div>
            <div className="md:col-span-2">
              <Label htmlFor="signed-file">Archivo PDF</Label>
              <Input className="mt-2" id="signed-file" type="file" />
              <p className="mt-2 text-xs text-ui-text-muted">El almacenamiento S3 compatible se conectara en sprint funcional.</p>
            </div>
          </div>
          <Button className="mt-5"><Upload size={16} /> Registrar carga visual</Button>
        </Card>
        <Card>
          <h2 className="text-lg font-black text-puce-blue">Estados del flujo</h2>
          <div className="mt-4 flex flex-wrap gap-2">
            <StatusBadge status="approved" />
            <StatusBadge status="signed" />
            <StatusBadge status="closed" />
          </div>
          <div className="mt-5">
            <Alert tone="info">No se versionan archivos cargados dentro del repositorio.</Alert>
          </div>
        </Card>
      </div>
    </>
  );
}
