export const roleCodes = [
  "administrator",
  "secretary",
  "career_coordinator",
  "teacher",
  "student",
  "academic_director",
  "wellbeing",
  "librarian",
  "guest",
] as const;

export type RoleCode = (typeof roleCodes)[number];

export const roleLabels: Record<RoleCode, string> = {
  administrator: "Administrador",
  secretary: "Secretaria academica",
  career_coordinator: "Coordinador de carrera",
  teacher: "Docente",
  student: "Estudiante",
  academic_director: "Direccion academica",
  wellbeing: "Bienestar / apoyo institucional",
  librarian: "Bibliotecario",
  guest: "Invitado / consulta",
};

export const staffRoles: RoleCode[] = [
  "administrator",
  "secretary",
  "career_coordinator",
  "academic_director",
];

export function normalizeRoleCode(role: string | null | undefined): RoleCode | null {
  if (!role) return null;
  const aliases: Record<string, RoleCode> = {
    admin: "administrator",
    coordinator: "career_coordinator",
  };
  const normalized = aliases[role] ?? role;
  return roleCodes.includes(normalized as RoleCode) ? (normalized as RoleCode) : null;
}

export function primaryRoleFrom(roles: string[]): RoleCode {
  for (const role of roles) {
    const normalized = normalizeRoleCode(role);
    if (normalized) return normalized;
  }
  return "guest";
}
