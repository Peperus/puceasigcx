# Sprints 9–17 — Bloque de Escalamiento ERP/SIG posterior al MVP

> Estos sprints se desarrollan después del MVP de Gestión Académica. El orden puede ajustarse por prioridad institucional, pero no conviene profundizar tickets finos hasta iniciar cada sprint. Al comenzar uno, crea su archivo específico `SPRINTS/sprint-XX-*.md` con tickets pequeños, criterios de aceptación y verificaciones.

---

## Criterio para iniciar el bloque de escala

Antes de iniciar Sprint 9, el MVP debe permitir:
- gestión de usuarios y roles;
- catálogos académicos;
- estudiantes y docentes;
- cursos/paralelos y matrículas;
- sílabos;
- notas S1/S2/S3;
- consulta estudiantil;
- reportes básicos;
- auditoría;
- despliegue piloto documentado.

---

## Sprint 9 — Admisiones y captación

**Objetivo:** implementar el flujo aspirante → preinscripción → reserva → revisión → creación de estudiante → habilitación de matrícula.
**Depende de:** usuarios, periodos, carreras, estudiantes y matrícula del MVP.

**Alcance general**
- Formulario de preinscripción pública con validaciones y protección anti-spam.
- Reserva de cupo para examen/atención según calendario configurado.
- Gestión de aspirantes por Secretaría/Admisiones.
- Registro de requisitos y estado documental.
- Conversión controlada de aspirante a estudiante.
- Trazabilidad del flujo completo.

**Salida:** módulo de admisiones funcional integrado con matrícula.

---

## Sprint 10 — Bienestar universitario

**Objetivo:** centralizar información de acompañamiento estudiantil, vulnerabilidad, solicitudes de recursos y seguimiento.
**Depende de:** estudiantes, matrícula, roles y seguridad.

**Alcance general**
- Perfil de bienestar por estudiante.
- Registro socioeconómico y vulnerabilidad con confidencialidad reforzada.
- Solicitudes de villa, transporte u otros recursos.
- Seguimiento psicológico/académico según permisos.
- Reportes agregados sin exponer datos sensibles.

**Salida:** módulo de bienestar con acceso restringido y trazabilidad.

---

## Sprint 11 — Biblioteca y repositorio académico

**Objetivo:** gestionar catálogo bibliográfico, libros digitales, préstamos/consultas y repositorio de tesis o trabajos académicos.
**Depende de:** usuarios, estudiantes/docentes, cursos y almacenamiento de archivos.

**Alcance general**
- Categorías, subcategorías y clasificaciones.
- Catálogo de libros físicos/digitales.
- Vinculación de bibliografía con asignaturas/sílabos.
- Consulta/lectura de libros según permisos.
- Registro de consultas y uso de biblioteca.
- Repositorio de tesis/trabajos académicos.

**Salida:** biblioteca integrada con sílabos y perfiles docente/estudiante.

---

## Sprint 12 — Requerimientos, PQRSD y mensajería institucional

**Objetivo:** implementar flujos institucionales de requerimientos, buzón de sugerencias, PQRSD y mensajería con adjuntos.
**Depende de:** usuarios, roles, documentos y auditoría.

**Alcance general**
- Registro público/privado de PQRSD con código único.
- Consulta de estado por código.
- Bandeja de gestión por responsables.
- Requerimientos internos con adjuntos obligatorios cuando aplique.
- Flujo de revisión, respuesta y archivo.
- Notificaciones por correo o bandeja interna.

**Salida:** módulo de atención y comunicaciones con trazabilidad.

---

## Sprint 13 — Integración Moodle y aula virtual

**Objetivo:** sincronizar cursos, usuarios, matrículas y eventualmente calificaciones/intentos con Moodle.
**Depende de:** cursos, estudiantes, docentes, notas, roles y APIs estables.

**Alcance general**
- Configuración segura de credenciales/API Moodle por variables de entorno.
- Sincronización usuario/curso/matrícula.
- Mapeo CourseSection ↔ curso Moodle.
- Recuperación controlada de calificaciones o intentos si se autoriza.
- Logs de sincronización y reintentos.

**Salida:** interoperabilidad académica con Moodle sin comprometer seguridad.

---

## Sprint 14 — Gestión documental institucional

**Objetivo:** crear un repositorio documental ordenado por módulos, perfiles y permisos.
**Depende de:** almacenamiento de archivos, roles y auditoría.

**Alcance general**
- Carpetas/categorías documentales.
- Metadatos, versionado y permisos.
- Integración futura con Google Drive/Workspace o S3.
- Búsqueda y filtros.
- Reglas de retención y archivado.

**Salida:** repositorio documental transversal para el ERP/SIG.

---

## Sprint 15 — Inventario y activos

**Objetivo:** gestionar catálogo de bienes, ubicación, estado, daños, asignaciones y reportes.
**Depende de:** roles, auditoría y catálogos institucionales.

**Alcance general**
- Catálogo de activos.
- Ubicaciones, estanterías, aulas/laboratorios.
- Estados, daños, mantenimientos y responsables.
- Historial de movimientos.
- Reportes por ubicación, estado y responsable.

**Salida:** módulo de inventario institucional auditable.

---

## Sprint 16 — Analítica institucional y tableros estratégicos

**Objetivo:** consolidar dashboards operativos y estratégicos alimentados por módulos académicos y administrativos.
**Depende de:** MVP y módulos de escala implementados.

**Alcance general**
- Dashboard académico: matrícula, notas, RA, sílabos, rendimiento.
- Dashboard admisiones: aspirantes, reservas, conversiones.
- Dashboard bienestar: indicadores agregados y protegidos.
- Dashboard biblioteca: uso y préstamos/consultas.
- Dashboard PQRSD/requerimientos: estados, tiempos de respuesta.
- Exportación y filtros por periodo/carrera.

**Salida:** tableros institucionales para toma de decisiones.

---

## Sprint 17 — Portal integral, interoperabilidad y hardening de escala

**Objetivo:** consolidar el ERP/SIG como plataforma institucional robusta, integrable y escalable.
**Depende de:** MVP y módulos principales implementados.

**Alcance general**
- Portal integral para estudiantes, docentes, secretaría y coordinación.
- API pública/institucional documentada donde aplique.
- Mejoras de rendimiento y cache.
- Observabilidad: logs centralizados, métricas, monitoreo de errores.
- Backups automatizados y plan de recuperación.
- Hardening de seguridad y pruebas de carga.
- Preparación para despliegue institucional de mayor escala.

**Salida:** ERP/SIG académico-administrativo robusto para operación ampliada.

---

## Recordatorio estratégico

El bloque de escala no debe distraer del MVP. Cada sprint futuro debe iniciar con una revisión de procesos institucionales, permisos, datos sensibles, integraciones y riesgos. La regla práctica es: primero estabilizar Gestión Académica, luego incorporar procesos administrativos de forma incremental.
