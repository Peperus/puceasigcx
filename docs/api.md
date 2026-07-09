# API PUCEASIG

Base local: `/api/`.

La API usa JWT y valida permisos en backend. Los endpoints de catalogos
academicos requieren autenticacion.

## Autenticacion

| Metodo | Endpoint | Acceso | Descripcion |
|---|---|---|---|
| POST | `/api/auth/login/` | Publico | Obtiene `access`, `refresh` y datos de sesion. |
| POST | `/api/auth/refresh/` | Publico | Renueva el token de acceso. |
| POST | `/api/auth/logout/` | Autenticado | Invalida un refresh token. |
| POST | `/api/auth/password/reset/` | Publico | Solicita recuperacion de contrasena sin revelar cuentas. |
| POST | `/api/auth/password/reset/confirm/` | Publico | Confirma token y cambia contrasena. |
| GET/PATCH | `/api/me/` | Autenticado | Consulta o actualiza campos permitidos del perfil actual. |

## Catalogos Academicos

Permisos:

- Administrador y Secretaria: CRUD.
- Coordinador de carrera: lectura de catalogos vinculados a sus carreras cuando
  aplica; lectura global para catalogos institucionales.
- Direccion academica: lectura.
- Docente y Estudiante: sin acceso a estos endpoints en Sprint 2.

| Metodo | Endpoint | Recurso |
|---|---|---|
| GET/POST | `/api/academic/periods/` | Periodos academicos. |
| GET/PATCH/DELETE | `/api/academic/periods/{id}/` | Periodo academico. |
| GET/POST | `/api/academic/faculties/` | Unidades academicas. |
| GET/POST | `/api/academic/modalities/` | Modalidades. |
| GET/POST | `/api/academic/domains/` | Dominios academicos. |
| GET/POST | `/api/academic/careers/` | Carreras. |
| GET/POST | `/api/academic/study-plans/` | Planes de estudio. |
| GET/POST | `/api/academic/levels/` | Niveles academicos. |
| GET/POST | `/api/academic/grading-systems/` | Catalogo S1/S2/S3. |
| GET/POST | `/api/academic/subjects/` | Asignaturas. |
| GET/POST | `/api/academic/curriculum-subjects/` | Asignaturas dentro de malla. |
| GET/POST | `/api/academic/curriculum-prerequisites/` | Prerrequisitos de malla. |
| GET/POST | `/api/academic/settings/` | Configuracion academica de escala. |
| GET/POST | `/api/academic/achievement-levels/` | Niveles A/B/C/D. |

Las operaciones `PATCH`, `PUT` y `DELETE` se exponen en la ruta de detalle de
cada recurso y mantienen la misma politica de permisos.

## Personas, Estudiantes y Docentes

Permisos:

- Administrador y Secretaria: crean y editan personas, estudiantes y docentes.
- Coordinador de carrera y Direccion academica: consulta segun alcance
  academico disponible.
- Docente: consulta su propio perfil de persona/docente.
- Estudiante: consulta su propio perfil de persona/estudiante.
- Docente no consulta listados de estudiantes hasta existir alcance por curso en
  Sprint 4.

| Metodo | Endpoint | Recurso |
|---|---|---|
| GET/POST | `/api/people/` | Personas. |
| GET/PATCH/DELETE | `/api/people/{id}/` | Persona. |
| GET/POST | `/api/students/` | Estudiantes. |
| GET/PATCH/DELETE | `/api/students/{id}/` | Estudiante. |
| GET/POST | `/api/teachers/` | Docentes. |
| GET/PATCH/DELETE | `/api/teachers/{id}/` | Docente. |
| GET/POST | `/api/teachers/office-hours/` | Horarios de atencion docente. |
| GET/PATCH/DELETE | `/api/teachers/office-hours/{id}/` | Horario de atencion docente. |

Importacion administrativa:

```bash
python backend/manage.py import_people_csv ruta/al/archivo.csv --user-email admin@example.edu
```

El CSV debe ser sintetico, no debe guardarse en Git y reporta creados,
actualizados y rechazados. La importacion registra auditoria con accion
`people_imported`.

## Oferta Academica y Matriculas

Permisos:

- Administrador y Secretaria: CRUD completo de oferta, cursos, asignaciones,
  matriculas en periodo, matriculas en curso y homologaciones.
- Coordinador de carrera: gestiona oferta, cursos y asignaciones de sus
  carreras; consulta matriculas y homologaciones de sus carreras.
- Docente: consulta solo los cursos/paralelos asignados y sus estudiantes
  matriculados.
- Estudiante: consulta solo sus cursos matriculados y homologaciones propias.

