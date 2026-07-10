# Sprint 8.5 — Frontend Integration MVP

**Objetivo:** convertir el frontend del MVP de prototipo navegable a UI funcional conectada a las APIs reales de Gestion Academica.
**Salida esperada:** interfaz web usable para validacion piloto institucional, con autenticacion real, permisos por rol, CRUDs academicos, silabos, notas, reportes y auditoria conectados al backend.
**Dependencias:** Sprint 0.5, Sprint 8, `docs/frontend-design-system.md`, `docs/frontend-architecture.md`, `docs/api.md`.

> Este sprint es puente entre el MVP backend/documental y el bloque post-MVP. No implementa admisiones, bienestar, biblioteca, Moodle ni modulos posteriores. La seguridad sigue validandose en backend; el frontend solo mejora la experiencia y consume APIs ya protegidas.

---

## Prompt macro para Codex

```text
Lee PROGRESS.md, docs/project-reference-puceasig.md, docs/frontend-design-system.md,
docs/frontend-architecture.md y SPRINTS/sprint-08-5-frontend-integration-mvp.md.
Trabaja unicamente el ticket activo.
Convierte progresivamente los prototipos frontend del MVP a pantallas funcionales.
No uses datos reales ni credenciales reales.
No construyas modulos post-MVP.
```

---

## Reglas generales del sprint

- Reutilizar layout, tokens y componentes del Sprint 0.5.
- Reemplazar mocks por API real por pantalla, no con reescrituras masivas.
- Mantener estados de carga, error, vacio y permisos denegados.
- Formularios con labels visibles, foco claro, errores de backend y validacion cliente.
- No duplicar reglas criticas de negocio en frontend: mostrar resultados del backend.
- Ocultar acciones por rol no reemplaza permisos backend.
- Mantener texto visible en espanol y datos demo sinteticos.
- Ejecutar `npm run lint`, `npm run typecheck` y `npm run build` en cada ticket que toque frontend.

---

## S8.5-T1 — Cliente API, sesion y autenticacion real

**Tareas**
- Conectar login con `/api/auth/login/`.
- Implementar refresh/logout con endpoints reales.
- Reemplazar selector mock de rol por `/api/me/`.
- Guardar sesion de forma consistente para el MVP.
- Manejar 401, token expirado y cierre de sesion.
- Proteger rutas autenticadas y redirigir a `/login` cuando corresponda.

**Criterios de aceptacion**
- Login funcional contra backend local.
- El header muestra usuario/rol real de `/api/me/`.
- Rutas protegidas rechazan usuarios anonimos.
- No hay credenciales hardcodeadas.

**Verificacion**
```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

---

## S8.5-T2 — Navegacion por rol y shell autenticado funcional

**Tareas**
- Ajustar `AppShell` para consumir la sesion real.
- Filtrar navegacion segun roles reales.
- Implementar estados 401/403 coherentes.
- Eliminar o aislar el selector temporal de rol del prototipo.
- Mantener breadcrumbs, sidebar y header accesibles.

**Criterios de aceptacion**
- Administrador/Secretaria/Coordinador/Docente/Estudiante ven menus correctos.
- Accesos no autorizados muestran 403 y no rompen la app.
- No quedan controles mock de rol visibles en modo funcional.

**Verificacion**
```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

---

## S8.5-T3 — Catalogos academicos funcionales

**Tareas**
- Conectar pantallas de periodos, carreras, asignaturas y paralelos a API real.
- Implementar listados con busqueda, filtros basicos y paginacion si aplica.
- Crear formularios de alta/edicion para campos MVP.
- Mostrar errores de validacion del backend.
- Respetar permisos por rol en acciones visibles.

**Criterios de aceptacion**
- Se pueden consultar y gestionar catalogos base desde UI segun rol.
- Estados de carga, vacio y error estan cubiertos.
- No se usan mocks en estas pantallas funcionales.

**Verificacion**
```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

---

## S8.5-T4 — Personas, estudiantes y docentes funcionales

**Tareas**
- Conectar personas, estudiantes y docentes a APIs reales.
- Implementar formularios de creacion/edicion.
- Soportar busqueda por codigo, identificacion, nombre y correo donde aplique.
- Mostrar perfiles propios para docente/estudiante segun permisos.
- Mantener datos sinteticos en cualquier ejemplo o fixture frontend.

**Criterios de aceptacion**
- Secretaria/Admin gestionan estudiantes y docentes desde UI.
- Docente/estudiante no ven registros fuera de permiso.
- Los errores de unicidad y validacion se muestran con claridad.

**Verificacion**
```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

---

## S8.5-T5 — Oferta academica, asignacion docente y matricula funcionales

**Tareas**
- Conectar oferta, cursos/paralelos, asignaciones docentes y matricula.
- Implementar flujos para abrir curso, asignar docente y matricular estudiante.
- Mostrar cupos, estado de curso y validaciones de periodo/carrera.
- Manejar errores de curso cerrado, duplicados y cupos agotados.

**Criterios de aceptacion**
- Secretaria/Admin pueden completar oferta y matricula desde UI.
- Coordinador ve informacion filtrada por carrera.
- Validaciones backend se reflejan en formularios.

