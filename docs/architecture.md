# Arquitectura tecnica

PUCEASIG se construye como una plataforma modular con backend Django + DRF, base PostgreSQL, frontend Next.js y almacenamiento de archivos compatible con S3.

## Vista general

```text
Frontend Next.js
       |
       | HTTPS / JSON API
       v
Django REST Framework
       |
       +-- PostgreSQL
       +-- Redis
       +-- S3 compatible storage
       +-- Django Admin
```

## Backend

El backend sera un proyecto Django dentro de `backend/`, con apps separadas por dominio.

Apps iniciales previstas:

- `core`: base comun, healthcheck, utilidades y modelos abstractos.
- `accounts`: usuarios, perfiles, roles y permisos.
- `academic_catalogs`: periodos, carreras, planes, niveles y asignaturas.
- `people`: persona central y datos personales.
- `students`: estudiantes y trayectoria academica.
- `teachers`: docentes, perfiles academicos y horarios.
- `enrollment`: oferta academica, matriculas y cursos.
- `syllabus`: silabos, competencias, resultados y planificacion.
- `grading`: modelos S1, S2, S3, notas y recuperaciones.
- `documents`: archivos academicos y almacenamiento externo.
- `reports`: reportes y exportaciones.
- `audit`: bitacora de acciones criticas.

La logica de negocio debe vivir en servicios de dominio, no directamente en views. Las consultas reutilizables o complejas deben ubicarse en selectors.

## API

La API sera REST y versionable. Los endpoints minimos sugeridos se definiran por modulo bajo `/api/`.

Principios:

- Serializers validan estructura y reglas de entrada.
- Views validan autenticacion y permisos.
- Services aplican reglas de negocio transaccionales.
- Selectors concentran consultas reutilizables.
- Tests cubren reglas criticas y permisos.

## Base de datos

PostgreSQL es la base principal. Debe configurarse por variables de entorno y usarse desde Docker Compose a partir de S0-T3.

Lineamientos:

- Migraciones versionadas.
- Restricciones de unicidad en codigos institucionales.
- Indices para busquedas por periodo, carrera, curso, estudiante y docente.
- Relaciones explicitas entre persona, usuario, estudiante y docente.
- Auditoria para cambios criticos.

## Archivos

Los archivos cargados no deben guardarse en Git. El sistema usara almacenamiento compatible con S3 para:

- Silabos firmados.
- Reportes generados.
- Adjuntos academicos.
- Documentos institucionales futuros.

En desarrollo se podra usar un backend local o MinIO, segun se defina en tickets posteriores.

## Frontend

El MVP usara Next.js + TypeScript + Tailwind CSS, definido formalmente en Sprint 0.5 antes de construir pantallas funcionales.

El frontend debe consumir la API REST, reutilizar componentes centralizados y respetar validaciones de accesibilidad basica. Ocultar controles por rol no reemplaza permisos backend.

## Administracion auxiliar

Django Admin sera una herramienta interna para soporte, carga inicial y administracion tecnica. No sera el frontend principal del MVP.

## Entornos

Entornos previstos:

- `local`: desarrollo en maquina local.
- `test`: ejecucion automatizada de pruebas.
- `production`: despliegue piloto o productivo.

La configuracion sensible debe venir de variables de entorno: `SECRET_KEY`, `DATABASE_URL`, `REDIS_URL`, origenes CORS, credenciales S3 y parametros de seguridad.

## Observabilidad inicial

- Healthcheck publico: `/api/health/`.
- Logging basico por entorno.
- Auditoria de acciones academicas criticas.
- Reportes de errores por configurar en fases posteriores.
