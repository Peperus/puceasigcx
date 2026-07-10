import { ResourcePage } from "@/components/data/resource-page";

export default function CareersPage() {
  return (
    <ResourcePage
      config={{
        title: "Carreras",
        description: "Carreras, unidad, modalidad y dominio desde /api/academic/careers/.",
        endpoint: "/academic/careers/",
        actionLabel: "Nueva carrera",
        createRoles: ["administrator", "secretary"],
        columns: [
          { key: "code", label: "Codigo" },
          { key: "name", label: "Carrera" },
          { key: "faculty_name", label: "Unidad" },
          { key: "modality_name", label: "Modalidad" },
          { key: "is_active", label: "Activa" },
        ],
        fields: [
          { name: "code", label: "Codigo", required: true },
          { name: "name", label: "Nombre", required: true },
          { name: "faculty", label: "ID unidad academica", type: "number", required: true },
          { name: "modality", label: "ID modalidad", type: "number", required: true },
          { name: "domain", label: "ID dominio", type: "number" },
          { name: "coordinator_user", label: "ID usuario coordinador", type: "number" },
          { name: "is_active", label: "Activa", type: "checkbox" },
        ],
      }}
    />
  );
}
