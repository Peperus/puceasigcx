# Guia de usuario MVP - Estudiante

## Objetivo

Consultar informacion academica propia: cursos matriculados, notas visibles y
estado de resultados.

## Inicio de sesion

1. Ingrese con su cuenta institucional.
2. Abra Dashboard estudiante o Notas estudiante.
3. Si no puede ingresar, use el flujo de recuperacion de contrasena o contacte a
   soporte academico.

## Consulta de notas

1. Abra Notas estudiante.
2. Revise cada curso/paralelo matriculado.
3. Consulte nota final, letra, estado y detalle disponible.
4. Si un libro de calificaciones esta en borrador, no aparecera hasta estar
   visible segun el flujo academico.

## Estados frecuentes

- Aprobado: alcanza el minimo requerido.
- Recuperacion requerida: debe cumplir el proceso definido por la carrera.
- Intersemestral o reprobado: no alcanza la regla del modelo aplicado.
- Pendiente: existen notas incompletas o calculo provisional.

## Privacidad

El estudiante solo puede ver su propia informacion. No puede consultar reportes
masivos, notas de otros estudiantes ni auditoria.
# Uso desde frontend Sprint 8.5

- Ingrese por `/login` con una cuenta sintetica de estudiante.
- Use `/dashboard` para ver el resumen disponible del rol.
- Use `/notas/estudiante` para consultar solo sus cursos visibles, nota final, letra y estado calculado.
- Si no existen snapshots o notas publicadas, la pantalla muestra estado pendiente sin inventar datos.
