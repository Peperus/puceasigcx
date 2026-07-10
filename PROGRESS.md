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

- **Sprint activo:** Sprint 8.5 — Frontend Integration MVP
- **Ticket activo:** `S8.5-T1` (aún no iniciado)
- **Última sesión:** 2026-07-10 — creado plan de Sprint 8.5 para convertir el frontend del MVP en UI funcional conectada a APIs reales
- **Próximo paso:** Implementar autenticación real del frontend. Ver `SPRINTS/sprint-08-5-frontend-integration-mvp.md`, ticket `S8.5-T1`.

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
- ✅ Sprint 2 — Academic Catalogs & Institutional Setup
- ✅ Sprint 3 — People, Students & Teachers
- ✅ Sprint 4 — Academic Offer, Courses & Enrollment
- ✅ Sprint 5 — Syllabus Management
- ✅ Sprint 6 — Grading Engine S1/S2/S3
- ✅ **Sprint 7 — Grade Entry, Student Views & Closures**
- ✅ **Sprint 8 — Reports, Audit, QA & MVP Release**  ← **MVP funcional cerrado**
- 🟡 Sprint 8.5 — Frontend Integration MVP  ← **UI funcional antes del bloque post-MVP**

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

## Detalle de sprints

### Sprint 8.5 — Frontend Integration MVP
- 🟡 S8.5-T1 — Cliente API, sesión y autenticación real
- ⬜ S8.5-T2 — Navegación por rol y shell autenticado funcional
- ⬜ S8.5-T3 — Catálogos académicos funcionales
- ⬜ S8.5-T4 — Personas, estudiantes y docentes funcionales
- ⬜ S8.5-T5 — Oferta académica, asignación docente y matrícula funcionales
- ⬜ S8.5-T6 — Constructor de sílabos conectado a API
- ⬜ S8.5-T7 — Carga docente de notas S1/S2/S3 funcional
- ⬜ S8.5-T8 — Consulta estudiantil de notas funcional
- ⬜ S8.5-T9 — Reportes y auditoría funcionales
- ⬜ S8.5-T10 — Dashboards funcionales por rol
- ⬜ S8.5-T11 — QA E2E y accesibilidad básica
- ⬜ S8.5-T12 — Documentación y cierre UI MVP

> Sprint 8.5 creado el 2026-07-10. Este sprint no agrega módulos post-MVP; integra el frontend existente con APIs reales del MVP antes de iniciar Sprint 9.

### Sprint 8 — Reports, Audit, QA & MVP Release
- ✅ S8-T1 — Reportes académicos mínimos del MVP
- ✅ S8-T2 — Auditoría transversal
- ✅ S8-T3 — Hardening de permisos
- ✅ S8-T4 — QA de reglas de notas con fixtures representativos
- ✅ S8-T5 — Documentación de usuario MVP
- ✅ S8-T6 — Preparación de despliegue piloto
- ✅ S8-T7 — Smoke tests y UAT checklist
- ✅ S8-T8 — Cierre formal del MVP

> Sprint 8 cerrado el 2026-07-10. El MVP de Gestión Académica queda preparado como `v0.1.0-mvp`. El cursor se mueve a Sprint 8.5 / S8.5-T1 para completar la UI funcional antes de implementar módulos post-MVP.

### Sprint 7 — Grade Entry, Student Views & Closures
- ✅ S7-T1 — API de ingreso de notas para docentes
- ✅ S7-T2 — Flujo S1/S2: calificar por RA y criterio
- ✅ S7-T3 — Flujo S3: práctica + evaluación por parcial
- ✅ S7-T4 — Consulta de notas para estudiantes
- ✅ S7-T5 — Vistas de secretaría y coordinación
- ✅ S7-T6 — Cierre y reapertura de actas/gradebook
- ✅ S7-T7 — Exportación básica de actas

> Sprint 7 cerrado el 2026-07-10. El cursor queda en Sprint 8 / S8-T1.

### Sprint 6 — Grading Engine S1/S2/S3
- ✅ S6-T1 — Modelos base de libro de calificaciones
- ✅ S6-T2 — Servicio común de escala y niveles A/B/C/D
- ✅ S6-T3 — Motor S1 por resultados de aprendizaje
- ✅ S6-T4 — Motor S2 por resultados de aprendizaje con tolerancia de un RA
- ✅ S6-T5 — Motor S3 sílabo anterior: práctica + evaluación
- ✅ S6-T6 — Persistencia de resultados calculados
- ✅ S6-T7 — Auditoría de cambios de notas
- ✅ S6-T8 — Documentación técnica del motor

