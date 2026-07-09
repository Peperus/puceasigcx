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

- Una persona puede estar asociada opcionalmente a un usuario mediante
  `Person.user`.
- Una persona puede tener perfil de estudiante, docente o ambos si aplica institucionalmente.

Implementado en Sprint 3:

- `identification_number` es unico cuando esta presente.
- La busqueda administrativa cubre identificacion, nombres y correos.
- El registro permite personas sin identificacion inicial para casos
  controlados de carga o regularizacion.

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

Periodo academico con fechas de matricula.

Campos implementados en Sprint 2:

- `name`
- `code`, unico
- `start_date`
- `end_date`
- `enrollment_start_date`
- `enrollment_end_date`
- `status`: borrador, activo, cerrado, archivado
- `is_current`

Reglas:

- Solo un periodo puede marcarse como actual.
- Periodos activos no pueden solaparse en fechas.
- Las fechas de matricula deben estar dentro del periodo.

### Career

Carrera institucional. Se vincula con unidad academica, modalidad, dominio y,
si aplica, usuario coordinador.

Entidades de soporte implementadas:

- `FacultyOrUnit`
- `Modality`
- `AcademicDomain`

Reglas:

- Codigos unicos para unidad, modalidad, dominio y carrera.

### StudyPlan

Plan o malla academica asociado a una carrera.

Campos implementados:

- `career`
- `code`
- `name`
- `version`
- `effective_from`
- `effective_to`
- `is_current`
- `status`

Reglas:

- El codigo no se duplica dentro de la misma carrera.
- Solo un plan puede estar marcado como vigente por carrera.

### AcademicLevel

Nivel, semestre o ciclo dentro de un plan.

Reglas:

- Un plan puede tener multiples niveles.
- `number` y `order` no se duplican dentro del mismo plan.

### Subject

Asignatura asociada a carrera, plan y nivel. Define horas, prerrequisitos, silabo por defecto y sistema de calificacion por defecto.

En Sprint 2 la asignatura se define como catalogo de carrera y se asocia a plan
y nivel mediante `CurriculumSubject`.

Campos implementados:

- `career`
- `code`
- `name`
- `total_hours`
- `contact_hours`
- `autonomous_hours`
- `practical_hours`
- `default_syllabus_version`
- `default_grading_system`
- `status`

Reglas:

- El codigo de asignatura no se duplica dentro de la misma carrera.
- La suma de horas contacto, autonomas y practico-experimentales debe coincidir
  con las horas totales.

### CurriculumSubject

Relaciona una asignatura con un plan y nivel de la malla curricular.

Reglas:

- El nivel debe pertenecer al mismo plan.
- La asignatura debe pertenecer a la carrera del plan.
- Una asignatura no se duplica dentro del mismo plan.

### CurriculumPrerequisite

Relacion explicita de prerrequisitos entre asignaturas de malla.

Reglas:

- El prerrequisito debe pertenecer al mismo plan.
- No se permite una asignatura como prerrequisito de si misma.
- No se permiten ciclos simples A -> B y B -> A.

### AcademicSetting

Configuracion academica de escala de calificacion por defecto, periodo y/o
carrera.

Campos implementados:

- `score_min`
- `score_max`
- `passing_score`
- `default_grading_system`
- `is_default`

Reglas:

- La escala base del MVP es 0 a 50.
- El umbral de aprobacion base es 30.
- La configuracion efectiva se consulta por servicio con prioridad
  periodo+carrera, carrera, periodo y valor global.

### AchievementLevel

Niveles de logro configurables por `AcademicSetting`.

Configuracion base:

- A: 45 a 50.
- B: 40 a 44.99.
- C: 30 a 39.99.
- D: 0 a 29.99.

### AcademicOffer

Oferta academica abierta por periodo, carrera, plan y nivel.

Relaciones:

- Pertenece a un periodo.
- Pertenece a una carrera.
- Pertenece a un plan de estudio.
- Pertenece a un nivel academico.

Implementado en Sprint 4:

- Estados: borrador, publicada, cerrada, archivada.
- No se duplica una oferta para el mismo periodo, carrera, plan y nivel.

### CourseSection

Curso/paralelo abierto dentro de una oferta academica.

Relaciones:

- Pertenece a una oferta academica.
- Pertenece a una asignatura.
- Tiene paralelo, cupo, modalidad, aula, estado y sistema de calificacion S1/S2/S3.

Implementado en Sprint 4:

- Estados: planificado, activo, cerrado, cancelado.
- No se duplica un paralelo para la misma oferta y asignatura.
- El sistema de calificacion debe estar activo.
- Solo cursos activos aceptan matriculas con cupo disponible.

### TeachingAssignment

Asignacion de docente a curso.

