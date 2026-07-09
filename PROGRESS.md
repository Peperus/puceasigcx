# PROGRESS.md — Estado del proyecto PUCEASIG

> **Este es el archivo que Codex debe leer al iniciar CADA sesión de trabajo.**
> Instrucción sugerida para Codex: *"Lee PROGRESS.md, docs/project-reference-puceasig.md y el sprint activo. Continúa únicamente con el ticket activo."*
>
> Reglas operativas:
> - Solo trabajar el ticket marcado como 🟡 EN PROGRESO, o el primer ⬜ si no hay ninguno.
> - Cada ticket debe ejecutarse en una rama propia y cerrarse con un PR o commit verificable.
> - Al terminar un ticket: marcarlo ✅, mover el cursor al siguiente, anotar fecha, rama/PR y pruebas ejecutadas.
> - No marcar un ticket como ✅ si sus tests, verificaciones o criterios de aceptación no pasan.
> - No trabajar módulos futuros si el ticket activo no lo pide.
> - No usar datos reales de estudiantes, docentes, autoridades o credenciales institucionales en seeds, tests, mocks o ejemplos.
> - Para pantallas frontend, reutilizar el design system definido en el Sprint 0.5.

---

## 📍 Cursor actual

- **Sprint activo:** Sprint 0 — Foundation & Documentation
- **Ticket activo:** `S0-T4` (aún no iniciado)
- **Última sesión:** 2026-07-08 — cerrado `S0-T3`
- **Próximo paso:** Settings por entornos + variables de entorno. Ver `SPRINTS/sprint-00-foundation.md`, ticket `S0-T4`.

---

## Leyenda

- ⬜ Pendiente  🟡 En progreso  ✅ Hecho  ⏭️ Saltado/Aplazado  🔴 Bloqueado

---

## Tablero de sprints

### Bloque Foundation
- 🟡 **Sprint 0 — Foundation & Documentation**
- ⬜ Sprint 0.5 — Frontend Design System & UX Foundation

### Bloque MVP — Gestión Académica
- ⬜ Sprint 1 — Authentication, Roles & Access Control
- ⬜ Sprint 2 — Academic Catalogs & Institutional Setup
- ⬜ Sprint 3 — People, Students & Teachers
- ⬜ Sprint 4 — Academic Offer, Courses & Enrollment
- ⬜ Sprint 5 — Syllabus Management
- ⬜ Sprint 6 — Grading Engine S1/S2/S3
- ⬜ Sprint 7 — Grade Entry, Student Views & Closures
- ⬜ Sprint 8 — Reports, Audit, QA & MVP Release  ← **MVP funcional al cerrar este sprint**

### Bloque Escalamiento ERP/SIG posterior al MVP
- ⬜ Sprint 9 — Admisiones y captación
- ⬜ Sprint 10 — Bienestar universitario
- ⬜ Sprint 11 — Biblioteca y repositorio académico
- ⬜ Sprint 12 — Requerimientos, PQRSD y mensajería institucional
- ⬜ Sprint 13 — Integración Moodle y aula virtual
- ⬜ Sprint 14 — Gestión documental institucional
- ⬜ Sprint 15 — Inventario y activos
- ⬜ Sprint 16 — Analítica institucional y tableros estratégicos
- ⬜ Sprint 17 — Portal integral, interoperabilidad y hardening de escala

---

## Detalle del sprint activo

### Sprint 0 — Foundation & Documentation
- ✅ S0-T1 — Base documental del repositorio para Codex
- ✅ S0-T2 — Inicializar backend Django + DRF modular
- ✅ S0-T3 — Docker Compose con PostgreSQL y Redis
- ⬜ S0-T4 — Settings por entornos + variables de entorno
- ⬜ S0-T5 — Calidad de código, testing y pre-commit
- ⬜ S0-T6 — CI/CD con GitHub Actions
- ⬜ S0-T7 — Seguridad base, JWT scaffold, CORS y rate limiting
- ⬜ S0-T8 — Bootstrap de apps Django del MVP y healthcheck extendido

