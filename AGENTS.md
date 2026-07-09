# AGENTS.md — PUCEASIG

## Contexto

Este repositorio corresponde a PUCEASIG — Sistema ERP/SIG Académico para PUCE Amazonas. El MVP se enfoca en Gestión Académica: estudiantes, docentes, sílabos, notas, roles, periodos, carreras, asignaturas, cursos/paralelos, matrículas, reportes, archivos y auditoría.

## Archivos obligatorios de lectura

Antes de trabajar, Codex debe leer:

1. `PROGRESS.md`
2. `docs/project-reference-puceasig.md`
3. El archivo del sprint activo dentro de `SPRINTS/`
4. Documentos específicos del módulo si existen, por ejemplo `docs/grading-rules.md`, `docs/security.md` o `docs/frontend-design-system.md`.

## Regla de trabajo

Trabaja únicamente el ticket activo indicado en `PROGRESS.md`. No avances tickets posteriores sin autorización. Cada ticket debe ser pequeño, testeable y revisable.

## Stack principal

- Backend: Python + Django + Django REST Framework.
- Base de datos: PostgreSQL.
- Frontend del MVP: Next.js + TypeScript + Tailwind CSS.
- Administración auxiliar: Django Admin.
- Archivos: almacenamiento compatible con S3.
- Testing: pytest / pytest-django para backend; lint/build/typecheck para frontend.
- CI/CD: GitHub Actions.

## Reglas de frontend

- Ejecutar Sprint 0.5 antes de construir pantallas funcionales del MVP.
- Reutilizar tokens, layouts, componentes y navegación definidos en el design system.
- No duplicar componentes visuales sin justificación.
- No usar datos reales en mocks.
- No incluir logos oficiales o assets institucionales si no están presentes en el repositorio.
- Ocultar botones por rol no reemplaza validación de permisos en backend.
- Mantener accesibilidad básica: contraste, labels, foco visible y errores claros.

## Reglas de backend

- Mantener apps Django modulares.
- Usar services/selectors para lógica de negocio cuando corresponda.
- Mantener migraciones versionadas.
- Validar permisos en views, serializers y servicios críticos.
- Auditar cambios críticos: notas, sílabos, matrícula, roles y cierres académicos.
- No hardcodear reglas de calificación.
- Implementar S1, S2 y S3 como servicios de dominio probados.

## Seguridad y datos

- No usar credenciales reales.
- No guardar `.env` en Git.
- No usar datos reales de estudiantes, docentes, autoridades o personal administrativo en seeds, tests, mocks o documentación pública.
- No guardar archivos cargados en Git.
- Proteger datos académicos y personales.
- Toda corrección de notas cerradas debe requerir permiso especial y justificación.

## Cierre de ticket

Para cerrar un ticket:

1. Ejecuta las verificaciones indicadas en el sprint.
2. Documenta pruebas ejecutadas.
3. Actualiza `PROGRESS.md`.
4. Mueve el cursor al siguiente ticket.
5. No marques como ✅ si hay tests fallidos o criterios incompletos.
