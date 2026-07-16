"use client";

import {
  AlertTriangle,
  ArrowLeft,
  ClipboardPenLine,
  Save,
  Send,
  UserRound,
} from "lucide-react";
import Link from "next/link";
import {
  useRouter,
} from "next/navigation";
import {
  useMemo,
  useState,
} from "react";

import {
  createAssessment,
  updateAssessment,
} from "@/lib/api";
import type {
  AssessmentCreatePayload,
  AssessmentScoreField,
  AssessmentScorePayload,
  AssessmentUpdatePayload,
} from "@/types/assessments";
import type {
  StudentAssessment,
  StudentDetail,
} from "@/types/students";


interface AssessmentFormProps {
  student: StudentDetail;
  initialAssessment: StudentAssessment | null;
}


interface ScoreFieldConfiguration {
  key: AssessmentScoreField;
  label: string;
  description: string;
}


type SaveMode =
  | "draft"
  | "submitted";


const SCORE_FIELDS:
  ScoreFieldConfiguration[] = [
    {
      key: "visual_score",
      label: "Akses Visual",
      description: (
        "Kemampuan mengakses tulisan, gambar, "
        + "presentasi, dan lingkungan visual."
      ),
    },
    {
      key: "hearing_score",
      label: "Pendengaran",
      description: (
        "Kemampuan mengakses penjelasan lisan "
        + "dan materi berbasis suara."
      ),
    },
    {
      key: "communication_score",
      label: "Komunikasi",
      description: (
        "Kemampuan memahami dan menyampaikan "
        + "informasi dalam kegiatan belajar."
      ),
    },
    {
      key: "instruction_score",
      label: "Pemahaman Instruksi",
      description: (
        "Kemampuan mengikuti arahan dan urutan "
        + "kegiatan pembelajaran."
      ),
    },
    {
      key: "attention_score",
      label: "Perhatian dan Konsentrasi",
      description: (
        "Kebutuhan dukungan untuk mempertahankan "
        + "fokus selama pembelajaran."
      ),
    },
    {
      key: "mobility_score",
      label: "Mobilitas",
      description: (
        "Kemampuan berpindah dan mengakses ruang "
        + "serta fasilitas sekolah."
      ),
    },
    {
      key: "assistance_score",
      label: "Pendampingan",
      description: (
        "Tingkat bantuan individual yang diperlukan "
        + "selama kegiatan belajar."
      ),
    },
    {
      key: "evaluation_adjustment_score",
      label: "Penyesuaian Evaluasi",
      description: (
        "Kebutuhan penyesuaian waktu, bentuk soal, "
        + "atau cara memberikan jawaban."
      ),
    },
  ];


const MATERIAL_OPTIONS = [
  "Teks",
  "Visual",
  "Audio",
  "Video dengan Caption",
  "Caption dan Teks",
  "Materi Sederhana",
  "Ukuran Huruf Besar",
  "Braille",
  "Bahasa Isyarat",
];


const ASSISTIVE_TOOL_OPTIONS = [
  "Perangkat Caption",
  "Alat Bantu Dengar",
  "Pembaca Layar",
  "Pembesar Layar",
  "Keyboard Adaptif",
  "Perangkat Komunikasi",
  "Timer Visual",
  "Dukungan Mobilitas",
];


function getLocalDateValue(): string {
  const currentDate = new Date();

  const timezoneOffset =
    currentDate.getTimezoneOffset()
    * 60
    * 1000;

  return new Date(
    currentDate.getTime() - timezoneOffset,
  )
    .toISOString()
    .slice(0, 10);
}


function createInitialScoreValues(
  assessment: StudentAssessment | null,
): Record<AssessmentScoreField, string> {
  const result = {} as Record<
    AssessmentScoreField,
    string
  >;

  for (const field of SCORE_FIELDS) {
    const currentValue =
      assessment?.score?.[field.key];

    result[field.key] =
      currentValue === null
      || currentValue === undefined
        ? ""
        : String(currentValue);
  }

  return result;
}


