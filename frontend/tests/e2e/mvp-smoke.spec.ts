import { expect, test } from "@playwright/test";

test("login real muestra labels y no expone selector mock de rol", async ({ page }) => {
  await page.goto("/login");
  await expect(page.getByLabel("Correo institucional")).toBeVisible();
  await expect(page.getByLabel("Contrasena")).toBeVisible();
  await expect(page.getByRole("button", { name: "Ingresar" })).toBeVisible();
  await expect(page.getByText("Rol prototipo")).toHaveCount(0);
});

test("ruta autenticada redirige anonimos a login", async ({ page }) => {
  await page.goto("/dashboard");
  await expect(page).toHaveURL(/\/login/);
  await expect(page.getByRole("button", { name: "Ingresar" })).toBeVisible();
});

test("pantalla 403 mantiene mensaje accesible", async ({ page }) => {
  await page.goto("/403");
  await expect(page.getByRole("heading", { name: /acceso no autorizado/i })).toBeVisible();
});
