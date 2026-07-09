import Link from "next/link";
import { FileCheck, Upload } from "lucide-react";
import { syllabusSteps } from "@/lib/mock-data";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Dialog } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { StatusBadge } from "@/components/ui/badge";
import { Table } from "@/components/ui/table";
import { Tabs } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { PageHeader } from "@/components/prototypes/page-header";

export function SyllabusBuilder() {
  return (
    <>
      <PageHeader
        title="Constructor de silabo nueva version"
        description="Flujo visual por pasos para datos informativos, resultados de aprendizaje, rubricas, bibliografia, planificacion semanal y vista previa."
      />
      <div className="grid gap-4 xl:grid-cols-[280px_1fr]">
        <Card>
          <h2 className="text-lg font-black text-puce-blue">Pasos</h2>
          <ol className="mt-4 space-y-2">
            {syllabusSteps.map((step, index) => (
              <li className="flex items-center gap-3 rounded-puce-md bg-ui-surface-muted p-3 text-sm" key={step}>
                <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-puce-sm bg-puce-blue text-xs font-black text-white">{index + 1}</span>
                <span className="font-bold text-ui-text">{step}</span>
              </li>
            ))}
          </ol>
        </Card>
        <section className="space-y-4">
          <Card>
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <h2 className="text-xl font-black text-puce-blue">Asignatura demo: Investigacion aplicada</h2>
                <p className="mt-2 text-sm text-ui-text-muted">Borrador visual preparado para Sprint 5.</p>
              </div>
              <div className="flex gap-2">
                <StatusBadge status="draft" />
                <StatusBadge status="review" />
                <StatusBadge status="approved" />
                <StatusBadge status="correction" />
                <StatusBadge status="signed" />
              </div>
            </div>
            <Tabs active="Resultados de aprendizaje" tabs={["Datos", "Competencias", "Resultados de aprendizaje", "Rubrica", "Vista previa"]}>
              <div className="grid gap-4 lg:grid-cols-2">
                <div>
                  <Label htmlFor="subject-description">Descripcion de asignatura</Label>
                  <Textarea className="mt-2" id="subject-description" placeholder="Texto descriptivo mock del silabo" />
                </div>
                <div>
                  <Label htmlFor="teacher-summary">Docente / codocente</Label>
                  <Textarea className="mt-2" id="teacher-summary" placeholder="Resumen academico sintetico, sin datos reales" />
                </div>
              </div>
            </Tabs>
          </Card>
          <Table headers={["Resultado", "Criterio", "Peso", "Nivel esperado"]}>
            {["RA1", "RA2", "RA3"].map((ra, index) => (
              <tr key={ra}>
                <td className="px-4 py-3 font-black text-puce-blue">{ra}</td>
                <td className="px-4 py-3">Criterio de evaluacion demo {index + 1}</td>
                <td className="px-4 py-3">
                  <Input aria-label={`Peso ${ra}`} defaultValue="25%" />
                </td>
                <td className="px-4 py-3"><StatusBadge status={index === 1 ? "pending" : "approved"} /></td>
              </tr>
            ))}
          </Table>
          <Dialog title="Vista previa tipo documento" description="No genera PDF real; maqueta la lectura institucional del silabo.">
            <div className="rounded-puce-md border border-ui-border bg-ui-surface-muted p-5">
              <div className="flex items-center gap-3">
                <FileCheck className="text-puce-blue" size={26} />
                <div>
                  <p className="font-black text-puce-blue">Silabo nueva version</p>
                  <p className="text-sm text-ui-text-muted">Resultados de aprendizaje, rubricas, bibliografia y planificacion semanal.</p>
                </div>
              </div>
              <Alert tone="info">La persistencia, validaciones definitivas y exportacion PDF quedan para Sprint 5.</Alert>
            </div>
          </Dialog>
          <div className="flex flex-wrap gap-3">
            <Link href="/silabos/carga-firmado">
              <Button variant="outline">
                <Upload size={16} />
                Cargar firmado
              </Button>
            </Link>
            <Button>Enviar a revision</Button>
          </div>
        </section>
      </div>
    </>
  );
}
