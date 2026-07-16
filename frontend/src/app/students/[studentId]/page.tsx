import {
  AlertTriangle,
  ArrowLeft,
  CalendarDays,
  CheckCircle2,
  FileText,
  GraduationCap,
  Lightbulb,
  PencilLine,
  School,
  ShieldAlert,
  UserRound,
  Wrench,
} from "lucide-react";
import Link from "next/link";
import {
  notFound,
} from "next/navigation";
import type {
  ReactNode,
} from "react";

import {
  getAnalyticsStudentDetail,
  getStudentDetail,
} from "@/lib/api";
import type {
  AssessmentStatus,
} from "@/types/students";


interface StudentDetailPageProps {
  params: Promise<{
    studentId: string;
  }>;

  searchParams: Promise<{
    saved?: string;
    analytics?: string;
  }>;
}


export default async function StudentDetailPage({
  params,
  searchParams,
}: StudentDetailPageProps) {
  const {
    studentId,
  } = await params;

  const {
    saved,
    analytics: analyticsStatus,
  } = await searchParams;

  const savedMode =
    saved === "draft"
    || saved === "submitted"
      ? saved
      : null;

  const analyticsInvalidated =
    analyticsStatus === "invalidated";

  const parsedStudentId =
    Number(studentId);

  if (
    !Number.isInteger(parsedStudentId)
    || parsedStudentId <= 0
  ) {
    notFound();
  }

  const [
    student,
    analytics,
  ] = await Promise.all([
    getStudentDetail(parsedStudentId),
    getAnalyticsStudentDetail(
      parsedStudentId,
    ),
  ]);

  if (!student) {
    notFound();
  }

  const latestAssessment = [
    ...student.assessments,
  ].sort(
    (
      firstAssessment,
      secondAssessment,
    ) => {
      const dateComparison =
        secondAssessment.assessment_date
          .localeCompare(
            firstAssessment.assessment_date,
          );

      if (dateComparison !== 0) {
        return dateComparison;
      }

      return (
        secondAssessment.id
        - firstAssessment.id
      );
    },
  )[0] ?? null;

  const assessmentScore =
    latestAssessment?.score ?? null;

  const scoreItems = assessmentScore
    ? [
        {
          label: "Akses Visual",
          value:
            assessmentScore.visual_score,
        },
        {
          label: "Pendengaran",
          value:
            assessmentScore.hearing_score,
        },
        {
          label: "Komunikasi",
          value:
            assessmentScore
              .communication_score,
        },
        {
          label: "Pemahaman Instruksi",
          value:
            assessmentScore
              .instruction_score,
        },
        {
          label:
            "Perhatian dan Konsentrasi",
          value:
            assessmentScore.attention_score,
        },
        {
          label: "Mobilitas",
          value:
            assessmentScore.mobility_score,
        },
        {
          label: "Pendampingan",
          value:
            assessmentScore.assistance_score,
        },
        {
          label: "Penyesuaian Evaluasi",
          value:
            assessmentScore
              .evaluation_adjustment_score,
        },
      ]
    : [];

  return (
    <div className="px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <Link
          href="/students"
          className="mb-6 inline-flex items-center gap-2 rounded-lg text-sm font-semibold text-blue-700 hover:text-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-100"
        >
          <ArrowLeft size={18} />

          Kembali ke Data Siswa
        </Link>

        <header className="mb-8">
          <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-blue-700">
            Profil dan Hasil Asesmen
          </p>

          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight text-slate-900">
                {student.student_code}
              </h1>

              <p className="mt-2 text-slate-600">
                Detail kebutuhan akomodasi
                pembelajaran siswa.
              </p>
            </div>

            <div className="flex flex-col items-start gap-3 sm:items-end">
              <AssessmentStatusBadge
                status={
                  student.assessment_status
                }
              />

              <Link
                href={
                  `/students/${student.id}/assessment`
                }
                className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-100"
              >
                <PencilLine size={17} />

                {latestAssessment
                  ? "Edit Asesmen"
                  : "Mulai Asesmen"}
              </Link>
            </div>
          </div>
        </header>

        {savedMode && (
          <section
            role="status"
            className="mb-8 rounded-2xl border border-emerald-200 bg-emerald-50 p-5"
          >
            <div className="flex gap-3">
              <CheckCircle2
                size={23}
                className="mt-0.5 shrink-0 text-emerald-700"
              />

              <div>
                <h2 className="font-semibold text-emerald-900">
                  {savedMode === "draft"
                    ? (
                      "Draft asesmen berhasil "
                      + "disimpan"
                    )
                    : (
                      "Asesmen berhasil "
                      + "disubmit"
                    )}
                </h2>

                <p className="mt-1 text-sm leading-6 text-emerald-800">
                  {savedMode === "draft"
                    ? (
                      "Data asesmen telah "
                      + "tersimpan dan dapat "
                      + "dilanjutkan kembali."
                    )
                    : (
                      "Seluruh skor asesmen "
                      + "telah tersimpan "
                      + "dengan lengkap."
                    )}
                </p>

                {analyticsInvalidated && (
                  <p className="mt-2 text-sm font-medium leading-6 text-amber-800">
                    Hasil analytics sebelumnya
                    telah dihapus karena data
                    asesmen berubah. Analytics
                    perlu dijalankan kembali.
                  </p>
                )}
              </div>
            </div>
          </section>
        )}

        <section className="mb-8 grid gap-5 lg:grid-cols-3">
          <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">
            <div className="mb-5 flex items-center gap-3">
              <div className="rounded-xl bg-blue-50 p-3 text-blue-700">
                <UserRound size={22} />
              </div>

              <div>
                <h2 className="text-lg font-semibold text-slate-900">
                  Identitas Siswa
                </h2>

                <p className="text-sm text-slate-500">
                  Informasi akademik siswa
                </p>
              </div>
            </div>

            <dl className="grid gap-5 sm:grid-cols-2">
              <InformationItem
                icon={
                  <UserRound size={18} />
                }
                label="Inisial"
                value={
                  student.initials ?? "-"
                }
              />

              <InformationItem
                icon={
                  <GraduationCap
                    size={18}
                  />
                }
                label="Jenjang"
                value={
                  student.grade_level ?? "-"
                }
              />

              <InformationItem
                icon={
                  <School size={18} />
                }
                label="Kelas"
                value={
                  student.class_name ?? "-"
                }
              />

              <InformationItem
                icon={
                  <CalendarDays
                    size={18}
                  />
                }
                label="Semester"
                value={
                  student.semester ?? "-"
                }
              />

              <InformationItem
                icon={
                  <FileText size={18} />
                }
                label="Tahun Ajaran"
                value={
                  student.school_year ?? "-"
                }
              />

              <InformationItem
                icon={
                  <CalendarDays
                    size={18}
                  />
                }
                label="Tanggal Asesmen"
                value={
                  latestAssessment
                    ?.assessment_date
                  ?? "-"
                }
              />
            </dl>
          </article>

          <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">
              Ringkasan Asesmen
            </h2>

            <div className="mt-5 space-y-4">
              <InformationText
                label="Status"
                value={
                  latestAssessment
                    ?.status
                  ?? "-"
                }
              />

              <InformationText
                label="Sumber Data"
                value={
                  latestAssessment
                    ?.source_information
                  ?? "-"
                }
              />

              <InformationText
                label="Catatan Guru"
                value={
                  latestAssessment
                    ?.notes
                  ?? "-"
                }
              />
            </div>
          </article>
        </section>

        {!assessmentScore ? (
          <section className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
            <div className="flex gap-3">
              <AlertTriangle
                className="shrink-0 text-amber-700"
                size={23}
              />

              <div>
                <h2 className="font-semibold text-amber-900">
                  Asesmen belum tersedia
                </h2>

                <p className="mt-1 text-sm text-amber-800">
                  Data skor kebutuhan siswa
                  belum tersedia sehingga belum
                  dapat dianalisis.
                </p>
              </div>
            </div>
          </section>
        ) : (
          <>
            <section className="mb-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="mb-6">
                <h2 className="text-lg font-semibold text-slate-900">
                  Skor Kebutuhan Fungsional
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  Skala 0 menunjukkan tidak
                  membutuhkan dukungan dan
                  skala 3 menunjukkan kebutuhan
                  dukungan tinggi.
                </p>
              </div>

              <div className="grid gap-5 md:grid-cols-2">
                {scoreItems.map((item) => (
                  <ScoreItem
                    key={item.label}
                    label={item.label}
                    value={item.value}
                  />
                ))}
              </div>
            </section>

            <section className="mb-8 grid gap-5 lg:grid-cols-2">
              <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="mb-5 flex items-center gap-3">
                  <div className="rounded-xl bg-violet-50 p-3 text-violet-700">
                    <FileText size={21} />
                  </div>

                  <h2 className="text-lg font-semibold text-slate-900">
                    Preferensi Materi
                  </h2>
                </div>

                <TagList
                  values={
                    assessmentScore
                      .material_preferences
                  }
                  emptyMessage={
                    "Tidak ada preferensi tercatat."
                  }
                />
              </article>

              <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="mb-5 flex items-center gap-3">
                  <div className="rounded-xl bg-cyan-50 p-3 text-cyan-700">
                    <Wrench size={21} />
                  </div>

                  <h2 className="text-lg font-semibold text-slate-900">
                    Alat Bantu
                  </h2>
                </div>

                <TagList
                  values={
                    assessmentScore
                      .assistive_tools
                  }
                  emptyMessage={
                    "Tidak ada alat bantu tercatat."
                  }
                />
              </article>
            </section>
          </>
        )}

        {analytics ? (
          <>
            <section className="mb-8 grid gap-5 lg:grid-cols-3">
              <article className="rounded-2xl border border-blue-200 bg-blue-50 p-6 lg:col-span-2">
                <p className="text-sm font-semibold uppercase tracking-wider text-blue-700">
                  Kelompok Kebutuhan
                </p>

                <h2 className="mt-2 text-2xl font-bold text-blue-950">
                  {analytics.cluster_name}
                </h2>

                <div className="mt-4 flex flex-wrap gap-2">
                  {analytics.dominant_needs.map(
                    (need) => (
                      <span
                        key={need}
                        className="rounded-full border border-blue-200 bg-white px-3 py-1 text-xs font-semibold text-blue-800"
                      >
                        {need}
                      </span>
                    ),
                  )}
                </div>
              </article>

              <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <p className="text-sm font-medium text-slate-500">
                  Tingkat Prioritas
                </p>

                <div className="mt-3">
                  <PriorityBadge
                    priority={
                      analytics.priority_level
                    }
                  />
                </div>

                <p className="mt-4 text-sm leading-6 text-slate-600">
                  {analytics.priority_action
                    ?? (
                      "Belum ada tindakan "
                      + "prioritas."
                    )}
                </p>
              </article>
            </section>

            {(
              analytics.critical_access_flag
              || analytics.needs_human_review
            ) && (
              <section className="mb-8 rounded-2xl border border-amber-200 bg-amber-50 p-6">
                <div className="flex gap-3">
                  <ShieldAlert
                    className="shrink-0 text-amber-700"
                    size={24}
                  />

                  <div>
                    <h2 className="font-semibold text-amber-900">
                      Perlu Validasi Guru
                    </h2>

                    <p className="mt-1 text-sm leading-6 text-amber-800">
                      {analytics
                        .human_review_reason
                        ?? (
                          "Hasil analisis perlu "
                          + "ditinjau oleh guru."
                        )}
                    </p>
                  </div>
                </div>
              </section>
            )}

            <section className="grid gap-5 lg:grid-cols-2">
              <RecommendationCard
                title="Rekomendasi Kelompok"
                description={
                  "Akomodasi umum berdasarkan "
                  + "kelompok kebutuhan siswa."
                }
                values={
                  analytics
                    .cluster_recommendations
                }
              />

              <RecommendationCard
                title="Rekomendasi Individual"
                description={
                  "Akomodasi yang disesuaikan "
                  + "dengan hasil asesmen siswa."
                }
                values={
                  analytics
                    .individual_recommendations
                }
              />
            </section>
          </>
        ) : (
          student.assessment_status
            === "complete" && (
            <section
              className={[
                "rounded-2xl border p-6",
                analyticsInvalidated
                  ? (
                    "border-amber-200 "
                    + "bg-amber-50"
                  )
                  : (
                    "border-red-200 "
                    + "bg-red-50"
                  ),
              ].join(" ")}
            >
              <h2
                className={
                  analyticsInvalidated
                    ? (
                      "font-semibold "
                      + "text-amber-900"
                    )
                    : (
                      "font-semibold "
                      + "text-red-800"
                    )
                }
              >
                {analyticsInvalidated
                  ? (
                    "Analytics perlu "
                    + "dijalankan kembali"
                  )
                  : (
                    "Hasil analytics belum "
                    + "dapat dimuat"
                  )}
              </h2>

              <p
                className={[
                  "mt-2 text-sm leading-6",
                  analyticsInvalidated
                    ? "text-amber-800"
                    : "text-red-700",
                ].join(" ")}
              >
                {analyticsInvalidated
                  ? (
                    "Data asesmen sudah "
                    + "diperbarui. Jalankan "
                    + "kembali proses analytics "
                    + "untuk memperoleh kelompok "
                    + "kebutuhan dan rekomendasi "
                    + "terbaru."
                  )
                  : (
                    "Pastikan FastAPI masih "
                    + "berjalan dan hasil "
                    + "analytics siswa tersedia."
                  )}
              </p>
            </section>
          )
        )}
      </div>
    </div>
  );
}