> Sprint 6 cerrado el 2026-07-09. El cursor queda en Sprint 7 / S7-T1.

### Sprint 5 — Syllabus Management
- ✅ S5-T1 — Modelo Syllabus base
- ✅ S5-T2 — Competencias y resultados de aprendizaje
- ✅ S5-T3 — Rúbricas y criterios de evaluación
- ✅ S5-T4 — Bibliografía
- ✅ S5-T5 — Planificación semanal y experiencias de aprendizaje
- ✅ S5-T6 — Flujo de finalización y aprobación
- ✅ S5-T7 — Carga de sílabo firmado y archivos
- ✅ S5-T8 — Descarga/generación de sílabo

> Sprint 5 cerrado el 2026-07-09. El cursor queda en Sprint 6 / S6-T1.

### Sprint 4 — Academic Offer, Courses & Enrollment
- ✅ S4-T1 — Oferta académica por periodo
- ✅ S4-T2 — Cursos/paralelos
- ✅ S4-T3 — Asignación docente
- ✅ S4-T4 — Matrícula académica
- ✅ S4-T5 — Homologaciones y casos especiales mínimos
- ✅ S4-T6 — API/Admin de oferta y matrícula
- ✅ S4-T7 — Dashboard académico mínimo

> Sprint 4 cerrado el 2026-07-09. El cursor queda en Sprint 5 / S5-T1.

### Sprint 3 — People, Students & Teachers
- ✅ S3-T1 — Modelo Person central
- ✅ S3-T2 — Modelo Student
- ✅ S3-T3 — Modelo Teacher
- ✅ S3-T4 — Horarios de atención docente
- ✅ S3-T5 — API/Admin de personas, estudiantes y docentes
- ✅ S3-T6 — Importación controlada desde CSV

> Sprint 3 cerrado el 2026-07-09. El cursor queda en Sprint 4 / S4-T1.

### Sprint 2 — Academic Catalogs & Institutional Setup
- ✅ S2-T1 — Modelos de periodos académicos
- ✅ S2-T2 — Carreras, modalidades y dominios
- ✅ S2-T3 — Planes de estudio, niveles y malla
- ✅ S2-T4 — Asignaturas y prerrequisitos
- ✅ S2-T5 — Parámetros académicos configurables
- ✅ S2-T6 — API y Admin de catálogos
- ✅ S2-T7 — Seeds sintéticos mínimos

