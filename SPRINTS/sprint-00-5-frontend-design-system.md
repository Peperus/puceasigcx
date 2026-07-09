# Sprint 0.5 — Frontend Design System & UX Foundation

**Objetivo:** definir la base visual, de navegación y experiencia de usuario del ERP académico PUCE Amazonas antes de implementar pantallas funcionales por módulo.

**Salida esperada:** frontend inicial con diseño institucional, layout protegido, componentes reutilizables, wireframes navegables y pantallas prototipo del MVP usando datos mock, listo para que los sprints 1–8 implementen módulos reales sin improvisar diseño.

**Dependencias:**
- Sprint 0 — Foundation, al menos estructura de repositorio definida.
- `docs/project-reference-puceasig.md` disponible en el repositorio.
- `PROGRESS.md` disponible en la raíz.

**Sprint recomendado antes de:** Sprint 1 — Auth & Roles.

> Cada ticket = 1 rama = 1 PR = 1 sesión de trabajo con Codex.  
> Cierra un ticket solo cuando sus criterios de aceptación y verificaciones pasen.  
> Este sprint no debe implementar lógica de negocio completa ni conectar todavía todos los módulos al backend real. Su prioridad es dejar un sistema visual coherente, reusable y preparado para integración progresiva.

---

## Decisión de frontend para el MVP

Para el MVP se recomienda trabajar con:

- **Frontend:** Next.js + TypeScript.
- **Estilos:** Tailwind CSS.
- **Componentes base:** shadcn/ui o componentes propios equivalentes.
- **Validación de formularios:** React Hook Form + Zod, cuando existan formularios funcionales.
- **Tablas:** TanStack Table o componente propio inicialmente simple.
- **Iconografía:** Lucide React o librería equivalente.
- **Estado de datos:** TanStack Query cuando se empiece a consumir API real.
- **Gráficos futuros:** Recharts o alternativa equivalente para dashboards.
- **Autenticación futura:** consumo de JWT emitido por Django REST Framework.

Si el repositorio todavía no tiene frontend, este sprint debe crear `/frontend`. Si ya existe, debe adaptar lo existente sin romperlo.

---

## Principios de diseño del ERP académico

1. Priorizar claridad institucional sobre efectos visuales innecesarios.
2. Diseñar para usuarios administrativos, docentes y estudiantes con distintos niveles de competencia digital.
3. Mantener navegación lateral por rol, con opciones visibles según permisos.
4. Reutilizar componentes: formularios, tablas, filtros, tarjetas, badges, modales y layouts.
5. Evitar datos reales en prototipos; usar datos mock claramente ficticios.
6. Preparar pantallas responsive para escritorio, tablet y móvil.
7. Mantener accesibilidad básica: contraste, foco visible, labels, estados de error y navegación por teclado.
8. No incrustar credenciales, tokens, endpoints privados ni assets oficiales no proporcionados.
9. Separar componentes visuales de lógica de negocio.
10. Documentar decisiones para que Codex mantenga consistencia en sprints posteriores.

---

## Roles que deben guiar la navegación

El diseño debe contemplar, como mínimo, los siguientes perfiles:

| Rol | Enfoque de interfaz |
|---|---|
| Administrador | Configuración general, usuarios, roles, catálogos, auditoría y parámetros del sistema. |
| Secretaría | Periodos, oferta académica, estudiantes, matrícula, reportes y consulta de notas. |
| Coordinador de carrera | Oferta académica, docentes, sílabos, seguimiento académico, reportes por carrera. |
| Docente | Mis asignaturas, sílabos, calificaciones, inasistencias, guías y biblioteca académica. |
| Estudiante | Mis asignaturas, notas, sílabos, asistencia, biblioteca y requerimientos. |
| Bienestar / Apoyo institucional | Consulta de estudiantes, seguimiento, alertas y reportes permitidos. |

---

## Inventario mínimo de pantallas del MVP

Este sprint debe dejar prototipos navegables, no necesariamente integrados a API real, de:

