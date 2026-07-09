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
- Mantener tokens visuales completos en `config/theme.ts` y variables CSS en
  `app/globals.css`.

## Tema visual institucional

Referencia publica revisada: https://www.puce.edu.ec/ el 2026-07-09.

La identidad visual se traduce al ERP como una interfaz sobria y operativa:

- Azul institucional `#003B81` para navegacion principal, encabezados y
  acciones primarias.
- Azul profundo `#002B5C` para estados activos, sidebar o superficies de alto
  contraste.
- Turquesa `#00BFD8` y celeste `#00A0DD` para foco, enlaces, indicadores y
  acentos.
- Blanco y grises neutros para superficies, tablas, filtros y secciones de
  trabajo.
- Barra superior gris oscuro `#40424D` para utilidades o contexto de sesion.

Los colores semanticos no deben improvisarse desde la paleta de marca:

- Exito: `#0F8A5F`.
- Advertencia: `#B7791F`.
- Error: `#B42318`.
- Informacion: `#006FBF`.

Las superficies usan radios discretos entre `3px` y `8px`. Inputs y botones
parten de `42px` de alto. Las sombras deben ser sutiles y reservarse para
paneles, menus y foco.

No se incluye logotipo oficial. El layout debe reservar un espacio de marca que
pueda recibir un asset autorizado mas adelante.

## Verificacion del ticket

```bash
npm install
npm run lint
npm run typecheck
npm run build
```
