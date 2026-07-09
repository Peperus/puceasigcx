import type { RoleCode } from "@/config/roles";

export interface NavigationItem {
  label: string;
  href: string;
  description?: string;
  group: "principal" | "academico" | "gestion" | "seguimiento";
  roles: RoleCode[];
}
