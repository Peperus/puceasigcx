# Guia de usuario MVP - Secretaria academica

## Objetivo

Operar la gestion academica diaria del MVP: estudiantes, docentes, oferta,
matricula, silabos, notas consultivas, reportes y auditoria autorizada.

## Inicio de sesion

1. Ingrese al frontend institucional del MVP.
2. Use su cuenta institucional asignada por el administrador.
3. Verifique que el menu muestre opciones de gestion academica, matricula,
   silabos, reportes y auditoria.

## Estudiantes y docentes

1. Abra Estudiantes o Docentes.
2. Busque por codigo, identificacion, nombre o correo.
3. Cree o actualice registros con datos sinteticos en ambientes de prueba.
4. Desactive registros cuando corresponda; evite eliminar historial operativo.

## Matricula

1. Verifique que existan periodo, carrera, plan, nivel, asignatura y curso activo.
2. Cree la matricula academica del estudiante para el periodo.
3. Inscriba al estudiante en cursos/paralelos con cupo disponible.
4. Revise mensajes de validacion: carrera, periodo, cupos y estado del curso.

## Silabos

1. Consulte silabos por periodo, carrera, curso y estado.
2. Apoye el seguimiento de silabos pendientes, observados o aprobados.
3. Cargue PDF firmado solo cuando el silabo este aprobado y el archivo sea PDF.

## Notas y cierres

1. Consulte reportes de notas por periodo, carrera, curso, modelo y estado.
2. Exporte actas o reportes cuando la coordinacion o direccion lo requiera.
3. Cierre o reabra actas solo con autorizacion y justificacion.

## Reportes

Reportes MVP disponibles:

- Estudiantes por carrera y periodo.
- Docentes asignados por periodo.
- Cursos/paralelos activos.
- Silabos por estado.
- Notas por curso, modelo y estado.

Use filtros antes de exportar CSV/XLSX para limitar la informacion.

## Auditoria

1. Abra Auditoria o `/api/audit/logs/`.
2. Filtre por modulo, accion, modelo, objeto, usuario o fecha.
3. Use la auditoria para investigar cambios de notas, silabos, matriculas, roles
   y exportaciones.
4. No edite registros de auditoria; son evidencia institucional.
