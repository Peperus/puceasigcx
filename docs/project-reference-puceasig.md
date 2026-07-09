# Project Reference — PUCE Amazonas SIG Académico

## 1. Identificación del proyecto

**Nombre técnico sugerido:** PUCEASIG — Sistema Académico Integral para PUCE Amazonas  
**Nombre funcional:** Sistema ERP/SIG Académico PUCE Amazonas  
**Institución:** Pontificia Universidad Católica del Ecuador — Sede Amazonas  
**Ubicación:** Sucumbíos, Ecuador  
**Año de referencia:** 2026  
**Tipo de proyecto:** Plataforma institucional de gestión académica y administrativa, con desarrollo incremental por módulos.  
**Sistema de referencia:** SIG / SIGUEME actualmente utilizado por PUCE Amazonas.  
**MVP solicitado:** Gestión Académica.  
**Backend recomendado:** Django + Django REST Framework.  
**Base de datos recomendada:** PostgreSQL.  
**Frontend del MVP:** Next.js + TypeScript + Tailwind CSS, definido desde el Sprint 0.5. Django Admin queda como herramienta interna auxiliar para administración y soporte, no como frontend principal del MVP.  
**Almacenamiento de archivos:** Compatible con S3, por ejemplo Cloudflare R2, AWS S3 o MinIO.  
**Integraciones futuras:** Moodle, Google Drive/Workspace, correo institucional, analítica institucional y sistemas de autenticación institucional.

---

## 2. Propósito general

El proyecto busca desarrollar un sistema ERP/SIG académico para PUCE Amazonas que replique, ordene y mejore las funciones esenciales del sistema institucional actual, priorizando inicialmente el núcleo de **Gestión Académica**: estudiantes, docentes, sílabos, notas, roles, periodos, carreras, asignaturas, cursos/paralelos, matrículas, auditoría, reportes y archivos.

El sistema debe permitir administrar la trayectoria académica del estudiante, la asignación docente, la creación y aprobación de sílabos, el registro de calificaciones bajo tres modelos de evaluación vigentes, la consulta transparente de notas por parte del estudiante y el control de acceso según roles institucionales.

El desarrollo debe ser incremental. El MVP no debe intentar construir todo el SIG institucional desde el inicio. Primero debe consolidar una base académica sólida, segura, auditable y extensible; luego se podrán incorporar admisiones, bienestar, biblioteca, requerimientos, mensajería, gestión documental, Moodle, tableros e inventario.

---

## 3. Sistema actual analizado

Los documentos analizados muestran que el sistema actual integra procesos académicos y no académicos bajo un enfoque de trazabilidad institucional. El alcance general identificado incluye:

1. Configuración institucional y planeación.
2. Admisiones y captación.
3. Gestión académica.
4. Enseñanza, evaluación e integración con Moodle.
5. Bienestar universitario.
6. Biblioteca y repositorio académico.
7. Mensajería institucional.
8. Gestión documental.
9. Comunidad, participación y PQR/PQRSD.
10. Inventario y activos.
11. Identidad, seguridad y acceso.
12. Analítica y tableros.

El sistema se apoya en datos maestros compartidos: persona, usuario, carrera, semestre, asignatura, curso, paralelo y periodo académico. Estos datos deben diseñarse cuidadosamente porque serán la base de todos los módulos futuros.

---

## 4. Problema central

PUCE Amazonas requiere una plataforma académica propia, mantenible y escalable que permita replicar y mejorar las funciones críticas del sistema actual, reduciendo dependencia técnica, mejorando la trazabilidad de procesos, ordenando los modelos de calificación, fortaleciendo la seguridad por roles y facilitando la evolución hacia un ERP institucional completo.

El problema no es solo construir pantallas similares al sistema existente. El reto principal es diseñar una arquitectura limpia que soporte múltiples periodos, carreras, mallas, asignaturas, paralelos, docentes, estudiantes, modelos de sílabos, sistemas de notas y reportes institucionales sin duplicar datos ni generar inconsistencias.

---

## 5. Principios de diseño del sistema

1. **Trazabilidad académica completa:** cada acción relevante debe indicar responsable, fecha, estado y origen.
2. **Datos maestros únicos:** persona, usuario, carrera, asignatura, periodo, curso y matrícula no deben duplicarse.
3. **Control de acceso por roles:** ningún usuario debe ver o modificar información fuera de sus permisos.
4. **Configuración antes que hardcoding:** periodos, ponderaciones, criterios, umbrales, modelos de nota y reglas deben ser configurables.
5. **Auditoría obligatoria:** cambios de notas, sílabos, matrículas, usuarios y roles deben dejar registro.
6. **Separación de dominios:** estudiantes, docentes, sílabos, notas, roles, archivos y reportes deben ser módulos separados pero integrados.
7. **Compatibilidad con modelos actuales:** el MVP debe soportar los tres sistemas de notas identificados en los archivos Excel.
8. **Preparación para integración:** la arquitectura debe dejar lista la API para Moodle, dashboards, frontend Next.js y futuros servicios institucionales.
9. **Seguridad institucional:** no deben almacenarse credenciales reales en el repositorio ni en prompts de Codex.
10. **Desarrollo incremental:** cada fase debe dejar entregables ejecutables, probables y documentados.

---

## 6. Alcance total del ERP/SIG institucional

### 6.1 Configuración institucional y planeación

Debe permitir configurar:

- Institución y sede.
- Periodos académicos.
- Fechas de matrícula.
- Fechas de evaluación.
- Carreras.
- Dominios académicos.
- Planes de estudio.
- Mallas curriculares.
- Semestres o niveles.
- Asignaturas.
- Paralelos.
- Aulas o espacios.
- Oferta académica por periodo.
- Usuarios administrativos.
- Parámetros institucionales.

### 6.2 Admisiones y captación

Debe permitir en fases posteriores:

- Preinscripción de aspirantes.
- Reserva de cupos para examen o proceso de ingreso.
- Validación de requisitos.
- Citas con psicología o bienestar.
- Registro socioeconómico y vulnerabilidad.
- Cálculo de posibles becas según criterios institucionales.
- Conversión de aspirante en estudiante.
- Matrícula inicial.
- Generación de identificador o QR para carnet.

