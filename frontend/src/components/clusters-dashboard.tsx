"use client";

import {
  BarChart3,
  CheckCircle2,
  Eye,
  Network,
  RotateCcw,
  Search,
  ShieldAlert,
  Target,
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


interface ClustersDashboardProps {
  clusters: ClusterProfile[];
  students: AnalyticsStudentListResponse;
}


type ClusterFilter =
  | number
  | "all";


type PriorityFilter =
  | PriorityLevel
  | "all";


export default function ClustersDashboard({
  clusters,
  students,
}: ClustersDashboardProps) {
  const [
    selectedClusterNumber,
    setSelectedClusterNumber,
  ] = useState<ClusterFilter>("all");

  const [
    selectedPriority,
    setSelectedPriority,
  ] = useState<PriorityFilter>("all");

  const [
    search,
    setSearch,
  ] = useState("");

  const totalClusterStudents =
    clusters.reduce(
      (total, cluster) =>
        total + cluster.cluster_size,
      0,
    );

  const largestCluster =
    clusters.reduce<ClusterProfile | null>(
      (currentLargest, cluster) => {
        if (
          currentLargest === null
          || cluster.cluster_size
            > currentLargest.cluster_size
        ) {
          return cluster;
        }

        return currentLargest;
      },
      null,
    );

  const modelSilhouette =
    clusters[0]?.model_silhouette_score
    ?? null;

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

          const searchValues = [
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
            !cleanedSearch
            || searchValues.includes(
              cleanedSearch,
            );

          return (
            matchesCluster
            && matchesPriority
            && matchesSearch
          );
        },
      );
    },
    [
      search,
      selectedClusterNumber,
      selectedPriority,
      students.items,
    ],
  );


  function resetFilters() {
    setSelectedClusterNumber("all");
    setSelectedPriority("all");
    setSearch("");
  }


  return (
    <div className="space-y-8">
      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <SummaryCard
          title="Jumlah Kelompok"
          value={clusters.length}
          description="Kelompok kebutuhan aktif"
          icon={
            <Network size={22} />
          }
        />

        <SummaryCard
          title="Siswa Dianalisis"
          value={totalClusterStudents}
          description="Memiliki hasil clustering"
          icon={
            <Users size={22} />
          }
        />

        <SummaryCard
          title="Silhouette Model"
          value={
            modelSilhouette === null
              ? "-"
              : modelSilhouette.toFixed(4)
          }
          description="Kualitas pemisahan kelompok"
          icon={
            <BarChart3 size={22} />
          }
        />

        <SummaryCard
          title="Kelompok Terbesar"
          value={
            largestCluster?.cluster_size
            ?? 0
          }
          description={
            largestCluster?.cluster_name
            ?? "Belum tersedia"
          }
          icon={
            <Target size={22} />
          }
        />
      </section>

      <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="mb-5">
          <h2 className="text-lg font-semibold text-slate-900">
            Filter Data Kelompok
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Pilih kelompok atau tingkat prioritas
            untuk melihat siswa yang relevan.
          </p>
        </div>

        <div className="grid gap-4 lg:grid-cols-[1fr_240px_220px_auto]">
          <div>
            <label
              htmlFor="cluster-student-search"
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
                id="cluster-student-search"
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
              htmlFor="cluster-filter"
              className="mb-2 block text-sm font-medium text-slate-700"
            >
              Kelompok
            </label>

            <select
              id="cluster-filter"
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
              htmlFor="priority-filter"
              className="mb-2 block text-sm font-medium text-slate-700"
            >
              Prioritas
            </label>

            <select
              id="priority-filter"
              value={selectedPriority}
              onChange={(event) => {
                const priorityValue =
                  event.target.value as PriorityFilter;

                setSelectedPriority(
                  priorityValue,
                );
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

          <div className="flex items-end">
            <button
              type="button"
              onClick={resetFilters}
              className="inline-flex min-h-11 w-full items-center justify-center gap-2 rounded-xl border border-slate-300 px-4 text-sm font-semibold text-slate-700 transition hover:bg-slate-100 lg:w-auto"
            >
              <RotateCcw size={18} />

              Reset
            </button>
          </div>
        </div>
      </section>

      <section>
        <div className="mb-5">
          <h2 className="text-xl font-bold text-slate-900">
            Profil Kelompok Kebutuhan
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Setiap kelompok menggambarkan pola
            kebutuhan yang serupa, bukan diagnosis
            terhadap siswa.
          </p>
        </div>

        <div className="grid gap-5 xl:grid-cols-2">
          {clusters.map((cluster) => {
            const isSelected =
              selectedClusterNumber
              === cluster.cluster_number;

            return (
              <button
                key={cluster.id}
                type="button"
                onClick={() => {
                  setSelectedClusterNumber(
                    isSelected
                      ? "all"
                      : cluster.cluster_number,
                  );
                }}
                className={[
                  "rounded-2xl border p-6 text-left shadow-sm transition",
                  "focus:outline-none focus:ring-4 focus:ring-blue-100",
                  isSelected
                    ? (
                      "border-blue-400 "
                      + "bg-blue-50"
                    )
                    : (
                      "border-slate-200 "
                      + "bg-white "
                      + "hover:border-blue-200 "
                      + "hover:bg-slate-50"
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

                <div className="mt-5 grid gap-4 sm:grid-cols-3">
                  <ClusterFact
                    label="Kebutuhan Dominan"
                    value={cluster.dominant_need}
                  />

                  <ClusterFact
                    label="Siswa Representatif"
                    value={cluster.medoid_student_code}
                  />

                  <ClusterFact
                    label="Rata-rata Jarak"
                    value={
                      cluster.mean_medoid_distance
                        .toFixed(4)
                    }
                  />
                </div>

                <div className="mt-5">
                  <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Rekomendasi Utama
                  </p>

                  <ul className="mt-3 space-y-2">
                    {cluster.recommendations
                      .slice(0, 3)
                      .map((recommendation) => (
                        <li
                          key={recommendation}
                          className="flex gap-2 text-sm leading-6 text-slate-700"
                        >
                          <CheckCircle2
                            size={17}
                            className="mt-1 shrink-0 text-emerald-600"
                          />

                          <span>
                            {recommendation}
                          </span>
                        </li>
                      ))}
                  </ul>
                </div>
              </button>
            );
          })}
        </div>
      </section>

      {selectedCluster && (
        <section className="rounded-2xl border border-blue-200 bg-blue-50 p-6">
          <p className="text-sm font-semibold uppercase tracking-wider text-blue-700">
            Detail Kelompok{" "}
            {selectedCluster.cluster_number}
          </p>

          <h2 className="mt-2 text-2xl font-bold text-blue-950">
            {selectedCluster.cluster_name}
          </h2>

          <p className="mt-3 max-w-4xl text-sm leading-6 text-blue-900">
            {selectedCluster.description}
          </p>

          <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <ClusterFact
              label="Model"
              value={
                selectedCluster.model_name
              }
            />

            <ClusterFact
              label="Metrik Jarak"
              value={
                selectedCluster.distance_metric
              }
            />

            <ClusterFact
              label="Linkage"
              value={
                selectedCluster.linkage
              }
            />

            <ClusterFact
              label="Versi Model"
              value={
                selectedCluster.model_version
              }
            />
          </div>

          <div className="mt-6">
            <h3 className="font-semibold text-blue-950">
              Rekomendasi Kelompok
            </h3>

            <ul className="mt-3 grid gap-3 lg:grid-cols-2">
              {selectedCluster.recommendations.map(
                (recommendation) => (
                  <li
                    key={recommendation}
                    className="flex gap-3 rounded-xl border border-blue-200 bg-white p-4 text-sm leading-6 text-slate-700"
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
          </div>
        </section>
      )}

      <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="flex flex-col gap-3 border-b border-slate-200 p-5 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              Siswa dalam Kelompok
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
              siswa yang memiliki hasil analytics.
            </p>
          </div>

          {selectedCluster && (
            <span className="inline-flex w-fit rounded-full border border-blue-200 bg-blue-50 px-3 py-1.5 text-xs font-semibold text-blue-700">
              Kelompok{" "}
              {selectedCluster.cluster_number}
            </span>
          )}
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50">
              <tr>
                <TableHeader>
                  Kode siswa
                </TableHeader>

                <TableHeader>
                  Inisial
                </TableHeader>

                <TableHeader>
                  Kelas
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
                  Penanda
                </TableHeader>

                <TableHeader>
                  Aksi
                </TableHeader>
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-100 bg-white">
              {filteredStudents.map(
                (student) => (
                  <StudentRow
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
              Siswa tidak ditemukan
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

          <p className="mt-1 line-clamp-2 text-xs text-slate-500">
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


interface ClusterFactProps {
  label: string;
  value: string;
}


function ClusterFact({
  label,
  value,
}: ClusterFactProps) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
        {label}
      </p>

      <p className="mt-1 text-sm font-semibold text-slate-900">
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
      className="whitespace-nowrap px-5 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500"
    >
      {children}
    </th>
  );
}


interface StudentRowProps {
  student: AnalyticsStudentListItem;
}


function StudentRow({
  student,
}: StudentRowProps) {
  return (
    <tr className="transition hover:bg-slate-50">
      <TableCell>
        <span className="font-semibold text-slate-900">
          {student.student_code}
        </span>
      </TableCell>

      <TableCell>
        {student.initials ?? "-"}
      </TableCell>

      <TableCell>
        <div>
          <p>
            {student.grade_level ?? "-"}
          </p>

          <p className="text-xs text-slate-500">
            Kelas {student.class_name ?? "-"}
          </p>
        </div>
      </TableCell>

      <TableCell>
        <div className="max-w-60">
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
        <StudentFlags
          student={student}
        />
      </TableCell>

      <TableCell>
        <Link
          href={`/students/${student.student_id}`}
          aria-label={
            `Lihat detail ${student.student_code}`
          }
          className="inline-flex items-center gap-2 rounded-lg border border-blue-200 bg-blue-50 px-3 py-2 text-xs font-semibold text-blue-700 transition hover:bg-blue-100 focus:outline-none focus:ring-4 focus:ring-blue-100"
        >
          <Eye size={16} />

          Detail
        </Link>
      </TableCell>
    </tr>
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


interface StudentFlagsProps {
  student: AnalyticsStudentListItem;
}


function StudentFlags({
  student,
}: StudentFlagsProps) {
  const hasFlags =
    student.critical_access_flag
    || student.dbscan_unique_case
    || student.needs_human_review;

  if (!hasFlags) {
    return (
      <span className="inline-flex items-center gap-1.5 rounded-full border border-emerald-200 bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700">
        <CheckCircle2 size={14} />

        Tidak ada
      </span>
    );
  }

  return (
    <div className="flex max-w-56 flex-wrap gap-1.5">
      {student.critical_access_flag && (
        <FlagBadge label="Akses kritis" />
      )}

      {student.dbscan_unique_case && (
        <FlagBadge label="Kasus unik" />
      )}

      {student.needs_human_review && (
        <FlagBadge label="Perlu tinjauan" />
      )}
    </div>
  );
}


interface FlagBadgeProps {
  label: string;
}


function FlagBadge({
  label,
}: FlagBadgeProps) {
  return (
    <span className="inline-flex items-center gap-1.5 rounded-full border border-amber-200 bg-amber-50 px-2.5 py-1 text-xs font-semibold text-amber-800">
      <ShieldAlert size={14} />

      {label}
    </span>
  );
}
