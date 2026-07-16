"use client";

import {
  CheckCircle2,
  Eye,
  Filter,
  Lightbulb,
  RotateCcw,
  Search,
  ShieldAlert,
  Sparkles,
  Target,
  TriangleAlert,
  Users,
} from "lucide-react";
import Link from "next/link";
import {
  useMemo,
  useState,
  type ReactNode,
} from "react";

import type {
  AnalyticsStudentListItem,
  AnalyticsStudentListResponse,
  ClusterProfile,
  PriorityLevel,
} from "@/types/analytics";


interface RecommendationsDashboardProps {
  clusters: ClusterProfile[];
  students: AnalyticsStudentListResponse;
}


type ClusterFilter =
  | number
  | "all";


type PriorityFilter =
  | PriorityLevel
  | "all";


type AttentionFilter =
  | "all"
  | "critical"
  | "review";


export default function RecommendationsDashboard({
  clusters,
  students,
}: RecommendationsDashboardProps) {
  const [
    selectedClusterNumber,
    setSelectedClusterNumber,
  ] = useState<ClusterFilter>("all");

  const [
    selectedPriority,
    setSelectedPriority,
  ] = useState<PriorityFilter>("all");

  const [
    selectedAttention,
    setSelectedAttention,
  ] = useState<AttentionFilter>("all");

  const [
    search,
    setSearch,
  ] = useState("");

  const highPriorityCount =
    students.items.filter(
      (student) =>
        student.priority_level === "high",
    ).length;

  const reviewCount =
    students.items.filter(
      (student) =>
        student.needs_human_review,
    ).length;

  const criticalAccessCount =
    students.items.filter(
      (student) =>
        student.critical_access_flag,
    ).length;

  const uniqueRecommendationCount =
    new Set(
      clusters.flatMap(
        (cluster) =>
          cluster.recommendations,
      ),
    ).size;

  const selectedCluster =
    selectedClusterNumber === "all"
      ? null
      : (
        clusters.find(
          (cluster) =>
            cluster.cluster_number
            === selectedClusterNumber,
        )
        ?? null
      );

  const filteredStudents = useMemo(
    () => {
      const cleanedSearch =
        search.trim().toLowerCase();

      return students.items.filter(
        (student) => {
          const matchesCluster =
            selectedClusterNumber === "all"
            || student.cluster_number
              === selectedClusterNumber;

          const matchesPriority =
            selectedPriority === "all"
            || student.priority_level
              === selectedPriority;

          const matchesAttention =
            selectedAttention === "all"
            || (
              selectedAttention === "critical"
              && student.critical_access_flag
            )
            || (
              selectedAttention === "review"
              && student.needs_human_review
            );

          const searchableText = [
            student.student_code,
            student.initials ?? "",
            student.grade_level ?? "",
            student.class_name ?? "",
            student.cluster_name,
            ...student.dominant_needs,
          ]
            .join(" ")
            .toLowerCase();

          const matchesSearch =
            cleanedSearch.length === 0
            || searchableText.includes(
              cleanedSearch,
            );

          return (
            matchesCluster
            && matchesPriority
            && matchesAttention
            && matchesSearch
          );
        },
      );
    },
    [
      search,
      selectedAttention,
      selectedClusterNumber,
      selectedPriority,
      students.items,
    ],
  );


  function resetFilters() {
    setSelectedClusterNumber("all");
    setSelectedPriority("all");
    setSelectedAttention("all");
    setSearch("");
  }


  return (
    <div className="space-y-8">
      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <SummaryCard
          title="Rekomendasi Aktif"
          value={uniqueRecommendationCount}
          description="Akomodasi unik dari seluruh kelompok"
          icon={
            <Lightbulb size={22} />
          }
        />

        <SummaryCard
          title="Prioritas Tinggi"
          value={highPriorityCount}
          description="Siswa yang memerlukan tindak lanjut segera"
          icon={
            <Target size={22} />
          }
        />

        <SummaryCard
          title="Perlu Validasi"
          value={reviewCount}
          description="Hasil yang perlu ditinjau guru"
          icon={
            <ShieldAlert size={22} />
          }
        />

        <SummaryCard
          title="Akses Kritis"
          value={criticalAccessCount}
          description="Siswa dengan hambatan akses kritis"
          icon={
            <TriangleAlert size={22} />
          }
        />
      </section>

      <section className="rounded-2xl border border-blue-200 bg-blue-50 p-6">
        <div className="flex gap-4">
          <div className="rounded-xl bg-white p-3 text-blue-700">
            <Sparkles size={23} />
          </div>

          <div>
            <h2 className="font-semibold text-blue-950">
              Cara menggunakan rekomendasi
            </h2>

            <p className="mt-2 max-w-4xl text-sm leading-6 text-blue-900">
              Rekomendasi kelompok membantu sekolah
              menyusun langkah umum. Buka detail
              siswa untuk melihat kebutuhan dominan,
              rekomendasi individual, serta alasan
              validasi guru sebelum menerapkan
              akomodasi.
            </p>
          </div>
        </div>
      </section>

      <section>
        <div className="mb-5">
          <p className="text-sm font-semibold uppercase tracking-wider text-blue-700">
            Panduan Kelompok
          </p>

          <h2 className="mt-1 text-xl font-bold text-slate-900">
            Rekomendasi Berdasarkan Kelompok
          </h2>

          <p className="mt-2 text-sm leading-6 text-slate-500">
            Pilih kartu kelompok untuk memfokuskan
            daftar siswa dan melihat rekomendasi
            lengkap.
          </p>
        </div>

        <div className="grid gap-5 xl:grid-cols-2">
          {clusters.map((cluster) => {
            const isSelected =
              selectedClusterNumber
              === cluster.cluster_number;

            return (
              <article
                key={cluster.id}
                className={[
                  "rounded-2xl border p-6 shadow-sm transition",
                  isSelected
                    ? (
                      "border-blue-400 "
                      + "bg-blue-50"
                    )
                    : (
                      "border-slate-200 "
                      + "bg-white"
                    ),
                ].join(" ")}
              >
                <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                  <div>
                    <p className="text-sm font-semibold uppercase tracking-wider text-blue-700">
                      Kelompok{" "}
                      {cluster.cluster_number}
                    </p>

                    <h3 className="mt-2 text-xl font-bold text-slate-900">
                      {cluster.cluster_name}
                    </h3>
                  </div>

                  <span className="inline-flex w-fit rounded-full border border-blue-200 bg-white px-3 py-1 text-sm font-bold text-blue-800">
                    {cluster.cluster_size} siswa
                  </span>
                </div>

                <p className="mt-4 text-sm leading-6 text-slate-600">
                  {cluster.description}
                </p>

                <div className="mt-5 rounded-xl border border-slate-200 bg-white p-4">
                  <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Kebutuhan dominan
                  </p>

                  <p className="mt-1 font-semibold text-slate-900">
                    {cluster.dominant_need}
                  </p>
                </div>

                <ul className="mt-5 space-y-3">
                  {cluster.recommendations
                    .slice(0, 3)
                    .map((recommendation) => (
                      <li
                        key={recommendation}
                        className="flex gap-3 text-sm leading-6 text-slate-700"
                      >
                        <CheckCircle2
                          size={18}
                          className="mt-1 shrink-0 text-emerald-600"
                        />

                        <span>
                          {recommendation}
                        </span>
                      </li>
                    ))}
                </ul>

                <button
                  type="button"
                  onClick={() => {
                    setSelectedClusterNumber(
                      isSelected
                        ? "all"
                        : cluster.cluster_number,
                    );
                  }}
                  className={[
                    "mt-6 inline-flex min-h-11 w-full items-center justify-center rounded-xl px-4 text-sm font-semibold transition",
                    "focus:outline-none focus:ring-4 focus:ring-blue-100",
                    isSelected
                      ? (
                        "border border-blue-300 "
                        + "bg-white text-blue-700 "
                        + "hover:bg-blue-50"
                      )
                      : (
                        "bg-blue-600 text-white "
                        + "hover:bg-blue-700"
                      ),
                  ].join(" ")}
                >
                  {isSelected
                    ? "Tampilkan semua kelompok"
                    : "Fokuskan kelompok ini"}
                </button>
              </article>
            );
          })}
        </div>
      </section>

      {selectedCluster && (
        <section className="rounded-2xl border border-emerald-200 bg-emerald-50 p-6">
          <p className="text-sm font-semibold uppercase tracking-wider text-emerald-700">
            Rekomendasi Lengkap Kelompok{" "}
            {selectedCluster.cluster_number}
          </p>

          <h2 className="mt-2 text-2xl font-bold text-emerald-950">
            {selectedCluster.cluster_name}
          </h2>

          <ul className="mt-5 grid gap-3 lg:grid-cols-2">
            {selectedCluster.recommendations.map(
              (recommendation) => (
                <li
                  key={recommendation}
                  className="flex gap-3 rounded-xl border border-emerald-200 bg-white p-4 text-sm leading-6 text-slate-700"
                >
                  <CheckCircle2
                    size={18}
                    className="mt-1 shrink-0 text-emerald-600"
                  />

                  <span>
                    {recommendation}
                  </span>
                </li>
              ),
            )}
          </ul>
        </section>
      )}

      <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="mb-5 flex items-start gap-3">
          <div className="rounded-xl bg-blue-50 p-3 text-blue-700">
            <Filter size={20} />
          </div>

          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              Filter Tindak Lanjut Siswa
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Temukan siswa berdasarkan kelompok,
              prioritas, dan penanda perhatian.
            </p>
          </div>
        </div>

        <div className="grid gap-4 lg:grid-cols-2 xl:grid-cols-[1.2fr_220px_200px_220px_auto]">
          <div>
            <label
              htmlFor="recommendation-search"
              className="mb-2 block text-sm font-medium text-slate-700"
            >
              Cari siswa
            </label>

            <div className="relative">
              <Search
                aria-hidden="true"
                size={19}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
              />

              <input
                id="recommendation-search"
                type="search"
                value={search}
                onChange={(event) => {
                  setSearch(
                    event.target.value,
                  );
                }}
                placeholder="Kode, inisial, kelas, atau kebutuhan"
                className="w-full rounded-xl border border-slate-300 bg-white py-2.5 pl-10 pr-4 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
              />
            </div>
          </div>

          <div>
            <label
              htmlFor="recommendation-cluster"
              className="mb-2 block text-sm font-medium text-slate-700"
            >
              Kelompok
            </label>

            <select
              id="recommendation-cluster"
              value={selectedClusterNumber}
              onChange={(event) => {
                const value =
                  event.target.value;

                setSelectedClusterNumber(
                  value === "all"
                    ? "all"
                    : Number(value),
                );
              }}
              className="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
            >
              <option value="all">
                Semua kelompok
              </option>

              {clusters.map((cluster) => (
                <option
                  key={cluster.id}
                  value={cluster.cluster_number}
                >
                  Kelompok {cluster.cluster_number}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label
              htmlFor="recommendation-priority"
              className="mb-2 block text-sm font-medium text-slate-700"
            >
              Prioritas
            </label>

            <select
              id="recommendation-priority"
              value={selectedPriority}
              onChange={(event) => {
                const value =
                  event.target.value;

                if (
                  value === "all"
                  || value === "high"
                  || value === "medium"
                  || value === "low"
                ) {
                  setSelectedPriority(value);
                }
              }}
              className="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
            >
              <option value="all">
                Semua prioritas
              </option>

              <option value="high">
                Tinggi
              </option>

              <option value="medium">
                Sedang
              </option>

              <option value="low">
                Rendah
              </option>
            </select>
          </div>

          <div>
            <label
              htmlFor="recommendation-attention"
              className="mb-2 block text-sm font-medium text-slate-700"
            >
              Penanda
            </label>

            <select
              id="recommendation-attention"
              value={selectedAttention}
              onChange={(event) => {
                const value =
                  event.target.value;

                if (
                  value === "all"
                  || value === "critical"
                  || value === "review"
                ) {
                  setSelectedAttention(value);
                }
              }}
              className="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
            >
              <option value="all">
                Semua penanda
              </option>

              <option value="critical">
                Akses kritis
              </option>

              <option value="review">
                Perlu validasi
              </option>
            </select>
          </div>

          <div className="flex items-end">
            <button
              type="button"
              onClick={resetFilters}
              className="inline-flex min-h-11 w-full items-center justify-center gap-2 rounded-xl border border-slate-300 px-4 text-sm font-semibold text-slate-700 transition hover:bg-slate-100 xl:w-auto"
            >
              <RotateCcw size={18} />

              Reset
            </button>
          </div>
        </div>
      </section>

      <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="flex flex-col gap-3 border-b border-slate-200 p-5 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              Daftar Tindak Lanjut
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Menampilkan{" "}
              <span className="font-semibold">
                {filteredStudents.length}
              </span>{" "}
              dari{" "}
              <span className="font-semibold">
                {students.total}
              </span>{" "}
              siswa.
            </p>
          </div>

          <span className="inline-flex w-fit items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-semibold text-slate-700">
            <Users size={15} />

            Hasil analytics aktif
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50">
              <tr>
                <TableHeader>
                  Siswa
                </TableHeader>

                <TableHeader>
                  Kelompok
                </TableHeader>

                <TableHeader>
                  Prioritas
                </TableHeader>

                <TableHeader>
                  Kebutuhan dominan
                </TableHeader>

                <TableHeader>
                  Tindak lanjut
                </TableHeader>

                <TableHeader>
                  Aksi
                </TableHeader>
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-100 bg-white">
              {filteredStudents.map(
                (student) => (
                  <StudentRecommendationRow
                    key={student.cluster_result_id}
                    student={student}
                  />
                ),
              )}
            </tbody>
          </table>
        </div>

        {filteredStudents.length === 0 && (
          <div className="px-5 py-12 text-center">
            <p className="font-medium text-slate-700">
              Data tindak lanjut tidak ditemukan
            </p>

            <p className="mt-1 text-sm text-slate-500">
              Ubah pencarian atau reset filter.
            </p>
          </div>
        )}
      </section>
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
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-600">
            {title}
          </p>

          <p className="mt-2 text-3xl font-bold text-slate-900">
            {value}
          </p>

          <p className="mt-1 text-xs leading-5 text-slate-500">
            {description}
          </p>
        </div>

        <div className="rounded-xl bg-blue-50 p-3 text-blue-700">
          {icon}
        </div>
      </div>
    </article>
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
      className="whitespace-nowrap px-5 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500"
    >
      {children}
    </th>
  );
}


function TableCell({
  children,
}: TableContentProps) {
  return (
    <td className="px-5 py-4 align-top text-sm text-slate-600">
      {children}
    </td>
  );
}


interface StudentRecommendationRowProps {
  student: AnalyticsStudentListItem;
}


function StudentRecommendationRow({
  student,
}: StudentRecommendationRowProps) {
  return (
    <tr className="transition hover:bg-slate-50">
      <TableCell>
        <div className="min-w-32">
          <p className="font-semibold text-slate-900">
            {student.student_code}
          </p>

          <p className="mt-1 text-xs text-slate-500">
            Inisial {student.initials ?? "-"}
            {" · "}
            {student.class_name ?? "-"}
          </p>
        </div>
      </TableCell>

      <TableCell>
        <div className="max-w-64">
          <p className="font-semibold text-slate-800">
            Kelompok {student.cluster_number}
          </p>

          <p className="mt-1 text-xs leading-5 text-slate-500">
            {student.cluster_name}
          </p>
        </div>
      </TableCell>

      <TableCell>
        <PriorityBadge
          priority={student.priority_level}
        />
      </TableCell>

      <TableCell>
        <div className="flex max-w-72 flex-wrap gap-1.5">
          {student.dominant_needs.map(
            (need) => (
              <span
                key={need}
                className="rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1 text-xs font-medium text-slate-700"
              >
                {need}
              </span>
            ),
          )}
        </div>
      </TableCell>

      <TableCell>
        <div className="flex max-w-64 flex-wrap gap-1.5">
          {student.critical_access_flag && (
            <AttentionBadge
              label="Atasi akses kritis"
              variant="critical"
            />
          )}

          {student.needs_human_review && (
            <AttentionBadge
              label="Validasi guru"
              variant="review"
            />
          )}

          {!student.critical_access_flag
            && !student.needs_human_review && (
              <AttentionBadge
                label="Pantau penerapan"
                variant="normal"
              />
            )}
        </div>
      </TableCell>

      <TableCell>
        <Link
          href={`/students/${student.student_id}`}
          aria-label={
            `Buka rekomendasi ${student.student_code}`
          }
          className="inline-flex items-center gap-2 rounded-lg border border-blue-200 bg-blue-50 px-3 py-2 text-xs font-semibold text-blue-700 transition hover:bg-blue-100 focus:outline-none focus:ring-4 focus:ring-blue-100"
        >
          <Eye size={16} />

          Lihat Detail
        </Link>
      </TableCell>
    </tr>
  );
}


interface PriorityBadgeProps {
  priority: PriorityLevel;
}


function PriorityBadge({
  priority,
}: PriorityBadgeProps) {
  const configuration = {
    high: {
      label: "Tinggi",
      className: (
        "border-red-200 "
        + "bg-red-50 "
        + "text-red-700"
      ),
    },
    medium: {
      label: "Sedang",
      className: (
        "border-amber-200 "
        + "bg-amber-50 "
        + "text-amber-700"
      ),
    },
    low: {
      label: "Rendah",
      className: (
        "border-emerald-200 "
        + "bg-emerald-50 "
        + "text-emerald-700"
      ),
    },
  } satisfies Record<
    PriorityLevel,
    {
      label: string;
      className: string;
    }
  >;

  return (
    <span
      className={[
        "inline-flex rounded-full border px-3 py-1 text-xs font-semibold",
        configuration[priority].className,
      ].join(" ")}
    >
      {configuration[priority].label}
    </span>
  );
}


interface AttentionBadgeProps {
  label: string;
  variant:
    | "critical"
    | "normal"
    | "review";
}


function AttentionBadge({
  label,
  variant,
}: AttentionBadgeProps) {
  const className = {
    critical: (
      "border-red-200 "
      + "bg-red-50 "
      + "text-red-700"
    ),
    review: (
      "border-amber-200 "
      + "bg-amber-50 "
      + "text-amber-800"
    ),
    normal: (
      "border-emerald-200 "
      + "bg-emerald-50 "
      + "text-emerald-700"
    ),
  }[variant];

  return (
    <span
      className={[
        "inline-flex rounded-full border px-2.5 py-1 text-xs font-semibold",
        className,
      ].join(" ")}
    >
      {label}
    </span>
  );
}
