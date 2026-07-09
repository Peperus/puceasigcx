import Link from "next/link";
import { FileUp, PencilLine } from "lucide-react";
import { ModulePage } from "@/components/prototypes/module-page";
import { Button } from "@/components/ui/button";

export default function SyllabiPage() {
  return (
    <>
      <ModulePage title="Gestion de silabos" description="Wireframe de estados, revision, aprobacion, carga firmada y consulta por rol." action="Nuevo silabo" />
      <div className="mt-4 flex flex-wrap gap-3">
        <Link href="/silabos/constructor"><Button><PencilLine size={16} /> Constructor nueva version</Button></Link>
        <Link href="/silabos/carga-firmado"><Button variant="outline"><FileUp size={16} /> Carga firmado</Button></Link>
      </div>
    </>
  );
}
