import type { RoleCode } from "@/config/roles";
import type { DashboardMetric, PrototypeTableRow } from "@/types/academic";

export const frontendModules = [
  { name: "App Router", description: "Rutas publicas, autenticadas y paginas de error." },
  { name: "Componentes", description: "UI base, feedback, tablas, layout y dashboards." },
  { name: "Configuracion", description: "Navegacion por rol, tema y contratos de pantalla." },
  { name: "Mocks", description: "Datos sinteticos centralizados para prototipos sin API real." },
] as const;

export const mockUserByRole: Record<RoleCode, { name: string; context: string }> = {
  administrator: { name: "Alex Rivera", context: "Administracion general" },
  secretary: { name: "Mara Torres", context: "Secretaria academica" },
  career_coordinator: { name: "Nora Celi", context: "Coordinacion de carrera" },
  teacher: { name: "Tomas Lema", context: "Docencia" },
  student: { name: "Sofia Paredes", context: "Estudiante" },
  academic_director: { name: "Daniel Costa", context: "Direccion academica" },
  wellbeing: { name: "Elena Mora", context: "Apoyo institucional" },
  librarian: { name: "Lina Vega", context: "Biblioteca" },
  guest: { name: "Invitado demo", context: "Consulta" },
};

export const dashboardMetrics: Record<RoleCode, DashboardMetric[]> = {
  administrator: [
    { label: "Periodo activo", value: "2026-A", detail: "Calendario academico configurado", status: "approved" },
    { label: "Carreras activas", value: "6", detail: "Catalogos listos para oferta", status: "approved" },
    { label: "Usuarios pendientes", value: "12", detail: "Requieren revision de rol", status: "recovery" },
    { label: "Eventos auditados", value: "184", detail: "Ultimos 30 dias", status: "ungraded" },
  ],
  secretary: [
    { label: "Matriculas del periodo", value: "438", detail: "Registros sinteticos de prototipo", status: "approved" },
    { label: "Cursos abiertos", value: "42", detail: "Oferta academica 2026-A", status: "approved" },
    { label: "Actas pendientes", value: "9", detail: "Por validacion administrativa", status: "recovery" },
    { label: "Reportes listos", value: "5", detail: "Exportables futuros", status: "ungraded" },
  ],
  career_coordinator: [
    { label: "Silabos en revision", value: "11", detail: "Esperan observacion o aprobacion", status: "recovery" },
    { label: "Docentes asignados", value: "27", detail: "Periodo 2026-A", status: "approved" },
    { label: "RA en riesgo", value: "7", detail: "Alertas de seguimiento academico", status: "risk" },
    { label: "Cursos sin firma", value: "4", detail: "Carga de silabo aprobado pendiente", status: "recovery" },
  ],
  teacher: [
    { label: "Asignaturas asignadas", value: "4", detail: "Dos con notas abiertas", status: "approved" },
    { label: "Silabos borrador", value: "2", detail: "Pendientes de enviar a revision", status: "ungraded" },
    { label: "Notas pendientes", value: "36", detail: "Actividades por registrar", status: "recovery" },
    { label: "RA no alcanzados", value: "5", detail: "Seguimiento de estudiantes", status: "risk" },
  ],
  student: [
    { label: "Asignaturas matriculadas", value: "5", detail: "Periodo 2026-A", status: "approved" },
    { label: "Promedio referencial", value: "41/50", detail: "Dato mock no oficial", status: "approved" },
    { label: "Silabos disponibles", value: "4", detail: "Uno pendiente de firma", status: "recovery" },
    { label: "RA en seguimiento", value: "1", detail: "Revisar retroalimentacion docente", status: "risk" },
  ],
  wellbeing: [
    { label: "Alertas academicas", value: "18", detail: "Consulta limitada por permisos", status: "recovery" },
    { label: "Seguimientos abiertos", value: "7", detail: "Prototipo de apoyo institucional", status: "ungraded" },
    { label: "Reportes permitidos", value: "3", detail: "Sin datos sensibles reales", status: "approved" },
    { label: "Casos cerrados", value: "22", detail: "Historico sintetico", status: "approved" },
  ],
  academic_director: [
    { label: "Silabos por aprobar", value: "6", detail: "Revision academica", status: "recovery" },
    { label: "Cursos activos", value: "42", detail: "Periodo 2026-A", status: "approved" },
    { label: "Actas cerradas", value: "18", detail: "Seguimiento institucional", status: "approved" },
    { label: "Alertas", value: "3", detail: "Requieren atencion", status: "risk" },
  ],
  librarian: [
    { label: "Consultas", value: "0", detail: "Modulo posterior al MVP", status: "ungraded" },
    { label: "Bibliografia", value: "0", detail: "Solo referencias en silabos", status: "ungraded" },
    { label: "Prestamos", value: "0", detail: "No implementado", status: "ungraded" },
    { label: "Alertas", value: "0", detail: "Sin fuente real", status: "ungraded" },
  ],
  guest: [
    { label: "Acceso", value: "Limitado", detail: "Consulta restringida", status: "ungraded" },
    { label: "Datos", value: "0", detail: "Sin permisos", status: "ungraded" },
    { label: "Reportes", value: "0", detail: "No disponible", status: "ungraded" },
    { label: "Acciones", value: "0", detail: "Solo lectura", status: "ungraded" },
  ],
};