interface InformationItemProps {
  icon: ReactNode;
  label: string;
  value: string;
}


function InformationItem({
  icon,
  label,
  value,
}: InformationItemProps) {
  return (
    <div className="flex gap-3">
      <div className="mt-0.5 text-slate-400">
        {icon}
      </div>

      <div>
        <dt className="text-xs font-semibold uppercase tracking-wider text-slate-500">
          {label}
        </dt>

        <dd className="mt-1 font-medium text-slate-900">
          {value}
        </dd>
      </div>
    </div>
  );
}


interface InformationTextProps {
  label: string;
  value: string;
}


function InformationText({
  label,
  value,
}: InformationTextProps) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
        {label}
      </p>

      <p className="mt-1 text-sm leading-6 text-slate-700">
        {value}
      </p>
    </div>
  );
}


interface ScoreItemProps {
  label: string;
  value: number | null;
}


function ScoreItem({
  label,
  value,
}: ScoreItemProps) {
  const percentage =
    value === null
      ? 0
      : Math.min(
          100,
          Math.max(
            0,
            (value / 3) * 100,
          ),
        );

  return (
    <div>
      <div className="mb-2 flex items-center justify-between gap-3">
        <p className="text-sm font-medium text-slate-700">
          {label}
        </p>

        <span className="rounded-lg bg-slate-100 px-2.5 py-1 text-sm font-bold text-slate-800">
          {value === null
            ? "Belum diisi"
            : `${value}/3`}
        </span>
      </div>

      <div
        className="h-2.5 overflow-hidden rounded-full bg-slate-100"
        role="progressbar"
        aria-label={label}
        aria-valuemin={0}
        aria-valuemax={3}
        aria-valuenow={value ?? 0}
        aria-valuetext={
          value === null
            ? "Belum diisi"
            : `${value} dari 3`
        }
      >
        <div
          className="h-full rounded-full bg-blue-600"
          style={{
            width: `${percentage}%`,
          }}
        />
      </div>
    </div>
  );
}


