# PUCEASIG v0.1.0-mvp - Release notes

Fecha de preparacion: 2026-07-10.

## Alcance entregado

El MVP de Gestion Academica cubre:

- Autenticacion JWT, recuperacion de contrasena y perfil `/api/me/`.
- Roles institucionales base y permisos por backend.
- Catalogos academicos: periodos, carreras, planes, niveles, asignaturas,
  parametros y sistemas S1/S2/S3.
- Personas, estudiantes, docentes y horarios de atencion.
- Oferta academica, cursos/paralelos, asignaciones docentes y matricula.
- Silabos nueva version: competencias, RA, rubricas, bibliografia,
  planificacion, aprobacion, reapertura y PDF firmado.
- Motor de notas S1, S2 y S3 con snapshots reproducibles.
- Registro docente de notas, vista de estudiante, consultas de secretaria y
  coordinacion.
- Cierre/reapertura de actas con justificacion.
- Reportes MVP y exportacion CSV/XLSX.
- Auditoria transversal de acciones criticas.
- Guias de usuario, despliegue piloto, smoke tests y UAT checklist.

## Verificaciones de release

- `pytest apps/reports/tests/test_mvp_reports.py`
- `pytest apps/audit/tests/test_cross_module_audit.py`
- `pytest apps/accounts/tests apps/enrollment/tests apps/syllabus/tests apps/grading/tests -k permission`
- `pytest apps/grading/tests/test_grading_acceptance.py`
- `pytest tests/smoke/`
- `python manage.py check --deploy`
- `pytest`
- `ruff check .`
- `black --check .`
- `isort --check .`

## Limitaciones conocidas

- El frontend sigue operando principalmente como prototipo navegable con mocks;
  el backend ya expone APIs funcionales del MVP. Esta brecha queda planificada
  en `Sprint 8.5 — Frontend Integration MVP` antes de iniciar Sprint 9.
- El almacenamiento S3-compatible esta documentado como estrategia de despliegue;
  la configuracion por defecto usa storage local de Django.
- El correo institucional SMTP queda configurable por variables de entorno; en
  desarrollo se usa backend de consola o memoria.
- Politicas institucionales pendientes pueden ajustar recuperacion S1,
  diferenciacion intersemestral/reprobado y cuarta evaluacion S3.
- No se incluyen modulos post-MVP: admisiones, bienestar completo, biblioteca,
  mensajeria, Moodle, inventario ni analitica avanzada.

## Backlog post-MVP

Conectar con `SPRINTS/sprint-09-17-escala-epr.md`:

- Sprint 9: admisiones y captacion.
- Sprint 10: bienestar universitario.
- Sprint 11: biblioteca y repositorio academico.
- Sprint 12: requerimientos, PQRSD y mensajeria institucional.
- Sprint 13: integracion Moodle y aula virtual.
- Sprint 14: gestion documental institucional.
- Sprint 15: inventario y activos.
- Sprint 16: analitica institucional y tableros estrategicos.
- Sprint 17: portal integral, interoperabilidad y hardening de escala.

## Tag sugerido

Crear el tag anotado despues de merge a `main`:

```bash
git tag -a v0.1.0-mvp -m "PUCEASIG MVP Gestion Academica"
```
