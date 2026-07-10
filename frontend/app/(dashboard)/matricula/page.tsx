import { ResourceTabsPage } from "@/components/data/resource-tabs-page";

export default function EnrollmentPage() {
  return (
    <ResourceTabsPage
      tabs={[
        {
          id: "enrollments",
          label: "Matriculas",
          config: {
            title: "Matricula academica",
            description: "Matriculas de estudiante por periodo, carrera y plan.",
            endpoint: "/enrollment/enrollments/",
            actionLabel: "Registrar matricula",
            createRoles: ["administrator", "secretary"],
            columns: [
              { key: "student_code", label: "Codigo" },
              { key: "student_name", label: "Estudiante" },
              { key: "period_code", label: "Periodo" },
              { key: "career_name", label: "Carrera" },
              { key: "status", label: "Estado" },
            ],
            fields: [
              { name: "student", label: "ID estudiante", type: "number", required: true },
              { name: "period", label: "ID periodo", type: "number", required: true },
              { name: "career", label: "ID carrera", type: "number", required: true },
              { name: "study_plan", label: "ID plan", type: "number", required: true },
              { name: "status", label: "Estado", type: "select", required: true, options: [
                { label: "Activa", value: "active" },
                { label: "Anulada", value: "void" },
                { label: "Retirada", value: "withdrawn" },
              ] },
            ],
          },
        },
        {
          id: "course-enrollments",
          label: "Cursos",
          config: {
            title: "Matricula en cursos",
            description: "Inscripcion de estudiantes en cursos con cupos y estados validados por backend.",
            endpoint: "/enrollment/course-enrollments/",
            actionLabel: "Inscribir en curso",
            createRoles: ["administrator", "secretary"],
            columns: [
              { key: "student_code", label: "Codigo" },
              { key: "student_name", label: "Estudiante" },
              { key: "course_label", label: "Curso" },
              { key: "period_code", label: "Periodo" },
              { key: "status", label: "Estado" },
            ],
            fields: [
              { name: "enrollment", label: "ID matricula academica", type: "number", required: true },
              { name: "course_section", label: "ID curso", type: "number", required: true },
              { name: "status", label: "Estado", type: "select", required: true, options: [
                { label: "Matriculado", value: "enrolled" },
                { label: "Retirado", value: "withdrawn" },
                { label: "Anulado", value: "void" },
              ] },
            ],
          },
        },
      ]}
    />
  );
}
