# Gestion de silabos

Sprint 5 implementa el modulo `syllabus` para el MVP academico. La prioridad es
el silabo nueva version basado en resultados de aprendizaje; la version anterior
queda soportada como valor `legacy` para compatibilidad minima.

## Modelo principal

`Syllabus` pertenece a un `CourseSection` y mantiene un unico silabo activo por
curso. Los silabos archivados permiten conservar historial y crear una nueva
version activa del mismo curso.

Campos principales:

- `version`: `new` o `legacy`.
- `status`: `draft`, `in_review`, `approved`, `observed`, `finalized`,
  `archived`.
- `subject_description` y `methodology`.
- `lead_teacher` obligatorio y `co_teacher` opcional.
- Fechas de finalizacion, envio, aprobacion, carga de archivo y archivo.
- `signed_file` para PDF firmado/aprobado.

El docente titular debe estar asignado como titular del curso. El codocente, si
se registra, debe estar asignado como codocente del mismo curso.

## Componentes del silabo

- `SyllabusCompetency`: competencias transversales y disciplinares.
- `SyllabusLearningOutcome`: resultados de aprendizaje de carrera y asignatura.
- `SyllabusCriterion`: criterios de evaluacion asociados a RA de asignatura.
- `SyllabusAchievementLevel`: descriptores A, B, C y D por criterio.
- `SyllabusBibliography`: bibliografia basica, complementaria, recomendada o
  digital.
- `SyllabusWeeklyPlan`: planificacion semanal con experiencias de contacto
  docente, practico-experimentales y autonomas.

Reglas de completitud:

- Al menos 3 RA de carrera y 3 RA de asignatura.
- Cada RA de asignatura debe tener criterios.
- Los criterios por RA de asignatura deben sumar 100%.
- Cada criterio debe tener niveles A, B, C y D.
- Para finalizar se requiere descripcion, metodologia, competencias,
  bibliografia y planificacion semanal minima.

## Flujo de estados

El flujo operativo es:

```text
draft/observed -> finalized -> in_review -> approved
```

Acciones:

- `finalize`: valida completitud y deja el silabo finalizado.
- `submit`: envia el silabo finalizado a revision.
- `approve`: aprueba el silabo. El docente asignado no puede aprobar su propio
  silabo salvo rol institucional superior.
- `observe`: devuelve el silabo con observacion obligatoria.
- `reopen`: reabre con justificacion obligatoria.
- `upload-signed-file`: carga PDF firmado solo cuando el silabo esta aprobado.

Cada cambio de estado y carga de archivo registra auditoria en `AuditLog` con
modulo `syllabus`.

## Permisos

- Docente: crea, edita en borrador/observado, finaliza y envia sus cursos
  asignados.
- Coordinador de carrera: revisa y aprueba silabos de sus carreras.
- Secretaria, Administrador y Direccion academica: consulta, revision,
  aprobacion, reapertura y carga autorizada.
- Estudiante: consulta silabos de sus cursos matriculados.

La API valida permisos en backend; el frontend no debe depender solo de ocultar
controles.

## Archivos

La carga de silabo firmado acepta PDF y usa el storage configurado por Django.
En desarrollo se guarda bajo `MEDIA_ROOT`; en produccion debe usarse un storage
compatible con S3. El limite inicial se configura con:

```text
SYLLABUS_SIGNED_FILE_MAX_BYTES=5242880
```

`media/` esta excluido de Git.

## Relacion con notas

Sprint 5 deja preparado el contrato `is_syllabus_ready_for_grading(course)`.
Sprint 6 debe usarlo para bloquear la creacion o apertura del gradebook cuando
el curso requiera silabo nueva version y no exista un silabo aprobado.
