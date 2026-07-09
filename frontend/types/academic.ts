export type AcademicStatus =
  | "draft"
  | "pending_review"
  | "approved"
  | "observed"
  | "closed"
  | "archived";

export interface AcademicPeriodSummary {
  code: string;
  name: string;
  status: AcademicStatus;
}
