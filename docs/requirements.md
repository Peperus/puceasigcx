# Requerimientos del MVP

Este documento resume los requerimientos funcionales y no funcionales del MVP de PUCEASIG. El detalle extendido vive en `docs/project-reference-puceasig.md`.

## Requerimientos funcionales

### Identidad, roles y acceso

- Autenticar usuarios institucionales.
- Asociar usuarios con persona, estudiante o docente.
- Gestionar roles minimos: administrador general, secretaria academica, coordinador de carrera, docente, estudiante y direccion academica.
- Aplicar permisos por modulo y, cuando corresponda, por objeto.
- Desactivar usuarios sin eliminar historial academico.

### Catalogos academicos

- Gestionar periodos academicos.
- Gestionar carreras, planes de estudio, niveles o semestres.
- Gestionar asignaturas, paralelos, dominios y parametros institucionales.
- Mantener estados configurables para cursos, matriculas, silabos y actas.

### Personas, estudiantes y docentes

- Registrar datos personales basicos con un modelo central de persona.
- Crear, editar, consultar y desactivar estudiantes.
- Crear, editar, consultar y desactivar docentes.
- Asociar estudiantes a carrera, plan y periodo de ingreso.
- Asociar docentes a cursos/paralelos como titular, codocente o invitado.

### Oferta academica y matricula

- Abrir cursos/paralelos por periodo academico.
- Configurar cupos, aula y estado del curso.
- Matricular estudiantes en cursos.
- Registrar retiros, anulaciones y cambios de estado.

### Silabos

- Crear silabos por curso/paralelo.
- Soportar silabo nueva version y silabo antiguo.
- Registrar competencias, resultados de aprendizaje, criterios, rubricas, bibliografia y planificacion semanal.
- Gestionar estados: borrador, enviado, observado, aprobado, firmado, cerrado y archivado.
- Cargar silabo firmado en almacenamiento externo compatible con S3.
- Descargar o generar vista imprimible.

### Notas

- Configurar el modelo de calificacion por curso: S1, S2 o S3.
- Registrar notas por criterio, actividad, resultado de aprendizaje o parcial.
- Calcular notas, letras y estados finales automaticamente.
- Gestionar recuperaciones segun el modelo configurado.
- Bloquear cambios fuera de fecha o sin permiso.
- Auditar todo cambio critico de notas.

### Reportes y consultas

- Permitir al estudiante consultar sus propias notas y silabos disponibles.
- Permitir a docentes consultar sus cursos y registrar notas autorizadas.
- Permitir a coordinacion y secretaria consultar reportes academicos.
- Exportar listados, actas y reportes basicos.

### Auditoria

- Registrar usuario, accion, modulo, objeto afectado, datos anteriores, datos nuevos, motivo, fecha, IP y agente de usuario cuando aplique.
- Auditar especialmente notas, silabos, matriculas, roles y cierres academicos.

## Requerimientos no funcionales

### Seguridad

- No almacenar secretos reales en Git.
- Usar variables de entorno para credenciales y configuracion sensible.
- Proteger datos personales y academicos.
- Restringir CORS en entornos no locales.
- Aplicar HTTPS y cookies seguras en produccion.
- Validar archivos cargados por tipo, tamano y permisos.

### Integridad de datos

- Evitar duplicar personas, estudiantes y docentes.
- Aplicar restricciones de unicidad para codigos institucionales.
- Validar escalas de notas de 0 a 50.
- Validar que pesos y ponderaciones sean consistentes.
- No permitir actas cerradas con notas incompletas salvo autorizacion explicita.

### Mantenibilidad

- Mantener apps Django separadas por dominio.
- Usar services/selectors para reglas de negocio y consultas complejas.
- Mantener migraciones versionadas.
- Crear pruebas unitarias para los calculos S1, S2 y S3.
- Actualizar documentacion cuando cambien reglas o modelos.

### Rendimiento

- Paginacion en listados grandes.
- Indices en campos de busqueda frecuentes.
- Consultas optimizadas para reportes.
- Exportaciones asincronas si el volumen lo requiere.
- Cache para catalogos estables cuando sea necesario.

### Usabilidad

- Interfaz clara para docentes, estudiantes, secretaria y coordinacion.
- Formularios con labels, errores comprensibles y foco visible.
- Tablas filtrables para listados academicos.
- Flujos guiados para silabos y registro de notas.
- Diseno responsive desde Sprint 0.5.
