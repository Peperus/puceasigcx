export const roleCodes = [
  "admin",
  "secretary",
  "coordinator",
  "teacher",
  "student",
  "wellbeing",
] as const;

export type RoleCode = (typeof roleCodes)[number];

export const roleLabels: Record<RoleCode, string> = {
  admin: "Administrador",
  secretary: "Secretaria academica",
  coordinator: "Coordinador de carrera",
  teacher: "Docente",
  student: "Estudiante",
  wellbeing: "Bienestar / apoyo institucional",
};
