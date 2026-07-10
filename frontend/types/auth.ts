import type { RoleCode } from "@/config/roles";

export interface AuthenticatedUser {
  id: string;
  displayName: string;
  email: string;
  roles: RoleCode[];
}

export interface CurrentUser {
  id: number;
  email: string;
  names: string;
  last_names: string;
  full_name: string;
  phone: string;
  is_active: boolean;
  roles: string[];
  profile: Record<string, unknown>;
}
