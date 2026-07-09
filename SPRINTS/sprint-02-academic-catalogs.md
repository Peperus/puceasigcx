# Sprint 2 — Academic Catalogs & Institutional Setup

**Objetivo:** construir los catálogos académicos e institucionales que sostienen todo el MVP.
**Salida esperada:** periodos, carreras, planes de estudio, niveles, asignaturas, dominios, modalidades y parámetros académicos gestionables.
**Dependencias:** Sprint 1.



> Las pantallas de este sprint deben respetar el layout, navegación por rol, componentes y tokens definidos en `SPRINTS/sprint-00-5-frontend-design-system.md`. La seguridad siempre se valida en backend.

---

## Prompt macro para Codex

```text
Lee PROGRESS.md, docs/project-reference-puceasig.md, docs/database-model.md y SPRINTS/sprint-02-academic-catalogs.md.
Trabaja únicamente el ticket activo.
Prioriza datos maestros normalizados y evita duplicidades.
No implementes estudiantes, docentes, sílabos ni notas en este sprint salvo relaciones mínimas necesarias.
```

---

## S2-T1 — Modelos de periodos académicos

**Tareas**
- Crear `AcademicPeriod` con nombre, código, fecha_inicio, fecha_fin, estado, fecha_inicio_matricula, fecha_fin_matricula.
- Crear estados: borrador, activo, cerrado, archivado.
- Validar solapamiento de periodos activos cuando aplique.
- Admin con filtros por estado y fechas.

**Criterios de aceptación**
- Se puede crear un periodo académico.
- Solo un periodo puede marcarse como principal/actual si se define ese campo.
- Validaciones cubiertas por tests.

**Verificación**
```bash
pytest apps/academic_catalogs/tests/test_periods.py
```

---

## S2-T2 — Carreras, modalidades y dominios

**Tareas**
- Crear modelos:
  - `FacultyOrUnit` o unidad académica si aplica.
  - `Career`.
  - `Modality`.
  - `AcademicDomain`.
- Incluir códigos institucionales, nombre, estado y metadatos.
- Admin con búsqueda por código y nombre.

**Criterios de aceptación**
- Carreras y dominios se gestionan desde Admin.
- No se permiten códigos duplicados.

**Verificación**
```bash
pytest apps/academic_catalogs/tests/test_careers.py
```

---

## S2-T3 — Planes de estudio, niveles y malla

**Tareas**
- Crear `StudyPlan` asociado a carrera.
- Crear `AcademicLevel` o semestre/nivel asociado al plan.
- Crear estructura para malla curricular.
- Preparar relaciones para asignaturas por nivel.

**Criterios de aceptación**
- Un plan tiene varios niveles.
- Los niveles mantienen orden.
- No se duplican niveles por plan.

**Verificación**
```bash
pytest apps/academic_catalogs/tests/test_study_plan.py
```

---

## S2-T4 — Asignaturas y prerrequisitos

**Tareas**
- Crear `Subject` con código, nombre, horas totales, horas contacto docente, horas autónomas, horas práctico-experimentales.
- Asociar asignatura a plan y nivel mediante tabla intermedia `CurriculumSubject`.
- Soportar prerrequisitos mediante relación ManyToMany controlada.
- Admin con filtros por carrera, plan y nivel.

**Criterios de aceptación**
- Se pueden registrar asignaturas por plan/nivel.
- No se duplican códigos dentro de la misma carrera/plan.
- Prerrequisitos funcionan sin ciclos simples.

**Verificación**
```bash
pytest apps/academic_catalogs/tests/test_subjects.py
```

---

## S2-T5 — Parámetros académicos configurables

**Tareas**
- Crear modelo `AcademicSetting` o configuración por periodo/carrera.
- Configurar escala de notas 0–50.
- Configurar niveles de logro A/B/C/D.
- Configurar umbral de aprobación 30.
- Preparar configuración de modelos de calificación S1/S2/S3 como catálogo, no motor todavía.

**Criterios de aceptación**
- Las reglas base se pueden consultar desde servicios.
- No hay umbrales hardcodeados en vistas.
- Tests verifican lectura de configuración.

**Verificación**
```bash
pytest apps/academic_catalogs/tests/test_academic_settings.py
```

---

## S2-T6 — API y Admin de catálogos

**Tareas**
- Crear serializers y ViewSets de solo lectura o CRUD protegido según rol.
- Permitir que Secretaría/Administrador gestionen catálogos.
- Coordinador puede consultar catálogos de su carrera.
- Documentar endpoints en `docs/api.md`.

**Criterios de aceptación**
- Endpoints protegidos por permisos.
- Admin es usable con filtros y búsqueda.
- API documentada.

**Verificación**
```bash
pytest apps/academic_catalogs/tests/test_catalog_api.py
```

---

## S2-T7 — Seeds sintéticos mínimos

**Tareas**
- Crear comando `seed_academic_catalogs` con datos sintéticos.
- Incluir carreras de ejemplo genéricas o datos institucionales no sensibles si fueron autorizados.
- Evitar nombres de estudiantes/docentes reales.

**Criterios de aceptación**
- Seed es idempotente.
- No contiene datos personales reales.
- Permite probar flujos posteriores.

**Verificación**
```bash
python manage.py seed_academic_catalogs
python manage.py seed_academic_catalogs
pytest apps/academic_catalogs/tests/test_seeds.py
```

---

## Cierre del Sprint 2

- [ ] Catálogos académicos funcionales.
- [ ] Configuración base de escala y modelos de notas documentada.
- [ ] `docs/database-model.md` y `docs/api.md` actualizados.
- [ ] Cursor a **Sprint 3 / S3-T1**.
