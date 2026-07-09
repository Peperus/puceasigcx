import Link from "next/link";
import { ClipboardEdit, GraduationCap, ShieldCheck } from "lucide-react";
import { gradeSystems } from "@/lib/mock-data";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { StatusBadge } from "@/components/ui/badge";
import { Table } from "@/components/ui/table";
import { PageHeader } from "@/components/prototypes/page-header";

export function GradesPrototype({ mode = "overview" }: { mode?: "overview" | "teacher" | "student" | "secretary" }) {
  const titleByMode = {
    overview: "Gestion de notas S1/S2/S3",
    teacher: "Carga de calificaciones por docente",
    student: "Consulta de notas estudiante",
    secretary: "Consulta de notas secretaria y coordinacion",
  };

  return (
    <>
      <PageHeader
        title={titleByMode[mode]}
        description="Prototipo visual de estructuras de calificacion. No implementa formulas reales ni estados definitivos del motor de notas."
      />
      <div className="grid gap-4 lg:grid-cols-3">
        {gradeSystems.map((system) => (
          <Card key={system.code}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-sm font-black text-puce-turquoise-dark">{system.code}</p>
                <h2 className="mt-1 text-lg font-black text-puce-blue">{system.title}</h2>
              </div>
              <StatusBadge status={system.code === "S3" ? "ungraded" : "recovery"} />
            </div>
            <p className="mt-3 text-sm leading-6 text-ui-text-muted">{system.detail}</p>
            <ul className="mt-4 space-y-2">
              {system.rows.map((row) => (
                <li className="rounded-puce-sm bg-ui-surface-muted px-3 py-2 text-sm font-medium" key={row}>{row}</li>
              ))}
            </ul>
          </Card>
        ))}
      </div>

      <div className="mt-6 grid gap-4 xl:grid-cols-[1fr_340px]">
        <section className="space-y-4">
          <Card>
            <div className="grid gap-3 md:grid-cols-3">
              <div>
                <Label htmlFor="course">Asignatura</Label>
                <Select className="mt-2" id="course">
                  <option>Investigacion aplicada - Paralelo A</option>
                  <option>Gestion academica - Paralelo B</option>
                </Select>
              </div>
              <div>
                <Label htmlFor="system">Sistema</Label>
                <Select className="mt-2" id="system">
                  <option>S1</option>
                  <option>S2</option>
                  <option>S3</option>
                </Select>
              </div>
              <div>
                <Label htmlFor="activity">Actividad</Label>
                <Input className="mt-2" id="activity" placeholder="Actividad o criterio" />
              </div>
            </div>
          </Card>
          <Table headers={["Estudiante", "Estructura", "Nota", "Estado"]}>
            {["Estudiante demo A", "Estudiante demo B", "Estudiante demo C"].map((student, index) => (
              <tr key={student}>
                <td className="px-4 py-3 font-bold">{student}</td>
                <td className="px-4 py-3 text-sm text-ui-text-muted">{index === 2 ? "S3 parcial 2" : `RA${index + 1} / criterio ${index + 1}`}</td>
                <td className="px-4 py-3">
                  <Input aria-label={`Nota ${student}`} defaultValue={index === 1 ? "29" : "41"} />
                </td>
                <td className="px-4 py-3"><StatusBadge status={index === 1 ? "recovery" : "approved"} /></td>
              </tr>
            ))}
          </Table>
        </section>
        <aside className="space-y-4">
          <Alert tone="warning">Sprint 6 debe implementar el motor S1/S2/S3 como servicios de dominio probados, no como formulas copiadas de esta UI.</Alert>
          <Card>
            <h2 className="text-lg font-black text-puce-blue">Vistas relacionadas</h2>
            <div className="mt-4 grid gap-2">
              <Link href="/notas/carga-docente"><Button className="w-full justify-start" variant="outline"><ClipboardEdit size={16} /> Docente</Button></Link>
              <Link href="/notas/estudiante"><Button className="w-full justify-start" variant="outline"><GraduationCap size={16} /> Estudiante</Button></Link>
              <Link href="/notas/secretaria"><Button className="w-full justify-start" variant="outline"><ShieldCheck size={16} /> Secretaria</Button></Link>
            </div>
          </Card>
        </aside>
      </div>
    </>
  );
}
