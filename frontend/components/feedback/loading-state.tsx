export function LoadingState({ label = "Cargando datos de prototipo" }: { label?: string }) {
  return (
    <div className="rounded-puce-lg border border-ui-border bg-white p-6">
      <div className="h-3 w-40 rounded-puce-sm bg-ui-surface-muted" />
      <div className="mt-4 grid gap-3">
        <div className="h-12 rounded-puce-md bg-ui-surface-muted" />
        <div className="h-12 rounded-puce-md bg-ui-surface-muted" />
        <div className="h-12 rounded-puce-md bg-ui-surface-muted" />
      </div>
      <p className="mt-4 text-sm font-semibold text-ui-text-muted">{label}</p>
    </div>
  );
}
