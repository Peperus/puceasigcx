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

- **Sprint activo:** Sprint 2 — Academic Catalogs & Institutional Setup
- **Ticket activo:** `S2-T1` (aún no iniciado)
- **Última sesión:** 2026-07-09 — cerrado Sprint 1 completo (`S1-T1` a `S1-T7`)
- **Próximo paso:** Implementar catálogos académicos base. Ver `SPRINTS/sprint-02-academic-catalogs.md`, ticket `S2-T1`.

---

## Leyenda

- ⬜ Pendiente  🟡 En progreso  ✅ Hecho  ⏭️ Saltado/Aplazado  🔴 Bloqueado

---

## Tablero de sprints

### Bloque Foundation
- ✅ Sprint 0 — Foundation & Documentation
- ✅ Sprint 0.5 — Frontend Design System & UX Foundation

### Bloque MVP — Gestión Académica
- ✅ Sprint 1 — Authentication, Roles & Access Control
- 🟡 **Sprint 2 — Academic Catalogs & Institutional Setup**
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

### Sprint 1 — Authentication, Roles & Access Control
- ✅ S1-T1 — Custom User institucional
- ✅ S1-T2 — Roles institucionales base
- ✅ S1-T3 — Login JWT y refresh
- ✅ S1-T4 — Recuperación de contraseña segura
- ✅ S1-T5 — Permission classes DRF por rol
- ✅ S1-T6 — Perfil actual y sesión institucional
- ✅ S1-T7 — Auditoría base de autenticación y roles

> Sprint 1 cerrado el 2026-07-09. El cursor queda en Sprint 2 / S2-T1.

---

## Bitácora de sesiones

| Fecha | Sprint | Tickets cerrados | Rama / PR | Pruebas ejecutadas | Notas / pendientes |
|---|---|---|---|---|---|
| _(ejemplo)_ | S0 | S0-T1 | `feat/s0-t1-docs` / #1 | revisión manual docs | Falta definir versión exacta de Django |
| 2026-07-08 | S0 | S0-T1 | `4e839ad` | existencia de archivos; busqueda de secretos con `rg`; revision documental | Commit creado al inicializar Git despues del cierre documental |
| 2026-07-08 | S0 | S0-T2 | `f08fad9` | `python manage.py check`; `python manage.py migrate`; `GET /api/health/` local | Backend Django 6.0.7 + DRF 3.17.1 modular creado |
| 2026-07-08 | S0 | S0-T3 | `f27f9ee` | `docker compose up -d --build`; `docker compose ps`; `docker compose exec backend python backend/manage.py migrate`; `curl /api/health/` | Puerto 8000 ocupado por otro stack local; verificado en `BACKEND_PORT=8001` |
| 2026-07-08 | S0 | S0-T4 | `e7b918b` | busqueda de `SECRET_KEY`; `manage.py check` en local/test/production; `manage.py check --deploy` en Docker | Settings divididos en `base`, `local`, `test`, `production`; HTTPS redirect queda delegado al proxy |
| 2026-07-08 | S0 | S0-T5 | `113601b` | `pytest`; `ruff check .`; `black --check .`; `isort --check .`; `pre-commit run --all-files` | Configurados `pyproject.toml`, `.pre-commit-config.yaml` y pruebas core |
| 2026-07-08 | S0 | S0-T6 | `943b2f3` | `manage.py check`; `pytest`; `ruff check .`; `black --check .`; `isort --check .` | Workflow CI agregado; check verde remoto queda pendiente hasta push a GitHub |
| 2026-07-08 | S0 | S0-T7 | `f0b7029` | `manage.py check --deploy`; `pytest backend/apps/core`; `ruff check`; `black --check`; `curl /api/health/` | JWT, CORS y throttling configurados; healthcheck sigue publico |
| 2026-07-08 | S0 | S0-T8 | `2b1bf1a` | `pytest`; `manage.py check`; `curl /api/health/`; `curl /api/version/`; `ruff check`; `black --check` | Apps MVP con estructura consistente, routers base y convencion documentada |
| 2026-07-09 | S0.5 | S0.5-T1 | `feat/s0-5-t1-frontend-base` | `npm install`; `npm run lint`; `npm run typecheck`; `npm run build` | Frontend Next.js + TypeScript + Tailwind creado en `/frontend`; npm audit reporta 2 vulnerabilidades moderadas de dependencias transitivas |
| 2026-07-09 | S0.5 | S0.5-T2 | `feat/s0-5-t2-theme-tokens` | navegacion visual en `https://www.puce.edu.ec/`; `npm run lint`; `npm run typecheck`; `npm run build`; verificacion local `http://127.0.0.1:3000` | Tema institucional centralizado en tokens; documentacion inicial en `docs/frontend-design-system.md`; sin logos oficiales ni assets copiados |
| 2026-07-09 | S0.5 | S0.5-T3 a S0.5-T10 | `feat/s0-5-ux-foundation-complete` | `npm run lint`; `npm run typecheck`; `npm run build` | Componentes UI, layout autenticado, navegacion por rol, auth publica, dashboards, wireframes MVP, constructor de silabos, notas S1/S2/S3 y handoff documentado; `npm install lucide-react` mantiene 2 vulnerabilidades moderadas transitivas |
| 2026-07-09 | S1 | S1-T1 a S1-T7 | `feat/s1-auth-roles` | `manage.py check`; `manage.py makemigrations accounts audit`; `manage.py migrate`; `createsuperuser --noinput`; `manage.py seed_roles`; `pytest`; `ruff check .`; `black --check .`; `isort --check .` | Usuario institucional custom, roles Django Groups, JWT login/refresh/logout, password reset, `/api/me/`, permissions DRF y auditoria base implementados; base SQLite previa respaldada como `backend/db.sqlite3.pre-s1-backup-*` por cambio de `AUTH_USER_MODEL` |
| | | | | | |

---

## Decisiones de arquitectura tomadas

- Backend principal: Django + Django REST Framework.
- Versiones backend base: Python 3.14, Django 6.0.7, Django REST Framework 3.17.1.
- Base de datos: PostgreSQL.
- Versiones de servicios locales: PostgreSQL 18 Alpine, Redis 8 Alpine.
- Frontend del MVP: Next.js + TypeScript + Tailwind CSS.
- Sprint específico de frontend: Sprint 0.5 — Frontend Design System & UX Foundation, antes de Sprint 1.
- Gestor de paquetes frontend inicial: npm.
- Tema visual frontend inspirado en el sitio público de PUCE revisado el 2026-07-09: azul institucional, turquesa/celeste de apoyo, blanco y grises neutros; sin copiar logos ni assets oficiales.
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

- Confirmar si se usará shadcn/ui completo o componentes propios equivalentes.
- Definir proveedor S3 compatible: Cloudflare R2, AWS S3 o MinIO institucional.
- Definir estrategia de despliegue piloto: VPS, servidor institucional, Docker Compose o PaaS.
- Confirmar política institucional de cambio/corrección de notas cerradas.
- Confirmar si se usará correo institucional SMTP desde el MVP o quedará simulado en consola.

---

## Checklist global del MVP

- [x] Repositorio documentado para Codex.
- [x] Backend Django ejecutable localmente.
- [x] Frontend Next.js creado y compilando.
- [x] Design system institucional documentado.
- [x] Roles institucionales configurados.
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
