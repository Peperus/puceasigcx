# Grading Engine S1/S2/S3

Documento tecnico del motor de calificaciones implementado en Sprint 6.

## Objetivo

El motor calcula notas en escala 0 a 50 para los modelos S1, S2 y S3 sin
depender de hojas Excel. La logica vive en `apps.grading.services` y la
persistencia en `apps.grading.models`.

## Modelos principales

`Gradebook`

- Libro unico por `CourseSection`.
- Referencia el `Syllabus` aprobado del curso.
- Hereda y valida `grading_model` desde `CourseSection.grading_system.code`.
- Estados: borrador, abierto, enviado, cerrado, reabierto y archivado.
- No se crea si el curso no esta activo o el silabo no esta aprobado.

`GradeItem`

- Estructura jerarquica para items calificables.
- En S1/S2 representa RA, criterios, actividades y recuperaciones.
- En S3 representa parciales, actividades practicas, evaluaciones y cuarta evaluacion.
- Conserva orden, ponderacion y nota maxima.

`StudentGradeRecord`

- Nota fuente por estudiante matriculado e item.
- No sustituye snapshots calculados.
- Se invalida el snapshot vigente del estudiante cuando cambia una nota.
- Tiene eliminacion logica mediante estado.

`GradeCalculationSnapshot`

- Resultado calculado reproducible.
- Guarda nota final, letra, estado, regla usada, fuente, usuario y payload detallado.
- Solo un snapshot vigente por estudiante/libro; los anteriores quedan como historial.

## Servicios

Escala:

- `letter_from_score(score)` valida 0 a 50 y devuelve A/B/C/D.
- Si existe configuracion institucional por defecto con niveles, la usa.
- Si no existe configuracion, aplica rangos base: A >=45, B >=40, C >=30, D <30.

Motores:

- `calculate_s1_grade(learning_outcomes, config=None)`
- `calculate_s2_grade(learning_outcomes, config=None)`
- `calculate_s3_grade(partials, final_evaluation_score=None, config=None)`

Persistencia:

- `create_gradebook(...)`
- `open_gradebook(...)`
- `close_gradebook(...)`
- `reopen_gradebook(...)`
- `save_grade_record(...)`
- `delete_grade_record(...)`
- `recalculate_gradebook(...)`

## Reglas S1

S1 calcula cada RA con criterios ponderados. Un criterio puede tener nota directa
o actividades; si tiene actividades se usa su promedio. Los pesos del RA deben
sumar 100%.

Un RA final menor a 30 impide aprobar. Si hay recuperacion, el aporte se calcula
con `s1_recovery_contribution` y se limita por `recovery_cap`, ambos
configurables. Por defecto el aporte es 15% y el cap es 30.

Pendiente institucional: confirmar si un RA no recuperado debe quedar siempre
como `INTERSEMESTRAL` o si algunos casos pasan directo a `REPROBADO`.

## Reglas S2

S2 usa la misma estructura de RA que S1, pero cuenta RDA perdidos antes de
recuperar:

- 0 RDA perdidos: aprobado.
- 1 RDA perdido: recuperacion requerida.
- 2 o mas RDA perdidos: reprobado sin recuperacion ordinaria.

Si la recuperacion del unico RDA perdido es mayor o igual a 30, el RDA queda en
30 y el curso aprueba. Si es menor que 30, el curso reprueba.

## Reglas S3

S3 calcula tres parciales. Cada parcial tiene actividades practicas ponderadas y
una evaluacion. Por defecto practica y evaluacion pesan 50% cada una, pero se
puede configurar `practice_weight` y `evaluation_weight`.

Si el promedio de parciales es mayor o igual a 30, el curso aprueba. Si es menor
que 30, queda en recuperacion requerida. Una cuarta evaluacion mayor o igual a
30 aprueba con nota final 30; una menor que 30 reprueba.

Pendiente institucional: confirmar si la cuarta evaluacion debe capearse siempre
en 30 o si se debe usar una formula ponderada distinta.

## Auditoria

Los cambios de notas se registran con `AuditLog`:

- `grade_record_created`
- `grade_record_updated`
- `grade_record_deleted`
- `gradebook_reopened`
- `gradebook_recalculated`

Los libros cerrados bloquean modificaciones normales. La reapertura exige
justificacion. Una correccion autorizada en libro cerrado tambien exige
justificacion.

## Casos borde probados

- Letras A/B/C/D en bordes 0, 29.99, 30, 39.99, 40, 44.99, 45 y 50.
- Rechazo de notas fuera de rango.
- Validacion de pesos al 100%.
- S1 no aprueba con un RA final menor a 30.
- S1 recupera con cap en 30.
- S2 aprueba con cero RDA perdidos.
- S2 requiere recuperacion con un RDA perdido.
- S2 reprueba con dos o mas RDA perdidos.
- S3 calcula parcial desde practica y evaluacion.
- S3 habilita cuarta evaluacion cuando el promedio es menor a 30.
- Snapshots vigentes e historicos.
- Auditoria de creacion, actualizacion, eliminacion logica y reapertura.
