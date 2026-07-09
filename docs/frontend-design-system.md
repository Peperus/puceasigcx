# Frontend design system

Documento de handoff del Sprint 0.5 para el frontend PUCEASIG. La base visual
queda lista para que los sprints funcionales implementen autenticacion, permisos,
catalogos, silabos, notas, reportes y auditoria sobre una experiencia coherente.

## Stack frontend

- Next.js App Router + TypeScript.
- Tailwind CSS con tokens CSS definidos en `frontend/app/globals.css`.
- Tema central en `frontend/config/theme.ts`.
- Iconografia con `lucide-react`.
- Componentes propios equivalentes a shadcn/ui, ubicados en `frontend/components`.
- Mocks sinteticos centralizados en `frontend/lib/mock-data.ts`.
- Cliente API preparado en `frontend/lib/api.ts`, sin consumo real todavia.

## Estructura

```text
frontend/
├── app/
│   ├── (auth)/
│   ├── (dashboard)/
│   ├── 403/
│   ├── error.tsx
│   ├── globals.css
│   ├── layout.tsx
│   ├── not-found.tsx
│   └── page.tsx
├── components/
│   ├── dashboard/
│   ├── feedback/
│   ├── layout/
│   ├── prototypes/
│   └── ui/
├── config/
├── lib/
└── types/
```

## Tema visual

La referencia visual publica revisada fue `https://www.puce.edu.ec/` el
2026-07-09. Solo se toma inspiracion de color, contraste y tono institucional;
no se copian logos, fotografias ni assets oficiales.

Tokens principales:

| Uso | Token | Valor |
|---|---|---:|
| Marca primaria | `brand.primary` | `#003B81` |
| Marca profunda | `brand.primaryDark` | `#002B5C` |
| Fondo suave de marca | `brand.primarySoft` | `#E7F0FA` |
| Acento turquesa | `brand.secondary` | `#00BFD8` |
| Acento oscuro | `brand.secondaryDark` | `#008DA6` |
| Informativo visual | `brand.sky` | `#00A0DD` |
| Superficie | `neutral.surface` | `#FFFFFF` |
| Fondo app | `neutral.background` | `#F7F7F7` |
| Borde | `neutral.border` | `#DDE3EA` |

Semanticos:

- Exito: `#0F8A5F`.
- Advertencia: `#B7791F`.
- Error: `#B42318`.
- Informacion: `#006FBF`.

Reglas:

- Usar azul institucional para estructura y acciones primarias.
- Usar turquesa en foco, indicadores activos y acentos puntuales.
- Mantener superficies de trabajo mayormente blancas o grises neutras.
- Radios entre `3px` y `8px`; no usar cards con radios grandes.
- Inputs y botones parten de `42px` de alto.
- No usar assets oficiales hasta que existan dentro del repositorio.

## Componentes disponibles

UI base en `frontend/components/ui`:

- `Button`
- `Input`
- `Textarea`
- `Select`
- `Checkbox`
- `Label`
- `Card`
- `Badge` y `StatusBadge`
- `Table`
- `Dialog`
- `Alert`
- `Tabs`
- `Breadcrumbs`
- `Pagination`

Feedback en `frontend/components/feedback`:

- `EmptyState`
- `LoadingState`
- `ErrorState`

Layout y prototipos:

- `AppShell`: layout autenticado con sidebar, header, breadcrumb indirecto y selector temporal de rol.
- `MetricCard`: tarjeta reusable de dashboard.
- `ModulePage`: wireframe reusable para modulos CRUD/listado.
- `DashboardPage`: dashboard por rol con indicadores mock.
- `SyllabusBuilder`: flujo visual del constructor de silabos.
- `GradesPrototype`: estructura visual de notas S1/S2/S3.

Estados academicos soportados en badges:

- Borrador, pendiente, en revision, aprobado, rechazado, cerrado.
- Requiere correccion y firmado para silabos.
- Aprobado, reprobado, recuperacion, sin calificar y en riesgo para notas.

## Navegacion por rol

