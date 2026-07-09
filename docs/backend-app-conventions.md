# Convencion de apps Django

Cada app del backend debe mantenerse pequena, modular y alineada con su dominio.

## Estructura base

```text
backend/apps/<app_name>/
+-- __init__.py
+-- admin.py
+-- apps.py
+-- models.py
+-- serializers.py
+-- selectors.py
+-- services.py
+-- urls.py
+-- views.py
+-- migrations/
+-- tests/
```

## Responsabilidades

- `models.py`: entidades persistentes del dominio.
- `serializers.py`: validacion y representacion de entrada/salida API.
- `selectors.py`: consultas reutilizables y lectura optimizada.
- `services.py`: reglas de negocio, transacciones y cambios de estado.
- `views.py`: endpoints DRF del dominio, delgados y con permisos explicitos.
- `urls.py`: routers o rutas del dominio.
- `tests/`: pruebas unitarias e integracion del dominio.

## Reglas

- No mezclar logica de negocio critica dentro de views.
- No crear endpoints de negocio incompletos o falsos.
- Validar permisos en backend aunque el frontend oculte acciones.
- Auditar cambios criticos en notas, silabos, matriculas, roles y cierres.
- Mantener migraciones versionadas.
- Usar datos sinteticos en pruebas.
- No guardar archivos cargados dentro del repositorio.
