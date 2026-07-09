"use client";

import Link from "next/link";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import {
  BookOpen,
  ClipboardList,
  FileText,
  GraduationCap,
  LayoutDashboard,
  LogOut,
  Menu,
  ScrollText,
  Settings,
  ShieldCheck,
  Users,
} from "lucide-react";
import type { ReactNode } from "react";
import type { RoleCode } from "@/config/roles";
import { roleCodes, roleLabels } from "@/config/roles";
import { getNavigationForRole } from "@/config/navigation";
import { mockUserByRole } from "@/lib/mock-data";
import { cn } from "@/lib/utils";
import { Select } from "@/components/ui/select";
import { Button } from "@/components/ui/button";

const iconByHref = {
  "/dashboard": LayoutDashboard,
  "/estudiantes": GraduationCap,
  "/docentes": Users,
  "/roles": ShieldCheck,
  "/periodos": ClipboardList,
  "/carreras": BookOpen,
  "/asignaturas": BookOpen,
  "/paralelos": Settings,
  "/oferta": ClipboardList,
  "/matricula": GraduationCap,
  "/silabos": FileText,
  "/notas": ScrollText,
  "/reportes": FileText,
  "/auditoria": ShieldCheck,
} as const;

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const params = useSearchParams();
  const requestedRole = params.get("role") as RoleCode | null;
  const role = requestedRole && roleCodes.includes(requestedRole) ? requestedRole : "admin";
  const user = mockUserByRole[role];
  const navigation = getNavigationForRole(role);

  function setRole(nextRole: RoleCode) {
    const nextParams = new URLSearchParams(params.toString());
    nextParams.set("role", nextRole);
    router.push(`${pathname}?${nextParams.toString()}`);
  }

  return (
    <div className="min-h-screen bg-ui-background text-ui-text">
      <aside className="fixed inset-y-0 left-0 z-30 hidden w-[280px] border-r border-puce-blue-dark bg-puce-blue text-white lg:flex lg:flex-col">
        <div className="border-b border-white/15 p-5">
          <div className="text-xs font-bold uppercase text-puce-blue-soft">PUCEASIG</div>
          <div className="mt-2 text-xl font-black">ERP academico</div>
          <p className="mt-2 text-sm leading-5 text-blue-50">Prototipo Sprint 0.5 sin datos reales.</p>
        </div>
        <nav className="flex-1 space-y-1 overflow-y-auto p-3">
          {navigation.map((item) => {
            const Icon = iconByHref[item.href as keyof typeof iconByHref] ?? FileText;
            const active = pathname === item.href || pathname.startsWith(`${item.href}/`);

            return (
              <Link
                className={cn(
                  "flex min-h-11 items-center gap-3 rounded-puce-sm px-3 text-sm font-bold transition-colors",
                  active ? "bg-white text-puce-blue" : "text-blue-50 hover:bg-white/10",
                )}
                href={`${item.href}?role=${role}`}
                key={item.href}
              >
                <Icon size={18} />
                {item.label}
              </Link>
            );
          })}
        </nav>
      </aside>

      <div className="lg:pl-[280px]">
        <header className="sticky top-0 z-20 border-b border-ui-border bg-white/95 backdrop-blur">
          <div className="flex min-h-[64px] items-center justify-between gap-3 px-4 sm:px-6">
            <div className="flex min-w-0 items-center gap-3">
              <Button aria-label="Abrir menu movil" className="h-10 min-h-10 w-10 px-0 lg:hidden" variant="outline">
                <Menu size={18} />
              </Button>
              <div className="min-w-0">
                <p className="truncate text-sm font-bold text-puce-blue">{roleLabels[role]}</p>
                <p className="truncate text-xs text-ui-text-muted">{user.context}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <label className="hidden text-sm font-bold text-ui-text-muted sm:block" htmlFor="role-selector">
                Rol prototipo
              </label>
              <Select
                className="w-44"
                id="role-selector"
                onChange={(event) => setRole(event.target.value as RoleCode)}
                value={role}
              >
                {roleCodes.map((code) => (
                  <option key={code} value={code}>
                    {roleLabels[code]}
                  </option>
                ))}
              </Select>
              <div className="hidden text-right md:block">
                <p className="text-sm font-bold">{user.name}</p>
                <p className="text-xs text-ui-text-muted">Sesion visual</p>
              </div>
              <Button aria-label="Cerrar sesion placeholder" className="h-10 min-h-10 w-10 px-0" variant="ghost">
                <LogOut size={18} />
              </Button>
            </div>
          </div>
        </header>
        <main className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6">{children}</main>
      </div>
    </div>
  );
}
