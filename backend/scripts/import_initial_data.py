import argparse
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import func, select

from app.database import SessionLocal
from app.models import Assessment, AssessmentScore, Student


# FILE PATH

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Data_Siswa.csv"
)

PROCESSED_DATA_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

PROCESSED_DATA_PATH = (
    PROCESSED_DATA_DIRECTORY
    / "data_siswa_clean.csv"
)


# DATA CONFIGURATION

STATUS_MAPPING = {
    "Lengkap": "complete",
    "Belum Lengkap": "incomplete",
    "Belum Dimulai": "not_started",
}

SCORE_COLUMNS = [
    "Akses Visual",
    "Pendengaran",
    "Komunikasi",
    "Pemahaman Instruksi",
    "Perhatian & Konsentrasi",
    "Mobilitas",
    "Pendampingan",
    "Penyesuaian Evaluasi",
]

REQUIRED_COLUMNS = [
    "Kode Siswa",
    "Inisial",
    "Jenjang",
    "Kelas",
    "Semester",
    "Status Asesmen",
    "Tanggal Asesmen",
    *SCORE_COLUMNS,
    "Preferensi Materi",
    "Alat Bantu",
    "Catatan Guru",
]


# HELPER FUNCTIONS

def clean_text(value: Any) -> str | None:
    """
    Membersihkan nilai teks.

    Nilai kosong, NaN, atau string kosong
    akan dikembalikan sebagai None.
    """

    if pd.isna(value):
        return None

    cleaned_value = str(value).strip()

    if not cleaned_value:
        return None

    return cleaned_value


def split_semester(
    semester_value: Any,
) -> tuple[str | None, str | None]:
    """
    Memisahkan nilai semester dan tahun ajaran.

    Contoh:
    Ganjil 2026/2027

    Hasil:
    semester = Ganjil
    school_year = 2026/2027
    """

    semester_text = clean_text(
        semester_value
    )

    if semester_text is None:
        return None, None

    semester_parts = semester_text.split(
        maxsplit=1,
    )

    semester_name = semester_parts[0]

    school_year = (
        semester_parts[1]
        if len(semester_parts) > 1
        else None
    )

    return semester_name, school_year


def convert_to_list(
    value: Any,
) -> list[str]:
    """
    Mengubah preferensi materi atau alat bantu
    menjadi list untuk disimpan dalam JSONB.
    """

    cleaned_value = clean_text(value)

    if cleaned_value is None:
        return []

    empty_values = {
        "-",
        "Tidak Ada",
        "Tidak ada",
        "Belum Ditentukan",
        "Belum ditentukan",
    }

    if cleaned_value in empty_values:
        return []

    normalized_value = cleaned_value.replace(
        "|",
        ";",
    )

    values = [
        item.strip()
        for item in normalized_value.split(";")
        if item.strip()
    ]

    return values


# VALIDATION FUNCTIONS

