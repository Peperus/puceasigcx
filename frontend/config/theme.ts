export const themeConfig = {
  name: "PUCEASIG institutional theme",
  source: {
    label: "PUCE public website",
    url: "https://www.puce.edu.ec/",
    reviewedAt: "2026-07-09",
    notes: [
      "Blue institutional mark and navigation accents.",
      "Turquoise support color for highlights and interactive states.",
      "White content surfaces with soft gray section backgrounds.",
      "Dark gray utility bar and strong contrast over photography.",
    ],
  },
  colors: {
    brand: {
      primary: "#003B81",
      primaryDark: "#002B5C",
      primarySoft: "#E7F0FA",
      secondary: "#00BFD8",
      secondaryDark: "#008DA6",
      sky: "#00A0DD",
      topbar: "#40424D",
    },
    neutral: {
      white: "#FFFFFF",
      background: "#F7F7F7",
      surface: "#FFFFFF",
      surfaceMuted: "#F3F5F7",
      border: "#DDE3EA",
      text: "#1F2933",
      textMuted: "#5F6B7A",
      textSubtle: "#7B8794",
    },
    semantic: {
      success: "#0F8A5F",
      successSoft: "#E7F6EF",
      warning: "#B7791F",
      warningSoft: "#FFF5DA",
      danger: "#B42318",
      dangerSoft: "#FDECEC",
      info: "#006FBF",
      infoSoft: "#E6F2FC",
    },
  },
  typography: {
    heading:
      'var(--font-geist-sans), "Open Sans", Arial, Helvetica, sans-serif',
    body: 'var(--font-geist-sans), "Open Sans", Arial, Helvetica, sans-serif',
    mono: "var(--font-geist-mono), Consolas, monospace",
    weights: {
      regular: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      black: 900,
    },
  },
  radius: {
    xs: "3px",
    sm: "4px",
    md: "6px",
    lg: "8px",
  },
  shadows: {
    xs: "0 1px 2px rgb(15 23 42 / 0.06)",
    sm: "0 4px 10px rgb(15 23 42 / 0.08)",
    md: "0 12px 24px rgb(15 23 42 / 0.10)",
    focus: "0 0 0 3px rgb(0 191 216 / 0.28)",
  },
  spacing: {
    pageX: "24px",
    sectionY: "32px",
    cardPadding: "20px",
    fieldGap: "12px",
  },
  sizing: {
    inputHeight: "42px",
    buttonHeight: "42px",
    sidebarWidth: "280px",
    headerHeight: "64px",
  },
} as const;

export type ThemeConfig = typeof themeConfig;
