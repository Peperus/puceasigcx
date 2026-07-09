import type { RoleCode } from "@/config/roles";

export interface AuthenticatedUser {
  id: string;
  displayName: string;
  email: string;
  roles: RoleCode[];
}