1. Login institucional.
2. Recuperación de contraseña.
3. Layout base autenticado.
4. Dashboard administrador.
5. Dashboard secretaría.
6. Dashboard coordinador de carrera.
7. Dashboard docente.
8. Dashboard estudiante.
9. Gestión de estudiantes.
10. Gestión de docentes.
11. Gestión de roles y permisos.
12. Gestión de periodos académicos.
13. Gestión de carreras, mallas, asignaturas y paralelos.
14. Oferta académica y asignación docente.
15. Matrícula / inscripción de estudiantes.
16. Gestión de sílabos.
17. Constructor de sílabo nueva versión.
18. Carga de sílabo aprobado en PDF.
19. Gestión de notas S1/S2/S3.
20. Carga de calificaciones por docente.
21. Consulta de notas por secretaría.
22. Consulta de notas por estudiante.
23. Reportes académicos básicos.
24. Auditoría / trazabilidad.
25. Página 403 / acceso no autorizado.
26. Página 404.
27. Estado vacío, estado de carga y estado de error.

---

## S0.5-T1 — Crear estructura frontend base

**Tareas**
- Crear `/frontend` con Next.js + TypeScript, si no existe.
- Configurar Tailwind CSS.
- Configurar estructura de carpetas recomendada:

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

- Crear scripts básicos: `dev`, `build`, `lint`, `typecheck`.
- Configurar alias de imports, por ejemplo `@/components`, `@/lib`, `@/types`.
- Crear `.env.example` para frontend con variables públicas ficticias.

**Criterios de aceptación**
- `npm run dev` o `pnpm dev` levanta el frontend sin errores.
- `npm run build` o `pnpm build` compila correctamente.
- La estructura de carpetas queda documentada en `frontend/README.md`.
- No hay dependencias innecesarias ni credenciales reales.

**Verificación**
```bash
cd frontend
npm install
npm run lint
npm run build
```

**Prompt sugerido para Codex**

```text
Lee PROGRESS.md, docs/project-reference-puceasig.md y SPRINTS/sprint-00-5-frontend-design-system.md. Trabaja únicamente el ticket S0.5-T1.

Crea la estructura base del frontend para el ERP académico PUCE Amazonas usando Next.js + TypeScript + Tailwind CSS. Si /frontend no existe, créalo. Si existe, adapta lo mínimo necesario sin romper lo anterior.

No implementes todavía lógica real de autenticación ni consumo real de API. Deja preparada la estructura, scripts, alias de imports, carpetas, README del frontend y .env.example sin credenciales reales.

Al finalizar, ejecuta lint/build si el entorno lo permite y documenta cualquier limitación encontrada.
```

---

## S0.5-T2 — Definir tema visual institucional y tokens de diseño

**Tareas**
- Crear tokens de diseño en `frontend/config/theme.ts` o equivalente.
- Definir paleta institucional inspirada en PUCE Amazonas:
  - azul institucional,
  - celeste/turquesa de apoyo,
  - blanco,
  - grises neutros,
  - colores semánticos para éxito, advertencia, error e información.
- Definir tipografía base del sistema.
- Definir radios, sombras, espacios, alturas de inputs y botones.
- Crear guía breve de uso visual en `frontend/README.md` o `docs/frontend-design-system.md`.
- Reservar espacio para logotipo institucional sin incluir archivos oficiales si no han sido proporcionados.

**Criterios de aceptación**
- El tema visual está centralizado y no disperso en cada componente.
- Los colores semánticos se usan por intención, no por nombres improvisados.
- El diseño mantiene contraste suficiente en botones, textos y estados.
- Existe documentación breve para que Codex reutilice el tema en sprints posteriores.

**Verificación**
```bash
cd frontend
npm run lint
npm run build
```

**Prompt sugerido para Codex**

```text
Lee PROGRESS.md y el ticket S0.5-T2. Define un tema visual institucional para el frontend del ERP académico PUCE Amazonas.

Centraliza tokens de diseño: colores, tipografía, espaciado, radios, sombras y estados semánticos. No uses logos oficiales salvo que existan en el repositorio. Reserva un componente/espacio para el logo.

Actualiza la documentación del frontend con las decisiones visuales. No implementes pantallas funcionales todavía.
```

---

## S0.5-T3 — Crear componentes UI reutilizables

**Tareas**
- Crear componentes base en `components/ui` y `components/feedback`:
  - `Button`.
  - `Input`.
  - `Textarea`.
  - `Select`.
  - `Checkbox`.
  - `Label`.
  - `Card`.
  - `Badge`.
  - `Table`.
  - `Modal/Dialog`.
  - `Alert`.
  - `Tabs`.
  - `Breadcrumbs`.
  - `Pagination`.
  - `EmptyState`.
  - `LoadingState`.
  - `ErrorState`.
- Crear variantes visuales para estados académicos:
  - Borrador.
  - Pendiente.
  - En revisión.
  - Aprobado.
  - Rechazado.
  - Cerrado.