Roles sugeridos:

- Titular.
- Codocente.
- Invitado.

Implementado en Sprint 4:

- Roles: titular y codocente.
- El docente debe estar activo.
- Solo puede existir un docente titular activo por curso.

## Estudiantes y matricula

### Student

Perfil academico de una persona como estudiante.

Campos implementados en Sprint 3:

- `person`
- `career`
- `study_plan`
- `admission_period`
- `student_code`
- `status`
- `admission_date`
- `observations`

Estados:

- `aspirante_convertido`
- `activo`
- `retirado`
- `egresado`
- `graduado`
- `suspendido`
- `archivado`

Reglas:

- Una persona tiene como maximo un perfil de estudiante.
- `student_code` es unico.
- El plan de estudio debe pertenecer a la carrera principal.

### Enrollment

Matricula del estudiante en un periodo academico.

Implementado en Sprint 4:

- Relaciona estudiante, periodo, carrera y plan.
- No se duplica una matricula del mismo estudiante en el mismo periodo.
- Estados: matriculado, retirado, aprobado, reprobado, homologado y anulado.

### CourseEnrollment

Matricula del estudiante en un curso/paralelo especifico.

Estados sugeridos:

- Matriculado.
- Retirado.
- Anulado.
- Aprobado.
- Reprobado.
- En recuperacion.

Implementado en Sprint 4:

- No se duplica la matricula del mismo estudiante en el mismo curso.
- Valida periodo, carrera y plan contra la oferta del curso.
- Respeta cupo en cursos activos.

### Homologation

Registro minimo de homologaciones o equivalencias.

Implementado en Sprint 4:

- Relaciona estudiante, asignatura, periodo, resolucion/observacion y estado.
- No afecta notas automaticamente hasta el sprint de grading.
- Registra auditoria cuando se crea o actualiza desde servicio/API.

## Docentes

### Teacher

Perfil academico de una persona como docente.

Campos implementados en Sprint 3:

- `person`
- `teacher_code`
- `academic_degree`
- `professional_title`
- `academic_bio`
- `institutional_phone`
- `status`
- `domains`

Estados:

- `activo`
- `inactivo`
- `invitado`
- `codocente`
- `externo`

Reglas:

- Una persona tiene como maximo un perfil docente.
- `teacher_code` es unico.
- El perfil guarda datos base usados por silabos.

### TeacherOfficeHour

Horario de tutoria presencial o virtual.

Campos implementados:

- `teacher`
- `modality`: presencial o virtual.
- `day_of_week`
- `start_time`
- `end_time`
- `location_or_link`

Regla:

- `start_time` debe ser menor que `end_time`.

## Silabos

### Syllabus

Silabo asociado a un curso/paralelo.

Implementado en Sprint 5:

- `course_section`
- `version`: `new` o `legacy`
- `status`: borrador, en revision, aprobado, observado, finalizado o archivado
- `subject_description`
- `methodology`
- `lead_teacher`
- `co_teacher`
- `signed_file`
- `created_by`
- `finalized_at`
- `submitted_at`
- `approved_at`
- `approved_by`
- `signed_file_uploaded_by`
- `signed_file_uploaded_at`
- `archived_at`

Versiones:

- Nueva version.
- Legacy o antigua.

Reglas:

- Un curso puede tener un solo silabo activo; los archivados conservan historial.
- El docente titular debe estar asignado como titular del curso.
- El codocente debe estar asignado como codocente del curso.
- El silabo aprobado se considera listo para habilitar notas en Sprint 6.

### SyllabusCompetency

Competencia transversal o disciplinar.

Implementado con tipo, texto y orden.

### LearningOutcome

Resultado de aprendizaje de carrera o asignatura.

Implementado como `SyllabusLearningOutcome`, con minimo funcional de 3 RA de
carrera y 3 RA de asignatura antes de rubricas/finalizacion.

### EvaluationCriterion

Criterio de evaluacion asociado a un resultado de aprendizaje.

Implementado como `SyllabusCriterion`, con ponderacion 0.01 a 100.00 y
validacion de suma 100 por RA de asignatura.

### AchievementLevel

Descripcion de niveles A, B, C y D.

Implementado como `SyllabusAchievementLevel`, obligatorio A/B/C/D por criterio.

### SyllabusBibliography

Bibliografia basica, complementaria, recomendada o digital.

Implementado con referencia APA, codigo de biblioteca opcional, cantidad de
ejemplares y orden.

### WeeklyPlan

Planificacion semanal con estrategias, horas, recursos, escenarios y dimension del conocimiento.

Implementado como `SyllabusWeeklyPlan`, vinculado a RA de asignatura/carrera y
con experiencias de contacto docente, practico-experimentales y autonomas.

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
