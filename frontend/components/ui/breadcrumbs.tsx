import Link from "next/link";
import { ChevronRight, Home } from "lucide-react";

export function Breadcrumbs({ items }: { items: Array<{ label: string; href?: string }> }) {
  return (
    <nav aria-label="Ruta de navegacion" className="flex flex-wrap items-center gap-1 text-sm text-ui-text-muted">
      <Link aria-label="Inicio" className="inline-flex h-8 w-8 items-center justify-center rounded-puce-sm hover:bg-puce-blue-soft hover:text-puce-blue" href="/dashboard">
        <Home size={16} />
      </Link>
      {items.map((item) => (
        <span className="inline-flex items-center gap-1" key={item.label}>
          <ChevronRight size={14} />
          {item.href ? (
            <Link className="font-semibold hover:text-puce-blue" href={item.href}>
              {item.label}
            </Link>
          ) : (
            <span className="font-semibold text-ui-text">{item.label}</span>
          )}
        </span>
      ))}
    </nav>
  );
}
