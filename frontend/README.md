# PUCEASIG frontend

Frontend base del ERP/SIG academico PUCE Amazonas. El Sprint 0.5 deja lista la
fundacion visual y UX antes de iniciar pantallas funcionales del MVP.

## Stack

- Next.js con App Router.
- TypeScript.
- Tailwind CSS.
- Lucide React para iconografia.
- ESLint.
- npm como gestor inicial.

## Scripts

```bash
npm run dev
npm run lint
npm run typecheck
npm run build
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

## Que incluye el Sprint 0.5

- Tokens visuales institucionales en `config/theme.ts` y `app/globals.css`.
- Componentes UI reutilizables: botones, inputs, selects, cards, tablas, badges,
  dialog, alertas, tabs, breadcrumbs, paginacion y estados de feedback.
- Layout autenticado con sidebar, header, menu por rol y selector temporal de
  rol para prototipo.
- Prototipos publicos: login, recuperacion, preguntas de seguridad, 403, 404 y
  error general.
- Dashboards por rol.
- Wireframes navegables para estudiantes, docentes, roles, periodos, carreras,
  asignaturas, paralelos, oferta, matricula, silabos, notas, reportes y
  auditoria.
- Constructor visual de silabos nueva version.
- Prototipo visual de gestion de notas S1/S2/S3.

## Datos mock

Los datos sinteticos viven en `lib/mock-data.ts`. No usar datos reales de
estudiantes, docentes, autoridades, personal administrativo ni credenciales.

## Integracion futura

La autenticacion real, el consumo de API, permisos efectivos, persistencia de
silabos, motor de notas y reportes exportables quedan para los sprints
funcionales. El selector de rol se debe reemplazar en Sprint 1 por el perfil
obtenido desde la API.

## Verificacion

```bash
npm install
npm run lint
npm run typecheck
npm run build
```

`npm audit` reporta 2 vulnerabilidades moderadas transitivas en la base actual.
No se ejecuta `npm audit fix --force` por riesgo de cambios incompatibles.
