"use client";

import {
  AlertTriangle,
  BarChart3,
  CheckCircle2,
  ClipboardCheck,
  FileDown,
  Layers3,
  Printer,
  ShieldAlert,
  Target,
  Users,
  WalletCards,
} from "lucide-react";
import type {
  ReactNode,
} from "react";

import type {
  AnalyticsSummary,
  BudgetPriorityItem,
  BudgetPriorityResponse,
  ClusterProfile,
} from "@/types/analytics";
import type {
  StudentSummary,
} from "@/types/students";


interface ReportsDashboardProps {
  studentSummary: StudentSummary;
  analyticsSummary: AnalyticsSummary;
  clusters: ClusterProfile[];
  budgetPriorities: BudgetPriorityResponse;
  generatedAt: string;
}


export default function ReportsDashboard({
  studentSummary,
  analyticsSummary,
  clusters,
  budgetPriorities,
  generatedAt,
}: ReportsDashboardProps) {
  const completionRate = percentage(
    studentSummary.complete,
    studentSummary.total_students,
  );

  const analysisCoverage = percentage(
    analyticsSummary.total_students,
    studentSummary.total_students,
  );

  const highestBudgetPriority =
    budgetPriorities.items[0];

  const highestUrgency =
    [...budgetPriorities.items].sort(
      (firstItem, secondItem) =>
        secondItem.urgency_index
        - firstItem.urgency_index,
    )[0];

  return (
    <div className="space-y-8 print:space-y-5">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between print:hidden">
        <div>
          <p className="text-sm font-semibold uppercase tracking-widest text-blue-700">
            Dokumentasi Hasil
          </p>

          <h1 className="mt-1 text-3xl font-bold tracking-tight text-slate-900">
            Laporan Analitik InkluMap
          </h1>

          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
            Tinjau ringkasan hasil asesmen,
            pemetaan kebutuhan, rekomendasi, dan
            prioritas sumber daya dalam satu laporan.
          </p>
        </div>

        <button
          type="button"
          onClick={() => {
            window.print();
          }}
          className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-100"
        >
          <Printer size={18} />

          Cetak / Simpan PDF
        </button>
      </div>

      <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm print:rounded-none print:border-0 print:shadow-none">
        <div className="border-b border-slate-200 bg-slate-950 px-6 py-7 text-white print:bg-white print:px-0 print:py-0 print:text-slate-950">
          <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.22em] text-blue-300 print:text-blue-700">
                InkluMap
              </p>

              <h2 className="mt-2 text-3xl font-bold">
                Laporan Pemetaan Kebutuhan
                Akomodasi Pembelajaran
              </h2>

              <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-300 print:text-slate-600">
                Ringkasan data asesmen, hasil
                pengelompokan, rekomendasi
                akomodasi, dan prioritas sumber
                daya sekolah inklusif.
              </p>
            </div>

            <div className="rounded-xl border border-slate-700 bg-slate-900/70 px-4 py-3 text-sm print:border-slate-300 print:bg-white">
              <p className="text-xs uppercase tracking-wider text-slate-400 print:text-slate-500">
                Dibuat pada
              </p>

              <p className="mt-1 font-semibold text-white print:text-slate-900">
                {generatedAt} WIB
              </p>
            </div>
          </div>
        </div>

        <div className="grid gap-4 p-6 sm:grid-cols-2 xl:grid-cols-4 print:grid-cols-4 print:px-0">
          <SummaryCard
            title="Total Siswa"
            value={studentSummary.total_students}
            description="Siswa terdaftar"
            icon={
              <Users size={21} />
            }
          />

          <SummaryCard
            title="Asesmen Lengkap"
            value={studentSummary.complete}
            description={`${completionRate}% dari siswa`}
            icon={
              <ClipboardCheck size={21} />
            }
          />

          <SummaryCard
            title="Siswa Dianalisis"
            value={analyticsSummary.total_students}
            description={`${analysisCoverage}% cakupan`}
            icon={
              <BarChart3 size={21} />
            }
          />

          <SummaryCard
            title="Kelompok Kebutuhan"
            value={analyticsSummary.cluster_count}
            description="Profil kebutuhan aktif"
            icon={
              <Layers3 size={21} />
            }
          />
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-2 print:grid-cols-2 print:break-inside-avoid">
        <ReportSection
          eyebrow="Kelengkapan Data"
          title="Status Asesmen Siswa"
          icon={
            <ClipboardCheck size={20} />
          }
        >
          <div className="space-y-5">
            <ProgressRow
              label="Asesmen lengkap"
              value={studentSummary.complete}
              total={studentSummary.total_students}
              className="bg-emerald-600"
            />

            <ProgressRow
              label="Belum lengkap"
              value={studentSummary.incomplete}
              total={studentSummary.total_students}
              className="bg-amber-500"
            />

            <ProgressRow
              label="Belum dimulai"
              value={studentSummary.not_started}
              total={studentSummary.total_students}
              className="bg-slate-400"
            />
          </div>

          <div className="mt-6 grid grid-cols-2 gap-3">
            <MetricBox
              label="Total asesmen"
              value={studentSummary.total_assessments}
            />

            <MetricBox
              label="Total skor"
              value={studentSummary.total_scores}
            />
          </div>
        </ReportSection>

        <ReportSection
          eyebrow="Distribusi Hasil"
          title="Prioritas Tindak Lanjut"
          icon={
            <Target size={20} />
          }
        >
          <div className="space-y-5">
            <ProgressRow
              label="Prioritas tinggi"
              value={analyticsSummary.high_priority}
              total={analyticsSummary.total_students}
              className="bg-red-600"
            />

            <ProgressRow
              label="Prioritas sedang"
              value={analyticsSummary.medium_priority}
              total={analyticsSummary.total_students}
              className="bg-amber-500"
            />

            <ProgressRow
              label="Prioritas rendah"
              value={analyticsSummary.low_priority}
              total={analyticsSummary.total_students}
              className="bg-emerald-600"
            />
          </div>

          <div className="mt-6 grid grid-cols-3 gap-3">
            <MetricBox
              label="Akses kritis"
              value={analyticsSummary.critical_access}
            />

            <MetricBox
              label="Perlu validasi"
              value={analyticsSummary.needs_human_review}
            />

            <MetricBox
              label="Kasus unik"
              value={analyticsSummary.dbscan_unique_cases}
            />
          </div>
        </ReportSection>
      </section>

      <ReportSection
        eyebrow="Pemetaan Kebutuhan"
        title="Profil Kelompok Siswa"
        icon={
          <Layers3 size={20} />
        }
      >
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 text-sm">
            <thead>
              <tr className="bg-slate-50">
                <TableHeader>
                  Kelompok
                </TableHeader>

                <TableHeader>
                  Nama dan kebutuhan
                </TableHeader>

                <TableHeader>
                  Jumlah
                </TableHeader>

                <TableHeader>
                  Siswa representatif
                </TableHeader>

                <TableHeader>
                  Rata-rata jarak
                </TableHeader>
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-100">
              {clusters.map((cluster) => (
                <tr
                  key={cluster.id}
                  className="align-top"
                >
                  <TableCell>
                    <span className="inline-flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 font-bold text-white">
                      {cluster.cluster_number}
                    </span>
                  </TableCell>

                  <TableCell>
                    <p className="font-semibold text-slate-900">
                      {cluster.cluster_name}
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      {cluster.dominant_need}
                    </p>
                  </TableCell>

                  <TableCell>
                    {cluster.cluster_size} siswa
                  </TableCell>

                  <TableCell>
                    {cluster.medoid_student_code}
                  </TableCell>

                  <TableCell>
                    {cluster.mean_medoid_distance
                      .toFixed(4)}
                  </TableCell>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="mt-5 rounded-xl border border-blue-200 bg-blue-50 p-4 text-sm leading-6 text-blue-900">
          Model{" "}
          <strong>
            {analyticsSummary.model_name}
          </strong>{" "}
          menghasilkan silhouette score{" "}
          <strong>
            {analyticsSummary.silhouette_score
              ?.toFixed(4)
              ?? "-"}
          </strong>
          . Semakin mendekati 1, semakin baik
          pemisahan antarkelompok dibandingkan
          kedekatan di dalam kelompok.
        </div>
      </ReportSection>

      <ReportSection
        eyebrow="Perencanaan Sumber Daya"
        title="Ranking Prioritas Anggaran"
        icon={
          <WalletCards size={20} />
        }
      >
        <div className="mb-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-4 print:grid-cols-4">
          <MetricBox
            label="Total poin"
            value={budgetPriorities.total_priority_points}
          />

          <MetricBox
            label="Poin terbesar"
            value={
              highestBudgetPriority
                ?.priority_points
              ?? 0
            }
          />

          <MetricBox
            label="Kelompok teratas"
            value={
              highestBudgetPriority
                ? `K${highestBudgetPriority.cluster_number}`
                : "-"
            }
          />

          <MetricBox
            label="Urgensi tertinggi"
            value={
              highestUrgency
                ?.urgency_index
                .toFixed(2)
              ?? "-"
            }
          />
        </div>

        <div className="space-y-4">
          {budgetPriorities.items.map((item) => (
            <BudgetRankingRow
              key={item.cluster_number}
              item={item}
            />
          ))}
        </div>

        <div className="mt-5 rounded-xl border border-amber-200 bg-amber-50 p-4">
          <div className="flex gap-3">
            <AlertTriangle
              size={19}
              className="mt-0.5 shrink-0 text-amber-700"
            />

            <p className="text-sm leading-6 text-amber-900">
              {budgetPriorities.budget_note}
            </p>
          </div>
        </div>
      </ReportSection>

      <section className="grid gap-6 xl:grid-cols-2 print:grid-cols-2 print:break-inside-avoid">
        <ReportSection
          eyebrow="Metodologi"
          title="Dasar Perhitungan"
          icon={
            <BarChart3 size={20} />
          }
        >
          <p className="text-sm leading-6 text-slate-700">
            {budgetPriorities.methodology}
          </p>

          <div className="mt-5 rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm leading-6 text-slate-700">
            Model aktif:{" "}
            <strong>
              {analyticsSummary.model_name}
            </strong>
            , versi{" "}
            <strong>
              {analyticsSummary.model_version}
            </strong>
            .
          </div>
        </ReportSection>

        <ReportSection
          eyebrow="Catatan Keputusan"
          title="Validasi dan Tindak Lanjut"
          icon={
            <ShieldAlert size={20} />
          }
        >
          <ul className="space-y-3 text-sm leading-6 text-slate-700">
            <ReportNote>
              Rekomendasi kelompok merupakan
              panduan awal dan harus disesuaikan
              dengan kondisi individual siswa.
            </ReportNote>

            <ReportNote>
              Hasil dengan penanda akses kritis
              perlu ditangani sebelum kegiatan
              pembelajaran berlangsung.
            </ReportNote>

            <ReportNote>
              Siswa yang memerlukan validasi guru
              perlu ditinjau bersama hasil asesmen
              dan observasi pembelajaran.
            </ReportNote>

            <ReportNote>
              Skor prioritas sumber daya tidak
              menggantikan proses penyusunan
              Rencana Anggaran Biaya.
            </ReportNote>
          </ul>
        </ReportSection>
      </section>

      <footer className="border-t border-slate-200 pt-5 text-xs leading-5 text-slate-500 print:break-inside-avoid">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <p>
            Laporan dibuat otomatis oleh InkluMap
            berdasarkan data pada model aktif.
          </p>

          <p>
            Dibuat {generatedAt} WIB
          </p>
        </div>
      </footer>

      <div className="flex justify-end print:hidden">
        <button
          type="button"
          onClick={() => {
            window.print();
          }}
          className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border border-blue-200 bg-blue-50 px-5 text-sm font-semibold text-blue-700 transition hover:bg-blue-100"
        >
          <FileDown size={18} />

          Cetak atau Simpan sebagai PDF
        </button>
      </div>
    </div>
  );
}


interface SummaryCardProps {
  title: string;
  value: number | string;
  description: string;
  icon: ReactNode;
}


function SummaryCard({
  title,
  value,
  description,
  icon,
}: SummaryCardProps) {
  return (
    <article className="rounded-xl border border-slate-200 bg-slate-50 p-4 print:p-3">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium text-slate-500">
            {title}
          </p>

          <p className="mt-1 text-2xl font-bold text-slate-900">
            {value}
          </p>

          <p className="mt-1 text-xs text-slate-500">
            {description}
          </p>
        </div>

        <div className="rounded-lg bg-blue-50 p-2 text-blue-700">
          {icon}
        </div>
      </div>
    </article>
  );
}


interface ReportSectionProps {
  eyebrow: string;
  title: string;
  icon: ReactNode;
  children: ReactNode;
}


function ReportSection({
  eyebrow,
  title,
  icon,
  children,
}: ReportSectionProps) {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm print:break-inside-avoid print:rounded-none print:shadow-none">
      <div className="mb-5 flex items-start gap-3 border-b border-slate-200 pb-4">
        <div className="rounded-xl bg-blue-50 p-3 text-blue-700 print:p-2">
          {icon}
        </div>

        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-blue-700">
            {eyebrow}
          </p>

          <h2 className="mt-1 text-xl font-bold text-slate-900">
            {title}
          </h2>
        </div>
      </div>

      {children}
    </section>
  );
}


interface ProgressRowProps {
  label: string;
  value: number;
  total: number;
  className: string;
}


function ProgressRow({
  label,
  value,
  total,
  className,
}: ProgressRowProps) {
  const progress = percentage(
    value,
    total,
  );

  return (
    <div>
      <div className="mb-2 flex items-center justify-between gap-4 text-sm">
        <span className="font-medium text-slate-700">
          {label}
        </span>

        <span className="font-semibold text-slate-900">
          {value} ({progress}%)
        </span>
      </div>

      <div className="h-2.5 overflow-hidden rounded-full bg-slate-100">
        <div
          className={[
            "h-full rounded-full",
            className,
          ].join(" ")}
          style={{
            width: `${progress}%`,
          }}
        />
      </div>
    </div>
  );
}


interface MetricBoxProps {
  label: string;
  value: number | string;
}


function MetricBox({
  label,
  value,
}: MetricBoxProps) {
  return (
    <div className="rounded-xl border border-slate-200 bg-slate-50 p-3">
      <p className="text-xs leading-5 text-slate-500">
        {label}
      </p>

      <p className="mt-1 text-lg font-bold text-slate-900">
        {value}
      </p>
    </div>
  );
}


interface TableContentProps {
  children: ReactNode;
}


function TableHeader({
  children,
}: TableContentProps) {
  return (
    <th
      scope="col"
      className="whitespace-nowrap px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500"
    >
      {children}
    </th>
  );
}


function TableCell({
  children,
}: TableContentProps) {
  return (
    <td className="px-4 py-4 text-sm text-slate-700">
      {children}
    </td>
  );
}


interface BudgetRankingRowProps {
  item: BudgetPriorityItem;
}


function BudgetRankingRow({
  item,
}: BudgetRankingRowProps) {
  return (
    <article className="rounded-xl border border-slate-200 p-4 print:break-inside-avoid">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-start gap-4">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-slate-900 font-bold text-white">
            {item.rank}
          </div>

          <div>
            <p className="font-semibold text-slate-900">
              Kelompok {item.cluster_number}
              {" Â· "}
              {item.cluster_name}
            </p>

            <p className="mt-1 text-xs leading-5 text-slate-500">
              {item.dominant_need}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-2 sm:min-w-80">
          <SmallMetric
            label="Poin"
            value={item.priority_points}
          />

          <SmallMetric
            label="Proporsi"
            value={`${item.priority_share_percentage}%`}
          />

          <SmallMetric
            label="Urgensi"
            value={item.urgency_index.toFixed(2)}
          />
        </div>
      </div>

      <div className="mt-4 h-2.5 overflow-hidden rounded-full bg-slate-100">
        <div
          className="h-full rounded-full bg-blue-600"
          style={{
            width: `${Math.min(
              item.priority_share_percentage,
              100,
            )}%`,
          }}
        />
      </div>

      <p className="mt-3 text-xs leading-5 text-slate-600">
        {item.rationale}
      </p>
    </article>
  );
}


interface SmallMetricProps {
  label: string;
  value: number | string;
}


function SmallMetric({
  label,
  value,
}: SmallMetricProps) {
  return (
    <div className="rounded-lg bg-slate-50 px-3 py-2 text-center">
      <p className="text-[11px] text-slate-500">
        {label}
      </p>

      <p className="mt-0.5 text-sm font-bold text-slate-900">
        {value}
      </p>
    </div>
  );
}


interface ReportNoteProps {
  children: ReactNode;
}


function ReportNote({
  children,
}: ReportNoteProps) {
  return (
    <li className="flex gap-3">
      <CheckCircle2
        size={18}
        className="mt-1 shrink-0 text-emerald-600"
      />

      <span>
        {children}
      </span>
    </li>
  );
}


function percentage(
  value: number,
  total: number,
): number {
  if (total <= 0) {
    return 0;
  }

  return Number(
    (
      (value / total)
      * 100
    ).toFixed(1),
  );
}
