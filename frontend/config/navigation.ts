import type { NavigationItem } from "@/types/navigation";

export const navigationShell: NavigationItem[] = [
  {
    label: "Dashboard",
    href: "/dashboard",
    description: "Indicadores y alertas del rol activo.",
    group: "principal",
    roles: ["administrator", "secretary", "career_coordinator", "teacher", "student", "academic_director", "wellbeing"],
  },
  {
    label: "Estudiantes",
    href: "/estudiantes",
    description: "Consulta y gestion academica de estudiantes.",
    group: "gestion",
    roles: ["administrator", "secretary", "career_coordinator", "teacher", "academic_director", "wellbeing"],
  },
  {
    label: "Docentes",
    href: "/docentes",
    description: "Docentes, asignaciones y datos academicos.",
    group: "gestion",
    roles: ["administrator", "secretary", "career_coordinator", "academic_director"],
  },
  {
    label: "Roles",
    href: "/roles",
    description: "Permisos y perfiles institucionales.",
    group: "gestion",
    roles: ["administrator"],
  },
  {
    label: "Periodos",
    href: "/periodos",
    description: "Calendario academico y fechas de proceso.",
    group: "academico",
    roles: ["administrator", "secretary", "career_coordinator", "academic_director"],
  },
  {
    label: "Carreras",
    href: "/carreras",
    description: "Carreras, mallas y planes de estudio.",
    group: "academico",
    roles: ["administrator", "secretary", "career_coordinator", "academic_director"],
  },
  {
    label: "Asignaturas",
    href: "/asignaturas",
    description: "Catalogo de materias y resultados esperados.",
    group: "academico",
    roles: ["administrator", "secretary", "career_coordinator", "academic_director"],
  },
  {
    label: "Paralelos",
    href: "/paralelos",
    description: "Paralelos y cupos por periodo.",
    group: "academico",
    roles: ["administrator", "secretary", "career_coordinator", "academic_director"],
  },
  {
    label: "Oferta",
    href: "/oferta",
    description: "Cursos abiertos y asignacion docente.",
    group: "academico",
    roles: ["administrator", "secretary", "career_coordinator"],
  },
  {
    label: "Matricula",
    href: "/matricula",
    description: "Inscripcion de estudiantes en cursos.",
    group: "academico",
    roles: ["administrator", "secretary"],
  },
  {
    label: "Silabos",
    href: "/silabos",
    description: "Seguimiento, constructor y carga firmada.",
    group: "seguimiento",
    roles: ["administrator", "career_coordinator", "academic_director", "teacher", "student"],
  },
  {
    label: "Notas",
    href: "/notas",
    description: "Prototipos S1, S2 y S3.",
    group: "seguimiento",
    roles: ["administrator", "secretary", "career_coordinator", "academic_director", "teacher", "student"],
  },
  {
    label: "Reportes",
    href: "/reportes",
    description: "Actas y reportes academicos mock.",
    group: "seguimiento",
    roles: ["administrator", "secretary", "career_coordinator", "academic_director"],
  },
  {
    label: "Auditoria",
    href: "/auditoria",
    description: "Trazabilidad de acciones criticas.",
    group: "seguimiento",
    roles: ["administrator", "secretary", "career_coordinator", "academic_director"],
  },
];

export function getNavigationForRole(role: import("@/config/roles").RoleCode) {
  return navigationShell.filter((item) => item.roles.includes(role));
}
