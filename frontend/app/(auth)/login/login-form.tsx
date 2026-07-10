"use client";

import { useState, type FormEvent } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { AuthCard } from "@/components/prototypes/auth-card";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/lib/auth";

export function LoginForm() {
  const router = useRouter();
  const params = useSearchParams();
  const { login, error } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    try {
      await login(email, password);
      router.replace(params.get("next") || "/dashboard");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AuthCard
      title="Iniciar sesion"
      description="Use una cuenta institucional registrada en el backend local del MVP."
    >
      <form className="space-y-4" onSubmit={handleSubmit}>
        {error ? <Alert tone="danger">{error}</Alert> : null}
        <div>
          <Label htmlFor="email">Correo institucional</Label>
          <Input
            autoComplete="email"
            className="mt-2"
            id="email"
            onChange={(event) => setEmail(event.target.value)}
            placeholder="usuario@institucion.example"
            required
            type="email"
            value={email}
          />
        </div>
        <div>
          <Label htmlFor="password">Contrasena</Label>
          <Input
            autoComplete="current-password"
            className="mt-2"
            id="password"
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Minimo 8 caracteres"
            required
            type="password"
            value={password}
          />
        </div>
        <label className="flex items-center gap-2 text-sm text-ui-text-muted">
          <Checkbox />
          Mantener sesion en este navegador
        </label>
        <Button className="w-full" disabled={submitting} type="submit">
          {submitting ? "Validando..." : "Ingresar"}
        </Button>
      </form>
    </AuthCard>
  );
}
