import { ResourcePage } from "@/components/data/resource-page";

export default function SubjectsPage() {
  return (
    <ResourcePage
      config={{
        title: "Asignaturas",
        description: "Catalogo de asignaturas conectado a /api/academic/subjects/.",
        endpoint: "/academic/subjects/",
        actionLabel: "Nueva asignatura",
        createRoles: ["administrator", "secretary"],
        columns: [
          { key: "code", label: "Codigo" },
          { key: "name", label: "Asignatura" },
          { key: "career_name", label: "Carrera" },
          { key: "default_grading_system_code", label: "Modelo" },
          { key: "is_active", label: "Activa" },
        ],
        fields: [
          { name: "code", label: "Codigo", required: true },
          { name: "name", label: "Nombre", required: true },
          { name: "career", label: "ID carrera", type: "number", required: true },
          { name: "total_hours", label: "Horas totales", type: "number", required: true },
          { name: "contact_hours", label: "Horas contacto", type: "number" },
          { name: "practical_hours", label: "Horas practicas", type: "number" },
          { name: "autonomous_hours", label: "Horas autonomas", type: "number" },
          { name: "default_grading_system", label: "ID sistema notas", type: "number" },
          { name: "is_active", label: "Activa", type: "checkbox" },
        ],
      }}
    />
  );
}
