"use client";

import { FileText, FileUp, Send, Undo2 } from "lucide-react";
import { useState } from "react";
import { apiRequest } from "@/lib/api";
import { ResourceTabsPage } from "@/components/data/resource-tabs-page";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

const editorRoles = ["administrator", "career_coordinator", "academic_director", "teacher"] as const;

function workflowEndpoint(id: string, action: string) {
  return `/syllabi/${id}/${action}/`;
}

export function SyllabusWorkspace() {
  const [syllabusId, setSyllabusId] = useState("");
  const [reason, setReason] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function run(action: string, body?: Record<string, unknown>) {
    if (!syllabusId) {
      setError("Ingrese el ID del silabo.");
      return;
    }
    setError(null);
    setMessage(null);
    try {
      await apiRequest(workflowEndpoint(syllabusId, action), {
        method: "POST",
        body: JSON.stringify(body ?? {}),
      });
      setMessage("Accion ejecutada correctamente por la API.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo ejecutar la accion.");
    }
  }

  async function upload() {
    if (!syllabusId || !file) {
      setError("Ingrese ID de silabo y adjunte un PDF.");
      return;
    }
    const form = new FormData();
    form.append("signed_file", file);
    setError(null);
    setMessage(null);
    try {
      await apiRequest(workflowEndpoint(syllabusId, "upload-signed-file"), {
        method: "POST",
        body: form,
        headers: {},
      });
      setMessage("PDF firmado cargado correctamente.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo cargar el PDF.");
    }
  }

  return (
    <div className="space-y-4">
      <Card>
        <h2 className="text-lg font-black text-puce-blue">Acciones de flujo de silabo</h2>
        <div className="mt-4 grid gap-3 lg:grid-cols-[160px_1fr_auto] lg:items-end">
          <div>
            <Label htmlFor="syllabus-id">ID silabo</Label>
            <Input id="syllabus-id" onChange={(event) => setSyllabusId(event.target.value)} type="number" value={syllabusId} />
          </div>
          <div>
            <Label htmlFor="syllabus-reason">Justificacion / observacion</Label>
            <Textarea id="syllabus-reason" onChange={(event) => setReason(event.target.value)} value={reason} />
          </div>
          <div className="flex flex-wrap gap-2">
            <Button onClick={() => void run("finalize")} type="button" variant="outline"><FileText size={16} /> Finalizar</Button>
            <Button onClick={() => void run("submit")} type="button" variant="outline"><Send size={16} /> Enviar</Button>
            <Button onClick={() => void run("approve")} type="button" variant="outline">Aprobar</Button>
            <Button onClick={() => void run("observe", { reason })} type="button" variant="outline">Observar</Button>
            <Button onClick={() => void run("reopen", { reason })} type="button" variant="outline"><Undo2 size={16} /> Reabrir</Button>
          </div>
        </div>
        <div className="mt-4 grid gap-3 lg:grid-cols-[1fr_auto] lg:items-end">
          <div>
            <Label htmlFor="signed-file">PDF firmado</Label>
            <Input accept="application/pdf" id="signed-file" onChange={(event) => setFile(event.target.files?.[0] ?? null)} type="file" />
          </div>
          <Button onClick={() => void upload()} type="button"><FileUp size={16} /> Cargar firmado</Button>
        </div>
        {message ? <div className="mt-4"><Alert tone="success">{message}</Alert></div> : null}
        {error ? <div className="mt-4"><Alert tone="danger">{error}</Alert></div> : null}
      </Card>
      <ResourceTabsPage
        tabs={[
          {
            id: "syllabi",
            label: "Silabos",
            config: {
              title: "Gestion de silabos",
              description: "Silabos reales por curso, estado, docente y carrera.",
              endpoint: "/syllabi/",
              actionLabel: "Nuevo silabo",
              createRoles: [...editorRoles],
              columns: [
                { key: "id", label: "ID" },
                { key: "subject_code", label: "Asignatura" },
                { key: "subject_name", label: "Nombre" },
                { key: "lead_teacher_name", label: "Docente" },
                { key: "status", label: "Estado" },
              ],
              fields: [
                { name: "course_section", label: "ID curso", type: "number", required: true },
                { name: "version", label: "Version", type: "select", required: true, options: [
                  { label: "Nueva version", value: "new" },
                  { label: "Anterior", value: "legacy" },
                ] },
                { name: "subject_description", label: "Descripcion", type: "textarea", required: true },
                { name: "methodology", label: "Metodologia", type: "textarea", required: true },
                { name: "lead_teacher", label: "ID docente titular", type: "number", required: true },
                { name: "co_teacher", label: "ID codocente", type: "number" },
              ],
            },
          },
          {
            id: "competencies",
            label: "Competencias",
            config: {
              title: "Competencias",
              description: "Competencias transversales y disciplinares del silabo.",
              endpoint: "/syllabi/competencies/",
              actionLabel: "Agregar competencia",
              createRoles: [...editorRoles],
              columns: [
                { key: "syllabus", label: "Silabo" },
                { key: "competency_type", label: "Tipo" },
                { key: "text", label: "Texto" },
                { key: "order", label: "Orden" },
              ],
              fields: [
                { name: "syllabus", label: "ID silabo", type: "number", required: true },
                { name: "competency_type", label: "Tipo", type: "select", required: true, options: [
                  { label: "Transversal", value: "transversal" },
                  { label: "Disciplinar", value: "disciplinary" },
                ] },
                { name: "text", label: "Texto", type: "textarea", required: true },
                { name: "order", label: "Orden", type: "number", required: true },
              ],
            },
          },
          {
            id: "outcomes",
            label: "RA",
            config: {
              title: "Resultados de aprendizaje",
              description: "RA de carrera/asignatura conectados al constructor.",
              endpoint: "/syllabi/learning-outcomes/",
              actionLabel: "Agregar RA",
              createRoles: [...editorRoles],
              columns: [
                { key: "syllabus", label: "Silabo" },
                { key: "code", label: "Codigo" },
                { key: "outcome_type", label: "Tipo" },
                { key: "text", label: "Texto" },
                { key: "order", label: "Orden" },
              ],
              fields: [
                { name: "syllabus", label: "ID silabo", type: "number", required: true },
                { name: "outcome_type", label: "Tipo", type: "select", required: true, options: [
                  { label: "Carrera", value: "career" },
                  { label: "Asignatura", value: "subject" },
                ] },
                { name: "code", label: "Codigo", required: true },
                { name: "text", label: "Texto", type: "textarea", required: true },
                { name: "order", label: "Orden", type: "number", required: true },
              ],
            },
          },
          {
            id: "criteria",
            label: "Criterios",
            config: {
              title: "Criterios y rubricas",
              description: "Criterios ponderados por resultado de aprendizaje.",
              endpoint: "/syllabi/criteria/",
              actionLabel: "Agregar criterio",
              createRoles: [...editorRoles],
              columns: [
                { key: "outcome_label", label: "RA" },
                { key: "name", label: "Criterio" },
                { key: "weight", label: "Peso" },
                { key: "order", label: "Orden" },
              ],
              fields: [
                { name: "syllabus", label: "ID silabo", type: "number", required: true },
                { name: "learning_outcome", label: "ID RA", type: "number", required: true },
                { name: "name", label: "Nombre", required: true },
                { name: "description", label: "Descripcion", type: "textarea" },
                { name: "weight", label: "Peso", type: "number", required: true },
                { name: "order", label: "Orden", type: "number", required: true },
              ],
            },
          },
          {
            id: "bibliography",
            label: "Bibliografia",
            config: {
              title: "Bibliografia",
              description: "Bibliografia basica, complementaria, recomendada y digital.",
              endpoint: "/syllabi/bibliography/",
              actionLabel: "Agregar referencia",
              createRoles: [...editorRoles],
              columns: [
                { key: "syllabus", label: "Silabo" },
                { key: "bibliography_type", label: "Tipo" },
                { key: "apa_reference", label: "Referencia" },
                { key: "copies", label: "Ejemplares" },
              ],
              fields: [
                { name: "syllabus", label: "ID silabo", type: "number", required: true },
                { name: "bibliography_type", label: "Tipo", type: "select", required: true, options: [
                  { label: "Basica", value: "basic" },
                  { label: "Complementaria", value: "complementary" },
                  { label: "Recomendada", value: "recommended" },
                  { label: "Digital", value: "digital" },
                ] },
                { name: "apa_reference", label: "Referencia APA", type: "textarea", required: true },
                { name: "library_code", label: "Codigo biblioteca" },
                { name: "copies", label: "Ejemplares", type: "number" },
                { name: "order", label: "Orden", type: "number" },
              ],
            },
          },
          {
            id: "weekly",
            label: "Plan semanal",
            config: {
              title: "Planificacion semanal",
              description: "Experiencias de aprendizaje por semana y RA.",
              endpoint: "/syllabi/weekly-plans/",
              actionLabel: "Agregar semana",
              createRoles: [...editorRoles],
              columns: [
                { key: "syllabus", label: "Silabo" },
                { key: "week_label", label: "Semana" },
                { key: "outcome_label", label: "RA" },
                { key: "contact_hours", label: "Contacto" },
                { key: "autonomous_hours", label: "Autonomas" },
              ],
              fields: [
                { name: "syllabus", label: "ID silabo", type: "number", required: true },
                { name: "learning_outcome", label: "ID RA", type: "number", required: true },
                { name: "week_number", label: "Numero semana", type: "number", required: true },
                { name: "week_label", label: "Etiqueta", required: true },
                { name: "contact_strategy", label: "Contacto docente", type: "textarea" },
                { name: "contact_hours", label: "Horas contacto", type: "number" },
                { name: "practical_strategy", label: "Practico experimental", type: "textarea" },
                { name: "practical_hours", label: "Horas practicas", type: "number" },
                { name: "autonomous_strategy", label: "Autonomo", type: "textarea" },
                { name: "autonomous_hours", label: "Horas autonomas", type: "number" },
              ],
            },
          },
        ]}
      />
    </div>
  );
}
