# Sprint 1 — Authentication, Roles & Access Control

**Objetivo:** implementar identidad, autenticación, perfiles institucionales, roles y permisos base del MVP.
**Salida esperada:** usuarios institucionales autenticándose vía API/Admin, con roles PUCEASIG y permisos iniciales aplicados.
**Dependencias:** Sprint 0 y Sprint 0.5.



> Las pantallas de este sprint deben respetar el layout, navegación por rol, componentes y tokens definidos en `SPRINTS/sprint-00-5-frontend-design-system.md`. La seguridad siempre se valida en backend.

---

## Prompt macro para Codex

```text
Lee PROGRESS.md, docs/project-reference-puceasig.md, docs/security.md y SPRINTS/sprint-01-auth-roles.md.
Trabaja únicamente el ticket activo.
Implementa autenticación y roles institucionales para PUCEASIG, no roles SaaS comerciales.
No uses datos reales ni credenciales reales.
Toda autorización debe validarse en backend, no solo ocultarse en la interfaz.
```

---

## S1-T1 — Custom User institucional

**Tareas**
- Implementar `User` personalizado en `accounts` usando email institucional como identificador principal.
- Campos mínimos: email, names, last_names, identification, phone opcional, is_active, is_staff, is_superuser.
- Definir `AUTH_USER_MODEL` antes de migraciones definitivas.
- Crear `UserProfile` con relación a persona institucional cuando corresponda.
- Registrar modelos en Django Admin.

**Criterios de aceptación**
- Migraciones limpias desde base vacía.
- Se puede crear superusuario.
- Admin muestra usuarios con filtros y búsqueda.

**Verificación**
```bash
python manage.py makemigrations accounts
python manage.py migrate
python manage.py createsuperuser
pytest apps/accounts/tests/test_user_model.py
```

---

## S1-T2 — Roles institucionales base

**Tareas**
- Crear roles/grupos iniciales:
  - Administrador
  - Secretaría
  - Coordinador de carrera
  - Docente
  - Estudiante
  - Bienestar
  - Bibliotecario
  - Invitado/Consulta
- Crear data migration o comando seed seguro para grupos y permisos base.
- Documentar matriz de permisos en `docs/security.md`.

**Criterios de aceptación**
- Los roles se crean de forma idempotente.
- No se duplican grupos al ejecutar el seed varias veces.
- Matriz de permisos documentada.

**Verificación**
```bash
python manage.py seed_roles
python manage.py shell -c "from django.contrib.auth.models import Group; print(Group.objects.count())"
pytest apps/accounts/tests/test_roles_seed.py
```

---

## S1-T3 — Login JWT y refresh

**Tareas**
- Implementar endpoints:
  - `POST /api/auth/login/`
  - `POST /api/auth/refresh/`
  - `POST /api/auth/logout/` si se usa blacklist.
- Validar usuario activo.
- Incluir claims mínimos: user_id, email, roles.
- Agregar tests de login correcto, contraseña incorrecta, usuario inactivo y refresh.

**Criterios de aceptación**
- Login devuelve access y refresh.
- Usuario inactivo no puede ingresar.
- Tokens incluyen información necesaria sin exponer datos sensibles.

**Verificación**
```bash
pytest apps/accounts/tests/test_auth_jwt.py
```

---

## S1-T4 — Recuperación de contraseña segura

**Tareas**
- Implementar flujo de recuperación:
  - `POST /api/auth/password/reset/`
  - `POST /api/auth/password/reset/confirm/`
- En desarrollo, envío por consola o backend de email local.
- En producción, dejar preparado SMTP por variables de entorno.
- Tokens con expiración.

**Criterios de aceptación**
- Token válido permite cambiar contraseña.
- Token vencido o inválido se rechaza.
- No se revela si un correo existe o no.

**Verificación**
```bash
pytest apps/accounts/tests/test_password_reset.py
```

---

## S1-T5 — Permission classes DRF por rol

**Tareas**
- Crear clases reutilizables en `core/permissions.py`:
  - `IsAdministrator`
  - `IsSecretary`
  - `IsCareerCoordinator`
  - `IsTeacher`
  - `IsStudent`
  - `IsAcademicStaff`
- Crear helpers para validación de roles.
- Crear endpoints de prueba protegidos o tests directos.

**Criterios de aceptación**
- Usuario sin rol recibe 403 en endpoints restringidos.
- Usuario con rol correcto accede.
- Permisos se prueban en backend.

**Verificación**
```bash
pytest apps/core/tests/test_permissions.py
```

---

## S1-T6 — Perfil actual y sesión institucional

**Tareas**
- Implementar `GET /api/me/` con datos del usuario, roles y perfil asociado.
- Implementar `PATCH /api/me/` solo para campos editables permitidos.
- Evitar que el usuario modifique su rol o permisos desde este endpoint.

**Criterios de aceptación**
- Usuario autenticado consulta su perfil.
- Usuario anónimo recibe 401.
- Campos protegidos no se pueden modificar.

**Verificación**
```bash
pytest apps/accounts/tests/test_me.py
```

---

## S1-T7 — Auditoría base de autenticación y roles

**Tareas**
- Crear modelo `AuditLog` mínimo o preparar app `audit`.
- Registrar eventos críticos: login fallido, cambio de contraseña, cambio de rol, creación de usuario.
- Exponer solo en Admin inicialmente.

**Criterios de aceptación**
- Eventos críticos quedan registrados.
- AuditLog no permite edición casual desde roles no autorizados.

**Verificación**
```bash
pytest apps/audit/tests/test_auth_audit.py
```

---

## Cierre del Sprint 1

- [ ] Login JWT funcionando.
- [ ] Roles institucionales creados.
- [ ] Permisos base probados.
- [ ] `docs/security.md` actualizado.
- [ ] `PROGRESS.md` actualizado y cursor a **Sprint 2 / S2-T1**.
