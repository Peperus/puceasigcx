import { ResourcePage } from "@/components/data/resource-page";

export default function PeriodsPage() {
  return (
    <ResourcePage
      config={{
        title: "Periodos academicos",
        description: "Calendario academico conectado a /api/academic/periods/.",
        endpoint: "/academic/periods/",
        actionLabel: "Nuevo periodo",
        createRoles: ["administrator", "secretary"],
        columns: [
          { key: "code", label: "Codigo" },
          { key: "name", label: "Periodo" },
          { key: "start_date", label: "Inicio" },
          { key: "end_date", label: "Fin" },
          { key: "status", label: "Estado" },
        ],
        fields: [
          { name: "code", label: "Codigo", required: true },
          { name: "name", label: "Nombre", required: true },
          { name: "start_date", label: "Fecha inicio", type: "date", required: true },
          { name: "end_date", label: "Fecha fin", type: "date", required: true },
          { name: "enrollment_start", label: "Inicio matricula", type: "date" },
          { name: "enrollment_end", label: "Fin matricula", type: "date" },
          { name: "grading_open_date", label: "Apertura notas", type: "date" },
          { name: "grading_close_date", label: "Cierre notas", type: "date" },
          {
            name: "status",
            label: "Estado",
            type: "select",
            required: true,
            options: [
              { label: "Planificado", value: "planned" },
              { label: "Activo", value: "active" },
              { label: "Cerrado", value: "closed" },
              { label: "Archivado", value: "archived" },
            ],
          },
          { name: "is_current", label: "Periodo actual", type: "checkbox" },
        ],
      }}
    />
  );
}
