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
