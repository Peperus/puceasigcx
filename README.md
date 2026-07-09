# PUCEASIG

PUCEASIG es el Sistema ERP/SIG Academico para PUCE Amazonas. El MVP se enfoca en Gestion Academica: estudiantes, docentes, silabos, notas, roles, periodos, carreras, asignaturas, cursos/paralelos, matriculas, reportes, archivos y auditoria.

El desarrollo se ejecuta por sprints pequenos y verificables. El cursor de trabajo esta en `PROGRESS.md`; Codex debe trabajar unicamente el ticket activo.

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

## Comandos previstos

Los comandos se habilitaran gradualmente durante Sprint 0:

```bash
# Backend, desde S0-T2
cd backend
python manage.py check
python manage.py migrate
python manage.py runserver

# Docker, desde S0-T3
docker compose up -d
docker compose ps

# Calidad, desde S0-T5
pytest
ruff check .
black --check .
isort --check .
pre-commit run --all-files

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