### 6.3 Gestión académica

Es el núcleo del MVP. Debe permitir:

- Gestionar estudiantes.
- Gestionar docentes.
- Gestionar carreras, niveles, asignaturas, cursos y paralelos.
- Vincular docentes con cursos/paralelos.
- Matricular estudiantes en cursos.
- Crear, revisar, aprobar, descargar y cargar sílabos.
- Registrar notas bajo modelos vigentes.
- Consultar notas en tiempo real según permisos.
- Generar reportes académicos.

### 6.4 Enseñanza, evaluación y Moodle

Debe considerarse como fase posterior al MVP. Debe permitir:

- Sincronizar usuarios con Moodle.
- Sincronizar cursos y matrículas.
- Recuperar intentos, notas o actividades.
- Mapear actividades Moodle contra criterios o resultados de aprendizaje.
- Calcular resultados de aprendizaje.
- Generar equivalencias por letras y niveles de logro.

### 6.5 Bienestar universitario

Debe permitir en fases posteriores:

- Consultar información académica de estudiantes.
- Consultar vulnerabilidad o información socioeconómica autorizada.
- Registrar seguimientos.
- Gestionar solicitudes de recursos institucionales.
- Registrar uso de villa, transporte u otros servicios.

### 6.6 Biblioteca y repositorio académico

Debe permitir en fases posteriores:

- Crear categorías, subcategorías y clasificaciones.
- Registrar libros físicos o digitales.
- Vincular bibliografía a asignaturas y sílabos.
- Registrar consultas, préstamos y lecturas.
- Gestionar tesis o repositorio institucional.
- Permitir búsqueda y lectura según permisos.

### 6.7 Mensajería y gestión documental

Debe permitir en fases posteriores:

- Registrar comunicaciones externas.
- Gestionar flujo de revisión institucional.
- Asignar delegados responsables.
- Adjuntar documentos.
- Archivar documentos en almacenamiento externo.
- Consultar documentos por perfil y permisos.

### 6.8 Comunidad, participación y PQR/PQRSD

Debe permitir en fases posteriores:

- Crear solicitudes, peticiones, quejas, reclamos o sugerencias.
- Consultar estado mediante código único.
- Gestionar fases de atención.
- Asignar responsables.
- Registrar respuestas institucionales.
- Adjuntar evidencias.

### 6.9 Inventario y activos

Debe permitir en fases posteriores:

- Gestionar bienes.
- Registrar ubicación física.
- Registrar estado, daños y movimientos.
- Generar reportes.
- Asociar activos a áreas, aulas o responsables.

### 6.10 Analítica y tableros

Debe permitir:

- Dashboard académico.
- Dashboard de admisiones.
- Dashboard de notas y resultados de aprendizaje.
- Dashboard de asistencia.
- Dashboard de bienestar.
- Dashboard de biblioteca.
- Dashboard de PQR/PQRSD.
- Exportaciones institucionales.

---

## 7. Alcance del MVP — Gestión Académica

El MVP debe enfocarse en módulos estrictamente necesarios para operar la gestión académica inicial.

### 7.1 Módulo de gestión de estudiantes

Debe permitir:

- Crear, editar, consultar y desactivar estudiantes.
- Registrar datos personales básicos.
- Registrar documento de identidad.
- Registrar correo institucional.
- Registrar carrera, periodo de ingreso y estado académico.
- Asociar estudiante a matrícula académica.
- Consultar cursos matriculados.
- Consultar notas y resultados de aprendizaje.
- Consultar sílabos disponibles.
- Exportar listados por carrera, periodo, semestre y paralelo.

Estados sugeridos del estudiante:

- Aspirante.
- Activo.
- Matriculado.
- Retirado.
- Egresado.
- Graduado.
- Inactivo.
- Suspendido.

### 7.2 Módulo de gestión de docentes

Debe permitir:

- Crear, editar, consultar y desactivar docentes.
- Registrar datos personales básicos.
- Registrar correo institucional.
- Registrar grado académico y título profesional.
- Registrar breve reseña académica o profesional.
- Registrar horario de tutoría presencial y virtual.
- Asignar docentes a cursos/paralelos.
- Distinguir docente titular y codocente.
- Consultar asignaturas asignadas.
- Crear y cargar sílabos.
- Registrar calificaciones.
- Registrar inasistencias en fases posteriores.

Estados sugeridos del docente:

- Activo.
- Inactivo.
- Invitado.
- Codocente.
- Externo.

### 7.3 Módulo de gestión de sílabos

Debe soportar dos versiones:

1. Sílabo nueva versión basado en resultados de aprendizaje.
2. Sílabo anterior o antiguo basado en componentes de práctica y evaluación.

El módulo debe permitir:

- Listar asignaturas asignadas al docente.
- Crear sílabo por curso/paralelo.
- Guardar avances por pestañas o secciones.
- Validar campos obligatorios.
- Registrar datos informativos de la asignatura.
- Registrar docente titular y codocente.
- Registrar descripción de la asignatura.
- Registrar competencias transversales.
- Registrar competencias disciplinares del dominio.
- Registrar resultados de aprendizaje de la carrera.
- Registrar resultados de aprendizaje de la asignatura.
- Registrar criterios de evaluación por resultado de aprendizaje.
- Registrar niveles de logro A, B, C y D.
- Registrar metodología.
- Asignar pesos de criterios.
- Registrar bibliografía básica, complementaria, recomendada y digital.
- Registrar planificación semanal.
- Registrar experiencias de aprendizaje en contacto con el docente.
- Registrar experiencias práctico-experimentales.
- Registrar experiencias de aprendizaje autónomo.
- Registrar horas, recursos, escenarios y dimensión del conocimiento.
- Descargar sílabo en PDF o formato imprimible.
- Cargar sílabo firmado y aprobado.
- Controlar estado del sílabo.
- Bloquear carga de notas si el sílabo nueva versión no está finalizado o aprobado, según regla institucional.

Estados sugeridos del sílabo:

- Borrador.
- Enviado a revisión.
- Observado.
- Corregido.
- Aprobado por coordinación.
- Aprobado por dirección académica.
- Firmado/cargado.
- Cerrado.
- Archivado.

