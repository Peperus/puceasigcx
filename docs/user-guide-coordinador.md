# Guia de usuario MVP - Coordinador de carrera

## Objetivo

Supervisar la carrera asignada: oferta, docentes, silabos, notas, cierres,
reportes y auditoria consultiva.

## Alcance por carrera

El coordinador solo debe ver informacion de las carreras donde esta asignado
como coordinador. Si aparecen datos de otra carrera, reporte el caso como
incidente de permisos.

## Silabos

1. Consulte silabos por periodo, carrera, curso y estado.
2. Revise los silabos enviados por docentes.
3. Apruebe, observe o reabra segun corresponda.
4. Toda observacion o reapertura debe incluir justificacion clara.

## Notas y actas

1. Consulte notas por periodo, curso, estudiante, modelo y estado.
2. Revise resultados S1, S2 y S3 antes del cierre.
3. Cierre o reabra actas solo cuando el proceso academico lo permita.
4. La reapertura requiere justificacion y queda auditada.

## Reportes

Use `/api/reports/mvp/<tipo>/` o la pantalla de Reportes para:

- estudiantes;
- docentes asignados;
- cursos activos;
- silabos por estado;
- notas.

Filtre siempre por periodo y carrera antes de exportar.

## Auditoria

Use los filtros de auditoria para investigar acciones sobre su carrera:

- cambios de notas;
- aprobaciones u observaciones de silabos;
- matriculas y retiros;
- cierres y reaperturas;
- exportaciones de reportes.
# Uso desde frontend Sprint 8.5

- Ingrese por `/login` con una cuenta sintetica de coordinador.
- Use `/oferta` para consultar/gestionar oferta, cursos y asignaciones dentro del alcance permitido por backend.
- Use `/silabos` para aprobar, observar o reabrir silabos con justificacion cuando aplique.
- Use `/reportes` y `/auditoria` para seguimiento academico y trazabilidad filtrada por permisos.
