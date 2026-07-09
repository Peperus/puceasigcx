import { themeConfig } from "@/config/theme";

const brandSwatches = [
  ["Azul institucional", themeConfig.colors.brand.primary],
  ["Azul profundo", themeConfig.colors.brand.primaryDark],
  ["Turquesa apoyo", themeConfig.colors.brand.secondary],
  ["Celeste enlace", themeConfig.colors.brand.sky],
  ["Barra superior", themeConfig.colors.brand.topbar],
] as const;

const semanticSwatches = [
  ["Exito", themeConfig.colors.semantic.success],
  ["Advertencia", themeConfig.colors.semantic.warning],
  ["Error", themeConfig.colors.semantic.danger],
  ["Informacion", themeConfig.colors.semantic.info],
] as const;

export default function Home() {
  return (
    <main className="min-h-screen bg-ui-background text-ui-text">
      <div
        className="bg-puce-topbar px-6 py-2 text-sm font-semibold"
        style={{ color: themeConfig.colors.neutral.white }}
      >
        Tema visual institucional / S0.5-T2
      </div>

      <section className="mx-auto w-full max-w-6xl px-6 py-12">
        <div className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
          <div>
            <div className="inline-flex rounded-puce-sm border border-puce-turquoise bg-white px-3 py-1 text-sm font-semibold uppercase tracking-wide text-puce-turquoise-dark">
              PUCEASIG
            </div>
            <h1 className="mt-5 max-w-3xl text-4xl font-black leading-tight text-puce-blue sm:text-5xl">
              Identidad visual base para el ERP academico
            </h1>
            <p className="mt-4 max-w-2xl text-lg leading-8 text-ui-text-muted">
              Paleta inspirada en la presencia publica de PUCE: azul
              institucional, turquesa de apoyo, superficies blancas y grises
              neutros para una interfaz administrativa clara.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <a
                className="inline-flex h-[42px] items-center rounded-puce-sm bg-puce-blue px-5 text-sm font-bold uppercase tracking-wide shadow-puce-sm"
                href="#tokens"
                style={{ color: themeConfig.colors.neutral.white }}
              >
                Ver tokens
              </a>
              <a
                className="inline-flex h-[42px] items-center rounded-puce-sm border border-puce-turquoise bg-white px-5 text-sm font-bold uppercase tracking-wide text-puce-turquoise-dark"
                href="https://www.puce.edu.ec/"
              >
                Referencia PUCE
              </a>
            </div>
          </div>

          <div className="rounded-puce-lg border border-ui-border bg-white p-5 shadow-puce-md">
            <div
              className="rounded-puce-md bg-puce-blue p-5"
              style={{ color: themeConfig.colors.neutral.white }}
            >
              <p className="text-sm font-semibold uppercase tracking-wide text-puce-blue-soft">
                Espacio reservado para marca
              </p>
              <p className="mt-4 text-3xl font-black">PUCEASIG</p>
              <p className="mt-2 text-sm leading-6 text-blue-50">
                No se incluye logotipo oficial hasta que exista un asset
                autorizado dentro del repositorio.
              </p>
            </div>
            <div className="mt-5 grid gap-3 sm:grid-cols-2">
              <div className="rounded-puce-md bg-puce-blue-soft p-4">
                <p className="text-sm font-bold text-puce-blue">
                  Contraste
                </p>
                <p className="mt-1 text-sm text-ui-text-muted">
                  Acciones principales en azul profundo sobre blanco.
                </p>
              </div>
              <div className="rounded-puce-md bg-status-info-soft p-4">
                <p className="text-sm font-bold text-status-info">
                  Estados
                </p>
                <p className="mt-1 text-sm text-ui-text-muted">
                  Colores semanticos separados de colores de marca.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section
        className="border-y border-ui-border bg-white"
        id="tokens"
      >
        <div className="mx-auto grid w-full max-w-6xl gap-8 px-6 py-12 lg:grid-cols-2">
          <TokenGroup items={brandSwatches} title="Paleta de marca" />
          <TokenGroup items={semanticSwatches} title="Paleta semantica" />
        </div>
      </section>

      <section className="mx-auto w-full max-w-6xl px-6 py-12">
        <h2 className="text-2xl font-black text-puce-blue">
          Escala de interfaz
        </h2>
        <div className="mt-6 grid gap-4 md:grid-cols-3">
          <TokenCard title="Radios" value="3px / 4px / 6px / 8px" />
          <TokenCard title="Sombras" value="sutiles, para paneles y foco" />
          <TokenCard title="Controles" value="42px de alto base" />
        </div>
      </section>
    </main>
  );
}

function TokenGroup({
  items,
  title,
}: {
  items: readonly (readonly [string, string])[];
  title: string;
}) {
  return (
    <div>
      <h2 className="text-2xl font-black text-puce-blue">
        {title}
      </h2>
      <div className="mt-5 grid gap-3">
        {items.map(([name, value]) => (
          <div
            className="flex items-center justify-between rounded-puce-md border border-ui-border bg-ui-surface p-4 shadow-puce-xs"
            key={name}
          >
            <div className="flex items-center gap-3">
              <span
                className="h-10 w-10 rounded-puce-sm border border-black/10"
                style={{ backgroundColor: value }}
              />
              <span className="font-semibold">{name}</span>
            </div>
            <code className="rounded-[3px] bg-ui-surface-muted px-2 py-1 text-sm text-ui-text-muted">
              {value}
            </code>
          </div>
        ))}
      </div>
    </div>
  );
}

function TokenCard({ title, value }: { title: string; value: string }) {
  return (
    <article className="rounded-puce-lg border border-ui-border bg-white p-5 shadow-puce-sm">
      <p className="text-sm font-bold uppercase tracking-wide text-puce-turquoise-dark">
        {title}
      </p>
      <p className="mt-3 text-lg font-semibold text-ui-text">
        {value}
      </p>
    </article>
  );
}
