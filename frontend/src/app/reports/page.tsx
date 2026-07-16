import type {
  Metadata,
} from "next";

import ReportsDashboard from "@/components/reports-dashboard";
import {
  getAnalyticsSummary,
  getBudgetPriorities,
  getClusterProfiles,
  getStudentSummary,
} from "@/lib/api";


export const metadata: Metadata = {
  title: "Laporan",
};


export default async function ReportsPage() {
  const [
    studentSummary,
    analyticsSummary,
    clusters,
    budgetPriorities,
  ] = await Promise.all([
    getStudentSummary(),
    getAnalyticsSummary(),
    getClusterProfiles(),
    getBudgetPriorities(),
  ]);

  const generatedAt =
    new Intl.DateTimeFormat(
      "id-ID",
      {
        dateStyle: "long",
        timeStyle: "short",
        timeZone: "Asia/Jakarta",
      },
    ).format(new Date());

  const dataAvailable =
    studentSummary
    && analyticsSummary
    && clusters
    && budgetPriorities;

  return (
    <div className="px-4 py-8 sm:px-6 lg:px-8 print:px-0 print:py-0">
      <div className="mx-auto max-w-7xl print:max-w-none">
        {!dataAvailable ? (
          <section className="rounded-2xl border border-red-200 bg-red-50 p-6">
            <h1 className="font-semibold text-red-800">
              Laporan belum dapat dimuat
            </h1>

            <p className="mt-2 text-sm leading-6 text-red-700">
              Pastikan FastAPI dan PostgreSQL
              masih berjalan serta seluruh hasil
              analytics tersedia.
            </p>
          </section>
        ) : (
          <ReportsDashboard
            studentSummary={studentSummary}
            analyticsSummary={analyticsSummary}
            clusters={clusters}
            budgetPriorities={budgetPriorities}
            generatedAt={generatedAt}
          />
        )}
      </div>
    </div>
  );
}
