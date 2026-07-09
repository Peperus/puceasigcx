# Sprint 4 — Academic Offer, Courses & Enrollment

**Objetivo:** habilitar la oferta académica por periodo, cursos/paralelos, asignación docente y matrícula de estudiantes.
**Salida esperada:** Secretaría/Coordinación puede abrir cursos, asignar docentes y matricular estudiantes por periodo.
**Dependencias:** Sprint 3.



> Las pantallas de este sprint deben respetar el layout, navegación por rol, componentes y tokens definidos en `SPRINTS/sprint-00-5-frontend-design-system.md`. La seguridad siempre se valida en backend.

---

## Prompt macro para Codex

```text
Lee PROGRESS.md, docs/project-reference-puceasig.md, docs/database-model.md y SPRINTS/sprint-04-academic-offer-enrollment.md.
Trabaja únicamente el ticket activo.
Construye la base de cursos/paralelos y matrículas. No implementes sílabos ni notas salvo campos de relación necesarios.
Todo debe estar anclado a periodo, carrera/plan, asignatura y paralelo.
```

---

## S4-T1 — Oferta académica por periodo

**Tareas**
- Crear `AcademicOffer` asociada a periodo, carrera, plan y nivel.
- Estados: borrador, publicada, cerrada, archivada.
- Validar que no se duplique oferta para mismo periodo/carrera/plan/nivel.
- Admin con filtros por periodo/carrera/estado.

**Criterios de aceptación**
- Se puede abrir una oferta por periodo.
- No hay duplicidades críticas.

**Verificación**
```bash
pytest apps/enrollment/tests/test_academic_offer.py
```

---

## S4-T2 — Cursos/paralelos

**Tareas**
- Crear `CourseSection` asociado a oferta, asignatura, paralelo, cupo, modalidad y modelo de calificación S1/S2/S3.
- Estados: planificado, activo, cerrado, cancelado.
- Validar paralelo único por asignatura y periodo.
- Preparar relación con sílabo y notas.

**Criterios de aceptación**
- Se puede crear paralelo A/B/etc. por asignatura.
- Cada curso tiene modelo de calificación asignado.
- No hay duplicados por periodo/asignatura/paralelo.

**Verificación**
```bash
pytest apps/enrollment/tests/test_course_sections.py
```

---

## S4-T3 — Asignación docente

**Tareas**
- Crear `TeachingAssignment` con curso, docente, rol_docente (titular, codocente), carga_horaria opcional y estado.
- Validar docente activo.
- Permitir múltiples docentes con roles controlados.

**Criterios de aceptación**
- Curso puede tener docente titular y codocente.
- Docente ve solo sus cursos asignados.
- Coordinador ve cursos de su carrera.

**Verificación**
```bash
pytest apps/enrollment/tests/test_teaching_assignments.py
```

---

## S4-T4 — Matrícula académica

**Tareas**
- Crear `Enrollment` o matrícula por estudiante y periodo.
- Crear `CourseEnrollment` para inscripción del estudiante en cursos/paralelos.
- Estados: matriculado, retirado, aprobado, reprobado, homologado, anulado.
- Validar cupos y duplicidades.

**Criterios de aceptación**
- Estudiante puede matricularse en varios cursos del periodo.
- No se duplica matrícula del mismo estudiante en el mismo curso.
- Cupo se respeta si está activo.

**Verificación**
```bash
pytest apps/enrollment/tests/test_enrollment.py
```

---

## S4-T5 — Homologaciones y casos especiales mínimos

**Tareas**
- Crear estructura mínima para registrar homologaciones o equivalencias, sin flujo complejo.
- Asociar homologación a estudiante, asignatura, periodo y resolución/observación.
- Definir estado y auditoría.

**Criterios de aceptación**
- Secretaría puede registrar homologación básica.
- No afecta automáticamente notas hasta sprint de grading, salvo estado.

**Verificación**
```bash
pytest apps/enrollment/tests/test_homologations.py
```

---

## S4-T6 — API/Admin de oferta y matrícula

**Tareas**
- Crear endpoints protegidos para cursos, asignaciones y matrículas.
- Docente: consulta sus cursos.
- Estudiante: consulta sus cursos matriculados.
- Secretaría/Admin: CRUD completo según permisos.
- Coordinador: consulta/gestión según carrera.

**Criterios de aceptación**
- Permisos por rol probados.
- API no permite matricular en curso cerrado.

**Verificación**
```bash
pytest apps/enrollment/tests/test_enrollment_api.py
```

---

## S4-T7 — Dashboard académico mínimo

**Tareas**
- Crear endpoint `GET /api/academic/dashboard/` con conteos por periodo: estudiantes, docentes, cursos, matrículas.
- Proteger por rol Secretaría/Coordinador/Admin.
- No incluir notas todavía.

**Criterios de aceptación**
- Dashboard responde conteos correctos.
- Roles no autorizados reciben 403.

**Verificación**
```bash
pytest apps/reports/tests/test_academic_dashboard_minimal.py
```

---

## Cierre del Sprint 4

- [ ] Oferta académica funcional.
- [ ] Cursos/paralelos funcionales.
- [ ] Matrícula básica funcional.
- [ ] Docente/estudiante pueden consultar cursos correspondientes.
- [ ] Cursor a **Sprint 5 / S5-T1**.
