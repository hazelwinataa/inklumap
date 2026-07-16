import type {
  Metadata,
} from "next";

import BudgetPrioritiesDashboard from "@/components/budget-priorities-dashboard";
import {
  getBudgetPriorities,
} from "@/lib/api";


export const metadata: Metadata = {
  title: "Prioritas Anggaran",
};


export default async function BudgetPrioritiesPage() {
  const budgetPriorities =
    await getBudgetPriorities();

  return (
    <div className="px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8">
          <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-blue-700">
            Perencanaan Sumber Daya
          </p>

          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            Prioritas Anggaran
          </h1>

          <p className="mt-3 max-w-3xl text-slate-600">
            Gunakan pemeringkatan berbasis data
            untuk menentukan urutan kebutuhan
            sumber daya sekolah. Nilai yang tampil
            merupakan skor prioritas, bukan
            estimasi nominal biaya.
          </p>
        </header>

        {!budgetPriorities ? (
          <section className="rounded-2xl border border-red-200 bg-red-50 p-6">
            <h2 className="font-semibold text-red-800">
              Data prioritas belum dapat dimuat
            </h2>

            <p className="mt-2 text-sm leading-6 text-red-700">
              Pastikan FastAPI dan PostgreSQL
              masih berjalan serta endpoint
              prioritas anggaran tersedia.
            </p>
          </section>
        ) : budgetPriorities.items.length === 0 ? (
          <section className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
            <h2 className="font-semibold text-amber-900">
              Prioritas anggaran belum tersedia
            </h2>

            <p className="mt-2 text-sm leading-6 text-amber-800">
              Jalankan proses analytics terlebih
              dahulu agar kebutuhan sumber daya
              dapat diperingkat.
            </p>
          </section>
        ) : (
          <BudgetPrioritiesDashboard
            data={budgetPriorities}
          />
        )}
      </div>
    </div>
  );
}
