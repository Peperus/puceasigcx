import { Breadcrumbs } from "@/components/ui/breadcrumbs";

export function PageHeader({
  title,
  description,
  eyebrow = "Sprint 0.5",
}: {
  title: string;
  description: string;
  eyebrow?: string;
}) {
  return (
    <div className="mb-6">
      <Breadcrumbs items={[{ label: title }]} />
      <p className="mt-5 text-sm font-bold uppercase text-puce-turquoise-dark">{eyebrow}</p>
      <h1 className="mt-2 text-3xl font-black text-puce-blue">{title}</h1>
      <p className="mt-3 max-w-3xl text-sm leading-6 text-ui-text-muted">{description}</p>
    </div>
  );
}