**Verificacion**
```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

---

## S8.5-T6 — Constructor de silabos conectado a API

**Tareas**
- Reemplazar prototipo de silabos por datos reales.
- Conectar secciones: datos base, competencias, RA, criterios, niveles, bibliografia y plan semanal.
- Implementar acciones: finalizar, enviar, aprobar, observar y reabrir.
- Implementar carga de PDF firmado con validacion visual.
- Mostrar estado del silabo y permisos por rol.

**Criterios de aceptacion**
- Docente puede crear/completar/enviar silabo de curso asignado.
- Coordinador/Admin puede aprobar/observar/reabrir segun permisos.
- PDF firmado se carga solo cuando backend lo permite.

**Verificacion**
```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

---

## S8.5-T7 — Carga docente de notas S1/S2/S3 funcional

**Tareas**
- Conectar vista docente de cursos y estudiantes.
- Implementar estructura de gradebook real.
- Implementar carga S1/S2 por RA/criterio.
- Implementar carga S3 por parcial y cuarta evaluacion.
- Mostrar recalculo, snapshot y estados devueltos por backend.
- Bloquear edicion visual cuando el gradebook no este editable.

**Criterios de aceptacion**
- Docente registra notas solo en cursos asignados y abiertos.
- UI muestra errores de escala, permisos y gradebook cerrado.
- Resultados calculados provienen del backend.

**Verificacion**
```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

---

## S8.5-T8 — Consulta estudiantil de notas funcional

**Tareas**
- Conectar pantalla de notas del estudiante a `/api/student/grades/`.
- Mostrar cursos matriculados visibles, nota final, letra, estado y detalle.
- Cubrir estados sin notas, pendiente, recuperacion, aprobado y reprobado.
- Evitar mostrar informacion de otros estudiantes.

**Criterios de aceptacion**
- Estudiante autenticado ve solo sus notas.
- Estados academicos son claros y accesibles.
- Sin mocks en la vista funcional.

**Verificacion**
```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

---

## S8.5-T9 — Reportes y auditoria funcionales

**Tareas**
- Conectar reportes MVP a `/api/reports/mvp/<tipo>/`.
- Implementar filtros por periodo, carrera, modelo y estado cuando aplique.
- Implementar descargas CSV/XLSX.
- Conectar auditoria a `/api/audit/logs/` con filtros.
- Manejar 403 para roles no autorizados.

**Criterios de aceptacion**
- Secretaria/Coordinador/Admin consultan y exportan reportes desde UI.
- Auditoria permite investigar por modulo, accion, usuario, modelo y fecha.
- Estudiante/Docente no ven reportes masivos ni auditoria.

**Verificacion**
```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

---

## S8.5-T10 — Dashboards funcionales por rol

**Tareas**
- Reemplazar metricas mock por endpoints existentes o consultas agregadas disponibles.
- Mantener dashboard por rol con informacion accionable.
- Mostrar pendientes de silabos, notas, cursos y reportes segun rol cuando exista fuente real.
- No inventar datos si el backend no los expone; mostrar estados vacios honestos.

**Criterios de aceptacion**
- Cada rol tiene dashboard sin datos mock criticos.
- La UI distingue datos reales de estados sin informacion.
- No se agregan modulos post-MVP para llenar el dashboard.

**Verificacion**
```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

---

## S8.5-T11 — QA E2E y accesibilidad basica

**Tareas**
- Agregar Playwright o herramienta E2E equivalente.
- Cubrir flujos: login, CRUD academico minimo, matricula, silabo, notas estudiante, reportes y auditoria.
- Verificar 401/403 desde UI.
- Revisar labels, foco visible, contraste, errores y navegacion por teclado basica.

**Criterios de aceptacion**
- Smoke E2E cubre el flujo principal del MVP.
- Build y typecheck siguen verdes.
- No hay solapamientos o texto roto en vistas principales desktop/mobile.

**Verificacion**
```bash
cd frontend
npm run lint
npm run typecheck
npm run build
npm run e2e
```

---

## S8.5-T12 — Documentacion y cierre UI MVP

**Tareas**
- Actualizar `frontend/README.md`.
- Actualizar `docs/frontend-design-system.md` si cambian convenciones.
- Actualizar `docs/user-guide-*.md` con flujos frontend reales.
- Actualizar `docs/uat-checklist.md` para UI conectada.
- Actualizar `PROGRESS.md` y mover cursor a Sprint 9 solo al cerrar UI MVP.

**Criterios de aceptacion**
- Documentacion refleja pantallas funcionales reales.
- UAT puede ejecutarse desde la UI sin depender de API manual.
- Sprint 8.5 queda cerrado con pruebas registradas.

**Verificacion**
```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

---

## Cierre del Sprint 8.5

- [ ] Autenticacion frontend real.
- [ ] Navegacion por rol real.
- [ ] Catalogos, personas, oferta y matricula conectados.
- [ ] Silabos conectados.
- [ ] Notas docente/estudiante conectadas.
- [ ] Reportes y auditoria conectados.
- [ ] Dashboards sin mocks criticos.
- [ ] E2E minimo y accesibilidad basica.
- [ ] Documentacion actualizada.
- [ ] Cursor movido a Sprint 9 solo despues de cerrar UI MVP.
