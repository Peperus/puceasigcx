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

El porcentaje o formula exacta del aporte debe quedar parametrizado, no hardcodeado.

### Estado final S1

- Si todos los RDA finales son mayores o iguales a 30, el estudiante aprueba.
- Si cualquier RDA final queda por debajo de 30, el estudiante no aprueba la asignatura.
- El estado final puede ser `INTERSEMESTRAL` o `REPROBADO` segun politica institucional.

## Sistema S2: resultados de aprendizaje con tolerancia de un RDA

S2 tambien trabaja con resultados de aprendizaje y criterios ponderados. La diferencia principal esta en la regla de recuperacion.

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

## Auditoria y bloqueo

Para los tres sistemas:

- Toda nota debe registrar quien la ingreso o modifico.
- Las notas cerradas no se editan sin flujo de reapertura.
- Toda reapertura requiere permiso especial y justificacion.
- El sistema debe conservar datos anteriores y nuevos en auditoria.
- Los cierres de gradebook deben validar notas completas, pesos validos y estados finales calculados.

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
