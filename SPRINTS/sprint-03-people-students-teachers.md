# Sprint 3 — People, Students & Teachers

**Objetivo:** implementar la gestión de personas, estudiantes y docentes como datos maestros del MVP.
**Salida esperada:** una persona puede estar asociada a usuario, estudiante y/o docente sin duplicación de identidad.
**Dependencias:** Sprint 2.



> Las pantallas de este sprint deben respetar el layout, navegación por rol, componentes y tokens definidos en `SPRINTS/sprint-00-5-frontend-design-system.md`. La seguridad siempre se valida en backend.

---

## Prompt macro para Codex

```text
Lee PROGRESS.md, docs/project-reference-puceasig.md, docs/database-model.md y SPRINTS/sprint-03-people-students-teachers.md.
Trabaja únicamente el ticket activo.
Diseña Person como dato maestro central. Evita duplicar datos personales entre Student y Teacher.
No implementes matrícula ni cursos completos todavía.
```

---

## S3-T1 — Modelo Person central

**Tareas**
- Crear `Person` con identificación, nombres, apellidos, correo personal/institucional, teléfono, fecha de nacimiento opcional, dirección opcional.
- Validar identificación única cuando esté presente.
- Relacionar opcionalmente con `User`.
- Admin con búsqueda por identificación, nombres y correo.

**Criterios de aceptación**
- No se crean personas duplicadas con misma identificación.
- Un usuario puede vincularse a una persona.
- Admin permite búsqueda eficiente.

**Verificación**
```bash
pytest apps/people/tests/test_person_model.py
```

---

## S3-T2 — Modelo Student

**Tareas**
- Crear `Student` asociado OneToOne con `Person`.
- Campos: código_estudiante, carrera principal, estado, fecha_ingreso, periodo_ingreso, observaciones.
- Estados: aspirante_convertido, activo, retirado, egresado, graduado, suspendido, archivado.
- Preparar relación con matrícula en Sprint 4.

**Criterios de aceptación**
- Una persona puede tener perfil estudiante.
- Código de estudiante único.
- Secretaría/Admin pueden gestionar estudiantes.

**Verificación**
```bash
pytest apps/students/tests/test_student_model.py
```

---

## S3-T3 — Modelo Teacher

**Tareas**
- Crear `Teacher` asociado OneToOne con `Person`.
- Campos: código_docente, título/grado, perfil académico, teléfono institucional, estado, dominios o áreas.
- Preparar datos usados en sílabo: reseña académica/profesional y horario de atención.

**Criterios de aceptación**
- Una persona puede tener perfil docente.
- Perfil docente tiene datos necesarios para sílabo.
- Admin permite filtros por estado y dominio.

**Verificación**
```bash
pytest apps/teachers/tests/test_teacher_model.py
```

---

## S3-T4 — Horarios de atención docente

**Tareas**
- Crear `TeacherOfficeHour` con docente, modalidad, día, hora_inicio, hora_fin, lugar/enlace.
- Modalidades: presencial, virtual.
- Validar hora_inicio < hora_fin.
- Preparar consumo por módulo de sílabos.

**Criterios de aceptación**
- Docente puede tener varios horarios.
- Horarios inválidos se rechazan.

**Verificación**
```bash
pytest apps/teachers/tests/test_office_hours.py
```

---

## S3-T5 — API/Admin de personas, estudiantes y docentes

**Tareas**
- Crear serializers y ViewSets protegidos.
- Secretaría/Admin pueden crear y editar estudiantes.
- Admin/Coordinador pueden consultar docentes según permisos.
- Docente puede consultar su perfil.
- Estudiante puede consultar su perfil.

**Criterios de aceptación**
- Permisos por rol probados.
- No se exponen datos sensibles a roles no autorizados.

**Verificación**
```bash
pytest apps/people/tests/test_people_api.py
pytest apps/students/tests/test_students_api.py
pytest apps/teachers/tests/test_teachers_api.py
```

---

## S3-T6 — Importación controlada desde CSV

**Tareas**
- Crear comando o endpoint administrativo para importar personas/estudiantes/docentes desde CSV sintético.
- Validar columnas y errores por fila.
- No guardar archivos de importación en Git.
- Registrar auditoría de importación.

**Criterios de aceptación**
- Importación reporta creados, actualizados y rechazados.
- Errores no detienen toda la importación si se define modo tolerante.
- Auditoría registra responsable.

**Verificación**
```bash
pytest apps/people/tests/test_import_people.py
```

---

## Cierre del Sprint 3

- [ ] Person central implementado.
- [ ] Student y Teacher funcionales.
- [ ] Permisos probados.
- [ ] `docs/database-model.md` actualizado.
- [ ] Cursor a **Sprint 4 / S4-T1**.
