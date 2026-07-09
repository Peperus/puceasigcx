# Sprint 5 — Syllabus Management

**Objetivo:** implementar la gestión de sílabos del MVP, priorizando la nueva versión basada en resultados de aprendizaje, rúbricas, bibliografía y planificación semanal.
**Salida esperada:** docentes pueden crear, finalizar, descargar y cargar sílabos aprobados; coordinación/secretaría puede revisar estados.
**Dependencias:** Sprint 4.



> Las pantallas de este sprint deben respetar el layout, navegación por rol, componentes y tokens definidos en `SPRINTS/sprint-00-5-frontend-design-system.md`. La seguridad siempre se valida en backend.

---

## Prompt macro para Codex

```text
Lee PROGRESS.md, docs/project-reference-puceasig.md, docs/database-model.md y SPRINTS/sprint-05-syllabus.md.
Trabaja únicamente el ticket activo.
Implementa sílabo nueva versión como prioridad del MVP. La versión anterior debe quedar soportada como tipo o compatibilidad mínima, sin bloquear S1/S2/S3.
No permitas registrar notas de un curso si el sílabo requerido no está finalizado/aprobado, salvo permiso institucional explícito.
```

---

## S5-T1 — Modelo Syllabus base

**Tareas**
- Crear `Syllabus` asociado OneToOne o ForeignKey controlado a `CourseSection`.
- Campos: versión, estado, descripción, metodología, docente titular, codocente opcional, fecha_creación, fecha_finalización, fecha_aprobación.
- Estados: borrador, en_revision, aprobado, observado, finalizado, archivado.
- Validar un sílabo activo por curso.

**Criterios de aceptación**
- Curso puede tener sílabo.
- Estados se gestionan correctamente.
- No se duplica sílabo activo por curso.

**Verificación**
```bash
pytest apps/syllabus/tests/test_syllabus_model.py
```

---

## S5-T2 — Competencias y resultados de aprendizaje

**Tareas**
- Crear modelos:
  - `SyllabusCompetency`.
  - `LearningOutcome` o `SyllabusLearningOutcome`.
  - Relación con resultados de carrera y asignatura.
- Soportar al menos 3 resultados de aprendizaje de asignatura y carrera según regla institucional actual.
- Validar que los RA requeridos existan antes de pasar a rúbricas.

**Criterios de aceptación**
- Sílabo puede registrar competencias transversales/disciplinares.
- Sílabo puede registrar RA de carrera y de asignatura.
- Tests validan mínimos requeridos.

**Verificación**
```bash
pytest apps/syllabus/tests/test_learning_outcomes.py
```

---

## S5-T3 — Rúbricas y criterios de evaluación

**Tareas**
- Crear `SyllabusCriterion` asociado a RA.
- Crear niveles de logro A/B/C/D por criterio.
- Guardar ponderación por criterio sobre 100.
- Validar que ponderaciones por RA sumen 100.
- Preparar relación con motor de notas del Sprint 6.

**Criterios de aceptación**
- Cada RA tiene criterios y niveles A-D.
- Las ponderaciones se validan.
- No se permite finalizar si faltan criterios.

**Verificación**
```bash
pytest apps/syllabus/tests/test_rubrics.py
```

---

## S5-T4 — Bibliografía

**Tareas**
- Crear `SyllabusBibliography` con tipo: básica, complementaria, recomendada, digital.
- Campos: referencia APA, código_biblioteca, cantidad_ejemplares.
- Validar campos obligatorios.
- Preparar integración futura con biblioteca.

**Criterios de aceptación**
- Docente puede agregar, editar y eliminar bibliografía en borrador.
- No se permite editar bibliografía si el sílabo está aprobado, salvo reapertura autorizada.

**Verificación**
```bash
pytest apps/syllabus/tests/test_bibliography.py
```

---

## S5-T5 — Planificación semanal y experiencias de aprendizaje

**Tareas**
- Crear `SyllabusWeeklyPlan` con RA, semana/fecha, dimensión del conocimiento.
- Registrar experiencias en contacto con docente, práctico-experimental y autónomo.
- Registrar horas, recursos y escenarios por componente.
- Validar horas contra horas de la asignatura de forma flexible inicialmente.

**Criterios de aceptación**
- Docente puede registrar planificación semanal.
- Se puede listar, editar y eliminar actividades en borrador.
- No se finaliza sílabo sin planificación mínima.

**Verificación**
```bash
pytest apps/syllabus/tests/test_weekly_plan.py
```

---

## S5-T6 — Flujo de finalización y aprobación

**Tareas**
- Implementar acciones:
  - finalizar por docente.
  - enviar a revisión.
  - aprobar por coordinador/secretaría autorizada.
  - observar/devolver.
  - reabrir con justificación.
- Registrar auditoría de cambios de estado.

**Criterios de aceptación**
- Docente no puede aprobar su propio sílabo salvo rol autorizado.
- Cambios de estado quedan auditados.
- Sílabo aprobado bloquea edición general.

**Verificación**
```bash
pytest apps/syllabus/tests/test_syllabus_workflow.py
```

---

## S5-T7 — Carga de sílabo firmado y archivos

**Tareas**
- Implementar carga de PDF firmado/aprobado.
- Validar extensión PDF y tamaño máximo configurable.
- Guardar archivo usando storage compatible S3 o storage local en desarrollo.
- Evitar caracteres problemáticos en nombres o normalizarlos.
- Registrar quién subió el archivo y cuándo.

**Criterios de aceptación**
- PDF se carga y queda asociado al sílabo.
- Archivos no se guardan en Git.
- Usuario no autorizado no puede cargar/reemplazar.

**Verificación**
```bash
pytest apps/documents/tests/test_syllabus_upload.py
```

---

## S5-T8 — Descarga/generación de sílabo

**Tareas**
- Crear endpoint o vista para generar/visualizar sílabo final en formato HTML imprimible.
- Preparar exportación PDF vía navegador o librería definida.
- Incluir secciones del formato: datos informativos, competencias/RA, evaluación, metodología, planificación, bibliografía y firmas.

**Criterios de aceptación**
- Sílabo puede visualizarse en formato imprimible.
- El formato incluye datos del curso, docente, RA, rúbricas y bibliografía.

**Verificación**
```bash
pytest apps/syllabus/tests/test_syllabus_render.py
```

---

## Cierre del Sprint 5

- [ ] Sílabo nueva versión funcional.
- [ ] Flujo de aprobación y carga de PDF operativo.
- [ ] Relación sílabo-notas preparada.
- [ ] `docs/syllabus.md` actualizado.
- [ ] Cursor a **Sprint 6 / S6-T1**.
