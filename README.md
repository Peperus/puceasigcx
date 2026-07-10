# PUCEASIG

PUCEASIG es el Sistema ERP/SIG Academico para PUCE Amazonas. El MVP se enfoca en Gestion Academica: estudiantes, docentes, silabos, notas, roles, periodos, carreras, asignaturas, cursos/paralelos, matriculas, reportes, archivos y auditoria.

El desarrollo se ejecuta por sprints pequenos y verificables. El cursor de trabajo esta en `PROGRESS.md`; Codex debe trabajar unicamente el ticket activo.

## Estado MVP

El MVP `v0.1.0-mvp` queda preparado para validacion piloto al cierre del
Sprint 8. Incluye backend funcional para gestion academica, reportes,
auditoria, QA automatizado, guias de usuario, guia de despliegue y checklist
UAT. El frontend Next.js conserva la base visual y prototipos navegables del
Sprint 0.5 para conectar progresivamente a las APIs reales.

## Alcance del MVP

El MVP debe permitir:

- Gestionar usuarios, roles y permisos institucionales.
- Configurar periodos, carreras, planes, niveles, asignaturas y oferta academica.
- Registrar personas, estudiantes, docentes y asignaciones docentes.
- Matricular estudiantes en cursos/paralelos.
- Crear, revisar, aprobar y cargar silabos.
- Registrar y calcular notas bajo los modelos S1, S2 y S3.
- Consultar notas por rol, generar reportes basicos y auditar acciones criticas.

Los modulos de admisiones, bienestar, biblioteca, mensajeria, gestion documental, Moodle, inventario y analitica avanzada quedan fuera del MVP inicial, aunque la arquitectura debe permitir incorporarlos despues.

## Stack principal

- Backend: Python, Django y Django REST Framework.
- Base de datos: PostgreSQL.
- Frontend del MVP: Next.js, TypeScript y Tailwind CSS.
- Administracion auxiliar: Django Admin.
- Archivos: almacenamiento compatible con S3.
- Cache/tareas futuras: Redis.
- Testing: pytest, pytest-django, lint/build/typecheck en frontend.
- CI/CD: GitHub Actions.

## Estructura esperada del repositorio

```text
.
+-- backend/                 # Proyecto Django y apps modulares
+-- frontend/                # Aplicacion Next.js desde Sprint 0.5
+-- docs/                    # Documentacion tecnica y funcional
+-- SPRINTS/                 # Plan de tickets por sprint
+-- AGENTS.md                # Reglas de trabajo para Codex
+-- PROGRESS.md              # Cursor activo y bitacora
+-- .env.example             # Variables de entorno de ejemplo
+-- docker-compose.yml       # Stack local desde S0-T3
```

Al inicio del proyecto algunas carpetas todavia no existen; se crean en sus tickets correspondientes.

## Documentacion principal

- `docs/project-reference-puceasig.md`: documento maestro del proyecto.
- `docs/requirements.md`: requerimientos funcionales y no funcionales del MVP.
- `docs/architecture.md`: arquitectura tecnica inicial.
- `docs/database-model.md`: entidades y relaciones base.
- `docs/grading-rules.md`: reglas de negocio S1, S2 y S3.
- `docs/security.md`: roles, permisos, auditoria y proteccion de datos.
- `docs/frontend-architecture.md`: decision frontend para el MVP.
- `docs/mvp-roadmap.md`: fases y entregables.
- `docs/backend-app-conventions.md`: convencion de estructura para apps Django.
- `docs/user-guide-secretaria.md`: guia MVP para secretaria academica.
- `docs/user-guide-docente.md`: guia MVP para docentes.
- `docs/user-guide-coordinador.md`: guia MVP para coordinacion de carrera.
- `docs/user-guide-estudiante.md`: guia MVP para estudiantes.
- `docs/deployment.md`: despliegue piloto, variables, static/media y backups.
- `docs/uat-checklist.md`: escenarios de aceptacion institucional.
- `docs/mvp-release-notes.md`: release notes, limitaciones y backlog post-MVP.

## APIs MVP destacadas

- `/api/auth/login/`, `/api/auth/refresh/`, `/api/auth/logout/`
- `/api/me/`
- `/api/academic/`
- `/api/people/`, `/api/students/`, `/api/teachers/`
- `/api/enrollment/`
- `/api/syllabi/`
- `/api/grading/teacher/gradebooks/`
- `/api/student/grades/`
- `/api/reports/grades/` y `/api/reports/grades/export/`
- `/api/reports/mvp/<students|teachers|courses|syllabi|grades>/`
- `/api/audit/logs/`

## Comandos previstos

Instala dependencias de backend en un entorno virtual local:

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r backend/requirements.txt
```

Comandos principales:

```bash
# Backend
.venv/Scripts/python backend/manage.py check
.venv/Scripts/python backend/manage.py migrate
.venv/Scripts/python backend/manage.py runserver

# Docker
docker compose up -d
docker compose ps

# Calidad
.venv/Scripts/python -m pytest
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m black --check .
.venv/Scripts/python -m isort --check .
.venv/Scripts/python -m pre_commit run --all-files

# Frontend, desde Sprint 0.5
cd frontend
npm run lint
npm run build
```

## Reglas de datos y seguridad

- No guardar credenciales reales en el repositorio.
- No versionar `.env`.
- No usar datos reales de estudiantes, docentes, autoridades o personal administrativo en seeds, tests, mocks o documentacion publica.
- No guardar archivos cargados en Git.
- Validar permisos en backend; ocultar botones en frontend no reemplaza autorizacion.
- Auditar cambios criticos: notas, silabos, matriculas, roles y cierres academicos.

## Flujo de trabajo

1. Leer `PROGRESS.md`, `docs/project-reference-puceasig.md` y el sprint activo.
2. Trabajar solo el ticket activo.
3. Ejecutar las verificaciones indicadas en el sprint.
4. Actualizar `PROGRESS.md` con fecha, pruebas y siguiente ticket.
5. No marcar un ticket como completado si hay criterios pendientes o verificaciones fallidas.
