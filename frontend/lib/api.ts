const fallbackApiBaseUrl = "http://localhost:8000/api";

export const apiConfig = {
  baseUrl: process.env.NEXT_PUBLIC_API_BASE_URL ?? fallbackApiBaseUrl,
  mocksEnabled: process.env.NEXT_PUBLIC_ENABLE_MOCKS !== "false",
} as const;
