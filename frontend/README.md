# PUCEASIG frontend

Frontend base del ERP/SIG academico PUCE Amazonas. Este directorio corresponde
al ticket `S0.5-T1` y deja preparada la estructura para el sistema de diseno,
layout autenticado, navegacion por rol y prototipos navegables del Sprint 0.5.

## Stack

- Next.js con App Router.
- TypeScript en modo estricto.
- Tailwind CSS.
- ESLint.
- npm como gestor de paquetes inicial.

## Scripts

```bash
npm run dev
npm run lint
npm run typecheck
npm run build
```

## Estructura

```text
frontend/
├── app/
│   ├── (auth)/
│   ├── (dashboard)/
│   ├── globals.css
│   └── layout.tsx
├── components/
│   ├── layout/
│   ├── ui/
│   ├── forms/
│   ├── tables/
│   ├── dashboard/
│   └── feedback/
├── config/
│   ├── navigation.ts
│   ├── roles.ts
│   └── theme.ts
├── lib/
│   ├── api.ts
│   ├── mock-data.ts
│   └── utils.ts
├── types/
│   ├── academic.ts
│   ├── auth.ts
│   └── navigation.ts
└── README.md
```

## Variables de entorno

Copiar las claves de `.env.example` al entorno local cuando se necesite
configuracion. Los valores incluidos son ficticios y no contienen credenciales.

## Convenciones iniciales

- Mantener mocks sinteticos y centralizados en `lib/mock-data.ts`.
- Centralizar roles y navegacion en `config/`.
- No consumir API real hasta que el sprint funcional correspondiente lo pida.
- No incluir logos oficiales ni datos reales si no existen en el repositorio.
- Definir tokens visuales completos en `config/theme.ts` durante `S0.5-T2`.

## Verificacion del ticket

```bash
npm install
npm run lint
npm run typecheck
npm run build
```
