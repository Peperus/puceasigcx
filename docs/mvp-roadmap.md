# Roadmap del MVP

El proyecto se desarrolla por sprints pequenos, testeables y revisables. El cursor activo vive en `PROGRESS.md`.

## Bloque Foundation

### Sprint 0: Foundation & Documentation

Entregables:

- Base documental del repositorio.
- Backend Django + DRF modular.
- Docker Compose con PostgreSQL y Redis.
- Settings por entornos.
- Calidad de codigo, testing y pre-commit.
- CI/CD con GitHub Actions.
- Seguridad base, JWT scaffold, CORS y rate limiting.
- Bootstrap de apps Django y healthcheck extendido.

### Sprint 0.5: Frontend Design System & UX Foundation

Debe ejecutarse antes de Sprint 1.

Entregables:

- Aplicacion `/frontend` con Next.js, TypeScript y Tailwind CSS.
- Tema visual institucional centralizado.
- Componentes UI reutilizables.
- Layout autenticado.
- Navegacion por rol.
- Prototipos navegables con datos mock sinteticos.
- `docs/frontend-design-system.md`.
- `frontend/README.md`.

## Bloque MVP: Gestion Academica

### Sprint 1: Authentication, Roles & Access Control

- Login/logout.
- Perfiles de usuario.
- Roles base.
- Permisos por modulo.
- Auditoria inicial.
- Seeds de roles sin datos reales.

### Sprint 2: Academic Catalogs & Institutional Setup

- Periodos.
- Carreras.
- Planes de estudio.
- Niveles.
- Asignaturas.
- Paralelos.
- Dominios y parametros academicos.

### Sprint 3: People, Students & Teachers

- Modelo central de persona.
- CRUD de estudiantes.
- CRUD de docentes.
- Perfiles academicos.
- Consultas base.

### Sprint 4: Academic Offer, Courses & Enrollment

- Oferta academica por periodo.
- Cursos/paralelos.
- Asignacion docente.
- Matriculas.
- Listas de estudiantes por curso.

### Sprint 5: Syllabus Management

- Silabo nueva version.
- Silabo antiguo.
- Competencias.
- Resultados de aprendizaje.
- Criterios, rubricas y bibliografia.
- Flujo de revision y aprobacion.
- Carga de silabo firmado.

### Sprint 6: Grading Engine S1/S2/S3

- Gradebooks.
- Criterios y actividades.
- Motor S1.
- Motor S2.
- Motor S3.
- Recuperaciones.
- Pruebas unitarias de reglas de notas.

### Sprint 7: Grade Entry, Student Views & Closures

- Registro de notas por docente.
- Consulta de notas por estudiante.
- Cierre y reapertura autorizada.
- Estados finales.
- Validaciones de permisos.

### Sprint 8: Reports, Audit, QA & MVP Release

- Reportes academicos.
- Actas.
- Exportaciones.
- Auditoria completa de acciones criticas.
- Pruebas de integracion.
- Hardening del MVP.
- Documentacion de despliegue piloto.

## Posterior al MVP

Los sprints 9 a 17 incorporaran macroprocesos institucionales:

- Admisiones.
- Bienestar universitario.
- Biblioteca y repositorio.
- Requerimientos, PQRSD y mensajeria.
- Moodle.
- Gestion documental.
- Inventario y activos.
- Analitica institucional.
- Portal integral, interoperabilidad y hardening de escala.

Estos modulos no deben adelantarse dentro del MVP salvo que un ticket activo lo pida explicitamente.