### 7.4 Módulo de gestión de notas

Debe soportar los tres sistemas de notas identificados:

- S1: Modelo principal con 3 resultados de aprendizaje; pérdida de un RA implica pérdida de asignatura si no se supera en recuperación.
- S2: Modelo similar al S1, pero permite recuperación cuando solo un RA está perdido; pérdida de dos o más RA implica pérdida de asignatura.
- S3: Modelo de sílabo antiguo con 3 parciales; cada parcial combina nota práctica y evaluación.

El módulo debe permitir:

- Configurar modelo de calificación por asignatura/curso.
- Registrar notas por criterio, actividad, resultado de aprendizaje o parcial.
- Calcular promedios automáticamente.
- Calcular letras A, B, C y D.
- Calcular estado de aprobación, recuperación, evaluación final, intersemestral o reprobación.
- Permitir recuperación según modelo.
- Bloquear modificaciones fuera de fechas o sin permiso.
- Registrar auditoría de cambios de notas.
- Consultar notas por docente, coordinación, secretaría y estudiante según permisos.
- Exportar actas o reportes.

### 7.5 Módulo de gestión de roles y permisos

Roles mínimos del MVP:

- Administrador general.
- Secretaría académica.
- Coordinador de carrera.
- Docente.
- Estudiante.
- Dirección académica.
- Bienestar universitario, para consulta futura.
- Bibliotecario, para fase posterior.
- Invitado o auditor, si se requiere.

El módulo debe permitir:

- Crear usuarios.
- Asignar roles.
- Asociar usuarios con persona, estudiante o docente.
- Asociar permisos por módulo.
- Restringir vistas y acciones por rol.
- Registrar auditoría de cambios de permisos.
- Desactivar usuarios sin eliminar historial.

### 7.6 Módulos técnicos adicionales necesarios para el MVP

Para que el MVP sea funcional, Codex debe considerar estos módulos técnicos desde el inicio:

1. **Autenticación:** login, logout, recuperación segura de contraseña, cambio de contraseña.
2. **Autorización:** roles, permisos, políticas por módulo y por objeto.
3. **Catálogos académicos:** periodos, carreras, niveles, asignaturas, paralelos, dominios, competencias, estados.
4. **Oferta académica:** apertura de cursos/paralelos por periodo.
5. **Matrícula académica:** inscripción de estudiantes en cursos.
6. **Archivos:** carga de sílabos firmados y documentos académicos.
7. **Auditoría:** bitácora de acciones críticas.
8. **Notificaciones internas:** alertas simples para sílabos pendientes, notas pendientes o cierre de periodo.
9. **Reportes:** listados, actas, reportes de notas, reporte de sílabos y exportaciones.
10. **Configuración institucional:** parámetros generales, escalas, umbrales y fechas.
11. **API REST:** endpoints para frontend, integraciones futuras y reportes.
12. **Backups y mantenimiento:** estrategia de respaldo y recuperación.

---

## 8. Sistemas de notas inferidos

### 8.1 Escala común

Los tres modelos trabajan con una escala base de **0 a 50 puntos**.

Equivalencia por letras:

| Letra | Rango sugerido | Interpretación |
|---|---:|---|
| A | 45 a 50 | Alcanzado con excelencia |
| B | 40 a 44.99 | Alcanzado muy bien |
| C | 30 a 39.99 | Alcanzado |
| D | 0 a 29.99 | No alcanzado |

Regla general: una nota igual o superior a 30/50 representa logro mínimo del resultado, parcial o asignatura, según el modelo aplicado.

### 8.2 Sistema S1 — Modelo principal por resultados de aprendizaje

**Archivo de referencia:** `2do. Semestre. NOTAS_FUNDAMENTOS Y METODOLOGÍA DE LA INVESTIGACIÓN.xlsx`

Características:

- Se trabaja con 3 resultados de aprendizaje: RDA1, RDA2 y RDA3.
- Cada RDA tiene 4 criterios de evaluación.
- Cada criterio puede tener una o varias actividades.
- La nota de cada criterio se calcula como promedio de las actividades registradas.
- Cada criterio tiene un peso.
- En el ejemplo de Excel los cuatro criterios tienen peso de 0.25, aunque el sistema debe permitir pesos configurables.
- La nota final de cada RDA se calcula sobre 50 puntos.
- Cada RDA aporta aproximadamente 33.33% al resultado semestral.
- El RDA se considera aprobado si su nota es mayor o igual a 30/50.

Fórmula conceptual por RDA:

```text
criterio_1 = promedio(actividades_criterio_1)
criterio_2 = promedio(actividades_criterio_2)
criterio_3 = promedio(actividades_criterio_3)
criterio_4 = nota_evaluacion_o_criterio_4

nota_rda = criterio_1 * peso_1
         + criterio_2 * peso_2
         + criterio_3 * peso_3
         + criterio_4 * peso_4
```

Regla de recuperación inferida:

```text
si nota_rda >= 30:
    nota_rda_final = nota_rda
si nota_rda < 30:
    nota_rda_final = min(nota_rda + nota_recuperacion * 0.15, 30)
```

Regla de aprobación final del S1:

```text
si RDA1_final >= 30 y RDA2_final >= 30 y RDA3_final >= 30:
    estado_final = APROBADO
si cualquier RDA_final < 30:
    estado_final = INTERSEMESTRAL / REPROBADO, según política institucional
```

Interpretación funcional:

- El S1 es el modelo más estricto.
- La asignatura no debe aprobarse si queda un resultado de aprendizaje no superado.
- La recuperación puede elevar un RDA perdido hasta máximo 30.
- El sistema debe identificar claramente el o los RDA no superados.

### 8.3 Sistema S2 — Modelo por resultados de aprendizaje con tolerancia de un RA

**Archivo de referencia:** `4to. Semestre. NOTAS_INVESTIGACION OPERATIVA.xlsx`

Características:

- También trabaja con 3 resultados de aprendizaje.
- Cada RDA usa 4 criterios de evaluación.
- Cada criterio se calcula por promedio de actividades y ponderación.
- La nota de cada RDA se expresa sobre 50 puntos.
- La escala A/B/C/D es la misma.
- La diferencia principal está en la regla de aprobación y recuperación.