export default function AssessmentForm({
  student,
  initialAssessment,
}: AssessmentFormProps) {
  const router = useRouter();

  const [
    assessmentDate,
    setAssessmentDate,
  ] = useState(
    initialAssessment?.assessment_date
    ?? getLocalDateValue(),
  );

  const [
    sourceInformation,
    setSourceInformation,
  ] = useState(
    initialAssessment?.source_information
    ?? "",
  );

  const [
    notes,
    setNotes,
  ] = useState(
    initialAssessment?.notes ?? "",
  );

  const [
    scoreValues,
    setScoreValues,
  ] = useState(
    createInitialScoreValues(
      initialAssessment,
    ),
  );

  const [
    materialPreferences,
    setMaterialPreferences,
  ] = useState<string[]>(
    initialAssessment?.score
      ?.material_preferences
    ?? [],
  );

  const [
    assistiveTools,
    setAssistiveTools,
  ] = useState<string[]>(
    initialAssessment?.score
      ?.assistive_tools
    ?? [],
  );

  const [
    activeSaveMode,
    setActiveSaveMode,
  ] = useState<SaveMode | null>(null);

  const [
    errorMessage,
    setErrorMessage,
  ] = useState("");

  const materialOptions = useMemo(
    () => Array.from(
      new Set([
        ...MATERIAL_OPTIONS,
        ...materialPreferences,
      ]),
    ),
    [materialPreferences],
  );

  const assistiveToolOptions = useMemo(
    () => Array.from(
      new Set([
        ...ASSISTIVE_TOOL_OPTIONS,
        ...assistiveTools,
      ]),
    ),
    [assistiveTools],
  );

  const isSaving =
    activeSaveMode !== null;


  function updateScore(
    fieldName: AssessmentScoreField,
    value: string,
  ) {
    setScoreValues(
      (currentValues) => ({
        ...currentValues,
        [fieldName]: value,
      }),
    );
  }


  function toggleListValue(
    value: string,
    currentValues: string[],
    setter: (
      values: string[]
    ) => void,
  ) {
    if (currentValues.includes(value)) {
      setter(
        currentValues.filter(
          (currentValue) =>
            currentValue !== value,
        ),
      );

      return;
    }

    setter([
      ...currentValues,
      value,
    ]);
  }


  function buildScorePayload():
    AssessmentScorePayload {
    return {
      visual_score:
        parseScoreValue(
          scoreValues.visual_score,
        ),
      hearing_score:
        parseScoreValue(
          scoreValues.hearing_score,
        ),
      communication_score:
        parseScoreValue(
          scoreValues.communication_score,
        ),
      instruction_score:
        parseScoreValue(
          scoreValues.instruction_score,
        ),
      attention_score:
        parseScoreValue(
          scoreValues.attention_score,
        ),
      mobility_score:
        parseScoreValue(
          scoreValues.mobility_score,
        ),
      assistance_score:
        parseScoreValue(
          scoreValues.assistance_score,
        ),
      evaluation_adjustment_score:
        parseScoreValue(
          scoreValues
            .evaluation_adjustment_score,
        ),
      material_preferences:
        materialPreferences,
      assistive_tools:
        assistiveTools,
    };
  }


  async function saveAssessment(
    saveMode: SaveMode,
  ) {
    setErrorMessage("");

    const scorePayload =
      buildScorePayload();

    if (saveMode === "submitted") {
      const incompleteFields =
        SCORE_FIELDS.filter(
          (field) =>
            scorePayload[field.key]
            === null,
        );

      if (incompleteFields.length > 0) {
        setErrorMessage(
          (
            "Lengkapi seluruh delapan skor "
            + "sebelum mengirim asesmen. "
            + "Skor yang belum diisi: "
            + incompleteFields
              .map((field) => field.label)
              .join(", ")
            + "."
          ),
        );

        window.scrollTo({
          top: 0,
          behavior: "smooth",
        });

        return;
      }
    }

    setActiveSaveMode(saveMode);

    const basePayload = {
      assessment_date: assessmentDate,
      source_information:
        sourceInformation.trim() || null,
      notes: notes.trim() || null,
      status: saveMode,
      score: scorePayload,
    };

    const updatePayload:
      AssessmentUpdatePayload = {
        ...basePayload,
      };

    const createPayload:
      AssessmentCreatePayload = {
        student_id: student.id,
        ...basePayload,
      };

    const result = initialAssessment
      ? await updateAssessment(
          initialAssessment.id,
          updatePayload,
        )
      : await createAssessment(
          createPayload,
        );

    setActiveSaveMode(null);

    if (!result.data) {
      setErrorMessage(
        result.error
        ?? "Asesmen gagal disimpan.",
      );

      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });

      return;
    }

    const queryParameters =
      new URLSearchParams({
        saved: saveMode,
      });

    if (
      result.data.analytics_invalidated
    ) {
      queryParameters.set(
        "analytics",
        "invalidated",
      );
    }

    router.push(
      (
        `/students/${student.id}?`
        + queryParameters.toString()
      ),
    );
  }


  return (
    <div className="px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-6xl">
        <Link
          href={`/students/${student.id}`}
          className="mb-6 inline-flex items-center gap-2 rounded-lg text-sm font-semibold text-blue-700 hover:text-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-100"
        >
          <ArrowLeft size={18} />

          Kembali ke Detail Siswa
        </Link>

        <header className="mb-8">
          <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-blue-700">
            Asesmen Kebutuhan Fungsional
          </p>

          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            {initialAssessment
              ? "Edit Asesmen"
              : "Mulai Asesmen"}
          </h1>

          <p className="mt-3 max-w-3xl text-slate-600">
            Isi berdasarkan pengamatan guru,
            diskusi dengan siswa atau orang tua,
            dan informasi pembelajaran yang
            relevan. Form ini bukan instrumen
            diagnosis medis.
          </p>
        </header>

        {errorMessage && (
          <section
            role="alert"
            className="mb-6 rounded-2xl border border-red-200 bg-red-50 p-5"
          >
            <div className="flex gap-3">
              <AlertTriangle
                size={22}
                className="mt-0.5 shrink-0 text-red-700"
              />

              <div>
                <h2 className="font-semibold text-red-900">
                  Asesmen belum dapat disimpan
                </h2>

                <p className="mt-1 text-sm leading-6 text-red-700">
                  {errorMessage}
                </p>
              </div>
            </div>
          </section>
        )}

        <section className="mb-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-start gap-4">
            <div className="rounded-xl bg-blue-50 p-3 text-blue-700">
              <UserRound size={22} />
            </div>

            <div>
              <h2 className="text-lg font-semibold text-slate-900">
                {student.student_code}
              </h2>

              <p className="mt-1 text-sm text-slate-600">
                Inisial {student.initials ?? "-"}
                {" · "}
                {student.grade_level ?? "-"}
                {" · "}
                Kelas {student.class_name ?? "-"}
              </p>
            </div>
          </div>
        </section>

        {initialAssessment && (
          <section className="mb-6 rounded-2xl border border-amber-200 bg-amber-50 p-5">
            <div className="flex gap-3">
              <AlertTriangle
                size={22}
                className="mt-0.5 shrink-0 text-amber-700"
              />

              <div>
                <h2 className="font-semibold text-amber-900">
                  Anda sedang mengedit asesmen
                </h2>

                <p className="mt-1 text-sm leading-6 text-amber-800">
                  Perubahan tanggal, status, atau
                  skor akan menghapus hasil
                  analytics lama. Analytics perlu
                  dijalankan kembali setelah data
                  asesmen selesai diperbarui.
                </p>
              </div>
            </div>
          </section>
        )}

        <form
          onSubmit={(event) => {
            event.preventDefault();
          }}
          className="space-y-6"
        >
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-6 flex items-center gap-3">
              <div className="rounded-xl bg-blue-50 p-3 text-blue-700">
                <ClipboardPenLine size={22} />
              </div>

              <div>
                <h2 className="text-lg font-semibold text-slate-900">
                  Informasi Asesmen
                </h2>

                <p className="text-sm text-slate-500">
                  Catat tanggal dan sumber
                  informasi yang digunakan.
                </p>
              </div>
            </div>

            <div className="grid gap-5 md:grid-cols-2">
              <div>
                <label
                  htmlFor="assessment-date"
                  className="mb-2 block text-sm font-medium text-slate-700"
                >
                  Tanggal asesmen
                </label>

                <input
                  id="assessment-date"
                  type="date"
                  required
                  value={assessmentDate}
                  onChange={(event) => {
                    setAssessmentDate(
                      event.target.value,
                    );
                  }}
                  className="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                />
              </div>

              <div>
                <label
                  htmlFor="source-information"
                  className="mb-2 block text-sm font-medium text-slate-700"
                >
                  Sumber informasi
                </label>

                <input
                  id="source-information"
                  type="text"
                  maxLength={255}
                  value={sourceInformation}
                  onChange={(event) => {
                    setSourceInformation(
                      event.target.value,
                    );
                  }}
                  placeholder="Contoh: Observasi guru dan diskusi orang tua"
                  className="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                />
              </div>

              <div className="md:col-span-2">
                <label
                  htmlFor="assessment-notes"
                  className="mb-2 block text-sm font-medium text-slate-700"
                >
                  Catatan guru
                </label>

                <textarea
                  id="assessment-notes"
                  rows={4}
                  maxLength={5000}
                  value={notes}
                  onChange={(event) => {
                    setNotes(
                      event.target.value,
                    );
                  }}
                  placeholder="Tuliskan konteks, perilaku yang diamati, atau informasi pendukung lainnya."
                  className="w-full resize-y rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm leading-6 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                />
              </div>
            </div>
          </section>

          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-6">
              <h2 className="text-lg font-semibold text-slate-900">
                Skor Kebutuhan Fungsional
              </h2>

              <p className="mt-1 text-sm leading-6 text-slate-500">
                Skor 0 berarti tidak memerlukan
                dukungan, sedangkan skor 3 berarti
                membutuhkan dukungan tinggi.
              </p>
            </div>

            <div className="grid gap-5 md:grid-cols-2">
              {SCORE_FIELDS.map((field) => (
                <div
                  key={field.key}
                  className="rounded-xl border border-slate-200 bg-slate-50 p-5"
                >
                  <label
                    htmlFor={field.key}
                    className="block font-semibold text-slate-900"
                  >
                    {field.label}
                  </label>

                  <p className="mt-1 min-h-12 text-sm leading-6 text-slate-500">
                    {field.description}
                  </p>

                  <select
                    id={field.key}
                    value={scoreValues[field.key]}
                    onChange={(event) => {
                      updateScore(
                        field.key,
                        event.target.value,
                      );
                    }}
                    className="mt-4 w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  >
                    <option value="">
                      Belum diisi
                    </option>

                    <option value="0">
                      0 — Tidak memerlukan dukungan
                    </option>

                    <option value="1">
                      1 — Dukungan ringan
                    </option>

                    <option value="2">
                      2 — Dukungan sedang
                    </option>

                    <option value="3">
                      3 — Dukungan tinggi
                    </option>
                  </select>
                </div>
              ))}
            </div>
          </section>

          <section className="grid gap-6 lg:grid-cols-2">
            <ChoiceSection
              title="Preferensi Materi"
              description="Pilih bentuk materi yang membantu siswa mengakses pembelajaran."
              values={materialOptions}
              selectedValues={materialPreferences}
              onToggle={(value) => {
                toggleListValue(
                  value,
                  materialPreferences,
                  setMaterialPreferences,
                );
              }}
            />

            <ChoiceSection
              title="Alat Bantu"
              description="Pilih alat bantu yang digunakan atau perlu dipertimbangkan."
              values={assistiveToolOptions}
              selectedValues={assistiveTools}
              onToggle={(value) => {
                toggleListValue(
                  value,
                  assistiveTools,
                  setAssistiveTools,
                );
              }}
            />
          </section>

          <section className="flex flex-col-reverse gap-3 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:flex-row sm:items-center sm:justify-between">
            <p className="max-w-xl text-sm leading-6 text-slate-500">
              Draft dapat disimpan meskipun skor
              belum lengkap. Tombol submit hanya
              dapat digunakan setelah seluruh
              skor terisi.
            </p>

            <div className="flex flex-col gap-3 sm:flex-row">
              <button
                type="button"
                disabled={isSaving}
                onClick={() => {
                  void saveAssessment("draft");
                }}
                className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border border-blue-200 bg-blue-50 px-5 text-sm font-semibold text-blue-700 transition hover:bg-blue-100 disabled:cursor-not-allowed disabled:opacity-60"
              >
                <Save size={18} />

                {activeSaveMode === "draft"
                  ? "Menyimpan..."
                  : "Simpan Draft"}
              </button>

              <button
                type="button"
                disabled={isSaving}
                onClick={() => {
                  void saveAssessment(
                    "submitted",
                  );
                }}
                className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
              >
                <Send size={18} />

                {activeSaveMode === "submitted"
                  ? "Mengirim..."
                  : "Submit Asesmen"}
              </button>
            </div>
          </section>
        </form>
      </div>
    </div>
  );
}


