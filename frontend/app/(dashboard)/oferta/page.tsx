import { ResourceTabsPage } from "@/components/data/resource-tabs-page";

const staff = ["administrator", "secretary", "career_coordinator"] as const;

export default function OfferPage() {
  return (
    <ResourceTabsPage
      tabs={[
        {
          id: "offers",
          label: "Oferta",
          config: {
            title: "Oferta academica",
            description: "Oferta por periodo, carrera, plan y nivel conectada a /api/enrollment/academic-offers/.",
            endpoint: "/enrollment/academic-offers/",
            actionLabel: "Nueva oferta",
            createRoles: [...staff],
            columns: [
              { key: "period_code", label: "Periodo" },
              { key: "career_name", label: "Carrera" },
              { key: "study_plan_code", label: "Plan" },
              { key: "level_name", label: "Nivel" },
              { key: "status", label: "Estado" },
            ],
            fields: [
              { name: "period", label: "ID periodo", type: "number", required: true },
              { name: "career", label: "ID carrera", type: "number", required: true },
              { name: "study_plan", label: "ID plan", type: "number", required: true },
              { name: "level", label: "ID nivel", type: "number", required: true },
              { name: "description", label: "Descripcion", type: "textarea" },
              { name: "status", label: "Estado", type: "select", required: true, options: [
                { label: "Planificada", value: "planned" },
                { label: "Abierta", value: "open" },
                { label: "Cerrada", value: "closed" },
              ] },
            ],
          },
        },
        {
          id: "courses",
          label: "Cursos",
          config: {
            title: "Cursos/paralelos",
            description: "Cursos, cupos, estado y modelo de notas desde la API real.",
            endpoint: "/enrollment/course-sections/",
            actionLabel: "Abrir curso",
            createRoles: [...staff],
            columns: [
              { key: "period_code", label: "Periodo" },
              { key: "subject_code", label: "Codigo" },
              { key: "subject_name", label: "Asignatura" },
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
              { name: "status", label: "Estado", type: "select", required: true, options: [
                { label: "Planificado", value: "planned" },
                { label: "Abierto", value: "open" },
                { label: "En curso", value: "in_progress" },
                { label: "Cerrado", value: "closed" },
              ] },
            ],
          },
        },
        {
          id: "assignments",
          label: "Asignacion docente",
          config: {
            title: "Asignacion docente",
            description: "Asignaciones titulares y codocentes con validaciones del backend.",
            endpoint: "/enrollment/teaching-assignments/",
            actionLabel: "Asignar docente",
            createRoles: [...staff],
            columns: [
              { key: "course_label", label: "Curso" },
              { key: "teacher_name", label: "Docente" },
              { key: "teacher_code", label: "Codigo" },
              { key: "role", label: "Rol" },
              { key: "status", label: "Estado" },
            ],
            fields: [
              { name: "course_section", label: "ID curso", type: "number", required: true },
              { name: "teacher", label: "ID docente", type: "number", required: true },
              { name: "role", label: "Rol", type: "select", required: true, options: [
                { label: "Titular", value: "lead" },
                { label: "Codocente", value: "co_teacher" },
                { label: "Invitado", value: "guest" },
              ] },
              { name: "weekly_hours", label: "Horas semanales", type: "number" },
              { name: "status", label: "Estado", type: "select", required: true, options: [
                { label: "Activa", value: "active" },
                { label: "Inactiva", value: "inactive" },
              ] },
            ],
          },
        },
      ]}
    />
  );
}
