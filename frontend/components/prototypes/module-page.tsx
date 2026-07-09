import { Plus, Search } from "lucide-react";
import { moduleRows } from "@/lib/mock-data";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { StatusBadge } from "@/components/ui/badge";
import { Table } from "@/components/ui/table";
import { Pagination } from "@/components/ui/pagination";
import { PageHeader } from "@/components/prototypes/page-header";
import { EmptyState } from "@/components/feedback/empty-state";

export function ModulePage({
  title,
  description,
  action = "Nuevo registro",
}: {
  title: string;
  description: string;
  action?: string;
}) {
  return (
    <>
      <PageHeader title={title} description={description} />
      <div className="grid gap-4 lg:grid-cols-[1fr_320px]">
        <section>
          <Card className="mb-4">
            <div className="grid gap-3 md:grid-cols-[1fr_180px_auto] md:items-end">
              <div>
                <Label htmlFor={`${title}-search`}>Busqueda</Label>
                <div className="relative mt-2">
                  <Search className="pointer-events-none absolute left-3 top-3 text-ui-text-subtle" size={16} />
                  <Input className="pl-9" id={`${title}-search`} placeholder="Codigo, nombre o estado" />
                </div>
              </div>
              <div>
                <Label htmlFor={`${title}-status`}>Estado</Label>
                <Select className="mt-2" id={`${title}-status`}>
                  <option>Todos</option>
                  <option>Borrador</option>
                  <option>Pendiente</option>
                  <option>Aprobado</option>
                  <option>Cerrado</option>
                </Select>
              </div>
              <Button>
                <Plus size={16} />
                {action}
              </Button>
            </div>
          </Card>
          <Table headers={["Codigo", "Registro", "Responsable", "Estado", "Detalle"]}>
            {moduleRows.map((row) => (
              <tr key={`${title}-${row.id}`}>
                <td className="px-4 py-3 font-mono text-xs text-ui-text-muted">{row.id}</td>
                <td className="px-4 py-3">
                  <p className="font-bold text-ui-text">{row.primary}</p>
                  <p className="text-sm text-ui-text-muted">{row.secondary}</p>
                </td>
                <td className="px-4 py-3 text-sm">{row.owner}</td>
                <td className="px-4 py-3"><StatusBadge status={row.status} /></td>
                <td className="px-4 py-3 text-sm text-ui-text-muted">{row.meta}</td>
              </tr>
            ))}
          </Table>
          <div className="mt-4">
            <Pagination />
          </div>
        </section>
        <aside className="space-y-4">
          <Card>
            <h2 className="text-lg font-black text-puce-blue">Formulario visual</h2>
            <div className="mt-4 space-y-3">
              <div>
                <Label htmlFor={`${title}-name`}>Nombre</Label>
                <Input className="mt-2" id={`${title}-name`} placeholder="Dato sintetico" />
              </div>
              <div>
                <Label htmlFor={`${title}-owner`}>Responsable</Label>
                <Select className="mt-2" id={`${title}-owner`}>
                  <option>Secretaria</option>
                  <option>Coordinacion</option>
                  <option>Docente</option>
                </Select>
              </div>
              <Button className="w-full" variant="outline">Guardar prototipo</Button>
            </div>
          </Card>
          <EmptyState title="Estado vacio" description="Referencia reutilizable para listados sin registros." />
        </aside>
      </div>
    </>
  );
}
