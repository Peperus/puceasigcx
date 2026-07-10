"use client";

import { Plus, RefreshCcw, Search } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";
import { ApiError, apiRequest, listItems, type ListResponse } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import type { RoleCode } from "@/config/roles";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { Table } from "@/components/ui/table";
import { Textarea } from "@/components/ui/textarea";
import { EmptyState } from "@/components/feedback/empty-state";
import { ErrorState } from "@/components/feedback/error-state";
import { LoadingState } from "@/components/feedback/loading-state";
import { PageHeader } from "@/components/prototypes/page-header";

export type ResourceRecord = Record<string, unknown> & { id?: number | string };

export type ResourceField = {
  name: string;
  label: string;
  type?: "text" | "number" | "date" | "email" | "textarea" | "select" | "checkbox";
  required?: boolean;
  placeholder?: string;
  options?: { label: string; value: string | number | boolean }[];
  readOnly?: boolean;
};

export type ResourceColumn = {
  key: string;
  label: string;
  render?: (record: ResourceRecord) => React.ReactNode;
};

export type ResourceConfig = {
  title: string;
  description: string;
  endpoint: string;
  searchPlaceholder?: string;
  actionLabel?: string;
  columns: ResourceColumn[];
  fields?: ResourceField[];
  createRoles?: RoleCode[];
  emptyTitle?: string;
};