function parseScoreValue(
  value: string,
): number | null {
  if (value === "") {
    return null;
  }

  return Number(value);
}


interface ChoiceSectionProps {
  title: string;
  description: string;
  values: string[];
  selectedValues: string[];
  onToggle: (value: string) => void;
}


function ChoiceSection({
  title,
  description,
  values,
  selectedValues,
  onToggle,
}: ChoiceSectionProps) {
  return (
    <fieldset className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <legend className="text-lg font-semibold text-slate-900">
        {title}
      </legend>

      <p className="mt-1 text-sm leading-6 text-slate-500">
        {description}
      </p>

      <div className="mt-5 space-y-3">
        {values.map((value) => {
          const isChecked =
            selectedValues.includes(value);

          return (
            <label
              key={value}
              className={[
                "flex cursor-pointer items-center gap-3 rounded-xl border px-4 py-3 text-sm transition",
                isChecked
                  ? (
                    "border-blue-300 "
                    + "bg-blue-50 "
                    + "text-blue-900"
                  )
                  : (
                    "border-slate-200 "
                    + "bg-white "
                    + "text-slate-700 "
                    + "hover:bg-slate-50"
                  ),
              ].join(" ")}
            >
              <input
                type="checkbox"
                checked={isChecked}
                onChange={() => {
                  onToggle(value);
                }}
                className="h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
              />

              <span className="font-medium">
                {value}
              </span>
            </label>
          );
        })}
      </div>
    </fieldset>
  );
}