import {
  getAnalyticsSummary,
} from "@/lib/api";


export default async function Home() {
  const summary =
    await getAnalyticsSummary();

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-10 text-slate-900">
      <div className="mx-auto max-w-7xl">
        <header className="mb-10">
          <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-blue-700">
            Dashboard Sekolah Inklusif
          </p>

          <h1 className="text-4xl font-bold tracking-tight">
            InkluMap
          </h1>

          <p className="mt-3 max-w-3xl text-slate-600">
            Sistem pemetaan kebutuhan akomodasi
            pembelajaran berbasis data mining.
          </p>
        </header>

        {!summary ? (
          <section className="rounded-2xl border border-red-200 bg-red-50 p-6">
            <h2 className="text-lg font-semibold text-red-800">
              Backend belum terhubung
            </h2>

            <p className="mt-2 text-red-700">
              Pastikan FastAPI berjalan pada
              http://127.0.0.1:8000.
            </p>
          </section>
        ) : (
          <>
            <section className="mb-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <p className="text-sm text-slate-500">
                Model analitik aktif
              </p>

              <h2 className="mt-1 text-xl font-semibold">
                {summary.model_name}
              </h2>

              <p className="mt-2 text-sm text-slate-600">
                Silhouette Score:{" "}
                <span className="font-semibold">
                  {summary.silhouette_score?.toFixed(
                    4,
                  )}
                </span>
              </p>
            </section>

            <section className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
              <SummaryCard
                title="Siswa Dianalisis"
                value={summary.total_students}
              />

              <SummaryCard
                title="Kelompok Kebutuhan"
                value={summary.cluster_count}
              />

              <SummaryCard
                title="Prioritas Tinggi"
                value={summary.high_priority}
              />

              <SummaryCard
                title="Prioritas Sedang"
                value={summary.medium_priority}
              />

              <SummaryCard
                title="Prioritas Rendah"
                value={summary.low_priority}
              />

              <SummaryCard
                title="Akses Kritis"
                value={summary.critical_access}
              />

              <SummaryCard
                title="Perlu Validasi Guru"
                value={
                  summary.needs_human_review
                }
              />

              <SummaryCard
                title="Kasus Unik"
                value={
                  summary.dbscan_unique_cases
                }
              />
            </section>
          </>
        )}
      </div>
    </main>
  );
}


interface SummaryCardProps {
  title: string;
  value: number;
}


function SummaryCard({
  title,
  value,
}: SummaryCardProps) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-medium text-slate-600">
        {title}
      </p>

      <p className="mt-3 text-4xl font-bold text-slate-900">
        {value}
      </p>
    </article>
  );
}