Regla de conteo de RDA perdidos:

```text
rda_perdidos = cantidad de RDA con nota < 30

si rda_perdidos == 0:
    estado = APROBADO
si rda_perdidos == 1:
    estado = RECUPERACIÓN
si rda_perdidos >= 2:
    estado = REPROBADO
```

Regla de recuperación cuando existe un solo RDA perdido:

```text
si rda_perdidos == 1:
    identificar RDA perdido
    si nota_recuperacion >= 30:
        nota_rda_recuperada = 30
        estado_final = APROBADO
    si nota_recuperacion < 30:
        nota_rda_recuperada = nota_rda_original
        estado_final = REPROBADO
```

Cálculo del promedio final posterior a recuperación:

```text
promedio_final = promedio(RDA1_final, RDA2_final, RDA3_final)
```

Interpretación funcional:

- El S2 permite que un estudiante recupere un único RDA no alcanzado.
- Si pierde dos o tres RDA, no debe habilitarse recuperación ordinaria y debe quedar reprobado, salvo política institucional distinta.
- La recuperación del RDA no debe generar una nota superior a 30; solamente permite alcanzar el mínimo.
- El sistema debe evitar reproducir errores de fórmula observados en hojas de cálculo y aplicar reglas de negocio explícitas y probadas.

### 8.4 Sistema S3 — Modelo de sílabo antiguo por parciales

**Archivo de referencia:** `6to. Semestre. NOTAS_ADMINISTRACIÓN DE OPERACIONES.xlsx`

Características:

- Se trabaja con 3 parciales.
- Cada parcial contiene actividades prácticas configurables.
- Las actividades prácticas tienen ponderaciones que deben sumar 100% por parcial.
- La nota práctica del parcial se calcula sobre 50 puntos.
- Cada parcial también tiene una evaluación.
- La nota del parcial se calcula como promedio entre evaluación y nota práctica.

Fórmula conceptual por parcial:

```text
nota_practica_parcial = sumatoria(nota_actividad_i * peso_i / 100)
nota_parcial = (evaluacion_parcial + nota_practica_parcial) / 2
```

Cálculo semestral:

```text
promedio_3_parciales = promedio(nota_parcial_1, nota_parcial_2, nota_parcial_3)

si promedio_3_parciales >= 30:
    estado = APROBADO
si promedio_3_parciales < 30:
    estado = RENDIR_EVALUACION_FINAL / CUARTA_EVALUACION
```

Regla de cuarta evaluación inferida:

```text
promedio_practicas = promedio(nota_practica_1, nota_practica_2, nota_practica_3)
nota_final = (promedio_practicas + cuarta_evaluacion) / 2

si nota_final >= 30:
    estado_final = APROBADO
si nota_final < 30:
    estado_final = REPROBADO
```

Interpretación funcional:

- Este modelo debe mantenerse por compatibilidad con asignaturas que aún usen sílabo anterior.
- No trabaja directamente con RDA en la operación de notas.
- Debe configurarse por parciales, actividades prácticas, evaluación y cuarta evaluación.

---

## 9. Reglas críticas del módulo de notas

1. El sistema debe guardar nota original, nota calculada, nota recuperada y estado final.
2. Ninguna nota debe sobrescribirse sin auditoría.
3. El docente solo debe editar notas de cursos asignados.
4. Secretaría y coordinación pueden consultar y, si se autoriza, abrir periodos de corrección.
5. El estudiante solo debe ver sus propias notas.
6. Toda modificación posterior al cierre debe requerir permiso especial y justificación.
7. Los pesos deben sumar 1.0 o 100%, según el modelo.
8. Las actividades vacías no deben distorsionar promedios; debe definirse si se ignoran o se computan como cero.
9. Las reglas S1, S2 y S3 deben implementarse como servicios de dominio con pruebas unitarias.
10. No deben depender de fórmulas Excel en producción.
11. El sistema debe permitir exportar actas en formato institucional.
12. Los modelos de nota deben ser configurables por periodo, carrera, asignatura y curso.

---

## 10. Arquitectura tecnológica recomendada

### 10.1 Stack del MVP

- **Backend:** Python + Django.
- **API:** Django REST Framework.
- **Base de datos:** PostgreSQL.
- **Frontend del MVP:** Next.js + TypeScript + Tailwind CSS.
- **Componentes UI:** shadcn/ui o componentes propios equivalentes, centralizados y reutilizables.
- **Gestión de formularios frontend:** React Hook Form + Zod cuando existan formularios funcionales.
- **Gestión de datos frontend:** TanStack Query cuando se consuma la API real.
- **Autenticación inicial:** JWT emitido por Django REST Framework y consumido por el frontend Next.js.
- **Autorización:** Django Groups, Permissions y reglas por objeto.
- **Archivos:** almacenamiento compatible con S3.
- **Reportes:** generación PDF/Excel/CSV desde backend.
- **Auditoría:** modelo propio de AuditLog y/o django-simple-history.
- **Tareas asíncronas futuras:** Celery + Redis, si se integran Moodle, correos o reportes pesados.
- **Contenedores:** Docker para desarrollo y despliegue.
- **CI/CD:** GitHub Actions.

### 10.2 Separación de responsabilidades

| Capa | Responsabilidad |
|---|---|
| Django Models | Entidades académicas y reglas de integridad. |
| Services | Cálculos de notas, estados, sílabos y procesos académicos. |
| Django Admin | Administración interna auxiliar, soporte técnico, carga inicial y operación restringida. |
| DRF API | Endpoints para frontend Next.js, integraciones y reportes. |
| Frontend Next.js | Experiencia principal de usuario para docentes, estudiantes, secretaría, coordinación y administración. |
| PostgreSQL | Persistencia transaccional. |
| S3 compatible | Archivos firmados, sílabos, guías y documentos. |
| AuditLog | Trazabilidad de acciones críticas. |


### 10.3 Decisiones específicas de frontend

El frontend del MVP queda definido como una aplicación **Next.js + TypeScript + Tailwind CSS** dentro de `/frontend`. Esta decisión evita que cada módulo improvise pantallas y permite construir una experiencia institucional coherente para administradores, secretaría, coordinadores, docentes y estudiantes.