- Crear variantes para resultados académicos:
  - Aprobado.
  - Reprobado.
  - Recuperación.
  - Sin calificar.

**Criterios de aceptación**
- Los componentes son reutilizables y tipados.
- No hay duplicación innecesaria de estilos.
- Las variantes están documentadas o son fáciles de identificar.
- Los componentes no dependen de datos reales ni de API real.

**Verificación**
```bash
cd frontend
npm run lint
npm run build
```

**Prompt sugerido para Codex**

```text
Lee PROGRESS.md y el ticket S0.5-T3. Implementa componentes UI reutilizables para el frontend del ERP académico.

Crea componentes tipados y simples para botones, inputs, selects, cards, tablas, badges, modales, alertas, breadcrumbs, paginación y estados de carga/error/vacío. Agrega variantes para estados académicos y resultados de calificación.

No conectes con API real. No crees lógica de negocio compleja. Mantén el diseño consistente con el tema visual definido.
```

---

## S0.5-T4 — Layout institucional autenticado y navegación por rol

**Tareas**
- Crear layout base para usuarios autenticados:
  - sidebar lateral,
  - header superior,
  - área principal de contenido,
  - breadcrumb,
  - menú de usuario,
  - botón de cerrar sesión placeholder.
- Crear `config/navigation.ts` con menús por rol.
- Crear navegación mínima para:
  - Administrador.
  - Secretaría.
  - Coordinador.
  - Docente.
  - Estudiante.
- Crear selector temporal de rol en modo prototipo para visualizar cada menú sin autenticación real.
- Preparar estructura para que en Sprint 1 el rol venga desde `/api/me` o `/api/profile`.

**Criterios de aceptación**
- El layout se visualiza correctamente en escritorio.
- En pantallas pequeñas, el sidebar puede colapsar o transformarse en menú móvil.
- Los menús cambian según el rol seleccionado en modo prototipo.
- El diseño no asume que todos los usuarios ven todos los módulos.

**Verificación**
```bash
cd frontend
npm run lint
npm run build
```

**Prompt sugerido para Codex**

```text
Lee PROGRESS.md y el ticket S0.5-T4. Crea el layout autenticado del ERP académico PUCE Amazonas y la navegación por rol.

Implementa sidebar, header, área de contenido, breadcrumb y menú de usuario. Define navigation.ts con opciones diferenciadas para Administrador, Secretaría, Coordinador, Docente y Estudiante.

Usa un selector temporal de rol únicamente para prototipo. No implementes autenticación real en este ticket.
```

---

## S0.5-T5 — Prototipos de autenticación y páginas públicas

**Tareas**
- Crear página de login institucional.
- Crear página de recuperación de contraseña.
- Crear página de validación de preguntas de seguridad como referencia funcional futura.
- Crear página 403.
- Crear página 404.
- Crear página de error general.
- Usar formularios visuales con validaciones mínimas del lado cliente, sin conexión real al backend.

**Criterios de aceptación**
- Login y recuperación de contraseña tienen apariencia institucional.
- Los formularios tienen labels, mensajes de ayuda y estados de error.
- Las páginas públicas no muestran menús internos.
- Las páginas 403/404 son claras y permiten volver al inicio.

**Verificación**
```bash
cd frontend
npm run lint
npm run build
```

**Prompt sugerido para Codex**

```text
Lee PROGRESS.md y el ticket S0.5-T5. Crea prototipos visuales para login, recuperación de contraseña, validación de preguntas de seguridad, página 403, página 404 y error general.

No conectes aún con el backend. Usa formularios visuales, validaciones mínimas y mensajes claros. Mantén consistencia con el tema institucional.
```

---

## S0.5-T6 — Dashboards prototipo por rol

**Tareas**
- Crear dashboards con datos mock para:
  - Administrador.
  - Secretaría.
  - Coordinador de carrera.
  - Docente.
  - Estudiante.
- Cada dashboard debe incluir tarjetas e indicadores coherentes con su rol.
- Ejemplos de indicadores:
  - Periodo académico activo.
  - Carreras activas.
  - Estudiantes matriculados.
  - Docentes vinculados.
  - Sílabos pendientes/aprobados.
  - Asignaturas asignadas.
  - Notas pendientes.
  - Resultados de aprendizaje en riesgo.
  - Requerimientos pendientes.
- Crear componentes de tarjetas reutilizables.

