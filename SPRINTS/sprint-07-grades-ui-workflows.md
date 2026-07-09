# Sprint 7 — Grade Entry, Student Views & Closures

**Objetivo:** construir los flujos de uso del motor de notas: ingreso docente, consulta estudiantil, visualización de secretaría/coordinación y cierre de actas.
**Salida esperada:** docentes registran notas, estudiantes consultan su avance y secretaría/coordinación revisa resultados por curso.
**Dependencias:** Sprint 6.



> Las pantallas de este sprint deben respetar el layout, navegación por rol, componentes y tokens definidos en `SPRINTS/sprint-00-5-frontend-design-system.md`. La seguridad siempre se valida en backend.

---

## Prompt macro para Codex

```text
Lee PROGRESS.md, docs/project-reference-puceasig.md, docs/grading-rules.md y SPRINTS/sprint-07-grades-ui-workflows.md.
Trabaja únicamente el ticket activo.
Usa el motor de notas del Sprint 6; no dupliques cálculos en views o serializers.
Toda edición de nota debe pasar por servicios y auditoría.
```

---

## S7-T1 — API de ingreso de notas para docentes

**Tareas**
- Crear endpoints para listar cursos asignados al docente.
- Crear endpoints para listar estudiantes del curso.
- Crear endpoints para registrar/actualizar notas según S1/S2/S3.
- Validar que docente solo edite cursos asignados.
- Validar que gradebook esté abierto.

**Criterios de aceptación**
- Docente no puede editar curso ajeno.
- Nota fuera de rango se rechaza.
- Cada guardado dispara recálculo y auditoría.

**Verificación**
```bash
pytest apps/grading/tests/test_teacher_grade_entry_api.py
```

---

## S7-T2 — Flujo S1/S2: calificar por RA y criterio

**Tareas**
- Implementar endpoints para seleccionar RA y criterio.
- Registrar notas masivas por estudiante para ese criterio.
- Calcular avance por RA y parcial.
- Retornar resumen con letras A/B/C/D.

**Criterios de aceptación**
- Flujo reproduce la lógica de selección RA/criterio del sistema actual.
- Guardado masivo es transaccional.
- Errores por estudiante se reportan claramente.

**Verificación**
```bash
pytest apps/grading/tests/test_ra_criterion_entry.py
```

---

## S7-T3 — Flujo S3: práctica + evaluación por parcial

**Tareas**
- Implementar endpoints para registrar práctica y evaluación por parcial.
- Calcular promedio del parcial y promedio final.
- Registrar cuarta evaluación si aplica.

**Criterios de aceptación**
- Tres parciales se registran correctamente.
- Sistema indica si requiere cuarta evaluación.
- Cuarta evaluación actualiza estado final.

**Verificación**
```bash
pytest apps/grading/tests/test_s3_grade_entry.py
```

---

## S7-T4 — Consulta de notas para estudiantes

**Tareas**
- Crear endpoint `GET /api/student/grades/`.
- Mostrar cursos matriculados, notas por RA/parcial, letras, porcentaje o estado según modelo.
- Ocultar notas de cursos no publicados/cerrados según configuración.
- Evitar que estudiante consulte datos de otro estudiante.

**Criterios de aceptación**
- Estudiante solo ve sus notas.
- Información coincide con cálculo del motor.
- Estados son comprensibles: aprobado, reprobado, en curso, requiere recuperación.

**Verificación**
```bash
pytest apps/grading/tests/test_student_grade_view.py
```

---

## S7-T5 — Vistas de secretaría y coordinación

**Tareas**
- Crear endpoints de consulta por periodo, carrera, curso, docente, estudiante.
- Permitir filtros por modelo de calificación, estado y resultado.
- Restringir coordinador a su carrera si se configura alcance.

**Criterios de aceptación**
- Secretaría/Admin ve reportes académicos amplios.
- Coordinador ve cursos de su carrera.
- Docente no ve información masiva de cursos ajenos.

**Verificación**
```bash
pytest apps/reports/tests/test_academic_grade_queries.py
```

---

## S7-T6 — Cierre y reapertura de actas/gradebook

**Tareas**
- Implementar acción de cerrar gradebook.
- Validar que no existan notas incompletas salvo permiso explícito.
- Implementar reapertura con justificación y rol autorizado.
- Registrar auditoría.

**Criterios de aceptación**
- Gradebook cerrado bloquea edición.
- Reapertura exige motivo.
- Cierre genera snapshot final.

**Verificación**
```bash
pytest apps/grading/tests/test_gradebook_closure.py
```

---

## S7-T7 — Exportación básica de actas

**Tareas**
- Exportar CSV/XLSX básico de notas por curso.
- Incluir datos del periodo, carrera, asignatura, paralelo, docente y fecha de generación.
- Registrar auditoría de exportación.
- No incluir datos no necesarios.

**Criterios de aceptación**
- Exportación descarga archivo válido.
- Respeta permisos.
- Auditoría registra usuario y filtros.

**Verificación**
```bash
pytest apps/reports/tests/test_grade_exports.py
```

---

## Cierre del Sprint 7

- [ ] Docente puede registrar notas de sus cursos.
- [ ] Estudiante puede consultar notas.
- [ ] Secretaría/coordinación puede consultar reportes.
- [ ] Cierre/reapertura con auditoría implementado.
- [ ] Cursor a **Sprint 8 / S8-T1**.
