# Modelo de datos inicial

Este documento resume las entidades principales del MVP. El detalle puede evolucionar durante los sprints, pero debe conservar la separacion de dominios y evitar duplicacion de datos.

## Personas y usuarios

### Person

Representa a una persona natural, sin importar si es estudiante, docente o administrativo.

Campos sugeridos:

- `first_name`
- `last_name`
- `identification_type`
- `identification_number`
- `institutional_email`
- `personal_email`
- `phone`
- `birth_date`
- `address`
- `is_active`
- `created_at`
- `updated_at`

Relaciones:

- Una persona puede estar asociada a un usuario.
- Una persona puede tener perfil de estudiante, docente o ambos si aplica institucionalmente.

### UserProfile

Extiende el usuario de autenticacion.

Campos sugeridos:

- `user`
- `person`
- `primary_role`
- `assigned_careers`
- `must_change_password`
- `is_active`

### Role

Define roles institucionales.

Campos sugeridos:

- `name`
- `code`
- `description`
- `is_system_role`

## Catalogos academicos

### AcademicPeriod

Periodo academico con fechas de matricula y calificacion.

### Career

Carrera institucional. Puede tener coordinador y modalidad.

### StudyPlan

Plan o malla academica asociado a una carrera.

### AcademicLevel

Nivel, semestre o ciclo dentro de un plan.

### Subject

Asignatura asociada a carrera, plan y nivel. Define horas, prerrequisitos, silabo por defecto y sistema de calificacion por defecto.

### CourseOffering

Curso/paralelo abierto en un periodo.

Relaciones:

- Pertenece a un periodo.
- Pertenece a una carrera y asignatura.
- Tiene paralelo, cupo, aula y estado.

### TeachingAssignment

Asignacion de docente a curso.

Roles sugeridos:

- Titular.
- Codocente.
- Invitado.

## Estudiantes y matricula

### Student

Perfil academico de una persona como estudiante.

Campos sugeridos:

- `person`
- `career`
- `study_plan`
- `admission_period`
- `student_code`
- `status`

### Enrollment

Matricula del estudiante en un periodo academico.

### CourseEnrollment

Matricula del estudiante en un curso/paralelo especifico.

Estados sugeridos:

- Matriculado.
- Retirado.
- Anulado.
- Aprobado.
- Reprobado.
- En recuperacion.

## Docentes

### Teacher

Perfil academico de una persona como docente.

Campos sugeridos:

- `person`
- `teacher_code`
- `academic_degree`
- `professional_title`
- `academic_bio`
- `institutional_phone`
- `status`

### TeacherOfficeHour

Horario de tutoria presencial o virtual.

## Silabos

### Syllabus

Silabo asociado a un curso/paralelo.

Campos sugeridos:

- `course_offering`
- `version`
- `status`
- `domain`
- `subject_description`
- `methodology`
- `signed_file`
- `created_by`
- `submitted_at`
- `approved_at`
- `closed_at`

Versiones:

- Nueva version.
- Legacy o antigua.

### SyllabusCompetency

Competencia transversal o disciplinar.

### LearningOutcome

Resultado de aprendizaje de carrera o asignatura.

### EvaluationCriterion

Criterio de evaluacion asociado a un resultado de aprendizaje.

### AchievementLevel

Descripcion de niveles A, B, C y D.

### SyllabusBibliography

Bibliografia basica, complementaria, recomendada o digital.

### WeeklyPlan

Planificacion semanal con estrategias, horas, recursos, escenarios y dimension del conocimiento.

## Notas

### GradingSystem

Sistema de calificacion: S1, S2 o S3.

### Gradebook

Acta o libro de notas por curso.

Estados sugeridos:

- Borrador.
- Abierto.
- Enviado.
- Observado.
- Cerrado.
- Reabierto por autorizacion.
- Archivado.

### GradeLearningOutcome

Resultado de aprendizaje dentro de un gradebook S1/S2.

### GradeCriterion

Criterio ponderado de un resultado de aprendizaje.

### GradeActivity

Actividad calificable dentro de un criterio.

### StudentGradeActivity

Nota de un estudiante para una actividad.

### StudentLearningOutcomeResult

Resultado calculado por estudiante y resultado de aprendizaje.

### StudentCourseGrade

Resultado final del estudiante en el curso.

### RecoveryAttempt

Intento de recuperacion asociado a estudiante, gradebook y resultado de aprendizaje.

### LegacyPartial

Parcial del modelo S3.

### LegacyPartialActivity

Actividad practica ponderada de un parcial S3.

### StudentLegacyPartialGrade

Nota practica, evaluacion y resultado de parcial S3.

### LegacyFinalEvaluation

Cuarta evaluacion o evaluacion final cuando aplique en S3.

## Auditoria

### AuditLog

Registra acciones criticas.

Campos sugeridos:

- `user`
- `action`
- `module`
- `model_name`
- `object_id`
- `previous_data`
- `new_data`
- `reason`
- `ip_address`
- `user_agent`
- `created_at`

## Relaciones clave

- `Person` es la entidad central de identidad humana.
- `UserProfile` conecta autenticacion con persona y roles.
- `Student` y `Teacher` referencian a `Person`.
- `CourseOffering` conecta periodo, carrera, asignatura, nivel y paralelo.
- `TeachingAssignment` conecta docentes con cursos.
- `Enrollment` y `CourseEnrollment` conectan estudiantes con periodos y cursos.
- `Syllabus` y `Gradebook` pertenecen a un `CourseOffering`.
- `Gradebook` usa un `GradingSystem`.
- `AuditLog` referencia acciones sobre objetos criticos.
