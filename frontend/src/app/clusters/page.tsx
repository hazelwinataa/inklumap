import type {
  Metadata,
} from "next";

import ClustersDashboard from "@/components/clusters-dashboard";
import {
  getAnalyticsStudents,
  getClusterProfiles,
} from "@/lib/api";


export const metadata: Metadata = {
  title: "Kelompok Kebutuhan",
};


export default async function ClustersPage() {
  const [
    clusters,
    students,
  ] = await Promise.all([
    getClusterProfiles(),
    getAnalyticsStudents({
      limit: 100,
    }),
  ]);

  return (
    <div className="px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8">
          <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-blue-700">
            Pemetaan Kebutuhan
          </p>

          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            Kelompok Kebutuhan
          </h1>

          <p className="mt-3 max-w-3xl text-slate-600">
            Tinjau kelompok siswa berdasarkan
            kemiripan kebutuhan fungsional untuk
            mendukung perencanaan akomodasi,
            sumber daya, dan tindak lanjut guru.
          </p>
        </header>

        {!clusters || !students ? (
          <section className="rounded-2xl border border-red-200 bg-red-50 p-6">
            <h2 className="font-semibold text-red-800">
              Data kelompok belum dapat dimuat
            </h2>

            <p className="mt-2 text-sm leading-6 text-red-700">
              Pastikan FastAPI dan PostgreSQL
              masih berjalan serta hasil analytics
              sudah tersedia.
            </p>
          </section>
        ) : clusters.length === 0 ? (
          <section className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
            <h2 className="font-semibold text-amber-900">
              Kelompok kebutuhan belum tersedia
            </h2>

            <p className="mt-2 text-sm leading-6 text-amber-800">
              Jalankan proses analytics terlebih
              dahulu untuk membentuk kelompok
              kebutuhan siswa.
            </p>
          </section>
        ) : (
          <ClustersDashboard
            clusters={clusters}
            students={students}
          />
        )}
      </div>
    </div>
  );
}
