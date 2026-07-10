"use client";

import Link from "next/link";
import { ClipboardEdit, GraduationCap, RefreshCcw, Save, ShieldCheck } from "lucide-react";
import { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api";
import { useAuth } from "@/lib/auth";
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

type Gradebook = {
  id: number;
  subject_code: string;
  subject_name: string;
  parallel: string;
  grading_model: string;
  status: string;
  enrolled_count: number;
};

type GradeStudent = {
  id: number;
  student_code: string;
  student_name: string;
  status: string;
};

type GradeItem = {
  id: number;
  name: string;
  item_type: string;
  weight: string | null;
  children: GradeItem[];
};

type StudentGrade = {
  course_enrollment_id: number;
  gradebook_id: number;
  period_code: string;
  subject_code: string;
  subject_name: string;
  parallel: string;
  grading_model: string;
  gradebook_status: string;
  snapshot: null | {
    final_score: string;
    final_letter: string;
    final_status: string;
    recovery_required: boolean;
    payload: unknown;
  };
};

function flattenItems(items: GradeItem[]): GradeItem[] {
  return items.flatMap((item) => [item, ...flattenItems(item.children ?? [])]);
}

function finalTone(status: string | undefined) {
  const normalized = (status ?? "").toLowerCase();
  if (normalized.includes("approved") || normalized.includes("aprobado")) return "success";
  if (normalized.includes("recover") || normalized.includes("recuper")) return "warning";
  if (normalized.includes("failed") || normalized.includes("reprob")) return "danger";
  return "neutral";
}

export function GradesWorkspace({ mode = "overview" }: { mode?: "overview" | "teacher" | "student" | "secretary" }) {
  const { role } = useAuth();
  const [gradebooks, setGradebooks] = useState<Gradebook[]>([]);
  const [selected, setSelected] = useState("");
  const [students, setStudents] = useState<GradeStudent[]>([]);
  const [items, setItems] = useState<GradeItem[]>([]);
  const [courseEnrollment, setCourseEnrollment] = useState("");
  const [gradeItem, setGradeItem] = useState("");
  const [score, setScore] = useState("");
  const [studentGrades, setStudentGrades] = useState<StudentGrade[]>([]);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        if (mode === "student" || (mode === "overview" && role === "student")) {
          setStudentGrades(await apiRequest<StudentGrade[]>("/student/grades/"));
        } else {
          const payload = await apiRequest<Gradebook[] | { results: Gradebook[] }>("/grading/teacher/gradebooks/");
          setGradebooks(Array.isArray(payload) ? payload : payload.results);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "No se pudo cargar notas.");
      } finally {
        setLoading(false);
      }
    }
    void load();
  }, [mode, role]);

  async function loadGradebook(id: string) {
    setSelected(id);
    setStudents([]);
    setItems([]);
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const [studentRows, structure] = await Promise.all([
        apiRequest<GradeStudent[]>(`/grading/teacher/gradebooks/${id}/students/`),
        apiRequest<{ items: GradeItem[] }>(`/grading/teacher/gradebooks/${id}/structure/`),
      ]);
      setStudents(studentRows);
      setItems(flattenItems(structure.items));
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo cargar el libro.");
    } finally {
      setLoading(false);
    }
  }

  async function saveRecord() {
    setMessage(null);
    setError(null);
    try {
      const response = await apiRequest<{ snapshot: { final_score: string; final_letter: string; final_status: string } }>(
        `/grading/teacher/gradebooks/${selected}/record/`,
        {
          method: "POST",
          body: JSON.stringify({
            course_enrollment: Number(courseEnrollment),
            grade_item: Number(gradeItem),
            score,
            reason: "Registro desde UI MVP",
          }),
        },
      );
      setMessage(`Nota guardada. Resultado actual: ${response.snapshot.final_score} (${response.snapshot.final_letter}) - ${response.snapshot.final_status}.`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo guardar la nota.");
    }
  }

  const showStudent = mode === "student" || (mode === "overview" && role === "student");

  return (
    <>
      <PageHeader
        title={showStudent ? "Consulta estudiantil de notas" : "Gestion de notas S1/S2/S3"}
        description="UI conectada al motor de notas; la UI registra entradas y muestra snapshots calculados por el backend."
      />
      <div className="mb-4 flex flex-wrap gap-2">
        <Link href="/notas/carga-docente"><Button variant="outline"><ClipboardEdit size={16} /> Carga docente</Button></Link>
        <Link href="/notas/estudiante"><Button variant="outline"><GraduationCap size={16} /> Estudiante</Button></Link>
        <Link href="/notas/secretaria"><Button variant="outline"><ShieldCheck size={16} /> Secretaria</Button></Link>
      </div>
      {loading ? <LoadingState label="Cargando notas" /> : null}
      {error ? <ErrorState title="Notas no disponibles" description={error} /> : null}
      {message ? <Alert tone="success">{message}</Alert> : null}
      {showStudent ? (
        <Table headers={["Periodo", "Asignatura", "Modelo", "Nota", "Letra", "Estado"]}>
          {studentGrades.map((row) => (
            <tr key={row.course_enrollment_id}>
              <td className="px-4 py-3">{row.period_code}</td>
              <td className="px-4 py-3 font-bold">{row.subject_code} - {row.subject_name}</td>
              <td className="px-4 py-3">{row.grading_model}</td>
              <td className="px-4 py-3">{row.snapshot?.final_score ?? "Pendiente"}</td>
              <td className="px-4 py-3">{row.snapshot?.final_letter ?? "-"}</td>
              <td className="px-4 py-3"><Badge tone={finalTone(row.snapshot?.final_status)}>{row.snapshot?.final_status ?? "Sin notas"}</Badge></td>
            </tr>
          ))}
        </Table>
      ) : (
        <div className="grid gap-4 xl:grid-cols-[1fr_360px]">
          <section className="space-y-4">
            <Card>
              <div className="grid gap-3 md:grid-cols-[1fr_auto] md:items-end">
                <div>
                  <Label htmlFor="gradebook">Libro de calificaciones</Label>
                  <Select className="mt-2" id="gradebook" onChange={(event) => void loadGradebook(event.target.value)} value={selected}>
                    <option value="">Seleccione un curso asignado</option>
                    {gradebooks.map((gradebook) => (
                      <option key={gradebook.id} value={gradebook.id}>
                        {gradebook.subject_code} - {gradebook.subject_name} / {gradebook.parallel} / {gradebook.grading_model}
                      </option>
                    ))}
                  </Select>
                </div>
                <Button onClick={() => selected && void loadGradebook(selected)} type="button" variant="outline"><RefreshCcw size={16} /> Actualizar</Button>
              </div>
            </Card>
            <Table headers={["Codigo", "Estudiante", "Estado"]}>
              {students.map((student) => (
                <tr key={student.id}>
                  <td className="px-4 py-3 font-mono text-xs">{student.student_code}</td>
                  <td className="px-4 py-3 font-bold">{student.student_name}</td>
                  <td className="px-4 py-3"><Badge tone={finalTone(student.status)}>{student.status}</Badge></td>
                </tr>
              ))}
            </Table>
          </section>
          <aside className="space-y-4">
            <Card>
              <h2 className="text-lg font-black text-puce-blue">Registrar nota</h2>
              <div className="mt-4 space-y-3">
                <div>
                  <Label htmlFor="course-enrollment">Estudiante</Label>
                  <Select className="mt-2" id="course-enrollment" onChange={(event) => setCourseEnrollment(event.target.value)} value={courseEnrollment}>
                    <option value="">Seleccione</option>
                    {students.map((student) => <option key={student.id} value={student.id}>{student.student_code} - {student.student_name}</option>)}
                  </Select>
                </div>
                <div>
                  <Label htmlFor="grade-item">Item de nota</Label>
                  <Select className="mt-2" id="grade-item" onChange={(event) => setGradeItem(event.target.value)} value={gradeItem}>
                    <option value="">Seleccione</option>
                    {items.map((item) => <option key={item.id} value={item.id}>{item.item_type} - {item.name}</option>)}
                  </Select>
                </div>
                <div>
                  <Label htmlFor="score">Nota 0 a 50</Label>
                  <Input id="score" max="50" min="0" onChange={(event) => setScore(event.target.value)} type="number" value={score} />
                </div>
                <Button className="w-full" disabled={!selected || !courseEnrollment || !gradeItem || !score} onClick={() => void saveRecord()} type="button">
                  <Save size={16} />
                  Guardar y recalcular
                </Button>
              </div>
            </Card>
            <Alert tone="info">Para S1/S2 se seleccionan RA, criterios o actividades del arbol real; para S3 se registran los items de parcial o evaluacion final que expone el gradebook.</Alert>
          </aside>
        </div>
      )}
    </>
  );
}