interface TagListProps {
  values: string[];
  emptyMessage: string;
}


function TagList({
  values,
  emptyMessage,
}: TagListProps) {
  if (values.length === 0) {
    return (
      <p className="text-sm text-slate-500">
        {emptyMessage}
      </p>
    );
  }

  return (
    <div className="flex flex-wrap gap-2">
      {values.map((value) => (
        <span
          key={value}
          className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-sm font-medium text-slate-700"
        >
          {value}
        </span>
      ))}
    </div>
  );
}


interface RecommendationCardProps {
  title: string;
  description: string;
  values: string[];
}


function RecommendationCard({
  title,
  description,
  values,
}: RecommendationCardProps) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5 flex items-start gap-3">
        <div className="rounded-xl bg-emerald-50 p-3 text-emerald-700">
          <Lightbulb size={21} />
        </div>

        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            {title}
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            {description}
          </p>
        </div>
      </div>

      {values.length === 0 ? (
        <p className="text-sm text-slate-500">
          Belum ada rekomendasi tersedia.
        </p>
      ) : (
        <ul className="space-y-3">
          {values.map((value) => (
            <li
              key={value}
              className="flex gap-3 text-sm leading-6 text-slate-700"
            >
              <CheckCircle2
                size={18}
                className="mt-1 shrink-0 text-emerald-600"
              />

              <span>
                {value}
              </span>
            </li>
          ))}
        </ul>
      )}
    </article>
  );
}