def validate_required_columns(
    dataframe: pd.DataFrame,
) -> None:
    """
    Memastikan seluruh kolom yang dibutuhkan
    tersedia di dalam Data_Siswa.csv.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Kolom berikut tidak ditemukan: "
            + ", ".join(missing_columns)
        )


def validate_student_codes(
    dataframe: pd.DataFrame,
) -> None:
    """
    Memastikan Kode Siswa tidak memiliki
    nilai duplikat.
    """

    duplicate_mask = dataframe[
        "Kode Siswa"
    ].duplicated(
        keep=False,
    )

    duplicate_codes = dataframe.loc[
        duplicate_mask,
        "Kode Siswa",
    ].tolist()

    if duplicate_codes:
        duplicate_code_text = ", ".join(
            sorted(
                set(
                    map(
                        str,
                        duplicate_codes,
                    )
                )
            )
        )

        raise ValueError(
            "Ditemukan Kode Siswa duplikat: "
            + duplicate_code_text
        )


def validate_assessment_status(
    dataframe: pd.DataFrame,
) -> None:
    """
    Memastikan nilai Status Asesmen hanya
    menggunakan kategori yang didukung.
    """

    available_statuses = set(
        dataframe["Status Asesmen"]
        .dropna()
        .unique()
    )

    valid_statuses = set(
        STATUS_MAPPING.keys()
    )

    unknown_statuses = (
        available_statuses
        - valid_statuses
    )

    if unknown_statuses:
        raise ValueError(
            "Status asesmen tidak dikenal: "
            + ", ".join(
                sorted(
                    map(
                        str,
                        unknown_statuses,
                    )
                )
            )
        )


def validate_complete_assessments(
    dataframe: pd.DataFrame,
) -> None:
    """
    Memvalidasi tanggal dan delapan nilai domain
    untuk siswa berstatus Lengkap.

    Siswa berstatus Belum Lengkap atau
    Belum Dimulai diperbolehkan memiliki
    tanggal dan nilai domain yang kosong.
    """

    complete_mask = (
        dataframe["Status Asesmen"]
        == "Lengkap"
    )

    # DATE VALIDATION

    parsed_dates = pd.to_datetime(
        dataframe["Tanggal Asesmen"],
        errors="coerce",
    )

    invalid_date_mask = (
        complete_mask
        & parsed_dates.isna()
    )

    if invalid_date_mask.any():
        invalid_codes = dataframe.loc[
            invalid_date_mask,
            "Kode Siswa",
        ].astype(str).tolist()

        raise ValueError(
            "Tanggal asesmen kosong atau "
            "tidak valid untuk siswa: "
            + ", ".join(invalid_codes)
        )

    # Mengganti seluruh kolom agar pandas dapat
    # mengubah dtype string menjadi datetime.
    dataframe["Tanggal Asesmen"] = (
        parsed_dates
    )

    # SCORE VALIDATION

    for column in SCORE_COLUMNS:
        numeric_values = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        )

        complete_values = numeric_values.loc[
            complete_mask
        ]

        invalid_value_mask = (
            complete_mask
            & numeric_values.isna()
        )

        if invalid_value_mask.any():
            invalid_codes = dataframe.loc[
                invalid_value_mask,
                "Kode Siswa",
            ].astype(str).tolist()

            raise ValueError(
                f"Nilai kosong atau tidak valid "
                f"ditemukan pada kolom "
                f"'{column}' untuk siswa: "
                + ", ".join(invalid_codes)
            )

        outside_range_mask = (
            complete_mask
            & ~numeric_values.between(
                0,
                3,
            )
        )

        if outside_range_mask.any():
            invalid_codes = dataframe.loc[
                outside_range_mask,
                "Kode Siswa",
            ].astype(str).tolist()

            raise ValueError(
                f"Nilai pada kolom '{column}' "
                "harus berada antara 0 dan 3. "
                "Kode siswa: "
                + ", ".join(invalid_codes)
            )

        non_integer_mask = (
            complete_mask
            & numeric_values.notna()
            & ((numeric_values % 1) != 0)
        )

        if non_integer_mask.any():
            invalid_codes = dataframe.loc[
                non_integer_mask,
                "Kode Siswa",
            ].astype(str).tolist()

            raise ValueError(
                f"Nilai pada kolom '{column}' "
                "harus berupa bilangan bulat. "
                "Kode siswa: "
                + ", ".join(invalid_codes)
            )

        # Int64 milik pandas mendukung integer
        # sekaligus nilai kosong.
        dataframe[column] = (
            numeric_values.astype("Int64")
        )

        if (
            complete_values.empty
            and complete_mask.any()
        ):
            raise ValueError(
                f"Tidak terdapat nilai lengkap "
                f"pada kolom '{column}'."
            )


# DATA CLEANING

def load_and_clean_data() -> pd.DataFrame:
    """
    Membaca Data_Siswa.csv, menghapus baris kosong,
    memvalidasi data, dan menyimpan data bersih.
    """

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            "File Data_Siswa.csv tidak ditemukan: "
            f"{RAW_DATA_PATH}"
        )

    dataframe = pd.read_csv(
        RAW_DATA_PATH,
        encoding="utf-8-sig",
    )

    # Membersihkan nama kolom.
    dataframe.columns = (
        dataframe.columns
        .astype(str)
        .str.strip()
    )

    validate_required_columns(
        dataframe
    )

    # CLEAN STUDENT CODE

    dataframe["Kode Siswa"] = (
        dataframe["Kode Siswa"]
        .astype("string")
        .str.strip()
    )

    # CSV memiliki baris kosong karena hasil ekspor
    # worksheet. Hanya baris yang memiliki Kode Siswa
    # yang akan digunakan.
    dataframe = dataframe.loc[
        dataframe["Kode Siswa"].notna()
        & dataframe["Kode Siswa"].ne("")
    ].copy()

    # CLEAN ASSESSMENT STATUS

    dataframe["Status Asesmen"] = (
        dataframe["Status Asesmen"]
        .astype("string")
        .str.strip()
    )

    validate_student_codes(
        dataframe
    )

    validate_assessment_status(
        dataframe
    )

    validate_complete_assessments(
        dataframe
    )

    # Mengurutkan data berdasarkan Kode Siswa.
    dataframe = dataframe.sort_values(
        by="Kode Siswa",
    ).reset_index(
        drop=True,
    )

    # Menyiapkan folder data processed.
    PROCESSED_DATA_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Menyimpan data hasil pembersihan.
    dataframe.to_csv(
        PROCESSED_DATA_PATH,
        index=False,
        encoding="utf-8-sig",
        date_format="%Y-%m-%d",
    )

    return dataframe


# SUMMARY

def print_data_summary(
    dataframe: pd.DataFrame,
) -> None:
    """
    Menampilkan ringkasan hasil validasi data.
    """

    status_counts = (
        dataframe["Status Asesmen"]
        .value_counts()
    )

    complete_count = int(
        status_counts.get(
            "Lengkap",
            0,
        )
    )

    incomplete_count = int(
        status_counts.get(
            "Belum Lengkap",
            0,
        )
    )

    not_started_count = int(
        status_counts.get(
            "Belum Dimulai",
            0,
        )
    )

    print()
    print("VALIDASI DATA BERHASIL")
    print("-" * 50)
    print(
        f"Total siswa       : "
        f"{len(dataframe)}"
    )
    print(
        f"Lengkap           : "
        f"{complete_count}"
    )
    print(
        f"Belum Lengkap     : "
        f"{incomplete_count}"
    )
    print(
        f"Belum Dimulai     : "
        f"{not_started_count}"
    )
    print(
        f"Data bersih       : "
        f"{PROCESSED_DATA_PATH}"
    )
    print("-" * 50)
    print()


# DATABASE IMPORT

def import_data_to_database(
    dataframe: pd.DataFrame,
) -> None:
    """
    Memasukkan data siswa, asesmen lengkap,
    dan nilai asesmen ke PostgreSQL.
    """

    database = SessionLocal()

    try:
        existing_student_count = (
            database.scalar(
                select(
                    func.count(
                        Student.id
                    )
                )
            )
            or 0
        )

        if existing_student_count > 0:
            raise RuntimeError(
                "Import dibatalkan karena tabel "
                f"students sudah memiliki "
                f"{existing_student_count} data. "
                "Hal ini dilakukan untuk mencegah "
                "duplikasi data."
            )

        imported_students = 0
        imported_assessments = 0
        imported_scores = 0

        for _, row in dataframe.iterrows():
            source_status = clean_text(
                row["Status Asesmen"]
            )

            if source_status is None:
                raise ValueError(
                    "Status asesmen tidak boleh kosong."
                )

            if source_status not in STATUS_MAPPING:
                raise ValueError(
                    "Status asesmen tidak dikenal: "
                    f"{source_status}"
                )

            student_code = clean_text(
                row["Kode Siswa"]
            )

            if student_code is None:
                raise ValueError(
                    "Kode Siswa tidak boleh kosong."
                )

            semester, school_year = (
                split_semester(
                    row["Semester"]
                )
            )

            student = Student(
                student_code=student_code,
                initials=clean_text(
                    row["Inisial"]
                ),
                grade_level=clean_text(
                    row["Jenjang"]
                ),
                class_name=clean_text(
                    row["Kelas"]
                ),
                semester=semester,
                school_year=school_year,
                assessment_status=(
                    STATUS_MAPPING[
                        source_status
                    ]
                ),
            )

            database.add(student)
            database.flush()

            imported_students += 1

            # Hanya siswa berstatus Lengkap yang
            # memiliki assessment dan score.
            if source_status != "Lengkap":
                continue

            assessment_date_value = (
                row["Tanggal Asesmen"]
            )

            if pd.isna(
                assessment_date_value
            ):
                raise ValueError(
                    "Tanggal asesmen tidak ditemukan "
                    f"untuk siswa {student_code}."
                )

            assessment_date = (
                pd.Timestamp(
                    assessment_date_value
                ).date()
            )

            assessment = Assessment(
                student_id=student.id,
                assessor_id=None,
                assessment_date=(
                    assessment_date
                ),
                source_information=(
                    "Import data awal "
                    "Data_Siswa.csv"
                ),
                notes=clean_text(
                    row["Catatan Guru"]
                ),
                status="submitted",
            )

            database.add(assessment)
            database.flush()

            imported_assessments += 1

            assessment_score = (
                AssessmentScore(
                    assessment_id=(
                        assessment.id
                    ),
                    visual_score=int(
                        row[
                            "Akses Visual"
                        ]
                    ),
                    hearing_score=int(
                        row[
                            "Pendengaran"
                        ]
                    ),
                    communication_score=int(
                        row[
                            "Komunikasi"
                        ]
                    ),
                    instruction_score=int(
                        row[
                            "Pemahaman Instruksi"
                        ]
                    ),
                    attention_score=int(
                        row[
                            "Perhatian & Konsentrasi"
                        ]
                    ),
                    mobility_score=int(
                        row[
                            "Mobilitas"
                        ]
                    ),
                    assistance_score=int(
                        row[
                            "Pendampingan"
                        ]
                    ),
                    evaluation_adjustment_score=int(
                        row[
                            "Penyesuaian Evaluasi"
                        ]
                    ),
                    material_preferences=(
                        convert_to_list(
                            row[
                                "Preferensi Materi"
                            ]
                        )
                    ),
                    assistive_tools=(
                        convert_to_list(
                            row[
                                "Alat Bantu"
                            ]
                        )
                    ),
                )
            )

            database.add(
                assessment_score
            )

            imported_scores += 1

        database.commit()

        print()
        print("IMPORT DATABASE BERHASIL")
        print("-" * 50)
        print(
            f"Students           : "
            f"{imported_students}"
        )
        print(
            f"Assessments        : "
            f"{imported_assessments}"
        )
        print(
            f"Assessment scores  : "
            f"{imported_scores}"
        )
        print("-" * 50)
        print()

    except Exception:
        database.rollback()
        raise

    finally:
        database.close()


# MAIN PROGRAM

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Validasi, pembersihan, dan import "
            "data awal InkluMap."
        )
    )

    parser.add_argument(
        "--validate-only",
        action="store_true",
        help=(
            "Hanya membersihkan dan memvalidasi "
            "data tanpa memasukkannya ke database."
        ),
    )

    arguments = parser.parse_args()

    cleaned_dataframe = (
        load_and_clean_data()
    )

    print_data_summary(
        cleaned_dataframe
    )

    if arguments.validate_only:
        print(
            "Mode validasi selesai. "
            "Database belum diubah."
        )
        return

    import_data_to_database(
        cleaned_dataframe
    )


if __name__ == "__main__":
    main()