El **Sprint 0.5 — Frontend Design System & UX Foundation** debe ejecutarse después de la base técnica del Sprint 0 y antes del Sprint 1. Su propósito es crear la estructura visual, componentes reutilizables, navegación por rol, layout protegido y prototipos navegables con datos mock.

Reglas de frontend para Codex:

1. Usar los componentes y tokens definidos en el Sprint 0.5 antes de crear pantallas nuevas.
2. No usar datos reales de estudiantes, docentes, autoridades ni credenciales en prototipos.
3. No incluir logos oficiales o assets institucionales si no están proporcionados en el repositorio.
4. Validar permisos también en backend; ocultar botones en frontend no equivale a seguridad.
5. Diseñar navegación lateral por rol: Administrador, Secretaría, Coordinador de carrera, Docente, Estudiante y roles complementarios.
6. Mantener estados visuales consistentes para borrador, pendiente, en revisión, aprobado, rechazado, cerrado, aprobado, reprobado, recuperación y sin calificar.
7. Mantener accesibilidad básica: contraste, labels, foco visible, errores claros y navegación por teclado.
8. Separar componentes visuales, acceso a API, mocks y reglas de negocio.

### 10.4 Estructura recomendada del repositorio

```text
puceasig/
├── backend/
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── local.py
│   │   │   ├── test.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── accounts/
│   │   ├── core/
│   │   ├── academic_catalogs/
│   │   ├── people/
│   │   ├── students/
│   │   ├── teachers/
│   │   ├── enrollment/
│   │   ├── syllabus/
│   │   ├── grading/
│   │   ├── attendance/
│   │   ├── documents/
│   │   ├── notifications/
│   │   ├── reports/
│   │   ├── integrations/
│   │   └── audit/
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── (auth)/
│   │   ├── (dashboard)/
│   │   ├── globals.css
│   │   └── layout.tsx
│   ├── components/
│   │   ├── layout/
│   │   ├── ui/
│   │   ├── forms/
│   │   ├── tables/
│   │   ├── dashboard/
│   │   └── feedback/
│   ├── config/
│   │   ├── navigation.ts
│   │   ├── roles.ts
│   │   └── theme.ts
│   ├── lib/
│   │   ├── api.ts
│   │   ├── mock-data.ts
│   │   └── utils.ts
│   ├── types/
│   └── README.md
├── docs/
│   ├── project-reference-puceasig.md
│   ├── requirements.md
│   ├── architecture.md
│   ├── database-model.md
│   ├── grading-rules.md
│   ├── mvp-roadmap.md
│   ├── api.md
│   └── security.md
├── scripts/
├── tests/
├── .env.example
├── .gitignore
├── AGENTS.md
└── README.md
```

---

## 11. Apps Django sugeridas

| App | Responsabilidad |
|---|---|
| accounts | Usuarios, roles, permisos, perfiles y seguridad. |
| core | Parámetros institucionales, periodos, estados y utilidades compartidas. |
| academic_catalogs | Sede, carreras, dominios, planes, niveles, asignaturas, competencias y resultados. |
| people | Persona base compartida por estudiantes, docentes y administrativos. |
| students | Expediente académico básico del estudiante. |
| teachers | Perfil docente, títulos, reseña, tutorías y asignaciones. |
| enrollment | Oferta académica, cursos, paralelos, matrícula y listas de estudiantes. |
| syllabus | Sílabos nueva versión, sílabos antiguos, aprobación, carga y descarga. |
| grading | Modelos de notas S1, S2, S3, criterios, actividades, recuperaciones y actas. |
| attendance | Inasistencias; puede implementarse después del MVP estricto. |
| documents | Archivos, sílabos firmados, guías, documentos y almacenamiento externo. |
| notifications | Notificaciones internas y alertas operativas. |
| reports | Reportes académicos, actas, exportaciones y dashboards. |
| integrations | Moodle, Google Drive, correo, APIs externas. |
| audit | Auditoría y trazabilidad de cambios críticos. |

---

## 12. Modelo de datos inicial sugerido

### 12.1 Núcleo de personas y usuarios

#### Person

- first_name.
- last_name.
- identification_type.
- identification_number.
- institutional_email.
- personal_email.
- phone.
- birth_date.
- address.
- is_active.
- created_at.
- updated_at.

#### UserProfile

- user.
- person.
- primary_role.
- assigned_careers.
- must_change_password.
- security_questions_configured.
- is_active.
- created_at.
- updated_at.

#### Role

- name.
- code.
- description.
- is_system_role.

### 12.2 Catálogos académicos

#### AcademicPeriod

- name.
- code.
- start_date.
- end_date.
- enrollment_start.
- enrollment_end.
- grading_open_date.
- grading_close_date.
- is_current.
- status.

#### Career

- name.
- code.
- modality.
- coordinator.
- is_active.

#### StudyPlan

- career.
- code.
- name.
- version.
- effective_from.
- effective_to.
- is_active.

#### AcademicLevel

- study_plan.
- number.
- name.

#### Subject

- career.
- study_plan.
- level.
- code.
- name.
- total_hours.
- contact_hours.
- autonomous_hours.
- practical_hours.
- prerequisites.
- syllabus_version_default.
- grading_system_default.
- is_active.

#### CourseOffering

- period.
- career.
- subject.
- level.
- parallel.
- capacity.
- classroom.
- status.

#### TeachingAssignment

- course_offering.
- teacher.
- role: titular, codocente, invitado.
- assigned_at.
- is_active.

### 12.3 Estudiantes y matrícula

#### Student

- person.
- career.
- study_plan.
- admission_period.
- student_code.
- status.
- created_at.
- updated_at.

#### Enrollment

- student.
- period.
- career.
- level.
- status.
- created_by.
- created_at.

#### CourseEnrollment

- enrollment.
- course_offering.
- status.
- enrolled_at.
- withdrawn_at.

### 12.4 Docentes

#### Teacher

- person.
- teacher_code.
- academic_degree.
- professional_title.
- academic_bio.
- institutional_phone.
- status.

#### TeacherOfficeHour

- teacher.
- course_offering.
- modality: presencial, virtual.
- day_of_week.
- start_time.
- end_time.
- location_or_link.

