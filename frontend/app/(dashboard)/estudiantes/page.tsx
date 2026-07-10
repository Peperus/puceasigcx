import { ResourceTabsPage } from "@/components/data/resource-tabs-page";

export default function StudentsPage() {
  return (
    <ResourceTabsPage
      tabs={[
        {
          id: "people",
          label: "Personas",
          config: {
            title: "Personas",
            description: "Dato maestro central conectado a /api/people/.",
            endpoint: "/people/",
            actionLabel: "Nueva persona",
            createRoles: ["administrator", "secretary"],
            columns: [
              { key: "identification_number", label: "Identificacion" },
              { key: "full_name", label: "Nombre" },
              { key: "institutional_email", label: "Correo institucional" },
              { key: "phone", label: "Telefono" },
              { key: "is_active", label: "Activa" },
            ],
            fields: [
              { name: "identification_type", label: "Tipo identificacion", required: true },
              { name: "identification_number", label: "Identificacion", required: true },
              { name: "first_name", label: "Nombres", required: true },
              { name: "last_name", label: "Apellidos", required: true },
              { name: "institutional_email", label: "Correo institucional", type: "email", required: true },
              { name: "personal_email", label: "Correo personal", type: "email" },
              { name: "phone", label: "Telefono" },
              { name: "birth_date", label: "Fecha nacimiento", type: "date" },
              { name: "address", label: "Direccion", type: "textarea" },
              { name: "is_active", label: "Activa", type: "checkbox" },
            ],
          },
        },
        {
          id: "students",
          label: "Estudiantes",
          config: {
            title: "Gestion de estudiantes",
            description: "Consulta y alta de estudiantes contra /api/students/.",
            endpoint: "/students/",
            actionLabel: "Nuevo estudiante",
            createRoles: ["administrator", "secretary"],
            columns: [
              { key: "student_code", label: "Codigo" },
              { key: "person_full_name", label: "Estudiante" },
              { key: "career_name", label: "Carrera" },
              { key: "institutional_email", label: "Correo" },
              { key: "status", label: "Estado" },
            ],
            fields: [
              { name: "person", label: "ID persona", type: "number", required: true },
              { name: "student_code", label: "Codigo estudiante", required: true },
              { name: "career", label: "ID carrera", type: "number", required: true },
              { name: "study_plan", label: "ID plan de estudio", type: "number", required: true },
              { name: "admission_period", label: "ID periodo ingreso", type: "number", required: true },
              { name: "admission_date", label: "Fecha ingreso", type: "date" },
              {
                name: "status",
                label: "Estado",
                type: "select",
                required: true,
                options: [
                  { label: "Activo", value: "active" },
                  { label: "Matriculado", value: "enrolled" },
                  { label: "Retirado", value: "withdrawn" },
                  { label: "Inactivo", value: "inactive" },
                ],
              },
              { name: "observations", label: "Observaciones", type: "textarea" },
            ],
          },
        },
      ]}
    />
  );
}
