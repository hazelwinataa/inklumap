"use client";

import {
  ChevronLeft,
  ChevronRight,
  Eye,
  RotateCcw,
  Search,
} from "lucide-react";
import Link from "next/link";
import {
  useState,
  type FormEvent,
  type ReactNode,
} from "react";

import {
  getStudents,
} from "@/lib/api";
import type {
  AssessmentStatus,
  StudentListResponse,
} from "@/types/students";


interface StudentsTableProps {
  initialData: StudentListResponse;
}


export default function StudentsTable({
  initialData,
}: StudentsTableProps) {
  const [
    data,
    setData,
  ] = useState(initialData);

  const [
    search,
    setSearch,
  ] = useState("");

  const [
    assessmentStatus,
    setAssessmentStatus,
  ] = useState<AssessmentStatus | "">("");

  const [
    appliedSearch,
    setAppliedSearch,
  ] = useState("");

  const [
    appliedStatus,
    setAppliedStatus,
  ] = useState<AssessmentStatus | "">("");

  const [
    isLoading,
    setIsLoading,
  ] = useState(false);

  const [
    errorMessage,
    setErrorMessage,
  ] = useState("");

  const totalPages = Math.max(
    1,
    Math.ceil(
      data.total / data.limit,
    ),
  );

  const currentPage =
    Math.floor(
      data.skip / data.limit,
    ) + 1;


  async function loadStudents(
    skip: number,
    currentSearch: string,
    currentStatus: AssessmentStatus | "",
  ) {
    setIsLoading(true);
    setErrorMessage("");

    const result = await getStudents({
      skip,
      limit: data.limit,
      search: currentSearch || undefined,
      assessmentStatus:
        currentStatus || undefined,
    });

    if (!result) {
      setErrorMessage(
        "Data siswa gagal dimuat. Pastikan backend masih berjalan.",
      );

      setIsLoading(false);
      return;
    }

    setData(result);
    setIsLoading(false);
  }


  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    const cleanedSearch =
      search.trim();

    setAppliedSearch(cleanedSearch);
    setAppliedStatus(
      assessmentStatus,
    );

    await loadStudents(
      0,
      cleanedSearch,
      assessmentStatus,
    );
  }


  async function handleReset() {
    setSearch("");
    setAssessmentStatus("");
    setAppliedSearch("");
    setAppliedStatus("");

    await loadStudents(
      0,
      "",
      "",
    );
  }


  async function handlePreviousPage() {
    const nextSkip = Math.max(
      0,
      data.skip - data.limit,
    );

    await loadStudents(
      nextSkip,
      appliedSearch,
      appliedStatus,
    );
  }


  async function handleNextPage() {
    const nextSkip =
      data.skip + data.limit;

    if (nextSkip >= data.total) {
      return;
    }

    await loadStudents(
      nextSkip,
      appliedSearch,
      appliedStatus,
    );
  }


  return (
    <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="border-b border-slate-200 p-5">
        <form
          onSubmit={handleSubmit}
          className="grid gap-4 lg:grid-cols-[1fr_240px_auto]"
        >
          <div>
            <label
              htmlFor="student-search"
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
                id="student-search"
                type="search"
                value={search}
                onChange={(event) => {
                  setSearch(
                    event.target.value,
                  );
                }}
                placeholder="Kode siswa atau inisial"
                className="w-full rounded-xl border border-slate-300 bg-white py-2.5 pl-10 pr-4 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
              />
            </div>
          </div>

          <div>
            <label
              htmlFor="assessment-status"
              className="mb-2 block text-sm font-medium text-slate-700"
            >
              Status asesmen
            </label>

            <select
              id="assessment-status"
              value={assessmentStatus}
              onChange={(event) => {
                const selectedStatus =
                  event.target.value as
                    AssessmentStatus | "";

                setAssessmentStatus(
                  selectedStatus,
                );
              }}
              className="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
            >
              <option value="">
                Semua status
              </option>

              <option value="complete">
                Lengkap
              </option>

              <option value="incomplete">
                Belum lengkap
              </option>

              <option value="not_started">
                Belum dimulai
              </option>
            </select>
          </div>

          <div className="flex items-end gap-2">
            <button
              type="submit"
              disabled={isLoading}
              className="inline-flex min-h-11 items-center justify-center rounded-xl bg-blue-600 px-5 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isLoading
                ? "Memuat..."
                : "Terapkan"}
            </button>

            <button
              type="button"
              aria-label="Reset filter"
              disabled={isLoading}
              onClick={handleReset}
              className="inline-flex min-h-11 min-w-11 items-center justify-center rounded-xl border border-slate-300 text-slate-700 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-60"
            >
              <RotateCcw size={18} />
            </button>
          </div>
        </form>
      </div>

      {errorMessage && (
        <div
          role="alert"
          className="border-b border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700"
        >
          {errorMessage}
        </div>
      )}

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
                Jenjang
              </TableHeader>

              <TableHeader>
                Kelas
              </TableHeader>

              <TableHeader>
                Semester
              </TableHeader>

              <TableHeader>
                Tahun ajaran
              </TableHeader>

              <TableHeader>
                Status asesmen
              </TableHeader>

              <TableHeader>
                Aksi
              </TableHeader>
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-100 bg-white">
            {data.items.map((student) => (
              <tr
                key={student.id}
                className="transition hover:bg-slate-50"
              >
                <TableCell>
                  <span className="font-semibold text-slate-900">
                    {student.student_code}
                  </span>
                </TableCell>

                <TableCell>
                  {student.initials ?? "-"}
                </TableCell>

                <TableCell>
                  {student.grade_level ?? "-"}
                </TableCell>

                <TableCell>
                  {student.class_name ?? "-"}
                </TableCell>

                <TableCell>
                  {student.semester ?? "-"}
                </TableCell>

                <TableCell>
                  {student.school_year ?? "-"}
                </TableCell>

                <TableCell>
                  <StatusBadge
                    status={
                      student.assessment_status
                    }
                  />
                </TableCell>

                <TableCell>
                  <Link
                    href={`/students/${student.id}`}
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
            ))}
          </tbody>
        </table>
      </div>

      {data.items.length === 0 && (
        <div className="px-5 py-12 text-center">
          <p className="font-medium text-slate-700">
            Data siswa tidak ditemukan
          </p>

          <p className="mt-1 text-sm text-slate-500">
            Coba ubah kata pencarian atau
            status asesmen.
          </p>
        </div>
      )}

      <div className="flex flex-col gap-4 border-t border-slate-200 px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-sm text-slate-600">
          Menampilkan{" "}
          <span className="font-semibold">
            {data.items.length}
          </span>{" "}
          dari{" "}
          <span className="font-semibold">
            {data.total}
          </span>{" "}
          siswa
        </p>

        <div className="flex items-center gap-3">
          <button
            type="button"
            aria-label="Halaman sebelumnya"
            disabled={
              data.skip === 0 ||
              isLoading
            }
            onClick={handlePreviousPage}
            className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-slate-300 text-slate-700 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-40"
          >
            <ChevronLeft size={18} />
          </button>

          <span className="min-w-28 text-center text-sm font-medium text-slate-700">
            Halaman {currentPage} dari{" "}
            {totalPages}
          </span>

          <button
            type="button"
            aria-label="Halaman berikutnya"
            disabled={
              currentPage >= totalPages ||
              isLoading
            }
            onClick={handleNextPage}
            className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-slate-300 text-slate-700 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-40"
          >
            <ChevronRight size={18} />
          </button>
        </div>
      </div>
    </section>
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
    <td className="whitespace-nowrap px-5 py-4 text-sm text-slate-600">
      {children}
    </td>
  );
}


interface StatusBadgeProps {
  status: AssessmentStatus;
}


function StatusBadge({
  status,
}: StatusBadgeProps) {
  const statusConfiguration = {
    complete: {
      label: "Lengkap",
      className: (
        "border-emerald-200 "
        + "bg-emerald-50 "
        + "text-emerald-700"
      ),
    },
    incomplete: {
      label: "Belum lengkap",
      className: (
        "border-amber-200 "
        + "bg-amber-50 "
        + "text-amber-700"
      ),
    },
    not_started: {
      label: "Belum dimulai",
      className: (
        "border-slate-200 "
        + "bg-slate-100 "
        + "text-slate-700"
      ),
    },
  } satisfies Record<
    AssessmentStatus,
    {
      label: string;
      className: string;
    }
  >;

  const configuration =
    statusConfiguration[status];

  return (
    <span
      className={[
        "inline-flex rounded-full border px-3 py-1 text-xs font-semibold",
        configuration.className,
      ].join(" ")}
    >
      {configuration.label}
    </span>
  );
}