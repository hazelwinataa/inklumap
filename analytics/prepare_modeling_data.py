# STANDARD LIBRARY

import json
from pathlib import Path


# THIRD-PARTY LIBRARIES

import pandas as pd


# FILE PATHS

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "data_siswa_clean.csv"
)

MODELING_SOURCE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "modeling_complete_students.csv"
)

MODELING_FEATURE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "modeling_features_encoded.csv"
)

FEATURE_MANIFEST_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "modeling_feature_manifest.json"
)


# FEATURE CONFIGURATION

SCORE_COLUMN_MAPPING = {
    "Akses Visual": "visual_score",
    "Pendengaran": "hearing_score",
    "Komunikasi": "communication_score",
    "Pemahaman Instruksi": "instruction_score",
    "Perhatian & Konsentrasi": "attention_score",
    "Mobilitas": "mobility_score",
    "Pendampingan": "assistance_score",
    "Penyesuaian Evaluasi": (
        "evaluation_adjustment_score"
    ),
}

PREFERENCE_COLUMN_MAPPING = {
    "Caption dan Teks": (
        "preference_caption_text"
    ),
    "Materi Audio": (
        "preference_audio"
    ),
    "Kombinasi Audio-Visual": (
        "preference_audio_visual"
    ),
    "Materi Visual Sederhana": (
        "preference_simple_visual"
    ),
    "Materi Digital": (
        "preference_digital"
    ),
}

TOOL_COLUMN_MAPPING = {
    "Perangkat Caption": (
        "tool_caption_device"
    ),
    "Text-to-Speech": (
        "tool_text_to_speech"
    ),
    "Alat Tulis Adaptif": (
        "tool_adaptive_writing"
    ),
    "Tidak Ada": (
        "tool_none"
    ),
    "Perangkat Mobilitas": (
        "tool_mobility_device"
    ),
}

SOURCE_OUTPUT_COLUMNS = [
    "Kelompok Kebutuhan",
    "Kebutuhan Dominan",
    "Prioritas",
    "Status Tindak Lanjut",
    "Rekomendasi Utama",
    "Perlu Tindak Lanjut",
]

SOURCE_IDENTIFIER_COLUMNS = [
    "Kode Siswa",
    "Inisial",
    "Jenjang",
    "Kelas",
    "Semester",
    "Tanggal Asesmen",
]

REQUIRED_COLUMNS = [
    "Kode Siswa",
    "Inisial",
    "Jenjang",
    "Kelas",
    "Semester",
    "Status Asesmen",
    "Tanggal Asesmen",
    *SCORE_COLUMN_MAPPING.keys(),
    "Preferensi Materi",
    "Alat Bantu",
]


# VALIDATION FUNCTIONS

def validate_required_columns(
    dataframe: pd.DataFrame,
) -> None:
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Kolom wajib tidak ditemukan: "
            + ", ".join(missing_columns)
        )


def validate_complete_student_codes(
    dataframe: pd.DataFrame,
) -> None:
    if dataframe["Kode Siswa"].isna().any():
        raise ValueError(
            "Terdapat Kode Siswa kosong pada "
            "data modeling."
        )

    duplicate_mask = dataframe[
        "Kode Siswa"
    ].duplicated(
        keep=False,
    )

    if duplicate_mask.any():
        duplicate_codes = (
            dataframe.loc[
                duplicate_mask,
                "Kode Siswa",
            ]
            .astype(str)
            .tolist()
        )

        raise ValueError(
            "Kode Siswa duplikat ditemukan: "
            + ", ".join(
                sorted(
                    set(duplicate_codes)
                )
            )
        )


