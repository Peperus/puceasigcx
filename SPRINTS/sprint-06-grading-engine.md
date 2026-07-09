# Sprint 6 — Grading Engine S1/S2/S3

**Objetivo:** implementar el motor de calificaciones de PUCEASIG para los tres sistemas de notas, desacoplado de la interfaz y cubierto por pruebas unitarias.
**Salida esperada:** servicios de cálculo confiables para S1, S2 y S3, con configuración por curso y auditoría base.
**Dependencias:** Sprint 5.



> Las pantallas de este sprint deben respetar el layout, navegación por rol, componentes y tokens definidos en `SPRINTS/sprint-00-5-frontend-design-system.md`. La seguridad siempre se valida en backend.

---

## Prompt macro para Codex

```text
Lee PROGRESS.md, docs/project-reference-puceasig.md, docs/grading-rules.md y SPRINTS/sprint-06-grading-engine.md.
Trabaja únicamente el ticket activo.
Implementa S1, S2 y S3 como servicios de dominio probados, no como fórmulas Excel copiadas literalmente.
Todas las notas se manejan en escala 0 a 50 salvo configuración explícita.
No implementes todavía pantallas completas de ingreso masivo; eso va en Sprint 7.
```

---

## S6-T1 — Modelos base de libro de calificaciones

**Tareas**
- Crear `Gradebook` asociado a `CourseSection` y `Syllabus`.
- Campos: grading_model (S1/S2/S3), estado, fecha_apertura, fecha_cierre.
- Crear `GradeItem` o estructura base para criterios/actividades.
- Crear `StudentGradeRecord` asociado a matrícula del curso.
- Validar que exista sílabo finalizado/aprobado si el curso lo requiere.

**Criterios de aceptación**
- Cada curso tiene un libro de calificaciones.
- El modelo de calificación se hereda o valida desde el curso.
- No se crea gradebook si el curso no está activo o no cumple prerequisitos.

**Verificación**
```bash
pytest apps/grading/tests/test_gradebook_model.py
```

---

## S6-T2 — Servicio común de escala y niveles A/B/C/D

**Tareas**
- Implementar `letter_from_score(score)` usando configuración institucional.
- Reglas base:
  - A: >= 45
  - B: >= 40 y < 45
  - C: >= 30 y < 40
  - D: < 30
- Validar rango 0–50.
- Tests con bordes: 0, 29.99, 30, 39.99, 40, 44.99, 45, 50.

**Criterios de aceptación**
- Conversión de nota a letra es consistente.
- Valores fuera de rango se rechazan o normalizan según regla documentada.

**Verificación**
```bash
pytest apps/grading/tests/test_grade_scale.py
```

---

## S6-T3 — Motor S1 por resultados de aprendizaje

**Tareas**
- Implementar modelos o estructuras para RA, criterios y notas por estudiante.
- Implementar `calculate_s1_grade`.
- Regla principal: tres parciales; la pérdida de un RA final menor a 30 implica pérdida de la asignatura, salvo recuperación aprobada según política.
- Calcular nota final por RA y estado final del estudiante.
- Soportar recuperación por RA.

**Criterios de aceptación**
- S1 calcula resultado por RA.
- Un RA final menor a 30 reprueba si no hay recuperación aprobada.
- Recuperación aprobada ajusta estado según regla documentada.

**Verificación**
```bash
pytest apps/grading/tests/test_s1_engine.py
```

---

## S6-T4 — Motor S2 por resultados de aprendizaje con tolerancia de un RA

**Tareas**
- Implementar `calculate_s2_grade`.
- Regla principal: tres parciales; dos RA perdidos implican pérdida de asignatura.
- Si existe un RA perdido, habilitar recuperación y resolver según resultado de recuperación.
- Documentar diferencia con S1 en `docs/grading-rules.md`.

**Criterios de aceptación**
- Cero RA perdidos aprueba.
- Un RA perdido requiere recuperación.
- Dos o más RA perdidos reprueba.
- Tests cubren casos límite.

**Verificación**
```bash
pytest apps/grading/tests/test_s2_engine.py
```

---

## S6-T5 — Motor S3 sílabo anterior: práctica + evaluación

**Tareas**
- Implementar `calculate_s3_grade`.
- Soportar tres parciales con componentes práctica + evaluación.
- Configurar pesos por parcial/componente desde catálogo o configuración.
- Si promedio final < 30, habilitar cuarta evaluación/supletorio según regla institucional.
- Resolver estado final aprobado/reprobado.

**Criterios de aceptación**
- S3 calcula promedio por parcial y final.
- Cuarta evaluación se habilita cuando corresponde.
- Cuarta evaluación aprobada cambia estado según regla documentada.

**Verificación**
```bash
pytest apps/grading/tests/test_s3_engine.py
```

---

## S6-T6 — Persistencia de resultados calculados

**Tareas**
- Definir `GradeCalculationSnapshot` o campos para almacenar resultado calculado.
- Registrar fecha, versión de regla, usuario que recalculó y fuente.
- Evitar que snapshots sustituyan el dato fuente.
- Implementar servicio `recalculate_gradebook`.

**Criterios de aceptación**
- Cálculos son reproducibles.
- Snapshot conserva regla usada.
- Cambios de notas obligan a recalcular.

**Verificación**
```bash
pytest apps/grading/tests/test_grade_snapshots.py
```

---

## S6-T7 — Auditoría de cambios de notas

**Tareas**
- Auditar creación, modificación y eliminación lógica de notas.
- Guardar valor anterior, valor nuevo, usuario, fecha, motivo si aplica.
- Bloquear modificaciones si gradebook está cerrado, salvo permiso de reapertura.

**Criterios de aceptación**
- Todo cambio de nota queda auditado.
- Gradebook cerrado no permite cambios normales.
- Reapertura exige justificación.

**Verificación**
```bash
pytest apps/grading/tests/test_grade_audit.py
```

---

## S6-T8 — Documentación técnica del motor

**Tareas**
- Actualizar `docs/grading-rules.md`.
- Crear `docs/grading-engine.md` con modelos, servicios y casos borde.
- Documentar diferencias S1/S2/S3.
- Documentar qué aspectos requieren confirmación institucional.

**Criterios de aceptación**
- Documentación permite a otro desarrollador entender el motor.
- Casos no confirmados quedan marcados como pendientes, no asumidos silenciosamente.

**Verificación**
```bash
grep -n "S1\|S2\|S3\|pendiente" docs/grading-rules.md docs/grading-engine.md
```

---

## Cierre del Sprint 6

- [x] Motores S1, S2 y S3 implementados.
- [x] Casos límite probados.
- [x] Auditoría de notas lista.
- [x] `docs/grading-rules.md` actualizado.
- [x] Cursor a **Sprint 7 / S7-T1**.
