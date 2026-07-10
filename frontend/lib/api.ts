import type { CurrentUser } from "@/types/auth";

const fallbackApiBaseUrl = "http://localhost:8000/api";

export const apiConfig = {
  baseUrl: process.env.NEXT_PUBLIC_API_BASE_URL ?? fallbackApiBaseUrl,
} as const;

export type SessionTokens = {
  access: string;
  refresh: string;
};

export type LoginResponse = SessionTokens & {
  user: CurrentUser;
};

export type PaginatedResponse<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};

export type ListResponse<T> = T[] | PaginatedResponse<T>;

export class ApiError extends Error {
  status: number;
  details: unknown;

  constructor(message: string, status: number, details: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.details = details;
  }
}

let accessToken: string | null = null;
let refreshToken: string | null = null;

function isBrowser() {
  return typeof window !== "undefined";
}

export function setApiTokens(tokens: Partial<SessionTokens> | null) {
  accessToken = tokens?.access ?? null;
  refreshToken = tokens?.refresh ?? null;
  if (!isBrowser()) return;
  if (accessToken && refreshToken) {
    window.localStorage.setItem("puceasig_tokens", JSON.stringify({ access: accessToken, refresh: refreshToken }));
  } else {
    window.localStorage.removeItem("puceasig_tokens");
  }
}

export function loadApiTokens(): SessionTokens | null {
  if (!isBrowser()) return null;
  const raw = window.localStorage.getItem("puceasig_tokens");
  if (!raw) return null;
  try {
    const tokens = JSON.parse(raw) as SessionTokens;
    if (!tokens.access || !tokens.refresh) return null;
    accessToken = tokens.access;
    refreshToken = tokens.refresh;
    return tokens;
  } catch {
    setApiTokens(null);
    return null;
  }
}

function urlFor(path: string, params?: Record<string, string | number | boolean | null | undefined>) {
  const base = apiConfig.baseUrl.replace(/\/$/, "");
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  const url = new URL(`${base}${cleanPath}`);
  Object.entries(params ?? {}).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") url.searchParams.set(key, String(value));
  });
  return url.toString();
}

async function parseResponse(response: Response) {
  const contentType = response.headers.get("content-type") ?? "";
  if (contentType.includes("application/json")) return response.json();
  if (response.status === 204) return null;
  return response.text();
}

function errorMessage(details: unknown, status: number) {
  if (typeof details === "string" && details) return details;
  if (details && typeof details === "object") {
    const record = details as Record<string, unknown>;
    if (typeof record.detail === "string") return record.detail;
    const first = Object.values(record)[0];
    if (Array.isArray(first)) return String(first[0]);
    if (typeof first === "string") return first;
  }
  if (status === 401) return "La sesion expiro o no ha iniciado sesion.";
  if (status === 403) return "No tiene permisos para realizar esta accion.";
  return "No se pudo completar la solicitud.";
}

async function refreshAccessToken() {
  if (!refreshToken) return false;
  const response = await fetch(urlFor("/auth/refresh/"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh: refreshToken }),
  });
  if (!response.ok) {
    setApiTokens(null);
    return false;
  }
  const data = (await response.json()) as { access: string };
  setApiTokens({ access: data.access, refresh: refreshToken });
  return true;
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit & { params?: Record<string, string | number | boolean | null | undefined>; retry?: boolean } = {},
): Promise<T> {
  if (!accessToken) loadApiTokens();
  const headers = new Headers(options.headers);
  if (!(options.body instanceof FormData) && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (accessToken) headers.set("Authorization", `Bearer ${accessToken}`);
  const response = await fetch(urlFor(path, options.params), {
    ...options,
    headers,
  });
  if (response.status === 401 && options.retry !== false && refreshToken && (await refreshAccessToken())) {
    return apiRequest<T>(path, { ...options, retry: false });
  }
  const data = await parseResponse(response);
  if (!response.ok) throw new ApiError(errorMessage(data, response.status), response.status, data);
  return data as T;
}

export function listItems<T>(payload: ListResponse<T>): T[] {
  return Array.isArray(payload) ? payload : payload.results;
}

export async function login(email: string, password: string) {
  const response = await apiRequest<LoginResponse>("/auth/login/", {
    method: "POST",
    body: JSON.stringify({ email, password }),
    retry: false,
  });
  setApiTokens({ access: response.access, refresh: response.refresh });
  return response.user;
}

export async function logout() {
  const tokens = loadApiTokens();
  try {
    if (tokens?.refresh) {
      await apiRequest<null>("/auth/logout/", {
        method: "POST",
        body: JSON.stringify({ refresh: tokens.refresh }),
        retry: false,
      });
    }
  } finally {
    setApiTokens(null);
  }
}

export async function currentUser() {
  return apiRequest<CurrentUser>("/me/");
}

export async function downloadFile(
  path: string,
  filename: string,
  params?: Record<string, string | number | boolean | null | undefined>,
) {
  if (!accessToken) loadApiTokens();
  const headers = new Headers();
  if (accessToken) headers.set("Authorization", `Bearer ${accessToken}`);
  const response = await fetch(urlFor(path, params), { headers });
  if (!response.ok) {
    const details = await parseResponse(response);
    throw new ApiError(errorMessage(details, response.status), response.status, details);
  }
  const blob = await response.blob();
  const objectUrl = window.URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = objectUrl;
  anchor.download = filename;
  anchor.click();
  window.URL.revokeObjectURL(objectUrl);
}