> Al cambiar de sprint, copia aquí el desglose de tickets del archivo correspondiente en `SPRINTS/`.
> Después de cerrar Sprint 0, el siguiente cursor debe ser **Sprint 0.5 / S0.5-T1** para fijar el frontend antes del Sprint 1.

---

## Bitácora de sesiones

| Fecha | Sprint | Tickets cerrados | Rama / PR | Pruebas ejecutadas | Notas / pendientes |
|---|---|---|---|---|---|
| _(ejemplo)_ | S0 | S0-T1 | `feat/s0-t1-docs` / #1 | revisión manual docs | Falta definir versión exacta de Django |
| 2026-07-08 | S0 | S0-T1 | sin rama Git local | existencia de archivos; busqueda de secretos con `rg`; revision documental | Repositorio aun no tiene `.git`; cursor movido a S0-T2 |
| 2026-07-08 | S0 | S0-T2 | commit pendiente | `python manage.py check`; `python manage.py migrate`; `GET /api/health/` local | Backend Django 6.0.7 + DRF 3.17.1 modular creado |
| 2026-07-08 | S0 | S0-T3 | commit pendiente | `docker compose up -d --build`; `docker compose ps`; `docker compose exec backend python backend/manage.py migrate`; `curl /api/health/` | Puerto 8000 ocupado por otro stack local; verificado en `BACKEND_PORT=8001` |
| | | | | | |

---

## Decisiones de arquitectura tomadas

- Backend principal: Django + Django REST Framework.
- Base de datos: PostgreSQL.
- Frontend del MVP: Next.js + TypeScript + Tailwind CSS.
- Sprint específico de frontend: Sprint 0.5 — Frontend Design System & UX Foundation, antes de Sprint 1.
- Django Admin: herramienta interna auxiliar para administración, soporte y carga inicial; no será el frontend principal del MVP.
- Componentes UI frontend: shadcn/ui o componentes propios equivalentes, centralizados y reutilizables.
- Formularios frontend: React Hook Form + Zod cuando existan formularios funcionales.
- Tablas frontend: TanStack Table o componente propio inicialmente simple.
- Fetch/cache frontend: TanStack Query cuando se consuma API real.
- Archivos: almacenamiento compatible con S3 para sílabos firmados, reportes y adjuntos.
- Autenticación: JWT para API y frontend Next.js; Django Admin para operación interna inicial.
- Autorización: roles institucionales + permisos por objeto cuando aplique.
- Auditoría obligatoria para notas, sílabos, matrículas, roles y cambios críticos.
- Sistemas de notas del MVP: S1, S2 y S3 como motor de reglas probado, no como fórmulas copiadas de Excel.

---

## Decisiones pendientes

- Definir gestor de paquetes frontend: npm, pnpm o yarn.
- Confirmar si se usará shadcn/ui completo o componentes propios equivalentes.
- Definir proveedor S3 compatible: Cloudflare R2, AWS S3 o MinIO institucional.
- Definir estrategia de despliegue piloto: VPS, servidor institucional, Docker Compose o PaaS.
- Confirmar política institucional de cambio/corrección de notas cerradas.
- Confirmar si se usará correo institucional SMTP desde el MVP o quedará simulado en consola.

---

## Checklist global del MVP

- [ ] Repositorio documentado para Codex.
- [ ] Backend Django ejecutable localmente.
- [ ] Frontend Next.js creado y compilando.
- [ ] Design system institucional documentado.
- [ ] Roles institucionales configurados.
- [ ] Catálogos académicos mínimos funcionales.
- [ ] Personas, estudiantes y docentes gestionables.
- [ ] Cursos/paralelos y matrículas gestionables.
- [ ] Sílabos nueva versión gestionables.
- [ ] Motor de notas S1/S2/S3 probado.
- [ ] Registro de notas por docente.
- [ ] Consulta de notas por estudiante.
- [ ] Reportes básicos de secretaría/coordinación.
- [ ] Auditoría de acciones críticas.
- [ ] MVP desplegable y documentado.