def validate_score_columns(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    validated_dataframe = (
        dataframe.copy()
    )

    for source_column in SCORE_COLUMN_MAPPING:
        numeric_values = pd.to_numeric(
            validated_dataframe[
                source_column
            ],
            errors="coerce",
        )

        invalid_value_mask = (
            numeric_values.isna()
        )

        if invalid_value_mask.any():
            invalid_codes = (
                validated_dataframe.loc[
                    invalid_value_mask,
                    "Kode Siswa",
                ]
                .astype(str)
                .tolist()
            )

            raise ValueError(
                f"Nilai tidak valid pada "
                f"'{source_column}' untuk siswa: "
                + ", ".join(invalid_codes)
            )

        outside_range_mask = (
            ~numeric_values.between(
                0,
                3,
            )
        )

        if outside_range_mask.any():
            invalid_codes = (
                validated_dataframe.loc[
                    outside_range_mask,
                    "Kode Siswa",
                ]
                .astype(str)
                .tolist()
            )

            raise ValueError(
                f"Nilai '{source_column}' harus "
                "berada antara 0 dan 3. "
                "Kode siswa: "
                + ", ".join(invalid_codes)
            )

        non_integer_mask = (
            (numeric_values % 1) != 0
        )

        if non_integer_mask.any():
            invalid_codes = (
                validated_dataframe.loc[
                    non_integer_mask,
                    "Kode Siswa",
                ]
                .astype(str)
                .tolist()
            )

            raise ValueError(
                f"Nilai '{source_column}' harus "
                "berupa bilangan bulat. "
                "Kode siswa: "
                + ", ".join(invalid_codes)
            )

        validated_dataframe[
            source_column
        ] = numeric_values.astype(int)

    return validated_dataframe


def validate_categories(
    dataframe: pd.DataFrame,
) -> None:
    available_preferences = set(
        dataframe["Preferensi Materi"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    valid_preferences = set(
        PREFERENCE_COLUMN_MAPPING.keys()
    )

    unknown_preferences = (
        available_preferences
        - valid_preferences
    )

    if unknown_preferences:
        raise ValueError(
            "Preferensi materi tidak dikenal: "
            + ", ".join(
                sorted(
                    unknown_preferences
                )
            )
        )

    available_tools = set(
        dataframe["Alat Bantu"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    valid_tools = set(
        TOOL_COLUMN_MAPPING.keys()
    )

    unknown_tools = (
        available_tools
        - valid_tools
    )

    if unknown_tools:
        raise ValueError(
            "Alat bantu tidak dikenal: "
            + ", ".join(
                sorted(
                    unknown_tools
                )
            )
        )


# DATASET CREATION

def create_source_dataset(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    source_columns = [
        *SOURCE_IDENTIFIER_COLUMNS,
        *SCORE_COLUMN_MAPPING.keys(),
        "Preferensi Materi",
        "Alat Bantu",
    ]

    source_dataset = dataframe[
        source_columns
    ].copy()

    source_dataset = source_dataset.rename(
        columns={
            "Kode Siswa": "student_code",
            "Inisial": "initials",
            "Jenjang": "grade_level",
            "Kelas": "class_name",
            "Semester": "semester",
            "Tanggal Asesmen": (
                "assessment_date"
            ),
            "Preferensi Materi": (
                "material_preference"
            ),
            "Alat Bantu": (
                "assistive_tool"
            ),
            **SCORE_COLUMN_MAPPING,
        }
    )

    return source_dataset


def create_encoded_dataset(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    encoded_dataset = pd.DataFrame(
        {
            "student_code": (
                dataframe["Kode Siswa"]
                .astype(str)
            )
        }
    )

    for (
        source_column,
        output_column,
    ) in SCORE_COLUMN_MAPPING.items():
        encoded_dataset[
            output_column
        ] = dataframe[
            source_column
        ].astype(int)

    preferences = (
        dataframe["Preferensi Materi"]
        .astype(str)
        .str.strip()
    )

    for (
        category,
        output_column,
    ) in PREFERENCE_COLUMN_MAPPING.items():
        encoded_dataset[
            output_column
        ] = (
            preferences
            .eq(category)
            .astype(int)
        )

    tools = (
        dataframe["Alat Bantu"]
        .astype(str)
        .str.strip()
    )

    for (
        category,
        output_column,
    ) in TOOL_COLUMN_MAPPING.items():
        encoded_dataset[
            output_column
        ] = (
            tools
            .eq(category)
            .astype(int)
        )

    return encoded_dataset


def validate_encoded_dataset(
    dataframe: pd.DataFrame,
) -> None:
    feature_columns = [
        column
        for column in dataframe.columns
        if column != "student_code"
    ]

    missing_value_count = int(
        dataframe[
            feature_columns
        ]
        .isna()
        .sum()
        .sum()
    )

    if missing_value_count > 0:
        raise ValueError(
            "Dataset encoded masih memiliki "
            "missing value."
        )

    binary_columns = [
        *PREFERENCE_COLUMN_MAPPING.values(),
        *TOOL_COLUMN_MAPPING.values(),
    ]

    for column in binary_columns:
        valid_values = set(
            dataframe[column].unique()
        )

        if not valid_values.issubset(
            {0, 1}
        ):
            raise ValueError(
                f"Kolom binary '{column}' "
                "memiliki nilai selain 0 dan 1."
            )

    preference_columns = list(
        PREFERENCE_COLUMN_MAPPING.values()
    )

    preference_sum = dataframe[
        preference_columns
    ].sum(
        axis=1
    )

    invalid_preference_mask = (
        ~preference_sum.eq(1)
    )

    if invalid_preference_mask.any():
        invalid_codes = dataframe.loc[
            invalid_preference_mask,
            "student_code",
        ].tolist()

        raise ValueError(
            "Setiap siswa harus memiliki tepat "
            "satu preferensi materi. "
            "Kode siswa: "
            + ", ".join(invalid_codes)
        )

    tool_columns = list(
        TOOL_COLUMN_MAPPING.values()
    )

    tool_sum = dataframe[
        tool_columns
    ].sum(
        axis=1
    )

    invalid_tool_mask = (
        ~tool_sum.eq(1)
    )

    if invalid_tool_mask.any():
        invalid_codes = dataframe.loc[
            invalid_tool_mask,
            "student_code",
        ].tolist()

        raise ValueError(
            "Setiap siswa harus memiliki tepat "
            "satu kategori alat bantu. "
            "Kode siswa: "
            + ", ".join(invalid_codes)
        )


# FEATURE MANIFEST

def create_feature_manifest(
    source_row_count: int,
    modeling_row_count: int,
    feature_columns: list[str],
) -> dict:
    return {
        "dataset_name": (
            "InkluMap Initial Clustering Dataset"
        ),
        "source_file": (
            "data/processed/"
            "data_siswa_clean.csv"
        ),
        "source_row_count": (
            source_row_count
        ),
        "modeling_row_count": (
            modeling_row_count
        ),
        "status_filter": "Lengkap",
        "identifier_columns": [
            "student_code",
        ],
        "ordinal_features": list(
            SCORE_COLUMN_MAPPING.values()
        ),
        "binary_preference_features": list(
            PREFERENCE_COLUMN_MAPPING.values()
        ),
        "binary_assistive_tool_features": list(
            TOOL_COLUMN_MAPPING.values()
        ),
        "model_feature_columns": (
            feature_columns
        ),
        "feature_count": len(
            feature_columns
        ),
        "excluded_output_columns": (
            SOURCE_OUTPUT_COLUMNS
        ),
        "leakage_prevention": (
            "Kolom kelompok kebutuhan, kebutuhan "
            "dominan, prioritas, rekomendasi, "
            "dan status tindak lanjut tidak "
            "digunakan sebagai fitur clustering."
        ),
    }


# MAIN PROGRAM

def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            "Dataset bersih tidak ditemukan: "
            f"{INPUT_PATH}"
        )

    dataframe = pd.read_csv(
        INPUT_PATH,
        encoding="utf-8-sig",
    )

    dataframe.columns = (
        dataframe.columns
        .astype(str)
        .str.strip()
    )

    validate_required_columns(
        dataframe
    )

    source_row_count = len(
        dataframe
    )

    complete_dataframe = dataframe.loc[
        dataframe["Status Asesmen"]
        .astype(str)
        .str.strip()
        .eq("Lengkap")
    ].copy()

    if complete_dataframe.empty:
        raise ValueError(
            "Tidak terdapat siswa dengan "
            "asesmen lengkap."
        )

    complete_dataframe = (
        complete_dataframe
        .sort_values(
            by="Kode Siswa"
        )
        .reset_index(
            drop=True
        )
    )

    validate_complete_student_codes(
        complete_dataframe
    )

    complete_dataframe = (
        validate_score_columns(
            complete_dataframe
        )
    )

    validate_categories(
        complete_dataframe
    )

    source_dataset = (
        create_source_dataset(
            complete_dataframe
        )
    )

    encoded_dataset = (
        create_encoded_dataset(
            complete_dataframe
        )
    )

    validate_encoded_dataset(
        encoded_dataset
    )

    feature_columns = [
        column
        for column in encoded_dataset.columns
        if column != "student_code"
    ]

    manifest = create_feature_manifest(
        source_row_count=source_row_count,
        modeling_row_count=len(
            encoded_dataset
        ),
        feature_columns=feature_columns,
    )

    MODELING_SOURCE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    source_dataset.to_csv(
        MODELING_SOURCE_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    encoded_dataset.to_csv(
        MODELING_FEATURE_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    with FEATURE_MANIFEST_PATH.open(
        "w",
        encoding="utf-8",
    ) as manifest_file:
        json.dump(
            manifest,
            manifest_file,
            ensure_ascii=False,
            indent=2,
        )

    print()
    print(
        "DATASET MODELING BERHASIL DIBUAT"
    )
    print("-" * 55)

    print(
        f"Total data sumber       : "
        f"{source_row_count}"
    )

    print(
        f"Data asesmen lengkap    : "
        f"{len(encoded_dataset)}"
    )

    print(
        f"Jumlah fitur modeling   : "
        f"{len(feature_columns)}"
    )

    print(
        f"Dataset asli modeling   : "
        f"{MODELING_SOURCE_PATH}"
    )

    print(
        f"Dataset encoded         : "
        f"{MODELING_FEATURE_PATH}"
    )

    print(
        f"Feature manifest        : "
        f"{FEATURE_MANIFEST_PATH}"
    )

    print("-" * 55)


if __name__ == "__main__":
    main()