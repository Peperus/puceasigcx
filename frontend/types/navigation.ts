import type { RoleCode } from "@/config/roles";

export interface NavigationItem {
  label: string;
  href: string;
  roles: RoleCode[];
}