function valueAsText(value: unknown) {
  if (value === null || value === undefined || value === "") return "Sin dato";
  if (typeof value === "boolean") return value ? "Si" : "No";
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

function toneFor(value: unknown) {
  const normalized = valueAsText(value).toLowerCase();
  if (["approved", "active", "open", "enrolled", "closed", "signed", "aprobado"].includes(normalized)) return "success";
  if (["draft", "planned", "pending", "observed", "reopened", "recovery"].includes(normalized)) return "warning";
  if (["failed", "cancelled", "inactive", "rejected"].includes(normalized)) return "danger";
  return "neutral";
}

function initialForm(fields: ResourceField[]) {
  return Object.fromEntries(fields.filter((field) => !field.readOnly).map((field) => [field.name, field.type === "checkbox" ? false : ""]));
}

function renderInput(field: ResourceField, value: unknown, onChange: (value: unknown) => void) {
  if (field.type === "textarea") {
    return (
      <Textarea
        id={field.name}
        onChange={(event) => onChange(event.target.value)}
        placeholder={field.placeholder}
        required={field.required}
        value={String(value ?? "")}
      />
    );
  }
  if (field.type === "select") {
    return (
      <Select
        id={field.name}
        onChange={(event) => onChange(event.target.value)}
        required={field.required}
        value={String(value ?? "")}
      >
        <option value="">Seleccione...</option>
        {(field.options ?? []).map((option) => (
          <option key={String(option.value)} value={String(option.value)}>
            {option.label}
          </option>
        ))}
      </Select>
    );
  }
  if (field.type === "checkbox") {
    return (
      <input
        checked={Boolean(value)}
        className="h-5 w-5 rounded border-ui-border text-puce-blue focus:outline-none focus:ring-2 focus:ring-puce-turquoise"
        id={field.name}
        onChange={(event) => onChange(event.target.checked)}
        type="checkbox"
      />
    );
  }
  return (
    <Input
      id={field.name}
      onChange={(event) => onChange(event.target.value)}
      placeholder={field.placeholder}
      required={field.required}
      type={field.type ?? "text"}
      value={String(value ?? "")}
    />
  );
}

export function ResourcePage({ config }: { config: ResourceConfig }) {
  const { user } = useAuth();
  const [records, setRecords] = useState<ResourceRecord[]>([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const fields = config.fields ?? [];
  const [form, setForm] = useState<Record<string, unknown>>(() => initialForm(fields));

  const canCreate = useMemo(() => {
    if (!fields.length) return false;
    if (!config.createRoles?.length) return true;
    return config.createRoles.some((role) => user?.roles.includes(role));
  }, [config.createRoles, fields.length, user?.roles]);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      setError(null);
      const payload = await apiRequest<ListResponse<ResourceRecord>>(config.endpoint, {
        params: query ? { search: query } : undefined,
      });
      setRecords(listItems(payload));
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo cargar la informacion.");
    } finally {
      setLoading(false);
    }
  }, [config.endpoint, query]);

  useEffect(() => {
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setNotice(null);
    try {
      const payload = Object.fromEntries(
        Object.entries(form).map(([key, value]) => [key, value === "" ? null : value]),
      );
      await apiRequest<ResourceRecord>(config.endpoint, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setForm(initialForm(fields));
      setNotice("Registro guardado correctamente.");
      await load();
    } catch (err) {
      if (err instanceof ApiError && err.status === 403) {
        setError("El backend rechazo la accion por permisos del rol actual.");
      } else {
        setError(err instanceof Error ? err.message : "No se pudo guardar el registro.");
      }
    }
  }

  return (
    <>
      <PageHeader title={config.title} description={config.description} />
      <div className="grid gap-4 xl:grid-cols-[1fr_360px]">
        <section className="space-y-4">
          <Card>
            <form className="grid gap-3 md:grid-cols-[1fr_auto_auto] md:items-end" onSubmit={(event) => {
              event.preventDefault();
              void load();
            }}>
              <div>
                <Label htmlFor={`${config.endpoint}-search`}>Busqueda</Label>
                <div className="relative mt-2">
                  <Search className="pointer-events-none absolute left-3 top-3 text-ui-text-subtle" size={16} />
                  <Input
                    className="pl-9"
                    id={`${config.endpoint}-search`}
                    onChange={(event) => setQuery(event.target.value)}
                    placeholder={config.searchPlaceholder ?? "Codigo, nombre o estado"}
                    value={query}
                  />
                </div>
              </div>
              <Button type="submit" variant="outline">
                <Search size={16} />
                Buscar
              </Button>
              <Button onClick={() => void load()} type="button" variant="ghost">
                <RefreshCcw size={16} />
                Actualizar
              </Button>
            </form>
          </Card>
          {error ? <ErrorState title="No se pudo cargar" description={error} /> : null}
          {notice ? <Alert tone="success">{notice}</Alert> : null}
          {loading ? <LoadingState label={`Cargando ${config.title.toLowerCase()}`} /> : null}
          {!loading && !records.length && !error ? (
            <EmptyState title={config.emptyTitle ?? "Sin registros"} description="La API no devolvio datos para los filtros actuales." />
          ) : null}
          {!loading && records.length ? (
            <Table headers={config.columns.map((column) => column.label)}>
              {records.map((record, index) => (
                <tr key={String(record.id ?? index)}>
                  {config.columns.map((column) => {
                    const rawValue = record[column.key];
                    return (
                      <td className="px-4 py-3 align-top text-sm" key={column.key}>
                        {column.render ? column.render(record) : column.key === "status" ? (
                          <Badge tone={toneFor(rawValue)}>{valueAsText(rawValue)}</Badge>
                        ) : (
                          valueAsText(rawValue)
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </Table>
          ) : null}
        </section>
        <aside className="space-y-4">
          <Card>
            <h2 className="text-lg font-black text-puce-blue">{config.actionLabel ?? "Nuevo registro"}</h2>
            {canCreate ? (
              <form className="mt-4 space-y-3" onSubmit={submit}>
                {fields.map((field) => (
                  <div key={field.name}>
                    <Label htmlFor={field.name}>{field.label}</Label>
                    <div className="mt-2">
                      {renderInput(field, form[field.name], (value) => setForm((current) => ({ ...current, [field.name]: value })))}
                    </div>
                  </div>
                ))}
                <Button className="w-full" type="submit">
                  <Plus size={16} />
                  Guardar
                </Button>
              </form>
            ) : (
              <Alert tone="warning">El rol actual puede consultar esta pantalla, pero las acciones de escritura dependen de permisos del backend.</Alert>
            )}
          </Card>
          <Alert tone="info">Los permisos se validan nuevamente en la API; esta UI solo oculta acciones no esperadas para mejorar la experiencia.</Alert>
        </aside>
      </div>
    </>
  );
}