### 12.5 Sílabos

#### Syllabus

- course_offering.
- version: new, legacy.
- status.
- domain.
- subject_description.
- methodology.
- teacher_bio_snapshot.
- codocent_bio_snapshot.
- approved_by_coordinator.
- approved_by_academic_direction.
- signed_file.
- created_by.
- submitted_at.
- approved_at.
- closed_at.

#### SyllabusCompetency

- syllabus.
- competency_type: transversal, disciplinary.
- text.
- order.

#### LearningOutcome

- syllabus.
- outcome_type: career, subject.
- text.
- order.

#### EvaluationCriterion

- syllabus.
- learning_outcome.
- name.
- description.
- weight.
- order.

#### AchievementLevel

- criterion or learning_outcome.
- level: A, B, C, D.
- description.

#### SyllabusBibliography

- syllabus.
- bibliography_type: basic, complementary, recommended, digital.
- apa_reference.
- library_code.
- quantity.

#### WeeklyPlan

- syllabus.
- learning_outcome.
- week_label.
- start_date.
- end_date.
- contact_strategy.
- contact_hours.
- contact_resources.
- contact_scenarios.
- practical_strategy.
- practical_hours.
- practical_resources.
- practical_scenarios.
- autonomous_strategy.
- autonomous_hours.
- autonomous_resources.
- autonomous_scenarios.
- knowledge_dimension.

### 12.6 Notas

#### GradingSystem

- code: S1, S2, S3.
- name.
- description.
- is_active.
- config_json.

#### Gradebook

- course_offering.
- grading_system.
- syllabus.
- status: draft, open, submitted, closed, archived.
- created_at.
- closed_at.

#### GradeLearningOutcome

- gradebook.
- learning_outcome.
- order.
- weight_in_course.

#### GradeCriterion

- grade_learning_outcome.
- name.
- weight.
- criterion_type.
- order.

#### GradeActivity

- grade_criterion.
- name.
- max_score.
- due_date.
- order.

#### StudentGradeActivity

- activity.
- course_enrollment.
- score.
- entered_by.
- entered_at.
- updated_at.

#### StudentLearningOutcomeResult

- grade_learning_outcome.
- course_enrollment.
- original_score.
- recovered_score.
- final_score.
- letter.
- status.

#### StudentCourseGrade

- gradebook.
- course_enrollment.
- final_score.
- final_letter.
- final_status.
- failed_learning_outcomes_count.
- recovery_required.
- calculated_at.

#### RecoveryAttempt

- course_enrollment.
- gradebook.
- learning_outcome.
- recovery_type.
- score.
- applied_score.
- status.
- entered_by.
- entered_at.

#### LegacyPartial

- gradebook.
- partial_number: 1, 2, 3.
- name.
- status.

#### LegacyPartialActivity

- legacy_partial.
- name.
- weight.
- max_score.

#### StudentLegacyPartialGrade

- legacy_partial.
- course_enrollment.
- practice_score.
- evaluation_score.
- partial_score.

#### LegacyFinalEvaluation

- course_enrollment.
- gradebook.
- score.
- final_score.
- final_status.

### 12.7 Auditoría

#### AuditLog

- user.
- action.
- module.
- model_name.
- object_id.
- previous_data.
- new_data.
- reason.
- ip_address.
- user_agent.
- created_at.

---

## 13. Permisos por rol en el MVP

| Módulo / Acción | Administrador | Secretaría | Coordinador | Docente | Estudiante |
|---|---|---|---|---|---|
| Configurar periodos/carreras/asignaturas | Sí | Parcial | Consulta | No | No |
| Crear usuarios | Sí | Parcial | No | No | No |
| Gestionar estudiantes | Sí | Sí | Consulta | Consulta limitada | Propio perfil |
| Gestionar docentes | Sí | Sí | Consulta | Propio perfil | No |
| Abrir oferta académica | Sí | Sí | Sí | No | No |
| Matricular estudiantes | Sí | Sí | Consulta | No | No |
| Crear sílabo | No | No | Revisa | Sí | No |
| Aprobar sílabo | Sí | No | Sí | No | No |
| Cargar sílabo firmado | Sí | Sí | Sí | Sí, si autorizado | No |
| Registrar notas | No | No | Excepcional | Sí | No |
| Corregir notas cerradas | Sí | Sí, con autorización | Autoriza | No | No |
| Consultar notas | Sí | Sí | Sí | Sus cursos | Solo propias |
| Exportar actas | Sí | Sí | Sí | Sus cursos | No |
| Ver auditoría | Sí | Parcial | Parcial | No | No |

---

## 14. Estados académicos sugeridos

### 14.1 Estado de curso/paralelo

- Planificado.
- Abierto.
- En curso.
- Cerrado.
- Archivado.

### 14.2 Estado de matrícula en curso

- Matriculado.
- Retirado.
- Anulado.
- Aprobado.
- Reprobado.
- En recuperación.

### 14.3 Estado de acta o gradebook

- Borrador.
- Abierto para calificación.
- Enviado.
- Observado.
- Cerrado.
- Reabierto por autorización.
- Archivado.

### 14.4 Estado de resultado de aprendizaje

- Pendiente.
- Alcanzado.
- No alcanzado.
- En recuperación.
- Recuperado.
- No recuperado.

---

## 15. API REST inicial requerida

Endpoints mínimos sugeridos:

```text
/api/auth/login/
/api/auth/logout/
/api/me/
/api/accounts/users/
/api/accounts/roles/
/api/academic/periods/
/api/academic/careers/
/api/academic/study-plans/
/api/academic/subjects/
/api/academic/course-offerings/
/api/students/
/api/teachers/
/api/enrollments/
/api/course-enrollments/
/api/syllabi/
/api/syllabi/{id}/submit/
/api/syllabi/{id}/approve/
/api/syllabi/{id}/upload-signed-file/
/api/gradebooks/
/api/gradebooks/{id}/activities/
/api/gradebooks/{id}/student-results/
/api/gradebooks/{id}/calculate/
/api/gradebooks/{id}/close/
/api/recoveries/
/api/reports/gradebook/
/api/reports/student-transcript/
/api/audit/
```