La navegacion vive en `frontend/config/navigation.ts` y filtra elementos segun
`RoleCode` de `frontend/config/roles.ts`.

Roles contemplados:

- Administrador.
- Secretaria academica.
- Coordinador de carrera.
- Docente.
- Estudiante.
- Bienestar / apoyo institucional.

El selector de rol del header es solo un artefacto de prototipo. En Sprint 1 debe
reemplazarse por el rol devuelto desde `/api/me/` o el endpoint de perfil que se
defina. La UI nunca debe ser la unica barrera de permisos; el backend debe
validar permisos en views, serializers y servicios criticos.

## Rutas prototipo

Publicas:

- `/login`
- `/recuperar`
- `/seguridad`
- `/403`
- `not-found.tsx`
- `error.tsx`

Autenticadas:

- `/dashboard`
- `/dashboard/admin`
- `/dashboard/secretaria`
- `/dashboard/coordinador`
- `/dashboard/docente`
- `/dashboard/estudiante`
- `/estudiantes`
- `/docentes`
- `/roles`
- `/periodos`
- `/carreras`
- `/asignaturas`
- `/paralelos`
- `/oferta`
- `/matricula`
- `/silabos`
- `/silabos/constructor`
- `/silabos/carga-firmado`
- `/notas`
- `/notas/carga-docente`
- `/notas/estudiante`
- `/notas/secretaria`
- `/reportes`
- `/auditoria`

## Datos mock

Todos los datos de prototipo deben ser sinteticos y vivir en
`frontend/lib/mock-data.ts`. No usar nombres reales de estudiantes, docentes,
autoridades ni personal administrativo.

Los mocks actuales cubren:

- Usuario ficticio por rol.
- Metricas por dashboard.
- Filas genericas de modulos.
- Pasos del constructor de silabos.
- Sistemas de notas S1, S2 y S3.
- Eventos sinteticos de auditoria.

## Reemplazo por API real

Cuando un sprint funcional conecte una pantalla:

1. Mantener el componente visual si ya resuelve layout, estados y accesibilidad.
2. Crear tipos de respuesta en `frontend/types`.
3. Implementar llamadas en `frontend/lib/api.ts` o helpers especificos.
4. Reemplazar solo el origen de datos del prototipo.
5. Conservar estados de carga, error y vacio.
6. Validar permisos en backend; el filtrado del menu solo mejora la experiencia.
7. Retirar o aislar mocks que ya no apliquen.

## Convenciones

- Componentes de UI genericos en `components/ui`.
- Estados transversales en `components/feedback`.
- Estructura autenticada en `components/layout`.
- Componentes especificos de prototipo en `components/prototypes`.
- Configuracion institucional en `config`.
- Datos mock en `lib/mock-data.ts`.
- Tipos compartidos en `types`.
- Texto visible en espanol y sin datos reales.
- Formularios con `Label` asociado a cada control.
- Acciones criticas futuras deben mostrar estados claros y luego auditarse en backend.

## Accesibilidad minima

- Usar labels visibles en formularios.
- Mantener foco visible con tokens globales.
- No depender solo del color para estados; usar texto de badge.
- Mantener contraste alto en sidebar, botones y alertas.
- Proveer paginas 403, 404 y error general.
- No ocultar errores de validacion cuando se implementen formularios reales.

## Checklist para sprints frontend

- Reutilizar `AppShell`, `ModulePage`, `Table`, `StatusBadge`, `Alert` y estados de feedback.
- Confirmar que todo dato demo sea sintetico.
- Agregar permisos backend antes de tratar una pantalla como funcional.
- Mantener mocks separados de integraciones reales.
- Ejecutar `npm run lint`, `npm run typecheck` y `npm run build`.
- Actualizar esta documentacion si cambia un componente, flujo o convencion.

## Verificaciones del Sprint 0.5

Ejecutadas el 2026-07-09:

```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

Notas: `npm install lucide-react` mantiene el reporte existente de 2
vulnerabilidades moderadas transitivas; no se aplico `npm audit fix --force`
porque puede introducir cambios incompatibles fuera del alcance del sprint.
