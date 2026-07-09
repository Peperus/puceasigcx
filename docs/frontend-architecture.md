# Arquitectura frontend

El frontend del MVP se definira y construira en Sprint 0.5 antes de implementar pantallas funcionales del MVP.

## Decision tecnica

- Framework: Next.js.
- Lenguaje: TypeScript.
- Estilos: Tailwind CSS.
- Formularios: React Hook Form + Zod cuando existan formularios funcionales.
- Tablas: TanStack Table o componente propio simple al inicio.
- Fetch/cache: TanStack Query cuando se consuma API real.
- Componentes UI: shadcn/ui o componentes propios equivalentes, centralizados y reutilizables.

## Objetivo del Sprint 0.5

Sprint 0.5 debe fijar la base visual y de experiencia antes de Sprint 1:

- Crear `/frontend`.
- Configurar Next.js, TypeScript y Tailwind CSS.
- Definir tema visual institucional sin usar logos oficiales si no estan en el repositorio.
- Crear layout autenticado con sidebar y header.
- Crear navegacion por rol.
- Crear componentes reutilizables: botones, inputs, tablas, cards, badges, dialogs y estados vacios.
- Crear prototipos navegables con datos mock sinteticos.
- Documentar `docs/frontend-design-system.md` y `frontend/README.md`.

## Reglas de UX

- No usar datos reales en mocks.
- Mantener contraste, labels, foco visible y errores claros.
- Reutilizar tokens, layouts y componentes.
- Evitar duplicar componentes visuales sin justificacion.
- No incluir logos oficiales o assets institucionales si no existen en el repositorio.
- No depender del frontend para seguridad: los permisos reales se validan en backend.

## Pantallas prototipo esperadas

Durante Sprint 0.5 se prepararan prototipos para:

- Dashboard por rol.
- Estudiantes.
- Docentes.
- Catalogos academicos.
- Silabos.
- Notas.
- Reportes.
- Auditoria o actividad reciente.

Estos prototipos no deben implementar reglas de negocio reales ni consumir datos reales hasta que los endpoints existan.

## Integracion con API

Cuando el backend exponga endpoints reales:

- Centralizar cliente HTTP.
- Manejar estados de carga, error y vacio.
- Usar validacion de formularios con Zod.
- Propagar errores de permisos y validacion del backend.
- Evitar duplicar reglas criticas de negocio en frontend.