**Criterios de aceptación**
- Cada rol tiene una página de dashboard diferenciada.
- Los datos son mock y están centralizados en `lib/mock-data.ts`.
- Las tarjetas son reutilizables.
- No se exponen datos reales.

**Verificación**
```bash
cd frontend
npm run lint
npm run build
```

**Prompt sugerido para Codex**

```text
Lee PROGRESS.md y el ticket S0.5-T6. Crea dashboards prototipo para Administrador, Secretaría, Coordinador, Docente y Estudiante usando datos mock.

Cada dashboard debe reflejar las tareas principales de su rol dentro del ERP académico. Centraliza los datos mock y usa componentes reutilizables.

No conectes con API real ni uses datos reales.
```

---

## S0.5-T7 — Wireframes navegables de módulos del MVP

**Tareas**
- Crear pantallas prototipo navegables para:
  - Gestión de estudiantes.
  - Gestión de docentes.
  - Gestión de roles.
  - Periodos académicos.
  - Carreras.
  - Asignaturas.
  - Paralelos.
  - Oferta académica.
  - Matrícula.
  - Sílabos.
  - Constructor de sílabos.
  - Carga de sílabo firmado.
  - Gestión de notas.
  - Carga de notas docente.
  - Consulta de notas estudiante.
  - Reportes académicos.
  - Auditoría.
- Usar tablas, filtros, acciones y estados mock.
- Diseñar formularios representativos sin implementar validaciones complejas.
- Preparar estructura para que cada pantalla sea reemplazada por lógica real en su sprint correspondiente.

**Criterios de aceptación**
- Se puede navegar por las principales pantallas del MVP desde el layout.
- Cada pantalla tiene título, descripción breve, acciones principales y estado visual.
- Los formularios y tablas son coherentes con el dominio académico.
- Las pantallas no contienen lógica de negocio definitiva.

**Verificación**
```bash
cd frontend
npm run lint
npm run build
```

**Prompt sugerido para Codex**

```text
Lee PROGRESS.md y el ticket S0.5-T7. Crea wireframes navegables de los módulos principales del MVP: estudiantes, docentes, roles, periodos, carreras, asignaturas, paralelos, oferta, matrícula, sílabos, notas, reportes y auditoría.

Usa datos mock, tablas, filtros, cards, badges y formularios visuales. No implementes todavía la lógica de negocio real ni llamadas al backend.
```

---

## S0.5-T8 — Prototipo específico del constructor de sílabos

**Tareas**
- Crear prototipo visual del flujo de sílabo nueva versión en pasos:
  1. Datos informativos.
  2. Docente y codocente.
  3. Descripción de asignatura.
  4. Competencias.
  5. Resultados de aprendizaje.
  6. Rúbrica por RA.
  7. Pesos por criterios.
  8. Bibliografía.
  9. Planificación semanal.
  10. Vista previa y estado.
- Crear componente `Stepper` o navegación por pestañas.
- Diseñar vista previa tipo documento, sin generación PDF real todavía.
- Crear estados: borrador, pendiente de revisión, aprobado, requiere corrección, cargado firmado.

**Criterios de aceptación**
- El flujo de sílabos es comprensible para un docente.
- El prototipo representa el sílabo nueva versión basado en resultados de aprendizaje y rúbricas.
- La vista previa no genera documentos finales; solo maqueta visual.
- El diseño queda preparado para implementar persistencia real en Sprint 5.

**Verificación**
```bash
cd frontend
npm run lint
npm run build
```

**Prompt sugerido para Codex**

```text
Lee PROGRESS.md y el ticket S0.5-T8. Crea el prototipo visual del constructor de sílabos nueva versión.

Usa un flujo por pasos: datos informativos, docente/codocente, descripción, competencias, resultados de aprendizaje, rúbrica, pesos, bibliografía, planificación semanal y vista previa.

No implementes persistencia real ni generación PDF. Este ticket solo define UX/UI para que Sprint 5 implemente la lógica.
```

---

## S0.5-T9 — Prototipo específico de gestión de notas S1/S2/S3

**Tareas**
- Crear prototipo visual para selección de sistema de notas:
  - S1: 3 parciales, pérdida de 1 RA implica pérdida de asignatura.
  - S2: 3 parciales, pérdida de 2 RA implica pérdida de asignatura.
  - S3: sílabo antiguo, nota práctica + evaluación.
