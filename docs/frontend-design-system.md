# Frontend design system

Este documento se inicia en `S0.5-T2` para registrar el tema visual base del
frontend PUCEASIG. Se ampliara en tickets posteriores con componentes, layouts,
navegacion por rol y reglas de handoff.

## Referencia visual

- Sitio publico revisado: https://www.puce.edu.ec/
- Fecha de revision: 2026-07-09
- Uso permitido en el proyecto: inspiracion visual para paleta, contraste,
  jerarquia y estilo institucional.
- Restriccion: no copiar logos, fotografias, iconos oficiales ni otros assets
  que no existan dentro del repositorio.

## Lectura de identidad

La referencia publica de PUCE usa:

- Azul institucional fuerte como color dominante de marca.
- Turquesa y celeste para acentos, enlaces, iconos y controles secundarios.
- Blanco como superficie principal.
- Grises neutros para texto, bordes y barras de utilidad.
- Botones de borde marcado, tipografia en peso alto y algunos textos en
  uppercase.
- Tarjetas blancas con borde gris claro e iconografia circular azul/turquesa.

Para PUCEASIG, esta identidad se adapta a un ERP academico: menos promocional,
mas denso, legible y estable para trabajo administrativo repetido.

## Tokens centrales

Los tokens viven en `frontend/config/theme.ts` y sus equivalentes CSS viven en
`frontend/app/globals.css`.

### Marca

| Token | Valor | Uso recomendado |
|---|---:|---|
| `brand.primary` | `#003B81` | Sidebar, encabezados, acciones primarias. |
| `brand.primaryDark` | `#002B5C` | Estados activos y fondos de alto contraste. |
| `brand.primarySoft` | `#E7F0FA` | Fondos suaves relacionados con marca. |
| `brand.secondary` | `#00BFD8` | Acentos, foco, indicadores y bordes activos. |
| `brand.secondaryDark` | `#008DA6` | Texto sobre fondos claros y hover secundario. |
| `brand.sky` | `#00A0DD` | Enlaces y estados informativos ligeros. |
| `brand.topbar` | `#40424D` | Barra de utilidad o contexto de sesion. |

### Neutros

| Token | Valor | Uso recomendado |
|---|---:|---|
| `neutral.background` | `#F7F7F7` | Fondo de aplicacion. |
| `neutral.surface` | `#FFFFFF` | Cards, paneles, formularios y tablas. |
| `neutral.surfaceMuted` | `#F3F5F7` | Subpaneles, filtros y estados secundarios. |
| `neutral.border` | `#DDE3EA` | Bordes de cards, inputs y tablas. |
| `neutral.text` | `#1F2933` | Texto principal. |
| `neutral.textMuted` | `#5F6B7A` | Texto secundario. |
| `neutral.textSubtle` | `#7B8794` | Ayudas, metadatos y placeholders. |

### Semanticos

| Token | Valor | Uso recomendado |
|---|---:|---|
| `semantic.success` | `#0F8A5F` | Aprobado, activo, completado. |
| `semantic.warning` | `#B7791F` | Pendiente, observado, en recuperacion. |
| `semantic.danger` | `#B42318` | Error, rechazado, reprobado. |
| `semantic.info` | `#006FBF` | Informacion, consulta, seguimiento. |

## Escala de interfaz

- Tipografia base: stack sans con preferencia por `Open Sans` cuando este
  disponible, con fallback actual de Next.js.
- Radios: `3px`, `4px`, `6px`, `8px`; no usar radios grandes en superficies
  operativas.
- Sombras: sutiles, reservadas para elevacion funcional o foco.
- Alto base de inputs y botones: `42px`.
- Sidebar planificado: `280px`.
- Header planificado: `64px`.

## Reglas de uso

- Usar azul institucional para acciones primarias y estructura de navegacion.
- Usar turquesa para foco, indicadores activos y acentos, no para grandes
  bloques de texto.
- Separar colores semanticos de colores de marca.
- Mantener contraste suficiente: texto blanco sobre azul profundo, texto oscuro
  sobre turquesa o fondos suaves.
- No convertir todas las pantallas en una sola familia azul; los neutros deben
  dominar las superficies de trabajo.
- Mantener logos oficiales fuera del codigo hasta contar con assets autorizados.
