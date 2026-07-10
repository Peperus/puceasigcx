# Despliegue piloto del MVP

Esta guia describe un despliegue piloto reproducible para PUCEASIG. No incluye
secretos reales; todos los valores sensibles deben venir de variables de entorno
o de un gestor de secretos institucional.

## Componentes

- Backend Django + DRF.
- PostgreSQL.
- Frontend Next.js.
- Almacenamiento de archivos compatible con S3 para silabos firmados y adjuntos.
- Proxy HTTPS externo, por ejemplo Nginx, Caddy o balanceador institucional.

## Variables de entorno backend

Minimas:

```bash
APP_NAME=puceasig
APP_VERSION=0.1.0-mvp
APP_ENVIRONMENT=production
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY=<valor-secreto>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=<dominio-backend>
DATABASE_URL=postgres://<usuario>:<password>@<host>:5432/<db>
CORS_ALLOWED_ORIGINS=https://<dominio-frontend>
CSRF_TRUSTED_ORIGINS=https://<dominio-frontend>
JWT_ACCESS_TOKEN_MINUTES=15
JWT_REFRESH_TOKEN_DAYS=1
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DEFAULT_FROM_EMAIL=no-reply@example.edu
```

Archivos:

```bash
MEDIA_ROOT=/var/lib/puceasig/media
SYLLABUS_SIGNED_FILE_MAX_BYTES=5242880
S3_ENDPOINT_URL=<endpoint-compatible-s3>
S3_ACCESS_KEY_ID=<access-key>
S3_SECRET_ACCESS_KEY=<secret-key>
S3_BUCKET_NAME=<bucket>
S3_REGION_NAME=<region>
```

La implementacion actual usa storage de archivos local de Django por defecto.
Para produccion institucional se recomienda conectar `django-storages` con el
proveedor S3 elegido y mantener `MEDIA_ROOT` solo como fallback local.

## Preparacion backend

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r backend/requirements.txt
.venv/Scripts/python backend/manage.py check --deploy
.venv/Scripts/python backend/manage.py migrate
.venv/Scripts/python backend/manage.py collectstatic --noinput
.venv/Scripts/python backend/manage.py seed_roles
.venv/Scripts/python backend/manage.py seed_academic_catalogs
.venv/Scripts/python backend/manage.py createsuperuser
```

En Linux cambie `.venv/Scripts/python` por `.venv/bin/python`.

## Frontend

```bash
cd frontend
npm ci
npm run lint
npm run typecheck
npm run build
```

Configure:

```bash
NEXT_PUBLIC_API_BASE_URL=https://<dominio-backend>/api
```

## Static y media

- `STATIC_ROOT` apunta a `backend/staticfiles`.
- `MEDIA_ROOT` apunta a `backend/media` en desarrollo.
- En produccion, sirva static desde el proxy o CDN.
- No versionar archivos cargados.
- Para S3, use URLs firmadas o proxy autorizado cuando los documentos sean
  sensibles.

## Backups

Backup PostgreSQL:

```bash
pg_dump "$DATABASE_URL" --format=custom --file=puceasig-mvp.backup
```

Restore:

```bash
createdb puceasig_restore
pg_restore --dbname=puceasig_restore --clean --if-exists puceasig-mvp.backup
```

Archivos:

- Respaldar el bucket S3 o el directorio `MEDIA_ROOT`.
- Conservar backups cifrados.
- Probar restauracion antes del piloto.

## Checklist previo a piloto

- `DEBUG=False`.
- `DJANGO_ALLOWED_HOSTS` restringido.
- CORS restringido al frontend.
- HTTPS activo en proxy.
- `manage.py check --deploy` revisado.
- Roles y seeds sinteticos cargados.
- Superusuario creado fuera de Git.
- Backups probados.
- UAT completado con datos sinteticos.
