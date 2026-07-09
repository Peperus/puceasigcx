# Seguridad, permisos y proteccion de datos

PUCEASIG gestiona informacion academica y personal. La seguridad debe validarse en backend y auditarse en acciones criticas.

## Principios

- No guardar credenciales reales en Git.
- No versionar `.env`.
- No usar datos reales de estudiantes, docentes, autoridades o personal administrativo en seeds, tests, mocks o documentacion publica.
- Validar permisos en backend aunque el frontend oculte botones.
- Aplicar minimo privilegio por rol.
- Auditar cambios criticos.
- Proteger archivos cargados y restringir acceso por permisos.

## Roles minimos del MVP

- Administrador general.
- Secretaria academica.
- Coordinador de carrera.
- Docente.
- Estudiante.
- Direccion academica.
- Bienestar universitario, para consulta futura.
- Bibliotecario, para fase posterior.
- Invitado o auditor, si se requiere.

## Permisos iniciales por rol

| Accion | Administrador | Secretaria | Coordinador | Docente | Estudiante |
|---|---|---|---|---|---|
| Configurar catalogos academicos | Si | Parcial | Consulta | No | No |
| Crear usuarios | Si | Parcial | No | No | No |
| Gestionar estudiantes | Si | Si | Consulta | Consulta limitada | Perfil propio |
| Gestionar docentes | Si | Si | Consulta | Perfil propio | No |
| Abrir oferta academica | Si | Si | Si | No | No |
| Matricular estudiantes | Si | Si | Consulta | No | No |
| Crear silabos | No | No | Revisa | Si | No |
| Aprobar silabos | Si | No | Si | No | No |
| Registrar notas | No | No | Excepcional | Si | No |
| Corregir notas cerradas | Si | Con autorizacion | Autoriza | No | No |
| Consultar notas | Si | Si | Si | Sus cursos | Solo propias |
| Exportar actas | Si | Si | Si | Sus cursos | No |
| Ver auditoria | Si | Parcial | Parcial | No | No |

Los permisos exactos deben implementarse con politicas reutilizables y pruebas.

## Autenticacion

El MVP usara autenticacion para API y frontend. La decision inicial es JWT para la API, con scaffold desde Sprint 0 y flujos completos en Sprint 1.

Requisitos:

- ContraseÃ±as hasheadas por Django.
- Rotacion o expiracion razonable de tokens.
- Recuperacion de contraseÃ±a segura cuando se implemente.
- Desactivacion de usuarios sin borrar historial.

## Autorizacion

La autorizacion debe cubrir:

- Permisos por rol.
- Permisos por objeto cuando aplique, por ejemplo docente solo en sus cursos y estudiante solo en sus notas.
- Validacion en views, serializers y services criticos.
- Pruebas para accesos permitidos y denegados.

## Auditoria

Acciones obligatorias de auditar:

- Cambios de notas.
- Reapertura o correccion de notas cerradas.
- Cierre de actas.
- Cambios de silabos y aprobaciones.
- Matriculas, retiros y anulaciones.
- Asignacion o retiro de roles.
- Carga o reemplazo de archivos academicos criticos.

Cada auditoria debe registrar:

- Usuario responsable.
- Accion.
- Modulo.
- Modelo y objeto afectado.
- Datos anteriores y nuevos cuando aplique.
- Justificacion.
- Fecha y hora.
- IP y user agent cuando esten disponibles.

## Datos sensibles

Datos personales y academicos deben tratarse como sensibles:

- Identificacion.
- Correos y telefonos.
- Trayectoria academica.
- Matriculas.
- Notas.
- Silabos y documentos asociados.

Los datos de prueba deben ser sinteticos y no identificables.

## Archivos

- No guardar archivos cargados en Git.
- Validar tipo y tamano.
- Usar almacenamiento compatible con S3.
- Controlar acceso a descargas por permisos.
- Evitar URLs publicas permanentes para documentos sensibles.

## Produccion

En produccion:

- `DEBUG=False`.
- `ALLOWED_HOSTS` restringido.
- CORS restringido al frontend autorizado.
- HTTPS obligatorio.
- Cookies seguras cuando se usen sesiones.
- Secretos desde variables de entorno o gestor de secretos.
- Logs sin credenciales ni datos sensibles innecesarios.

