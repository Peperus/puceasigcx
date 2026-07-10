"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
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
import { useEffect } from "react";
import { roleLabels } from "@/config/roles";
import { getNavigationForRole } from "@/config/navigation";
import { useAuth } from "@/lib/auth";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { LoadingState } from "@/components/feedback/loading-state";

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
  const { user, role, loading, logout } = useAuth();
  const navigation = getNavigationForRole(role);

  useEffect(() => {
    if (!window.localStorage.getItem("puceasig_tokens")) {
      router.replace(`/login?next=${encodeURIComponent(pathname)}`);
    }
  }, [pathname, router]);

  useEffect(() => {
    if (!loading && !user) {
      const timer = window.setTimeout(() => {
        router.replace(`/login?next=${encodeURIComponent(pathname)}`);
      }, 0);
      return () => window.clearTimeout(timer);
    }
    return undefined;
  }, [loading, pathname, router, user]);

  if (loading || !user) {
    return (
      <main className="min-h-screen bg-ui-background p-6">
        <LoadingState label="Validando sesion institucional" />
      </main>
    );
  }

  return (
    <div className="min-h-screen bg-ui-background text-ui-text">
      <aside className="fixed inset-y-0 left-0 z-30 hidden w-[280px] border-r border-puce-blue-dark bg-puce-blue text-white lg:flex lg:flex-col">
        <div className="border-b border-white/15 p-5">
          <div className="text-xs font-bold uppercase text-puce-blue-soft">PUCEASIG</div>
          <div className="mt-2 text-xl font-black">ERP academico</div>
          <p className="mt-2 text-sm leading-5 text-blue-50">MVP conectado a API real.</p>
        </div>
        <nav className="flex-1 space-y-1 overflow-y-auto p-3">
          {navigation.map((item) => {
            const Icon = iconByHref[item.href as keyof typeof iconByHref] ?? FileText;
            const active = pathname === item.href || pathname.startsWith(`${item.href}/`);

            return (
              <Link
                className={cn(
                  "flex min-h-11 items-center gap-3 rounded-puce-sm px-3 text-sm font-bold transition-colors",
                  active ? "bg-white font-black shadow-puce-xs" : "text-blue-50 hover:bg-white/10",
                )}
                href={item.href}
                key={item.href}
                style={active ? { color: "var(--color-brand-primary)" } : undefined}
              >
                <Icon className="shrink-0" size={18} />
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
                <p className="truncate text-xs text-ui-text-muted">{user.email}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="hidden text-right md:block">
                <p className="text-sm font-bold">{user.full_name || user.email}</p>
                <p className="text-xs text-ui-text-muted">Sesion real</p>
              </div>
              <Button
                aria-label="Cerrar sesion"
                className="h-10 min-h-10 w-10 px-0"
                onClick={() => void logout().then(() => router.replace("/login"))}
                variant="ghost"
              >
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
