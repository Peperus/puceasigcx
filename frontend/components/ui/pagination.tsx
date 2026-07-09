import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Pagination({ current = 1, total = 4 }: { current?: number; total?: number }) {
  return (
    <div className="flex items-center justify-between gap-3 text-sm text-ui-text-muted">
      <span>
        Pagina {current} de {total}
      </span>
      <div className="flex gap-2">
        <Button aria-label="Pagina anterior" className="h-9 min-h-9 w-9 px-0" variant="outline">
          <ChevronLeft size={16} />
        </Button>
        <Button aria-label="Pagina siguiente" className="h-9 min-h-9 w-9 px-0" variant="outline">
          <ChevronRight size={16} />
        </Button>
      </div>
    </div>
  );
}
