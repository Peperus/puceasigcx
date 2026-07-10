import { Suspense } from "react";
import { LoginForm } from "@/app/(auth)/login/login-form";
import { LoadingState } from "@/components/feedback/loading-state";

export default function LoginPage() {
  return (
    <Suspense
      fallback={
        <main className="min-h-screen bg-ui-background p-6">
          <LoadingState label="Preparando acceso institucional" />
        </main>
      }
    >
      <LoginForm />
    </Suspense>
  );
}
