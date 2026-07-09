# Reglas de calificacion S1, S2 y S3

Las reglas de notas deben implementarse como servicios de dominio probados. Este documento describe reglas de negocio, no formulas copiadas literalmente desde hojas de calculo.

## Escala comun

La escala base es de 0 a 50 puntos.

| Letra | Rango | Interpretacion |
|---|---:|---|
| A | 45 a 50 | Alcanzado con excelencia |
| B | 40 a 44.99 | Alcanzado muy bien |
| C | 30 a 39.99 | Alcanzado |
| D | 0 a 29.99 | No alcanzado |

Reglas generales:

- Una nota menor que 0 o mayor que 50 es invalida.
- El logro minimo se alcanza con nota mayor o igual a 30.
- Los pesos deben ser configurables y validados.
- Los calculos deben ser deterministas y cubiertos por pruebas unitarias.
- Las correcciones de notas cerradas requieren permiso especial, justificacion y auditoria.

## Sistema S1: resultados de aprendizaje estricto

S1 trabaja con resultados de aprendizaje, usualmente 3 RDA. Cada RDA contiene criterios ponderados y cada criterio puede contener una o mas actividades.

Implementacion Sprint 6:

- El motor recibe RDA con criterios ponderados y actividades opcionales.
- Si un criterio tiene actividades, usa el promedio de esas actividades.
- Si un criterio no tiene actividades, usa la nota directa del criterio.
- Las ponderaciones de criterios se validan contra 100%.
- La nota final del curso es el promedio de los RDA finales.

### Calculo por criterio

- Si un criterio tiene varias actividades, su nota es el promedio de actividades validas.
- Si el criterio corresponde a una evaluacion unica, se toma la nota registrada.
- Todas las notas se expresan sobre 50.

### Calculo por RDA

La nota del RDA es la suma ponderada de sus criterios.

```text
nota_rda = sum(nota_criterio * peso_criterio)
```

Los pesos del RDA deben sumar 1.0 o 100%, segun la representacion elegida en el modelo.

### Recuperacion S1

Si un RDA queda por debajo de 30, puede registrar recuperacion segun politica institucional configurada.

Regla base:

- Si `nota_rda >= 30`, el RDA queda alcanzado.
- Si `nota_rda < 30`, se calcula recuperacion.
- La recuperacion no debe elevar el RDA recuperado por encima del minimo de aprobacion si la politica indica tope.

Regla conceptual inicial:

```text
si nota_rda >= 30:
    nota_rda_final = nota_rda
si nota_rda < 30:
    nota_rda_final = min(nota_rda + aporte_recuperacion, 30)
```

El aporte inicial de recuperacion queda parametrizado como
`s1_recovery_contribution`, con valor por defecto 15%. El tope tambien es
configurable y por defecto no permite superar 30 en el RDA recuperado.

### Estado final S1

- Si todos los RDA finales son mayores o iguales a 30, el estudiante aprueba.
- Si cualquier RDA final queda por debajo de 30, el estudiante no aprueba la asignatura.
- El estado final puede ser `INTERSEMESTRAL` o `REPROBADO` segun politica institucional.

## Sistema S2: resultados de aprendizaje con tolerancia de un RDA

S2 tambien trabaja con resultados de aprendizaje y criterios ponderados. La diferencia principal esta en la regla de recuperacion.

Implementacion Sprint 6:

- Usa la misma estructura de RDA, criterios y actividades que S1.
- Cuenta RDA perdidos antes de aplicar recuperacion.
- Con un RDA perdido deja el resultado en `RECUPERACION_REQUERIDA` hasta que se registre nota de recuperacion.
- Con dos o mas RDA perdidos reprueba sin recuperacion ordinaria.

### Conteo de RDA perdidos

```text
rda_perdidos = cantidad de RDA con nota < 30
```

Estados iniciales:

- `rda_perdidos == 0`: aprobado.
- `rda_perdidos == 1`: habilita recuperacion.
- `rda_perdidos >= 2`: reprobado sin recuperacion ordinaria.

### Recuperacion S2

Cuando solo un RDA esta perdido:

