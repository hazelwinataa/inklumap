import type {
  Metadata,
} from "next";
import {
  ClipboardCheck,
  ClipboardList,
  Clock3,
  Users,
} from "lucide-react";
import type {
  ComponentType,
} from "react";

import StudentsTable from "@/components/students-table";
import {
  getStudents,
  getStudentSummary,
} from "@/lib/api";


export const metadata: Metadata = {
  title: "Data Siswa",
};


export default async function StudentsPage() {
  const [
    summary,
    students,
  ] = await Promise.all([
    getStudentSummary(),
    getStudents({
      limit: 10,
    }),
  ]);

  return (
    <div className="px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8">
          <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-blue-700">
            Manajemen Data
          </p>

          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            Data Siswa
          </h1>

          <p className="mt-3 max-w-3xl text-slate-600">
            Lihat data siswa dan pantau status
            kelengkapan asesmen kebutuhan
            akomodasi pembelajaran.
          </p>
        </header>

        {!summary || !students ? (
          <section className="rounded-2xl border border-red-200 bg-red-50 p-6">
            <h2 className="font-semibold text-red-800">
              Data siswa belum dapat dimuat
            </h2>

            <p className="mt-2 text-sm text-red-700">
              Pastikan FastAPI dan PostgreSQL
              masih berjalan.
            </p>
          </section>
        ) : (
          <>
            <section className="mb-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              <SummaryCard
                title="Total Siswa"
                value={summary.total_students}
                description="Seluruh siswa terdaftar"
                icon={Users}
              />

              <SummaryCard
                title="Asesmen Lengkap"
                value={summary.complete}
                description="Siap dianalisis"
                icon={ClipboardCheck}
              />

              <SummaryCard
                title="Belum Lengkap"
                value={summary.incomplete}
                description="Perlu dilengkapi"
                icon={ClipboardList}
              />

              <SummaryCard
                title="Belum Dimulai"
                value={summary.not_started}
                description="Belum memiliki asesmen"
                icon={Clock3}
              />
            </section>

            <StudentsTable
              initialData={students}
            />
          </>
        )}
      </div>
    </div>
  );
}


interface SummaryCardProps {
  title: string;
  value: number;
  description: string;
  icon: ComponentType<{
    size?: number;
    className?: string;
  }>;
}


function SummaryCard({
  title,
  value,
  description,
  icon: Icon,
}: SummaryCardProps) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-600">
            {title}
          </p>

          <p className="mt-2 text-3xl font-bold text-slate-900">
            {value}
          </p>

          <p className="mt-1 text-xs text-slate-500">
            {description}
          </p>
        </div>

        <div className="rounded-xl bg-blue-50 p-3 text-blue-700">
          <Icon size={22} />
        </div>
      </div>
    </article>
  );
}