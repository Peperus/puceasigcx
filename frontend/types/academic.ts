export type AcademicStatus =
  | "draft"
  | "pending"
  | "pending_review"
  | "review"
  | "approved"
  | "observed"
  | "rejected"
  | "closed"
  | "archived"
  | "correction"
  | "signed";

export type AcademicResult =
  | "approved"
  | "failed"
  | "recovery"
  | "ungraded"
  | "risk";

export interface AcademicPeriodSummary {
  code: string;
  name: string;
  status: AcademicStatus;
}

export type DashboardMetric = {
  label: string;
  value: string;
  detail: string;
  status?: AcademicResult;
};

export type PrototypeTableRow = {
  id: string;
  primary: string;
  secondary: string;
  status: AcademicStatus | AcademicResult;
  owner: string;
  meta: string;
};