- Crear pantalla docente para carga de calificaciones por asignatura.
- Crear pantalla de calificación por RA y criterios para S1/S2.
- Crear pantalla de notas por práctica/evaluación para S3.
- Crear vista estudiante de avance académico.
- Crear vista secretaría/coordinación con resumen y alertas.
- Usar badges para RA alcanzado/no alcanzado/en riesgo.
- No implementar fórmulas reales; solo mostrar estructura visual y datos mock.

**Criterios de aceptación**
- El prototipo diferencia visualmente S1, S2 y S3.
- El docente puede identificar dónde cargar notas según el sistema.
- El estudiante puede visualizar su avance por RA/parcial.
- Secretaría/coordinación puede visualizar alertas y resumen académico.
- No se implementan cálculos definitivos; estos corresponden al Sprint 6.

**Verificación**
```bash
cd frontend
npm run lint
npm run build
```

**Prompt sugerido para Codex**

```text
Lee PROGRESS.md y el ticket S0.5-T9. Crea prototipos visuales para la gestión de notas S1, S2 y S3.

Diferencia claramente: S1 por resultados de aprendizaje con pérdida por 1 RA no alcanzado; S2 por resultados de aprendizaje con pérdida por 2 RA no alcanzados; S3 por nota práctica + evaluación del sílabo antiguo.

No implementes fórmulas reales. Usa datos mock y deja la UI preparada para que Sprint 6 implemente el motor de calificaciones.
```

---

## S0.5-T10 — Documentación de diseño y handoff para sprints funcionales

**Tareas**
- Crear `docs/frontend-design-system.md` con:
  - stack frontend,
  - estructura de carpetas,
  - tema visual,
  - componentes disponibles,
  - navegación por rol,
  - convenciones de nombres,
  - reglas para pantallas nuevas,
  - reglas de accesibilidad mínima,
  - cómo usar datos mock,
  - cómo reemplazar mocks por API real.
- Crear checklist para futuros sprints frontend.
- Actualizar `README-SPRINTS.md`, si existe, indicando que este sprint va después del Sprint 0 y antes del Sprint 1.
- Actualizar `PROGRESS.md` moviendo cursor al Sprint 1 si todos los tickets se completaron.

**Criterios de aceptación**
- Existe documentación clara para que Codex continúe pantallas de forma consistente.
- La documentación indica qué está mockeado y qué queda pendiente de integración.
- El handoff hacia Sprint 1 es claro.
- No quedan prompts iniciales sueltos fuera del sistema de sprints.

**Verificación**
```bash
cd frontend
npm run lint
npm run build
cd ..
grep -n "Sprint 0.5" PROGRESS.md README-SPRINTS.md docs/frontend-design-system.md
```

**Prompt sugerido para Codex**

```text
Lee PROGRESS.md y el ticket S0.5-T10. Documenta el sistema de diseño frontend y deja el handoff preparado para los sprints funcionales.

Crea docs/frontend-design-system.md con stack, estructura, tema visual, componentes, navegación por rol, convenciones, reglas de accesibilidad y guía para reemplazar datos mock por API real.

Actualiza README-SPRINTS.md si existe. Si todos los tickets del Sprint 0.5 están terminados, actualiza PROGRESS.md para mover el cursor al Sprint 1.
```

---

## Cierre del Sprint 0.5

Antes de marcar este sprint como completado, verificar:

- [ ] Frontend creado o adaptado sin romper backend.
- [ ] Diseño institucional base definido.
- [ ] Componentes UI reutilizables disponibles.
- [ ] Layout autenticado implementado.
- [ ] Navegación por rol disponible.
- [ ] Prototipos de login y recuperación listos.
- [ ] Dashboards por rol listos con datos mock.
- [ ] Wireframes de módulos MVP navegables.
- [ ] Constructor de sílabos prototipado.
- [ ] Gestión de notas S1/S2/S3 prototipada.
- [ ] Documentación frontend creada.
- [ ] `npm run lint` pasa.
- [ ] `npm run build` pasa.
- [ ] `PROGRESS.md` actualizado.

---

## Nota para Codex

Este sprint debe evitar que el frontend se construya pantalla por pantalla sin coherencia. La prioridad es crear una base visual y UX suficientemente clara para que los sprints funcionales puedan concentrarse en reglas académicas, permisos, datos y flujos reales.

No implementar todavía:

- Motor real de notas.
- Persistencia real de sílabos.
- CRUD funcional completo.
- Autenticación JWT real.
- Consumo real de API.
- Reportes PDF/Excel reales.
- Datos reales de estudiantes, docentes o asignaturas.
