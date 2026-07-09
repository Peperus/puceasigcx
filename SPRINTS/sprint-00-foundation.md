# Sprint 0 — Foundation & Documentation

**Objetivo:** preparar una base técnica y documental profesional para desarrollar PUCEASIG con Codex sin generar deuda técnica temprana.
**Salida esperada:** repositorio documentado, backend Django modular ejecutable, Docker Compose, configuración por entornos, calidad de código, CI, seguridad base y preparación para ejecutar el Sprint 0.5 de frontend.
**Dependencias:** ninguna.

> Cada ticket = 1 rama = 1 PR o commit revisable = 1 sesión de trabajo. Cierra un ticket solo cuando sus criterios y verificaciones pasen.

---

## Prompt macro para Codex

```text
Actúa como arquitecto de software senior para el proyecto PUCEASIG — Sistema ERP/SIG Académico para PUCE Amazonas.

Antes de modificar código, lee:
- PROGRESS.md
- docs/project-reference-puceasig.md
- SPRINTS/sprint-00-foundation.md

Trabaja únicamente el ticket activo indicado en PROGRESS.md. No avances tickets posteriores sin autorización.

Contexto:
El MVP se enfoca en Gestión Académica: estudiantes, docentes, sílabos, notas, roles, periodos, carreras, asignaturas, cursos/paralelos, matrículas, reportes, archivos y auditoría.

Restricciones:
- No agregues credenciales reales.
- No uses datos reales de estudiantes, docentes o autoridades.
- No implementes módulos completos si el ticket solo pide scaffolding.
- No hardcodees reglas de calificación.
- Mantén cambios pequeños, claros, testeables y documentados.
```

---

## S0-T1 — Base documental del repositorio para Codex

**Tareas**
- Crear o actualizar `README.md` con descripción del proyecto, alcance del MVP, stack, estructura del repositorio y comandos principales.
- Crear carpeta `docs/` si no existe.
- Copiar o ubicar `project-reference-puceasig.md` en `docs/project-reference-puceasig.md`.
- Crear `docs/requirements.md` con requerimientos funcionales y no funcionales del MVP.
- Crear `docs/architecture.md` con arquitectura Django + DRF + PostgreSQL, almacenamiento compatible S3 y frontend futuro.
- Crear `docs/database-model.md` con entidades principales y relaciones iniciales.
- Crear `docs/grading-rules.md` con reglas S1, S2 y S3 como reglas de negocio.
- Crear `docs/security.md` con roles, permisos, auditoría y protección de datos.
- Crear `docs/frontend-architecture.md` o una sección equivalente que confirme la decisión Next.js + TypeScript + Tailwind CSS para el MVP.
- Crear `docs/mvp-roadmap.md` con fases y entregables, incluyendo Sprint 0.5 antes de Sprint 1.
- Crear `AGENTS.md` con reglas de trabajo para Codex.
- Crear `.env.example` y `.gitignore` adecuados.

**Criterios de aceptación**
- Los documentos existen y son coherentes entre sí.
- `AGENTS.md` instruye a Codex a leer `PROGRESS.md` y el sprint activo.
- `docs/grading-rules.md` no depende de fórmulas Excel copiadas literalmente.
- `.env.example` no contiene secretos reales.
- `.gitignore` excluye `.env`, entornos virtuales, archivos cargados, caches y builds.

**Verificación**
```bash
ls README.md AGENTS.md PROGRESS.md .env.example .gitignore
ls docs/project-reference-puceasig.md docs/requirements.md docs/architecture.md docs/database-model.md docs/grading-rules.md docs/security.md docs/mvp-roadmap.md
grep -R "SECRET_KEY=.*real\|password=.*real\|puceamazonas.edu.ec.*clave" -n . || true
```

---

## S0-T2 — Inicializar backend Django + DRF modular

**Tareas**
- Crear `backend/`.
- Crear proyecto Django `config`.
- Instalar Django y Django REST Framework.
- Crear estructura `backend/apps/`.
- Crear apps iniciales:
  - `core`
  - `accounts`
  - `academic_catalogs`
  - `people`
  - `students`
  - `teachers`
  - `enrollment`
  - `syllabus`
  - `grading`
  - `documents`
  - `reports`
  - `audit`
- Registrar apps en `INSTALLED_APPS`.
- Crear `BaseModel` abstracto en `core` con `id`, `created_at`, `updated_at`, `is_active` cuando aplique.
- Crear endpoint `GET /api/health/` que responda `{"status": "ok", "service": "puceasig"}`.

**Criterios de aceptación**
- `python manage.py check` pasa.
- `python manage.py migrate` ejecuta sin errores.
- `GET /api/health/` responde 200.
- La estructura modular queda lista para sprints siguientes.

**Verificación**
```bash
cd backend
python manage.py check
python manage.py migrate
python manage.py runserver
curl http://localhost:8000/api/health/
```