interface AssessmentStatusBadgeProps {
  status: AssessmentStatus;
}


function AssessmentStatusBadge({
  status,
}: AssessmentStatusBadgeProps) {
  const configuration = {
    complete: {
      label: "Asesmen Lengkap",
      className: (
        "border-emerald-200 "
        + "bg-emerald-50 "
        + "text-emerald-700"
      ),
    },
    incomplete: {
      label: "Asesmen Belum Lengkap",
      className: (
        "border-amber-200 "
        + "bg-amber-50 "
        + "text-amber-700"
      ),
    },
    not_started: {
      label: "Asesmen Belum Dimulai",
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

  return (
    <span
      className={[
        (
          "inline-flex rounded-full "
          + "border px-3 py-1.5 "
          + "text-sm font-semibold"
        ),
        configuration[status].className,
      ].join(" ")}
    >
      {configuration[status].label}
    </span>
  );
}


interface PriorityBadgeProps {
  priority:
    | "high"
    | "medium"
    | "low";
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
    "high" | "medium" | "low",
    {
      label: string;
      className: string;
    }
  >;

  return (
    <span
      className={[
        (
          "inline-flex rounded-full "
          + "border px-3 py-1.5 "
          + "text-sm font-bold"
        ),
        configuration[priority].className,
      ].join(" ")}
    >
      {configuration[priority].label}
    </span>
  );
}