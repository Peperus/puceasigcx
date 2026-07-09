import type { NavigationItem } from "@/types/navigation";

export const navigationShell: NavigationItem[] = [
  {
    label: "Dashboard",
    href: "/dashboard",
    description: "Indicadores y alertas del rol activo.",
    group: "principal",
    roles: ["admin", "secretary", "coordinator", "teacher", "student", "wellbeing"],
  },
  {
    label: "Estudiantes",
    href: "/estudiantes",
    description: "Consulta y gestion academica de estudiantes.",
    group: "gestion",
    roles: ["admin", "secretary", "coordinator", "teacher", "wellbeing"],
  },
  {
    label: "Docentes",
    href: "/docentes",
    description: "Docentes, asignaciones y datos academicos.",
    group: "gestion",
    roles: ["admin", "secretary", "coordinator"],
  },
  {
    label: "Roles",
    href: "/roles",
    description: "Permisos y perfiles institucionales.",
    group: "gestion",
    roles: ["admin"],
  },
  {
    label: "Periodos",
    href: "/periodos",
    description: "Calendario academico y fechas de proceso.",
    group: "academico",
    roles: ["admin", "secretary", "coordinator"],
  },
  {
    label: "Carreras",
    href: "/carreras",
    description: "Carreras, mallas y planes de estudio.",
    group: "academico",
    roles: ["admin", "secretary", "coordinator"],
  },
  {
    label: "Asignaturas",
    href: "/asignaturas",
    description: "Catalogo de materias y resultados esperados.",
    group: "academico",
    roles: ["admin", "secretary", "coordinator"],
  },
  {
    label: "Paralelos",
    href: "/paralelos",
    description: "Paralelos y cupos por periodo.",
    group: "academico",
    roles: ["admin", "secretary", "coordinator"],
  },
  {
    label: "Oferta",
    href: "/oferta",
    description: "Cursos abiertos y asignacion docente.",
    group: "academico",
    roles: ["admin", "secretary", "coordinator"],
  },
  {
    label: "Matricula",
    href: "/matricula",
    description: "Inscripcion de estudiantes en cursos.",
    group: "academico",
    roles: ["admin", "secretary"],
  },
  {
    label: "Silabos",
    href: "/silabos",
    description: "Seguimiento, constructor y carga firmada.",
    group: "seguimiento",
    roles: ["admin", "coordinator", "teacher", "student"],
  },
  {
    label: "Notas",
    href: "/notas",
    description: "Prototipos S1, S2 y S3.",
    group: "seguimiento",
    roles: ["admin", "secretary", "coordinator", "teacher", "student"],
  },
  {
    label: "Reportes",
    href: "/reportes",
    description: "Actas y reportes academicos mock.",
    group: "seguimiento",
    roles: ["admin", "secretary", "coordinator"],
  },
  {
    label: "Auditoria",
    href: "/auditoria",
    description: "Trazabilidad de acciones criticas.",
    group: "seguimiento",
    roles: ["admin", "secretary", "coordinator"],
  },
];

export function getNavigationForRole(role: import("@/config/roles").RoleCode) {
  return navigationShell.filter((item) => item.roles.includes(role));
}
