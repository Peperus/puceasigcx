import type { NavigationItem } from "@/types/navigation";

export const navigationShell: NavigationItem[] = [
  {
    label: "Dashboard",
    href: "/dashboard",
    roles: ["admin", "secretary", "coordinator", "teacher", "student"],
  },
  {
    label: "Academico",
    href: "/academico",
    roles: ["admin", "secretary", "coordinator"],
  },
  {
    label: "Silabos",
    href: "/silabos",
    roles: ["admin", "coordinator", "teacher", "student"],
  },
  {
    label: "Notas",
    href: "/notas",
    roles: ["admin", "secretary", "coordinator", "teacher", "student"],
  },
  {
    label: "Reportes",
    href: "/reportes",
    roles: ["admin", "secretary", "coordinator"],
  },
];