| Metodo | Endpoint | Recurso |
|---|---|---|
| GET/POST | `/api/enrollment/academic-offers/` | Oferta academica por periodo, carrera, plan y nivel. |
| GET/PATCH/DELETE | `/api/enrollment/academic-offers/{id}/` | Oferta academica. |
| GET/POST | `/api/enrollment/course-sections/` | Cursos/paralelos por oferta y asignatura. |
| GET/PATCH/DELETE | `/api/enrollment/course-sections/{id}/` | Curso/paralelo. |
| GET/POST | `/api/enrollment/teaching-assignments/` | Asignaciones docentes. |
| GET/PATCH/DELETE | `/api/enrollment/teaching-assignments/{id}/` | Asignacion docente. |
| GET/POST | `/api/enrollment/enrollments/` | Matricula academica de estudiante en periodo. |
| GET/PATCH/DELETE | `/api/enrollment/enrollments/{id}/` | Matricula academica. |
| GET/POST | `/api/enrollment/course-enrollments/` | Inscripcion de estudiante en curso/paralelo. |
| GET/PATCH/DELETE | `/api/enrollment/course-enrollments/{id}/` | Matricula en curso. |
| GET/POST | `/api/enrollment/homologations/` | Homologaciones o equivalencias basicas. |
| GET/PATCH/DELETE | `/api/enrollment/homologations/{id}/` | Homologacion. |

Reglas principales:

- No se duplica una oferta para el mismo periodo, carrera, plan y nivel.
- No se duplica un paralelo para la misma oferta y asignatura.
- Un curso activo respeta cupo al matricular estudiantes.
- La API no permite matricular en cursos cerrados, cancelados o planificados.
- Matriculas, inscripciones en curso y homologaciones registran auditoria.

## Dashboard Academico Minimo

| Metodo | Endpoint | Acceso | Descripcion |
|---|---|---|---|
| GET | `/api/academic/dashboard/` | Administrador, Secretaria, Coordinador | Conteos por periodo de estudiantes, docentes, cursos y matriculas. |
| GET | `/api/reports/academic-dashboard/` | Administrador, Secretaria, Coordinador | Alias de reportes para el mismo dashboard. |

El parametro opcional `period` acepta `id` o `code`. Si no se envia, se usa el
periodo actual y, si no existe, el periodo mas reciente.

## Silabos

Permisos:

- Administrador, Secretaria y Direccion academica: consulta, revision,
  aprobacion, reapertura y carga autorizada.
- Coordinador de carrera: consulta y aprueba silabos de sus carreras.
- Docente: crea, edita en borrador/observado, finaliza y envia silabos de sus
  cursos asignados.
- Estudiante: consulta silabos de sus cursos matriculados.

| Metodo | Endpoint | Recurso |
|---|---|---|
| GET/POST | `/api/syllabi/` | Silabos por curso/paralelo. |
| GET/PATCH/DELETE | `/api/syllabi/{id}/` | Silabo. |
| POST | `/api/syllabi/{id}/finalize/` | Finaliza silabo con validacion de completitud. |
| POST | `/api/syllabi/{id}/submit/` | Envia silabo finalizado a revision. |
| POST | `/api/syllabi/{id}/approve/` | Aprueba silabo en revision. |
| POST | `/api/syllabi/{id}/observe/` | Devuelve silabo con observacion obligatoria. |
| POST | `/api/syllabi/{id}/reopen/` | Reabre silabo con justificacion obligatoria. |
| POST | `/api/syllabi/{id}/upload-signed-file/` | Carga PDF firmado/aprobado. |
| GET | `/api/syllabi/{id}/printable/` | Vista HTML imprimible del silabo. |
| GET/POST | `/api/syllabi/competencies/` | Competencias transversales y disciplinares. |
| GET/POST | `/api/syllabi/learning-outcomes/` | Resultados de aprendizaje de carrera/asignatura. |
| GET/POST | `/api/syllabi/criteria/` | Criterios de evaluacion ponderados. |
| GET/POST | `/api/syllabi/achievement-levels/` | Descriptores A/B/C/D por criterio. |
| GET/POST | `/api/syllabi/bibliography/` | Bibliografia del silabo. |
| GET/POST | `/api/syllabi/weekly-plans/` | Planificacion semanal. |

Reglas principales:

- Solo existe un silabo activo por curso; silabos archivados conservan historial.
- Para finalizar se requieren 3 RA de carrera, 3 RA de asignatura, criterios
  con pesos por RA que sumen 100, niveles A/B/C/D, bibliografia y planificacion.
- El silabo aprobado bloquea edicion general; reapertura exige justificacion.
- La carga de archivo acepta PDF y registra usuario/fecha de carga.
- Cambios de estado y carga de archivo registran auditoria.
