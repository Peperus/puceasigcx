import { ResourcePage } from "@/components/data/resource-page";

export default function TeachersPage() {
  return (
    <ResourcePage
      config={{
        title: "Gestion de docentes",
        description: "Docentes, perfiles academicos y estado desde /api/teachers/.",
        endpoint: "/teachers/",
        actionLabel: "Nuevo docente",
        createRoles: ["administrator", "secretary"],
        columns: [
          { key: "teacher_code", label: "Codigo" },
          { key: "person_full_name", label: "Docente" },
          { key: "professional_title", label: "Titulo" },
          { key: "institutional_email", label: "Correo" },
          { key: "status", label: "Estado" },
        ],
        fields: [
          { name: "person", label: "ID persona", type: "number", required: true },
          { name: "teacher_code", label: "Codigo docente", required: true },
          { name: "academic_degree", label: "Grado academico" },
          { name: "professional_title", label: "Titulo profesional" },
          { name: "academic_profile", label: "Perfil academico", type: "textarea" },
          { name: "institutional_phone", label: "Telefono institucional" },
          {
            name: "status",
            label: "Estado",
            type: "select",
            required: true,
            options: [
              { label: "Activo", value: "active" },
              { label: "Inactivo", value: "inactive" },
              { label: "Invitado", value: "guest" },
            ],
          },
        ],
      }}
    />
  );
}
