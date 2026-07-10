"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { currentUser, loadApiTokens, login as apiLogin, logout as apiLogout, setApiTokens } from "@/lib/api";
import { primaryRoleFrom, type RoleCode } from "@/config/roles";
import type { CurrentUser } from "@/types/auth";

type AuthContextValue = {
  user: CurrentUser | null;
  role: RoleCode;
  loading: boolean;
  error: string | null;
  refreshSession: () => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  hasAnyRole: (roles: RoleCode[]) => boolean;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refreshSession = useCallback(async () => {
    const tokens = loadApiTokens();
    if (!tokens) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      setError(null);
      setUser(await currentUser());
    } catch (err) {
      setApiTokens(null);
      setUser(null);
      setError(err instanceof Error ? err.message : "No se pudo cargar la sesion.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => void refreshSession(), 0);
    return () => window.clearTimeout(timer);
  }, [refreshSession]);

  const login = useCallback(async (email: string, password: string) => {
    setLoading(true);
    try {
      setError(null);
      setUser(await apiLogin(email, password));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Credenciales invalidas.");
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    setLoading(true);
    await apiLogout();
    setUser(null);
    setLoading(false);
  }, []);

  const role = primaryRoleFrom(user?.roles ?? []);
  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      role,
      loading,
      error,
      refreshSession,
      login,
      logout,
      hasAnyRole: (roles) => roles.some((candidate) => user?.roles.includes(candidate)),
    }),
    [error, loading, login, logout, refreshSession, role, user],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error("useAuth debe usarse dentro de AuthProvider.");
  return value;
}