La API debe validar permisos en backend. No basta con ocultar botones en el frontend.

---

## 16. Roadmap de desarrollo recomendado

### Fase 0. Descubrimiento técnico y normalización documental

Entregables:

- Documento maestro `docs/project-reference-puceasig.md`.
- Inventario funcional del sistema actual.
- Mapa de módulos del ERP/SIG.
- Reglas de notas S1, S2 y S3 documentadas.
- Glosario académico.
- Decisiones iniciales de arquitectura.

### Fase 1. Preparación del repositorio

Entregables:

- README.md.
- AGENTS.md.
- `.gitignore`.
- `.env.example`.
- Carpeta `/docs`.
- Documentación inicial: requirements, architecture, database-model, grading-rules, mvp-roadmap, security.

### Fase 2. Backend base

Entregables:

- Proyecto Django ejecutable.
- Django REST Framework configurado.
- PostgreSQL configurado por variables de entorno.
- Settings por ambiente: local, test, production.
- Docker Compose para desarrollo.
- Apps iniciales creadas.
- Pruebas mínimas de arranque.

### Fase 2.5. Frontend Design System & UX Foundation

Entregables:

- Aplicación `/frontend` con Next.js + TypeScript + Tailwind CSS.
- Tema visual institucional centralizado.
- Componentes UI reutilizables.
- Layout autenticado con sidebar/header.
- Navegación por rol.
- Prototipos navegables con datos mock para dashboards, estudiantes, docentes, sílabos, notas y reportes.
- Documentación `docs/frontend-design-system.md` y `frontend/README.md`.

### Fase 3. Seguridad, usuarios y roles

Entregables:

- Login y logout.
- Modelo de perfil de usuario.
- Roles base.
- Permisos por módulo.
- Middleware o helpers de autorización.
- Auditoría básica.
- Seeds de roles sin datos reales.

### Fase 4. Catálogos académicos

Entregables:

- Periodos académicos.
- Carreras.
- Planes de estudio.
- Niveles o semestres.
- Asignaturas.
- Paralelos.
- Dominios.
- Competencias.
- Resultados de aprendizaje base.

### Fase 5. Estudiantes, docentes y oferta académica

Entregables:

- CRUD de estudiantes.
- CRUD de docentes.
- Oferta académica por periodo.
- Asignación docente a cursos/paralelos.
- Matrícula de estudiantes en cursos.
- Listas de estudiantes por curso.

### Fase 6. Sílabos nueva versión y versión anterior

Entregables:

- Modelo de sílabo.
- Flujo de creación por secciones.
- Registro de competencias y resultados de aprendizaje.
- Registro de rúbricas y criterios.
- Registro de pesos.
- Registro de bibliografía.
- Registro de planificación semanal.
- Estados de revisión y aprobación.
- Carga de sílabo firmado.
- Exportación o vista imprimible.

### Fase 7. Motor de notas S1 y S2

Entregables:

- Modelos de gradebook por RDA.
- Criterios y actividades.
- Registro de notas por docente.
- Cálculo automático por RDA.
- Cálculo de letras A/B/C/D.
- Recuperaciones S1.
- Recuperaciones S2.
- Estados finales.
- Pruebas unitarias para reglas S1 y S2.
- Vista de consulta para estudiantes.

### Fase 8. Motor de notas S3

Entregables:

- Parciales 1, 2 y 3.
- Actividades prácticas ponderadas.
- Evaluación por parcial.
- Promedio de parcial.
- Promedio de 3 parciales.
- Cuarta evaluación.
- Nota final.
- Pruebas unitarias para reglas S3.

### Fase 9. Reportes académicos

Entregables:

- Reporte de notas por curso.
- Reporte de notas por estudiante.
- Acta de calificaciones.
- Reporte de sílabos por estado.
- Exportación CSV/Excel/PDF.
- Dashboard académico básico.

### Fase 10. Endurecimiento del MVP

Entregables:

- Validación de permisos por rol.
- Auditoría de cambios de notas.
- Pruebas de integración.
- Pruebas de seguridad básicas.
- Pruebas de importación/exportación.
- Backups.
- Manual técnico.
- Manual básico de usuario.
- Despliegue piloto.

### Fase 11. Módulos académicos complementarios

Entregables posteriores:

- Inasistencias.
- Guías teóricas y prácticas.
- Fichas prácticas.
- Evaluaciones institucionales.
- Integración Moodle.

### Fase 12. Módulos institucionales ampliados

Entregables posteriores:

- Admisiones.
- Bienestar universitario.
- Biblioteca.
- Repositorio académico.
- Mensajería.
- Gestión documental.
- PQR/PQRSD.
- Inventario.
- Dashboards estratégicos.

---

## 17. Requerimientos no funcionales

### 17.1 Seguridad

- Contraseñas hasheadas.
- Variables de entorno para secretos.
- HTTPS en producción.
- Protección CSRF si se usan sesiones.
- CORS restringido si se usa frontend separado.
- Permisos por rol y por objeto.
- Auditoría en cambios críticos.
- Sanitización de archivos cargados.
- Validación de tipos de archivo.
- Límite de tamaño de archivos.
- No usar credenciales reales en prompts, tests o seeds.

### 17.2 Rendimiento

- Paginación en listados grandes.
- Índices en campos de búsqueda frecuentes.
- Consultas optimizadas para reportes.
- Exportaciones asíncronas si crecen los datos.
- Caché para catálogos estables.

### 17.3 Mantenibilidad

- Apps Django separadas por dominio.
- Servicios de dominio para reglas de negocio.
- Pruebas unitarias para cálculos de notas.
- Documentación en `/docs`.
- Migraciones versionadas.
- Convenciones de nombres.
- Tipado gradual si se usa Python typing.

### 17.4 Usabilidad

- Interfaz clara para docentes.
- Flujo guiado para sílabos.
- Registro de notas tipo planilla, pero con validaciones.
- Mensajes de error comprensibles.
- Vistas responsive.
- Exportaciones con formato institucional.

### 17.5 Integridad de datos

- Restricciones de unicidad.
- Validaciones de pesos.
- Validaciones de escala 0-50.
- Validación de estados.
- No permitir curso sin periodo.
- No permitir nota sin matrícula.
- No permitir gradebook sin modelo de calificación.
- No permitir cierre de acta si existen notas incompletas, salvo autorización explícita.

