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