- Se identifica el RDA perdido.
- Si la nota de recuperacion es mayor o igual a 30, el RDA se marca recuperado con nota final 30.
- Si la nota de recuperacion es menor que 30, el RDA conserva la nota original y el curso queda reprobado.

```text
si rda_perdidos == 1 y nota_recuperacion >= 30:
    nota_rda_final = 30
    estado_final = APROBADO
si rda_perdidos == 1 y nota_recuperacion < 30:
    nota_rda_final = nota_rda_original
    estado_final = REPROBADO
```

La recuperacion S2 no debe producir una nota superior a 30 para el RDA recuperado.

## Sistema S3: silabo antiguo por parciales

S3 trabaja con 3 parciales. Cada parcial combina actividades practicas ponderadas y una evaluacion.

Implementacion Sprint 6:

- Cada parcial recibe actividades practicas ponderadas y una evaluacion.
- Por defecto, practica y evaluacion pesan 50% cada una.
- Las ponderaciones de actividades practicas deben sumar 100%.
- La nota final previa es el promedio de los 3 parciales.
- Si la nota previa es menor que 30, se habilita cuarta evaluacion.

### Practica del parcial

- Cada parcial tiene actividades practicas configurables.
- Los pesos de actividades practicas deben sumar 100%.
- La nota practica se calcula sobre 50.

```text
practica_parcial = sum(nota_actividad * peso_actividad)
```

### Nota del parcial

La nota del parcial combina practica y evaluacion. Regla base:

```text
nota_parcial = promedio(practica_parcial, evaluacion_parcial)
```

Si la institucion define otra ponderacion, debe parametrizarse.

### Nota previa final

```text
promedio_parciales = promedio(parcial_1, parcial_2, parcial_3)
```

Estados:

- Si `promedio_parciales >= 30`, el estudiante aprueba.
- Si `promedio_parciales < 30`, se habilita evaluacion final o cuarta evaluacion segun politica institucional.

### Evaluacion final S3

La cuarta evaluacion debe aplicarse como regla configurable. La implementacion inicial debe registrar:

- Nota previa.
- Nota de cuarta evaluacion.
- Nota final aplicada.
- Estado final.

Ningun calculo S3 debe depender de una hoja Excel en produccion.

Regla inicial Sprint 6: una cuarta evaluacion con nota mayor o igual a 30
aprueba la asignatura con nota final 30. Una cuarta evaluacion menor que 30
deja el curso reprobado.

## Auditoria y bloqueo

Para los tres sistemas:

- Toda nota debe registrar quien la ingreso o modifico.
- Las notas cerradas no se editan sin flujo de reapertura.
- Toda reapertura requiere permiso especial y justificacion.
- El sistema debe conservar datos anteriores y nuevos en auditoria.
- Los cierres de gradebook deben validar notas completas, pesos validos y estados finales calculados.
- Los servicios de Sprint 6 bloquean cambios normales cuando el libro esta cerrado.
- La reapertura de un libro exige justificacion y queda auditada.
- La correccion autorizada sobre un libro cerrado exige justificacion.

## Aspectos pendientes de confirmacion institucional

- Politica exacta para diferenciar `INTERSEMESTRAL` y `REPROBADO` en S1 cuando un RDA no se recupera.
- Formula oficial definitiva del aporte de recuperacion S1 si difiere del 15% inicial.
- Si la cuarta evaluacion S3 siempre capea la nota final en 30 o si puede recalcularse con otra ponderacion.
- Fechas institucionales de apertura/cierre de notas y permisos excepcionales por rol.

## Pruebas minimas esperadas

- Equivalencia de letras A/B/C/D.
- Validacion de escala 0 a 50.
- Validacion de suma de pesos.
- S1 aprueba solo si todos los RDA finales alcanzan 30.
- S1 no aprueba si queda un RDA final menor a 30.
- S2 habilita recuperacion con un solo RDA perdido.
- S2 reprueba con dos o mas RDA perdidos.
- S2 limita recuperacion exitosa a 30.
- S3 calcula parcial desde practica y evaluacion.
- S3 habilita evaluacion final si promedio de parciales es menor a 30.