---

## S0-T3 — Docker Compose con PostgreSQL y Redis

**Tareas**
- Crear `Dockerfile` para backend con Python 3.12-slim o versión estable definida.
- Crear `docker-compose.yml` con servicios `backend`, `db` y `redis`.
- Configurar volumen persistente para PostgreSQL.
- Configurar variables desde `.env`.
- Asegurar que el backend use PostgreSQL, no SQLite.
- Agregar healthchecks básicos cuando sea posible.

**Criterios de aceptación**
- `docker compose up -d` levanta servicios.
- El backend conecta a PostgreSQL.
- Migraciones corren dentro del contenedor.
- Healthcheck responde desde el contenedor.

**Verificación**
```bash
docker compose up -d
docker compose ps
docker compose exec backend python manage.py migrate
curl http://localhost:8000/api/health/
```

---

## S0-T4 — Settings por entornos + variables de entorno

**Tareas**
- Dividir settings en `base.py`, `local.py`, `test.py`, `production.py`.
- Leer variables con `django-environ` o alternativa equivalente.
- Configurar `DEBUG`, `SECRET_KEY`, `DATABASE_URL`, `REDIS_URL`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` desde entorno.
- Documentar variables en `.env.example`.
- Configurar logging básico por entorno.

**Criterios de aceptación**
- Cambiar `DJANGO_SETTINGS_MODULE` entre local/test/production funciona.
- No hay secretos hardcodeados.
- `check --deploy` no muestra advertencias críticas no justificadas.

**Verificación**
```bash
grep -R "SECRET_KEY = ['"]" -n backend/config || true
docker compose exec backend python manage.py check
docker compose exec backend python manage.py check --deploy
```

---

## S0-T5 — Calidad de código, testing y pre-commit

**Tareas**
- Configurar `pytest`, `pytest-django`.
- Configurar `ruff`, `black`, `isort` en `pyproject.toml`.
- Configurar `pre-commit`.
- Crear pruebas para healthcheck y configuración mínima.
- Documentar comandos de test y lint en README.

**Criterios de aceptación**
- `pytest` pasa.
- `ruff check .`, `black --check .`, `isort --check .` pasan.
- `pre-commit run --all-files` pasa.

**Verificación**
```bash
pytest
ruff check .
black --check .
isort --check .
pre-commit run --all-files
```

---

## S0-T6 — CI/CD con GitHub Actions

**Tareas**
- Crear `.github/workflows/ci.yml`.
- Configurar instalación de dependencias.
- Configurar PostgreSQL y Redis como services.
- Ejecutar linters y tests.
- Agregar cache de dependencias si aplica.

**Criterios de aceptación**
- El workflow corre en push y pull request.
- Tests y linters corren automáticamente.
- El PR de prueba queda verde.

**Verificación**
```bash
pytest
# verificar check verde en GitHub Actions
```

---

## S0-T7 — Seguridad base, JWT scaffold, CORS y rate limiting

**Tareas**
- Instalar y configurar `djangorestframework-simplejwt` sin implementar aún flujos completos de usuario.
- Configurar `django-cors-headers` desde entorno.
- Configurar throttling básico DRF para usuarios anónimos y autenticados.
- Configurar `SECURE_*`, `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE` para producción.
- Crear pruebas mínimas de throttling o configuración.

**Criterios de aceptación**
- CORS toma orígenes desde `.env`.
- JWT queda disponible para Sprint 1.
- Rate limiting se puede verificar en test.
- No se rompen endpoints públicos como healthcheck.

**Verificación**
```bash
python manage.py check --deploy
pytest apps/core/
```

---

## S0-T8 — Bootstrap de apps Django del MVP y healthcheck extendido

**Tareas**
- Crear archivos mínimos `urls.py`, `serializers.py`, `services.py`, `selectors.py`, `tests/` donde aplique.
- Conectar routers DRF base sin endpoints de negocio todavía.
- Agregar endpoint `GET /api/version/` con versión, ambiente y nombre del servicio.
- Documentar convención de apps: modelos, services, selectors, serializers, views, urls, tests.

**Criterios de aceptación**
- Todas las apps tienen estructura consistente.
- No hay endpoints de negocio falsos o incompletos.
- `api/health/` y `api/version/` funcionan.

**Verificación**
```bash
pytest
curl http://localhost:8000/api/health/
curl http://localhost:8000/api/version/
```

---

## Cierre del Sprint 0

- [ ] Todos los tickets están cerrados con pruebas.
- [ ] Docker Compose levanta backend, PostgreSQL y Redis.
- [ ] CI verde.
- [ ] `PROGRESS.md` actualizado con versiones exactas elegidas.
- [ ] Cursor movido a **Sprint 0.5 / S0.5-T1**.
