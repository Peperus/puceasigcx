# Sprint 8 — Reports, Audit, QA & MVP Release

**Objetivo:** consolidar el MVP de Gestión Académica con reportes, auditoría completa, pruebas de aceptación, documentación de usuario y preparación de despliegue piloto.
**Salida esperada:** MVP funcional y desplegable para validación institucional.
**Dependencias:** Sprint 7.



> Las pantallas de este sprint deben respetar el layout, navegación por rol, componentes y tokens definidos en `SPRINTS/sprint-00-5-frontend-design-system.md`. La seguridad siempre se valida en backend.

---

## Prompt macro para Codex

```text
Lee PROGRESS.md, docs/project-reference-puceasig.md y SPRINTS/sprint-08-reports-audit-release.md.
Trabaja únicamente el ticket activo.
Este sprint es de consolidación del MVP: no agregues módulos post-MVP.
Prioriza estabilidad, pruebas, documentación, auditoría y despliegue piloto.
```

---

## S8-T1 — Reportes académicos mínimos del MVP

**Tareas**
- Reporte de estudiantes por carrera/periodo.
- Reporte de docentes asignados por periodo.
- Reporte de cursos/paralelos activos.
- Reporte de sílabos por estado.
- Reporte de notas por curso/modelo/estado.

**Criterios de aceptación**
- Reportes filtran por periodo y carrera.
- Respetan roles.
- Exportación CSV/XLSX funciona donde aplique.

**Verificación**
```bash
pytest apps/reports/tests/test_mvp_reports.py
```

---

## S8-T2 — Auditoría transversal

**Tareas**
- Revisar auditoría para:
  - usuarios y roles.
  - estudiantes/docentes.
  - matrículas.
  - sílabos.
  - notas.
  - cierres/reaperturas.
  - exportaciones.
- Crear vista Admin para auditoría con filtros.

**Criterios de aceptación**
- Acciones críticas quedan auditadas.
- Auditoría no es editable por usuarios no autorizados.
- Filtros permiten investigar cambios.

**Verificación**
```bash
pytest apps/audit/tests/test_cross_module_audit.py
```

---

## S8-T3 — Hardening de permisos

**Tareas**
- Revisar endpoints del MVP.
- Agregar pruebas negativas por rol.
- Confirmar que permisos se validan en backend.
- Corregir filtrados por usuario, carrera y rol.

**Criterios de aceptación**
- Tests prueban 401/403 en endpoints críticos.
- No hay exposición cruzada de notas entre estudiantes.
- Docentes no editan cursos ajenos.

**Verificación**
```bash
pytest apps/accounts/tests apps/enrollment/tests apps/syllabus/tests apps/grading/tests -k permission
```

---

## S8-T4 — QA de reglas de notas con fixtures representativos

**Tareas**
- Crear fixtures sintéticos para S1, S2 y S3.
- Crear pruebas de aceptación con escenarios completos de inicio a cierre.
- Documentar resultados esperados.

**Criterios de aceptación**
- Los tres modelos de notas pasan escenarios end-to-end.
- Los casos borde están cubiertos.
- No se usan datos reales.

**Verificación**
```bash
pytest apps/grading/tests/test_grading_acceptance.py
```

---

## S8-T5 — Documentación de usuario MVP

**Tareas**
- Crear `docs/user-guide-secretaria.md`.
- Crear `docs/user-guide-docente.md`.
- Crear `docs/user-guide-coordinador.md`.
- Crear `docs/user-guide-estudiante.md`.
- Incluir flujos principales: login, consulta, sílabo, notas, reportes.

**Criterios de aceptación**
- Guías son accionables y coherentes con MVP.
- No incluyen credenciales reales.

**Verificación**
```bash
ls docs/user-guide-*.md
```

---

## S8-T6 — Preparación de despliegue piloto

**Tareas**
- Crear `docs/deployment.md`.
- Documentar variables de entorno productivas.
- Documentar migraciones, collectstatic, creación de superusuario y backups.
- Configurar static/media para desarrollo y producción.
- Definir estrategia de almacenamiento de archivos.

**Criterios de aceptación**
- Un desarrollador puede desplegar siguiendo la guía.
- No hay secretos en documentación.
- Backup/restore básico documentado.

**Verificación**
```bash
python manage.py check --deploy
```

---

## S8-T7 — Smoke tests y UAT checklist

**Tareas**
- Crear `docs/uat-checklist.md`.
- Incluir escenarios:
  - crear periodo/carrera/asignatura.
  - crear estudiante/docente.
  - abrir curso/paralelo.
  - asignar docente.
  - matricular estudiante.
  - crear y aprobar sílabo.
  - registrar notas S1/S2/S3.
  - consultar notas como estudiante.
  - cerrar acta.
  - exportar reporte.
- Crear smoke tests automatizados básicos.

**Criterios de aceptación**
- UAT cubre flujo completo del MVP.
- Smoke tests pasan.

**Verificación**
```bash
pytest tests/smoke/
```

---

## S8-T8 — Cierre formal del MVP

**Tareas**
- Actualizar `README.md`.
- Actualizar `PROGRESS.md` con estado de todos los sprints MVP.
- Crear `docs/mvp-release-notes.md`.
- Listar limitaciones conocidas y backlog post-MVP.
- Crear tag sugerido `v0.1.0-mvp` si aplica.

**Criterios de aceptación**
- MVP tiene release notes.
- Backlog post-MVP está conectado con `sprint-09-17-escala-epr.md`.
- Documentación y tests están actualizados.

**Verificación**
```bash
pytest
ruff check .
black --check .
isort --check .
```

---

## Cierre del Sprint 8

- [ ] MVP de Gestión Académica funcional.
- [ ] Reportes y auditoría listos.
- [ ] Documentación de usuario y despliegue completa.
- [ ] UAT checklist lista para validación institucional.
- [ ] Cursor movido al bloque de escalamiento según prioridad institucional.