---

## 18. Restricciones para Codex

Codex debe respetar estas restricciones:

1. No guardar credenciales reales en archivos, documentación, commits ni tests.
2. No usar datos reales de estudiantes, docentes o autoridades en seeds públicos.
3. No replicar errores de fórmulas Excel; implementar reglas de negocio claras y probadas.
4. No hardcodear ponderaciones, umbrales o periodos.
5. No permitir acceso a notas sin validación de rol.
6. No permitir edición de notas cerradas sin flujo de reapertura y auditoría.
7. No implementar módulos grandes en una sola tarea.
8. No mezclar lógica de notas dentro de views; usar servicios de dominio.
9. No guardar archivos cargados dentro del repositorio Git.
10. No depender de Excel para calcular notas en producción.
11. No exponer endpoints administrativos sin autenticación.
12. No crear modelos con nombres ambiguos como `Data` o `Info`.
13. No duplicar persona, estudiante y docente sin una relación clara.
14. No asumir que todos los sílabos usan el mismo modelo de calificación.
15. No hacer scraping del sistema productivo con credenciales institucionales desde código del repositorio.
16. Mantener documentación actualizada cuando cambien reglas o modelos.
17. Crear pruebas para todo cálculo de notas.
18. Mantener cambios pequeños, revisables y reversibles.

---

## 19. Reglas técnicas para AGENTS.md

El archivo `AGENTS.md` del repositorio debería incluir lo siguiente:

```md
# AGENTS.md — PUCEASIG

## Contexto
Este repositorio corresponde al Sistema ERP/SIG Académico para PUCE Amazonas. El MVP se enfoca en Gestión Académica: estudiantes, docentes, sílabos, notas, roles, periodos, cursos, matrículas, reportes y auditoría.

## Stack principal
- Python
- Django
- Django REST Framework
- PostgreSQL
- Frontend del MVP con Next.js + TypeScript + Tailwind CSS
- Almacenamiento compatible con S3 para archivos

## Principios obligatorios
- Proteger datos personales y académicos.
- Aplicar permisos por rol y por objeto.
- Auditar cambios críticos, especialmente notas, sílabos, matrículas y roles.
- No hardcodear reglas de calificación.
- Implementar modelos de notas S1, S2 y S3 como servicios de dominio probados.
- No usar datos reales en seeds o pruebas.
- No guardar archivos cargados en Git.
- No guardar secretos en el repositorio.

## Reglas de desarrollo
- Trabajar en cambios pequeños y revisables.
- Mantener apps Django modulares.
- Mantener migraciones versionadas.
- Agregar pruebas unitarias para reglas de negocio.
- Validar serializers, forms y permisos.
- Actualizar documentación en /docs cuando se agregue o cambie un módulo.
- Usar variables de entorno para configuración sensible.
- Priorizar claridad del modelo de datos sobre velocidad aparente.

## Reglas de notas
- Todas las notas se registran sobre escala 0 a 50.
- A: >=45, B: >=40, C: >=30, D: <30.
- S1: cualquier RDA final menor a 30 implica no aprobación.
- S2: un RDA perdido habilita recuperación; dos o más RDA perdidos implican reprobación.
- S3: tres parciales con práctica + evaluación; si promedio <30, habilitar cuarta evaluación.
- Toda corrección de nota cerrada requiere auditoría y justificación.
```

---

## 20. Definición de éxito del MVP

El MVP se considerará exitoso si permite:

1. Iniciar sesión con roles diferenciados.
2. Crear periodos académicos.
3. Crear carreras, planes, niveles y asignaturas.
4. Crear estudiantes y docentes.
5. Abrir cursos/paralelos por periodo.
6. Asignar docentes a cursos.
7. Matricular estudiantes en cursos.
8. Crear sílabos nueva versión.
9. Cargar sílabos firmados y aprobados.
10. Configurar el sistema de calificación por curso.
11. Registrar notas bajo S1, S2 y S3.
12. Calcular resultados y estados automáticamente.
13. Permitir al estudiante consultar sus notas.
14. Permitir a docentes consultar y registrar notas de sus cursos.
15. Permitir a coordinación y secretaría consultar reportes.
16. Exportar actas o reportes básicos.
17. Auditar cambios críticos.
18. Proteger datos personales y académicos por rol.
19. Mantener documentación técnica actualizada.
20. Dejar arquitectura lista para integrar Moodle y módulos institucionales posteriores.

---

## 21. Riesgos técnicos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Reglas de notas ambiguas | Cálculos incorrectos | Documentar reglas S1, S2, S3 y crear pruebas unitarias. |
| Copiar errores de Excel | Estados finales incorrectos | Implementar reglas de negocio explícitas, no fórmulas copiadas sin validación. |
| Falta de control por roles | Exposición de datos académicos | Permisos backend por rol y objeto. |
| Cambios de notas sin trazabilidad | Riesgo institucional | Auditoría obligatoria y flujo de reapertura. |
| Datos duplicados de personas | Inconsistencia | Modelo Person central y perfiles relacionados. |
| Hardcoding de periodos y pesos | Sistema poco mantenible | Catálogos y configuración por periodo/curso. |
| Alcance demasiado grande | MVP inconcluso | Priorizar Gestión Académica y diferir módulos institucionales. |
| Archivos en repositorio | Repositorio pesado e inseguro | Usar almacenamiento externo y excluir uploads en .gitignore. |
| Integración Moodle prematura | Complejidad temprana | Diseñar API preparada, integrar en fase posterior. |
| Uso de datos reales en pruebas | Riesgo de privacidad | Seeds sintéticos y anonimización. |

---

## 22. Nota final para Codex

Este proyecto no debe abordarse como una simple clonación visual del sistema actual. Debe construirse como una plataforma académica institucional, modular, segura y auditable, capaz de reproducir los procesos actuales y mejorar su mantenibilidad.

La prioridad del MVP es la **Gestión Académica**. Los demás macroprocesos del SIG deben quedar documentados y considerados en la arquitectura, pero no deben bloquear el desarrollo inicial.
