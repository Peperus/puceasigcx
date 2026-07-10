"use client";

import { Download, RefreshCcw, Search } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";
import { apiRequest, downloadFile, listItems, type ListResponse } from "@/lib/api";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { Table } from "@/components/ui/table";
import { PageHeader } from "@/components/prototypes/page-header";
import { LoadingState } from "@/components/feedback/loading-state";
import { ErrorState } from "@/components/feedback/error-state";
import { EmptyState } from "@/components/feedback/empty-state";

type ReportType = "students" | "teachers" | "courses" | "syllabi" | "grades";
type Tab = ReportType | "audit";
type Row = Record<string, unknown> & { id?: string | number };

const reportLabels: Record<ReportType, string> = {
  students: "Estudiantes",
  teachers: "Docentes",
  courses: "Cursos",
  syllabi: "Silabos",
  grades: "Notas",
};

function text(value: unknown) {
  if (value === null || value === undefined || value === "") return "-";
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

function columnsFor(rows: Row[], tab: Tab) {
  if (tab === "audit") return ["created_at", "user_email", "module", "action", "model_name", "object_id", "reason"];
  if (tab === "grades") return ["student_code", "student_name", "subject_code", "subject_name", "grading_model", "final_score", "final_letter", "final_status"];
  const first = rows[0] ?? {};
  return Object.keys(first).filter((key) => !["payload", "previous_data", "new_data"].includes(key)).slice(0, 8);
}

export function ReportsWorkspace({ initialTab = "students" }: { initialTab?: Tab }) {
  const [tab, setTab] = useState<Tab>(initialTab);
  const [period, setPeriod] = useState("");
  const [career, setCareer] = useState("");
  const [status, setStatus] = useState("");
  const [gradingModel, setGradingModel] = useState("");
  const [query, setQuery] = useState("");
  const [rows, setRows] = useState<Row[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const params = useMemo(() => ({
    period,
    career,
    status,
    grading_model: gradingModel,
    search: query,
    user_email: query,
    module: tab === "audit" ? status : "",
  }), [career, gradingModel, period, query, status, tab]);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      if (tab === "audit") {
        const payload = await apiRequest<ListResponse<Row>>("/audit/logs/", { params });
        setRows(listItems(payload));
      } else if (tab === "grades") {
        setRows(await apiRequest<Row[]>("/reports/grades/", { params }));
      } else {
        const payload = await apiRequest<{ results: Row[]; count: number }>(`/reports/mvp/${tab}/`, { params });
        setRows(payload.results);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo cargar el reporte.");
    } finally {
      setLoading(false);
    }
  }, [params, tab]);

  useEffect(() => {
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);

  async function exportReport(format: "csv" | "xlsx") {
    try {
      if (tab === "audit") {
        setError("La auditoria del MVP se consulta en pantalla; exportacion no expuesta por backend.");
        return;
      }
      const endpoint = tab === "grades" ? "/reports/grades/export/" : `/reports/mvp/${tab}/`;
      await downloadFile(endpoint, `puceasig-${tab}.${format}`, { ...params, file_format: format });
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo exportar.");
    }
  }

  const columns = columnsFor(rows, tab);

  return (
    <>
      <PageHeader
        title={tab === "audit" ? "Auditoria" : "Reportes academicos"}
        description="Reportes y trazabilidad conectados a endpoints protegidos del backend."
      />
      <div className="mb-4 flex flex-wrap gap-2">
        {(["students", "teachers", "courses", "syllabi", "grades"] as ReportType[]).map((type) => (
          <Button key={type} onClick={() => setTab(type)} type="button" variant={tab === type ? "primary" : "outline"}>
            {reportLabels[type]}
          </Button>
        ))}
        <Button onClick={() => setTab("audit")} type="button" variant={tab === "audit" ? "primary" : "outline"}>
          Auditoria
        </Button>
      </div>
      <Card className="mb-4">
        <form className="grid gap-3 md:grid-cols-2 xl:grid-cols-[1fr_1fr_1fr_1fr_auto]" onSubmit={(event) => {
          event.preventDefault();
          void load();
        }}>
          <div>
            <Label htmlFor="period-filter">Periodo</Label>
            <Input id="period-filter" onChange={(event) => setPeriod(event.target.value)} placeholder="Codigo o ID" value={period} />
          </div>
          <div>
            <Label htmlFor="career-filter">Carrera</Label>
            <Input id="career-filter" onChange={(event) => setCareer(event.target.value)} placeholder="ID carrera" value={career} />
          </div>
          <div>
            <Label htmlFor="status-filter">{tab === "audit" ? "Modulo" : "Estado"}</Label>
            <Input id="status-filter" onChange={(event) => setStatus(event.target.value)} placeholder={tab === "audit" ? "grading, syllabus..." : "approved, closed..."} value={status} />
          </div>
          <div>
            <Label htmlFor="model-filter">Modelo</Label>
            <Select id="model-filter" onChange={(event) => setGradingModel(event.target.value)} value={gradingModel}>
              <option value="">Todos</option>
              <option value="S1">S1</option>
              <option value="S2">S2</option>
              <option value="S3">S3</option>
            </Select>
          </div>
          <div className="flex items-end gap-2">
            <Button type="submit"><Search size={16} /> Consultar</Button>
            <Button onClick={() => void load()} type="button" variant="ghost"><RefreshCcw size={16} /></Button>
          </div>
        </form>
        <div className="mt-3">
          <Label htmlFor="free-search">Busqueda libre</Label>
          <Input id="free-search" onChange={(event) => setQuery(event.target.value)} placeholder="Correo usuario, texto o filtro adicional" value={query} />
        </div>
      </Card>
      <div className="mb-4 flex flex-wrap gap-2">
        <Button disabled={tab === "audit"} onClick={() => void exportReport("csv")} type="button" variant="outline"><Download size={16} /> CSV</Button>
        <Button disabled={tab === "audit"} onClick={() => void exportReport("xlsx")} type="button" variant="outline"><Download size={16} /> XLSX</Button>
      </div>
      {loading ? <LoadingState label="Cargando reporte" /> : null}
      {error ? <ErrorState title="Reporte no disponible" description={error} /> : null}
      {!loading && !rows.length && !error ? <EmptyState title="Sin resultados" description="La API no devolvio registros para estos filtros." /> : null}
      {rows.length ? (
        <Table headers={columns.map((column) => column.replaceAll("_", " "))}>
          {rows.map((row, index) => (
            <tr key={String(row.id ?? index)}>
              {columns.map((column) => (
                <td className="px-4 py-3 align-top text-sm" key={column}>
                  {column.includes("status") || column === "action" || column === "module" ? (
                    <Badge>{text(row[column])}</Badge>
                  ) : (
                    text(row[column])
                  )}
                </td>
              ))}
            </tr>
          ))}
        </Table>
      ) : null}
      <div className="mt-4">
        <Alert tone="info">Los accesos 403 se muestran como error de API y el backend sigue siendo la fuente de autorizacion.</Alert>
      </div>
    </>
  );
}
