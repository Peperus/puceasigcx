"use client";

import { BookOpen, GraduationCap, ScrollText, Users } from "lucide-react";
import { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { roleLabels } from "@/config/roles";
import { MetricCard } from "@/components/dashboard/metric-card";
import { Alert } from "@/components/ui/alert";
import { Card } from "@/components/ui/card";
import { PageHeader } from "@/components/prototypes/page-header";
import { LoadingState } from "@/components/feedback/loading-state";
import { ErrorState } from "@/components/feedback/error-state";

type DashboardPayload = {
  period: { id: number; code: string; name: string };
  counts: { students: number; teachers: number; courses: number; enrollments: number };
};

type TeacherCourse = {
  id: number;
  subject_code: string;
  subject_name: string;
  parallel: string;
  grading_model: string;
  status: string;
  enrolled_count: number;
};

export function AcademicDashboard() {
  const { role, user } = useAuth();
  const [staffData, setStaffData] = useState<DashboardPayload | null>(null);
  const [teacherCourses, setTeacherCourses] = useState<TeacherCourse[]>([]);
  const [studentGrades, setStudentGrades] = useState<unknown[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        if (["administrator", "secretary", "career_coordinator", "academic_director"].includes(role)) {
          setStaffData(await apiRequest<DashboardPayload>("/academic/dashboard/"));
        } else if (role === "teacher") {
          const payload = await apiRequest<TeacherCourse[] | { results: TeacherCourse[] }>("/grading/teacher/gradebooks/");
          setTeacherCourses(Array.isArray(payload) ? payload : payload.results);
        } else if (role === "student") {
          setStudentGrades(await apiRequest<unknown[]>("/student/grades/"));
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "No se pudo cargar el dashboard.");
      } finally {
        setLoading(false);
      }
    }
    void load();
  }, [role]);

  const metrics = staffData
    ? [
        { label: "Estudiantes", value: String(staffData.counts.students), detail: staffData.period.name, icon: GraduationCap },
        { label: "Docentes", value: String(staffData.counts.teachers), detail: "Asignados activos", icon: Users },
        { label: "Cursos", value: String(staffData.counts.courses), detail: "Cursos del periodo", icon: BookOpen },
        { label: "Matriculas", value: String(staffData.counts.enrollments), detail: "Inscripciones activas", icon: ScrollText },
      ]
    : [];

  return (
    <>
      <PageHeader
        title={`Dashboard ${roleLabels[role]}`}
        description="Indicadores reales disponibles para el rol autenticado; si la API no expone una metrica, se muestra un estado vacio honesto."
      />
      {loading ? <LoadingState label="Cargando dashboard" /> : null}
      {error ? <ErrorState title="Dashboard no disponible" description={error} /> : null}
      {staffData ? (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {metrics.map((metric) => (
            <MetricCard
              key={metric.label}
              metric={{ label: metric.label, value: metric.value, detail: metric.detail }}
            />
          ))}
        </div>
      ) : null}
      {!loading && role === "teacher" ? (
        <Card>
          <h2 className="text-lg font-black text-puce-blue">Cursos asignados</h2>
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            {teacherCourses.map((course) => (
              <div className="rounded-puce-md bg-ui-surface-muted p-3" key={course.id}>
                <p className="font-bold">{course.subject_code} - {course.subject_name}</p>
                <p className="text-sm text-ui-text-muted">Paralelo {course.parallel} | {course.grading_model} | {course.enrolled_count} estudiantes</p>
              </div>
            ))}
            {!teacherCourses.length ? <Alert tone="info">No hay cursos asignados disponibles desde la API.</Alert> : null}
          </div>
        </Card>
      ) : null}
      {!loading && role === "student" ? (
        <Card>
          <h2 className="text-lg font-black text-puce-blue">Cursos con notas visibles</h2>
          <p className="mt-2 text-sm text-ui-text-muted">{studentGrades.length} registro(s) devueltos por /api/student/grades/ para {user?.email}.</p>
        </Card>
      ) : null}
      {!loading && !staffData && role !== "teacher" && role !== "student" ? (
        <Alert tone="info">Este rol no tiene indicadores agregados expuestos en el MVP.</Alert>
      ) : null}
    </>
  );
}
