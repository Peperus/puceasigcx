import { frontendModules } from "@/lib/mock-data";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-950">
      <section className="mx-auto flex min-h-screen w-full max-w-6xl flex-col justify-center px-6 py-12">
        <p className="text-sm font-semibold uppercase tracking-wide text-sky-700">
          Sprint 0.5 / Ticket S0.5-T1
        </p>
        <div className="mt-4 max-w-3xl">
          <h1 className="text-4xl font-semibold leading-tight sm:text-5xl">
            PUCEASIG frontend base
          </h1>
          <p className="mt-4 text-lg leading-8 text-slate-700">
            Estructura inicial para el ERP/SIG academico de PUCE Amazonas con
            Next.js, TypeScript, Tailwind CSS y carpetas preparadas para el
            sistema de diseno, navegacion por rol y prototipos del MVP.
          </p>
        </div>
        <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {frontendModules.map((module) => (
            <article
              className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm"
              key={module.name}
            >
              <h2 className="text-base font-semibold text-slate-950">
                {module.name}
              </h2>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                {module.description}
              </p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
