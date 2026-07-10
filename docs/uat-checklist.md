# UAT checklist - MVP Gestion Academica

Use este checklist con datos sinteticos. No registre datos reales durante UAT.

## Preparacion

- [ ] Ambiente piloto disponible con HTTPS.
- [ ] Roles sincronizados con `seed_roles`.
- [ ] Catalogos base cargados con datos sinteticos.
- [ ] Usuarios sinteticos por rol: administrador, secretaria, coordinador,
      docente y estudiante.

## Flujo academico base

- [ ] Crear periodo academico.
- [ ] Crear carrera, modalidad, dominio, plan de estudio y nivel.
- [ ] Crear asignatura con sistema de calificacion S1, S2 o S3.
- [ ] Crear persona sintetica.
- [ ] Crear estudiante asociado a persona.
- [ ] Crear docente asociado a persona.
- [ ] Abrir oferta academica por periodo/carrera/nivel.
- [ ] Crear curso/paralelo activo con cupo.
- [ ] Asignar docente titular al curso.
- [ ] Crear matricula academica del estudiante.
- [ ] Matricular estudiante en el curso/paralelo.

## Silabo

- [ ] Crear silabo para el curso asignado.
- [ ] Registrar descripcion y metodologia.
- [ ] Registrar competencias.
- [ ] Registrar al menos 3 resultados de aprendizaje de carrera.
- [ ] Registrar al menos 3 resultados de aprendizaje de asignatura.
- [ ] Registrar criterios y niveles A/B/C/D.
- [ ] Registrar bibliografia.
- [ ] Registrar planificacion semanal.
- [ ] Finalizar silabo como docente.
- [ ] Enviar silabo a revision.
- [ ] Aprobar silabo como coordinador/secretaria autorizada.
- [ ] Cargar PDF firmado sintetico.

## Notas

- [ ] Abrir libro de calificaciones.
- [ ] Registrar notas S1 por RA/criterio.
- [ ] Registrar notas S2 con un RA en recuperacion y recuperarlo.
- [ ] Registrar notas S3 por practica/evaluacion de parciales.
- [ ] Registrar cuarta evaluacion S3 cuando aplique.
- [ ] Consultar notas como estudiante y verificar que solo vea sus cursos.
- [ ] Consultar notas como secretaria/coordinador con filtros.
- [ ] Cerrar acta.
- [ ] Intentar editar acta cerrada sin reapertura y confirmar bloqueo.
- [ ] Reabrir con justificacion y verificar auditoria.

## Reportes y auditoria

- [ ] Exportar estudiantes por carrera/periodo.
- [ ] Exportar docentes asignados por periodo.
- [ ] Exportar cursos/paralelos activos.
- [ ] Exportar silabos por estado.
- [ ] Exportar notas por curso/modelo/estado.
- [ ] Verificar registros de auditoria para roles, matriculas, silabos, notas,
      cierres/reaperturas y exportaciones.

## Criterios de aceptacion UAT

- [ ] Los roles ven solo la informacion permitida.
- [ ] No hay exposicion cruzada de notas entre estudiantes.
- [ ] Docentes no editan cursos ajenos.
- [ ] Reportes CSV/XLSX descargan correctamente.
- [ ] El MVP puede reiniciarse y conservar datos.
- [ ] Backups y restauracion basica fueron probados.
