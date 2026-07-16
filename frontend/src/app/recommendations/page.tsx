import type {
  Metadata,
} from "next";

import RecommendationsDashboard from "@/components/recommendations-dashboard";
import {
  getAnalyticsStudents,
  getClusterProfiles,
} from "@/lib/api";


export const metadata: Metadata = {
  title: "Rekomendasi",
};


export default async function RecommendationsPage() {
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
            Tindak Lanjut Pembelajaran
          </p>

          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            Rekomendasi Akomodasi
          </h1>

          <p className="mt-3 max-w-3xl text-slate-600">
            Gunakan rekomendasi kelompok sebagai
            panduan awal untuk menyusun akomodasi
            pembelajaran. Keputusan individual tetap
            perlu disesuaikan melalui validasi guru
            dan detail hasil asesmen siswa.
          </p>
        </header>

        {!clusters || !students ? (
          <section className="rounded-2xl border border-red-200 bg-red-50 p-6">
            <h2 className="font-semibold text-red-800">
              Data rekomendasi belum dapat dimuat
            </h2>

            <p className="mt-2 text-sm leading-6 text-red-700">
              Pastikan FastAPI dan PostgreSQL
              masih berjalan serta hasil analytics
              tersedia.
            </p>
          </section>
        ) : clusters.length === 0 ? (
          <section className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
            <h2 className="font-semibold text-amber-900">
              Rekomendasi belum tersedia
            </h2>

            <p className="mt-2 text-sm leading-6 text-amber-800">
              Jalankan proses analytics terlebih
              dahulu untuk membentuk kelompok dan
              rekomendasi akomodasi.
            </p>
          </section>
        ) : (
          <RecommendationsDashboard
            clusters={clusters}
            students={students}
          />
        )}
      </div>
    </div>
  );
}