export const moduleRows: PrototypeTableRow[] = [
  { id: "EST-001", primary: "Estudiante demo A", secondary: "Carrera de gestion academica", status: "approved", owner: "Secretaria", meta: "Matriculado" },
  { id: "DOC-014", primary: "Docente demo B", secondary: "Metodologia de investigacion", status: "pending", owner: "Coordinacion", meta: "Asignacion pendiente" },
  { id: "SIL-027", primary: "Silabo nueva version", secondary: "Resultados de aprendizaje y rubricas", status: "review", owner: "Docente", meta: "En revision" },
  { id: "NOT-112", primary: "Acta S2", secondary: "Un RA en recuperacion", status: "recovery", owner: "Docente", meta: "Abierta" },
  { id: "AUD-036", primary: "Cambio de rol", secondary: "Permiso academico actualizado", status: "closed", owner: "Administrador", meta: "Auditado" },
];

export const syllabusSteps = [
  "Datos informativos",
  "Docente y codocente",
  "Descripcion de asignatura",
  "Competencias",
  "Resultados de aprendizaje",
  "Rubrica por RA",
  "Pesos por criterios",
  "Bibliografia",
  "Planificacion semanal",
  "Vista previa y estado",
] as const;

export const gradeSystems = [
  {
    code: "S1",
    title: "Resultados de aprendizaje estricto",
    detail: "Tres RA; cualquier RA no alcanzado mantiene la asignatura en no aprobacion.",
    rows: ["RA1: 42/50 alcanzado", "RA2: 28/50 en riesgo", "RA3: 38/50 alcanzado"],
  },
  {
    code: "S2",
    title: "Resultados de aprendizaje con recuperacion",
    detail: "Un RA perdido habilita recuperacion; dos o mas RA perdidos reprueban.",
    rows: ["RA1: 35/50 alcanzado", "RA2: 29/50 recuperacion", "RA3: 41/50 alcanzado"],
  },
  {
    code: "S3",
    title: "Silabo antiguo por parciales",
    detail: "Practica mas evaluacion por parcial, con cuarta evaluacion visual futura.",
    rows: ["Parcial 1: practica 44 / evaluacion 39", "Parcial 2: practica 36 / evaluacion 31", "Parcial 3: pendiente"],
  },
] as const;

export const auditRows = [
  "Apertura de acta de notas con justificacion registrada",
  "Envio de silabo a revision de coordinacion",
  "Cambio de rol institucional auditado",
  "Carga de archivo firmado pendiente de antivirus futuro",
] as const;
