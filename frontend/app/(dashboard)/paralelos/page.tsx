import { ResourcePage } from "@/components/data/resource-page";

export default function ParallelsPage() {
  return (
    <ResourcePage
      config={{
        title: "Cursos y paralelos",
        description: "Cursos/paralelos reales desde /api/enrollment/course-sections/.",
        endpoint: "/enrollment/course-sections/",
        actionLabel: "Nuevo curso",
        createRoles: ["administrator", "secretary", "career_coordinator"],
        columns: [
          { key: "subject_code", label: "Asignatura" },
          { key: "subject_name", label: "Nombre" },
          { key: "parallel", label: "Paralelo" },
          { key: "available_seats", label: "Cupos" },
          { key: "status", label: "Estado" },
        ],
        fields: [
          { name: "offer", label: "ID oferta", type: "number", required: true },
          { name: "subject", label: "ID asignatura", type: "number", required: true },
          { name: "parallel", label: "Paralelo", required: true },
          { name: "capacity", label: "Cupo", type: "number", required: true },
          { name: "modality", label: "ID modalidad", type: "number", required: true },
          { name: "grading_system", label: "ID sistema notas", type: "number", required: true },
          { name: "classroom", label: "Aula" },
          {
            name: "status",
            label: "Estado",
            type: "select",
            required: true,
            options: [
              { label: "Planificado", value: "planned" },
              { label: "Abierto", value: "open" },
              { label: "En curso", value: "in_progress" },
              { label: "Cerrado", value: "closed" },
            ],
          },
        ],
      }}
    />
  );
}
