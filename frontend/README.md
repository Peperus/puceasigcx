# PUCEASIG frontend

Frontend del ERP/SIG academico PUCE Amazonas. Sprint 8.5 convierte la base visual
del Sprint 0.5 en una UI funcional conectada a las APIs reales del MVP.

## Stack

- Next.js con App Router.
- TypeScript.
- Tailwind CSS.
- Lucide React para iconografia.
- ESLint.
- Playwright para smoke E2E.
- npm como gestor inicial.

## Scripts

```bash
npm run dev
npm run lint
npm run typecheck
npm run build
npm run e2e
```

`npm run dev` usa Webpack por defecto. Next.js 16.2.10 con Turbopack puede
disparar un error interno de Next DevTools al navegar rutas anidadas del App
Router; el build de produccion no presenta ese problema.
En desarrollo tambien se reemplaza el modulo cliente de Next DevTools por un
shim no-op para evitar que el Segment Explorer interno capture la pantalla.

## Estructura principal

```text
frontend/
├── app/
│   ├── (auth)/
│   ├── (dashboard)/
│   ├── 403/
│   ├── error.tsx
│   ├── not-found.tsx
│   └── page.tsx
├── components/
│   ├── dashboard/
│   ├── feedback/
│   ├── layout/
│   ├── prototypes/
│   └── ui/
├── config/
├── lib/
└── types/
```

## Integracion Sprint 8.5

- Login real contra `/api/auth/login/`, refresh, logout y perfil `/api/me/`.
- Shell autenticado con navegacion filtrada por roles reales.
- Catalogos, personas, estudiantes, docentes, oferta, cursos, asignaciones y
  matriculas conectados a DRF.
- Workspace de silabos con secciones, flujo de revision y carga de PDF firmado.
- Workspace de notas docente/estudiante conectado a gradebooks y snapshots.
- Reportes MVP, consulta de notas, auditoria y exportaciones CSV/XLSX.
- Dashboards por rol usando endpoints reales disponibles y estados vacios honestos.
- Smoke E2E desktop/mobile para login, proteccion de rutas y 403.

## Datos mock

Los datos sinteticos viven en `lib/mock-data.ts`. No usar datos reales de
estudiantes, docentes, autoridades, personal administrativo ni credenciales.

## Configuracion API

Configure `NEXT_PUBLIC_API_BASE_URL` si el backend no corre en
`http://localhost:8000/api`. No guarde credenciales reales en archivos del repo.

## Verificacion

```bash
npm install
npm run lint
npm run typecheck
npm run build
npm run e2e
```

`npm audit` reporta 2 vulnerabilidades moderadas transitivas en la base actual.
No se ejecuta `npm audit fix --force` por riesgo de cambios incompatibles.