> Sprint 2 cerrado el 2026-07-09. El cursor queda en Sprint 3 / S3-T1.

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
| 2026-07-09 | S2 | S2-T1 | `feat/s2-academic-catalogs` | `pytest backend/apps/academic_catalogs/tests/test_periods.py`; `pytest`; `manage.py check`; `ruff check .`; `black --check .`; `isort --check .` | Periodos académicos con estados, periodo actual único, validación de solapamiento activo y admin con filtros. |
| 2026-07-09 | S2 | S2-T2 | `feat/s2-academic-catalogs` | `pytest backend/apps/academic_catalogs/tests/test_careers.py`; `pytest`; `manage.py check`; `ruff check .`; `black --check .`; `isort --check .` | Unidades académicas, modalidades, dominios y carreras con códigos únicos y permisos de admin por rol. |
| 2026-07-09 | S2 | S2-T3 | `feat/s2-academic-catalogs` | `pytest backend/apps/academic_catalogs/tests/test_study_plan.py`; `pytest`; `manage.py check`; `ruff check .`; `black --check .`; `isort --check .` | Planes de estudio, niveles ordenados y plan vigente único por carrera. |
| 2026-07-09 | S2 | S2-T4 | `feat/s2-academic-catalogs` | `pytest backend/apps/academic_catalogs/tests/test_subjects.py`; `pytest`; `manage.py check`; `ruff check .`; `black --check .`; `isort --check .` | Asignaturas por carrera, malla curricular y prerrequisitos con rechazo de ciclos simples. |
| 2026-07-09 | S2 | S2-T5 | `feat/s2-academic-catalogs` | `pytest backend/apps/academic_catalogs/tests/test_academic_settings.py`; `pytest`; `manage.py check`; `ruff check .`; `black --check .`; `isort --check .` | Configuración académica 0-50, umbral 30, niveles A/B/C/D y catálogo S1/S2/S3 consultable por servicio. |
| 2026-07-09 | S2 | S2-T6 | `feat/s2-academic-catalogs` | `pytest backend/apps/academic_catalogs/tests/test_catalog_api.py`; `pytest`; `manage.py check`; `ruff check .`; `black --check .`; `isort --check .` | API `/api/academic/` protegida por roles, admin con filtros/búsqueda y `docs/api.md` creado. |
| 2026-07-09 | S2 | S2-T7 | `feat/s2-academic-catalogs` | `manage.py seed_academic_catalogs`; `manage.py seed_academic_catalogs`; `pytest backend/apps/academic_catalogs/tests/test_seeds.py`; `pytest`; `manage.py seed_roles` | Seed sintético idempotente para catálogos base; roles sincronizados con permisos Django Admin de catálogos. |
| 2026-07-09 | S3 | S3-T1 | `feat/s3-people-students-teachers` | `pytest backend/apps/people/tests/test_person_model.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | `Person` central con identificacion unica opcional, relacion opcional con usuario y admin con busqueda. |
| 2026-07-09 | S3 | S3-T2 | `feat/s3-people-students-teachers` | `pytest backend/apps/students/tests/test_student_model.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | Perfil `Student` OneToOne con `Person`, codigo unico, carrera, plan, periodo de ingreso y estados academicos. |
| 2026-07-09 | S3 | S3-T3 | `feat/s3-people-students-teachers` | `pytest backend/apps/teachers/tests/test_teacher_model.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | Perfil `Teacher` OneToOne con `Person`, datos para silabo, estado y dominios/areas. |
| 2026-07-09 | S3 | S3-T4 | `feat/s3-people-students-teachers` | `pytest backend/apps/teachers/tests/test_office_hours.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | Horarios de atencion docente presenciales/virtuales con validacion de rango horario. |
| 2026-07-09 | S3 | S3-T5 | `feat/s3-people-students-teachers` | `pytest backend/apps/people/tests/test_people_api.py`; `pytest backend/apps/students/tests/test_students_api.py`; `pytest backend/apps/teachers/tests/test_teachers_api.py`; `pytest`; `manage.py check`; `ruff check .`; `black --check .`; `isort --check .` | API/Admin de personas, estudiantes y docentes protegida por roles; perfiles propios para docente/estudiante. |
| 2026-07-09 | S3 | S3-T6 | `feat/s3-people-students-teachers` | `pytest backend/apps/people/tests/test_import_people.py`; `pytest`; `manage.py check`; `manage.py migrate`; `manage.py seed_roles`; `ruff check .`; `black --check .`; `isort --check .` | Importacion CSV sintetica tolerante a errores, con resumen de creados/actualizados/rechazados y auditoria `people_imported`. |
| 2026-07-09 | S4 | S4-T1 | `feat/s4-academic-offer-enrollment` / `4ba9090` | `pytest backend/apps/enrollment/tests/test_academic_offer.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | Oferta academica por periodo, carrera, plan y nivel con estados y unicidad critica. |
| 2026-07-09 | S4 | S4-T2 | `feat/s4-academic-offer-enrollment` / `4ba9090` | `pytest backend/apps/enrollment/tests/test_course_sections.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | Cursos/paralelos con cupo, modalidad, sistema S1/S2/S3 y rechazo de duplicados por oferta/asignatura/paralelo. |
| 2026-07-09 | S4 | S4-T3 | `feat/s4-academic-offer-enrollment` / `4ba9090` | `pytest backend/apps/enrollment/tests/test_teaching_assignments.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | Asignacion docente con titular/codocente, docente activo, titular unico y visibilidad por docente/coordinador. |
| 2026-07-09 | S4 | S4-T4 | `feat/s4-academic-offer-enrollment` / `4ba9090` | `pytest backend/apps/enrollment/tests/test_enrollment.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | Matricula academica por estudiante/periodo e inscripcion en cursos con validacion de cupos, duplicados y curso activo. |
| 2026-07-09 | S4 | S4-T5 | `feat/s4-academic-offer-enrollment` / `4ba9090` | `pytest backend/apps/enrollment/tests/test_homologations.py`; `pytest`; `manage.py check`; `manage.py migrate`; `manage.py seed_roles`; `ruff check .`; `black --check .`; `isort --check .` | Homologaciones basicas por estudiante/asignatura/periodo con resolucion, estado y auditoria. |
| 2026-07-09 | S4 | S4-T6 | `feat/s4-academic-offer-enrollment` / `4ba9090` | `pytest backend/apps/enrollment/tests/test_enrollment_api.py`; `pytest`; `manage.py check`; `manage.py migrate`; `manage.py seed_roles`; `ruff check .`; `black --check .`; `isort --check .` | API/Admin de oferta, cursos, asignaciones, matriculas y homologaciones con permisos por rol y bloqueo de curso cerrado. |
| 2026-07-09 | S4 | S4-T7 | `feat/s4-academic-offer-enrollment` / `4ba9090` | `pytest backend/apps/reports/tests/test_academic_dashboard_minimal.py`; `pytest`; `manage.py check`; `manage.py migrate`; `manage.py seed_roles`; `ruff check .`; `black --check .`; `isort --check .` | Dashboard `/api/academic/dashboard/` con conteos por periodo y acceso Admin/Secretaria/Coordinador. |
| 2026-07-09 | S5 | S5-T1 | `feat/s5-syllabus-management` | `pytest backend/apps/syllabus/tests/test_syllabus_model.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | Modelo `Syllabus` por curso/paralelo con version nueva/legacy, estados, docente titular/codocente y silabo activo unico por curso. |
| 2026-07-09 | S5 | S5-T2 | `feat/s5-syllabus-management` | `pytest backend/apps/syllabus/tests/test_learning_outcomes.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | Competencias transversales/disciplinares y RA de carrera/asignatura con minimo de 3 por tipo antes de rubricas. |
| 2026-07-09 | S5 | S5-T3 | `feat/s5-syllabus-management` | `pytest backend/apps/syllabus/tests/test_rubrics.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | Criterios ponderados por RA, validacion de suma 100 y niveles A/B/C/D por criterio preparados para Sprint 6. |
| 2026-07-09 | S5 | S5-T4 | `feat/s5-syllabus-management` | `pytest backend/apps/syllabus/tests/test_bibliography.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | Bibliografia basica/complementaria/recomendada/digital editable solo en borrador u observado. |
| 2026-07-09 | S5 | S5-T5 | `feat/s5-syllabus-management` | `pytest backend/apps/syllabus/tests/test_weekly_plan.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | Planificacion semanal con experiencias de contacto docente, practico-experimentales y autonomas; finalizacion exige plan minimo. |
| 2026-07-09 | S5 | S5-T6 | `feat/s5-syllabus-management` | `pytest backend/apps/syllabus/tests/test_syllabus_workflow.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | Flujo finalizar/enviar/aprobar/observar/reabrir con auditoria y bloqueo de aprobacion del propio docente. |
| 2026-07-09 | S5 | S5-T7 | `feat/s5-syllabus-management` | `pytest backend/apps/documents/tests/test_syllabus_upload.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | Carga de PDF firmado con extension/tamano configurables, storage Django y usuario/fecha de subida auditables. |
| 2026-07-09 | S5 | S5-T8 | `feat/s5-syllabus-management` | `pytest backend/apps/syllabus/tests/test_syllabus_render.py`; `pytest`; `manage.py check`; `manage.py migrate`; `ruff check .`; `black --check .`; `isort --check .` | Vista HTML imprimible con datos del curso, docentes, competencias, RA, rubricas, planificacion, bibliografia y firmas. |
| 2026-07-09 | S6 | S6-T1 | `feat/s6-grading-engine` | `pytest backend/apps/grading/tests/test_gradebook_model.py` | `Gradebook`, `GradeItem` y `StudentGradeRecord` asociados a curso, silabo aprobado y matricula activa; migracion `grading.0001_initial`. |
| 2026-07-09 | S6 | S6-T2 | `feat/s6-grading-engine` | `pytest backend/apps/grading/tests/test_grade_scale.py` | Servicio `letter_from_score` con escala 0-50, letras A/B/C/D y bordes probados. |
| 2026-07-09 | S6 | S6-T3 | `feat/s6-grading-engine` | `pytest backend/apps/grading/tests/test_s1_engine.py` | Motor S1 estricto por RA, criterios ponderados, recuperacion con aporte configurable y cap a 30. |
| 2026-07-09 | S6 | S6-T4 | `feat/s6-grading-engine` | `pytest backend/apps/grading/tests/test_s2_engine.py` | Motor S2 con tolerancia de un RA, recuperacion requerida y reprobacion con dos o mas RA perdidos. |
| 2026-07-09 | S6 | S6-T5 | `feat/s6-grading-engine` | `pytest backend/apps/grading/tests/test_s3_engine.py` | Motor S3 con tres parciales, practica/evaluacion, cuarta evaluacion y estados finales. |
| 2026-07-09 | S6 | S6-T6 | `feat/s6-grading-engine` | `pytest backend/apps/grading/tests/test_grade_snapshots.py` | `GradeCalculationSnapshot` guarda resultado, regla, fuente, usuario y conserva historial al recalcular. |
| 2026-07-09 | S6 | S6-T7 | `feat/s6-grading-engine` | `pytest backend/apps/grading/tests/test_grade_audit.py` | Auditoria de creacion, modificacion, eliminacion logica y reapertura; bloqueo de libros cerrados. |
| 2026-07-09 | S6 | S6-T8 | `feat/s6-grading-engine` | `Select-String "S1|S2|S3|pendiente" docs/grading-rules.md docs/grading-engine.md` | Documentados modelos, servicios, casos borde y pendientes institucionales del motor. |
| 2026-07-10 | S7 | S7-T1 | `feat/s7-grade-entry-views-closures` | `pytest apps/grading/tests/test_teacher_grade_entry_api.py`; `manage.py check`; `pytest` | API docente para cursos asignados, estudiantes y guardado individual de notas con auditoria y recálculo tolerante a incompletos. |
| 2026-07-10 | S7 | S7-T2 | `feat/s7-grade-entry-views-closures` | `pytest apps/grading/tests/test_ra_criterion_entry.py`; `pytest backend/apps/grading/tests` | Carga masiva S1/S2 por RA/criterio, transaccional y con resumen de letras A/B/C/D desde snapshots. |
| 2026-07-10 | S7 | S7-T3 | `feat/s7-grade-entry-views-closures` | `pytest apps/grading/tests/test_s3_grade_entry.py`; `pytest backend/apps/grading/tests` | Carga S3 por parcial con práctica/evaluación y cuarta evaluación cuando aplica. |
| 2026-07-10 | S7 | S7-T4 | `feat/s7-grade-entry-views-closures` | `pytest apps/grading/tests/test_student_grade_view.py`; `pytest backend/apps/grading/tests` | Endpoint `GET /api/student/grades/` limitado al estudiante autenticado y a libros visibles. |
| 2026-07-10 | S7 | S7-T5 | `feat/s7-grade-entry-views-closures` | `pytest apps/reports/tests/test_academic_grade_queries.py`; `pytest backend/apps/reports/tests` | Consulta de notas por periodo, carrera, curso, docente, estudiante, modelo y estado; coordinador limitado a su carrera. |
| 2026-07-10 | S7 | S7-T6 | `feat/s7-grade-entry-views-closures` | `pytest apps/grading/tests/test_gradebook_closure.py`; `pytest backend/apps/grading/tests` | Cierre estricto con snapshot final, bloqueo de edición y reapertura autorizada con justificación y auditoria. |
| 2026-07-10 | S7 | S7-T7 | `feat/s7-grade-entry-views-closures` | `pytest apps/reports/tests/test_grade_exports.py`; `ruff check .`; `black --check .`; `isort --check .` | Exportación CSV/XLSX básica de actas con permisos y auditoria de descarga. |
| 2026-07-10 | S8 | S8-T1 | `feat/s8-reports-audit-release` | `pytest backend/apps/reports/tests/test_mvp_reports.py`; `pytest` | Reportes MVP `/api/reports/mvp/<tipo>/` para estudiantes, docentes, cursos, silabos y notas con filtros periodo/carrera y export CSV/XLSX auditada. |
| 2026-07-10 | S8 | S8-T2 | `feat/s8-reports-audit-release` | `pytest backend/apps/audit/tests/test_cross_module_audit.py`; `pytest` | Auditoria transversal reforzada para personas, estudiantes, docentes, oferta, cursos, asignaciones, matricula, silabos, notas, cierres y exportaciones; API `/api/audit/logs/` solo lectura con filtros. |
| 2026-07-10 | S8 | S8-T3 | `feat/s8-reports-audit-release` | `pytest backend/apps/accounts/tests backend/apps/enrollment/tests backend/apps/syllabus/tests backend/apps/grading/tests -k permission`; `pytest` | Pruebas negativas de permisos: estudiantes no ven notas ajenas ni reportes masivos; docentes no editan gradebooks no asignados. |
| 2026-07-10 | S8 | S8-T4 | `feat/s8-reports-audit-release` | `pytest backend/apps/grading/tests/test_grading_acceptance.py`; `pytest` | Escenarios sinteticos end-to-end S1, S2 y S3 desde registro de notas hasta cierre de acta. |
| 2026-07-10 | S8 | S8-T5 | `feat/s8-reports-audit-release` | `Get-ChildItem docs/user-guide-*.md`; revision documental | Guias MVP creadas para secretaria, docente, coordinador y estudiante, sin credenciales ni datos reales. |
| 2026-07-10 | S8 | S8-T6 | `feat/s8-reports-audit-release` | `DJANGO_SETTINGS_MODULE=config.settings.production manage.py check --deploy`; `pytest`; `ruff check .`; `black --check .`; `isort --check .` | `docs/deployment.md` creado; static/media configurables por entorno; estrategia S3-compatible y backup/restore documentados. |
| 2026-07-10 | S8 | S8-T7 | `feat/s8-reports-audit-release` | `pytest tests/smoke/`; `npm run lint`; `npm run typecheck`; `npm run build` | Smoke tests basicos, checklist UAT completo y frontend verificado sin cambios funcionales. |
| 2026-07-10 | S8 | S8-T8 | `feat/s8-reports-audit-release` | `pytest`; `ruff check .`; `black --check .`; `isort --check .` | README y release notes actualizados; limitaciones y backlog post-MVP conectados con sprints 9-17; tag sugerido `v0.1.0-mvp`. |
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
- Catálogos académicos Sprint 2: `AcademicPeriod`, `FacultyOrUnit`, `Modality`, `AcademicDomain`, `Career`, `StudyPlan`, `AcademicLevel`, `Subject`, `CurriculumSubject`, `CurriculumPrerequisite`, `AcademicSetting`, `AchievementLevel` y `GradingSystem`.
- Personas Sprint 3: `Person` es el dato maestro central; `Student` y `Teacher` son perfiles OneToOne y no duplican datos personales.
- Oferta y matricula Sprint 4: `AcademicOffer`, `CourseSection`, `TeachingAssignment`, `Enrollment`, `CourseEnrollment` y `Homologation` conectan periodo, carrera, plan, nivel, asignatura, docente y estudiante con permisos por rol y auditoria de matriculas/homologaciones.
- Silabos Sprint 5: `Syllabus`, competencias, RA, criterios, niveles A/B/C/D, bibliografia, planificacion semanal y PDF firmado quedan asociados a `CourseSection`; el silabo aprobado habilita el contrato de bloqueo para notas en Sprint 6.
- Motor de notas Sprint 6: `Gradebook`, `GradeItem`, `StudentGradeRecord` y `GradeCalculationSnapshot` implementan S1/S2/S3 como servicios de dominio probados, con snapshots reproducibles, auditoria de cambios y bloqueo de libros cerrados.
- Flujos de notas Sprint 7: docentes registran notas por curso asignado, S1/S2 por RA/criterio, S3 por parcial, estudiantes consultan solo sus notas, secretaría/coordinación consulta snapshots filtrados y las actas se cierran/reabren con auditoria.

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
- [x] Catálogos académicos mínimos funcionales.
- [x] Personas, estudiantes y docentes gestionables.
- [x] Cursos/paralelos y matrículas gestionables.
- [x] Sílabos nueva versión gestionables.
- [x] Motor de notas S1/S2/S3 probado.
- [x] Registro de notas por docente.
- [x] Consulta de notas por estudiante.
- [x] Reportes básicos de secretaría/coordinación.
- [x] Auditoría de acciones críticas.
- [x] MVP desplegable y documentado.
