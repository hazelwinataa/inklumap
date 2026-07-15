# STANDARD LIBRARY

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


# PROJECT PATH

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIRECTORY = PROJECT_ROOT / "backend"

if str(BACKEND_DIRECTORY) not in sys.path:
    sys.path.insert(
        0,
        str(BACKEND_DIRECTORY),
    )


# THIRD-PARTY LIBRARIES

import pandas as pd
from sqlalchemy import func, select
from sqlalchemy.orm import Session


# LOCAL IMPORTS

from app.database import SessionLocal
from app.models import (
    Assessment,
    ClusterProfile,
    Student,
    StudentClusterResult,
    StudentRecommendation,
)


# FILE PATHS

ANALYTICS_RESULTS_DIRECTORY = (
    PROJECT_ROOT
    / "analytics"
    / "results"
)

CLUSTER_CATALOG_PATH = (
    ANALYTICS_RESULTS_DIRECTORY
    / "cluster_catalog.csv"
)

CLUSTER_MEDOIDS_PATH = (
    ANALYTICS_RESULTS_DIRECTORY
    / "cluster_medoids.csv"
)

STUDENT_RECOMMENDATIONS_PATH = (
    ANALYTICS_RESULTS_DIRECTORY
    / "student_recommendations.csv"
)

CLUSTERING_SUMMARY_PATH = (
    ANALYTICS_RESULTS_DIRECTORY
    / "clustering_experiment_summary.json"
)

RECOMMENDATION_SUMMARY_PATH = (
    ANALYTICS_RESULTS_DIRECTORY
    / "recommendation_summary.json"
)


# MODEL CONFIGURATION

DEFAULT_MODEL_VERSION = "hierarchical_gower_v1"
MODEL_NAME = "hierarchical_gower"
DISTANCE_METRIC = "gower"
LINKAGE_METHOD = "average"

EXPECTED_CLUSTER_COUNT = 5
EXPECTED_STUDENT_COUNT = 96


# REQUIRED COLUMNS

CLUSTER_CATALOG_COLUMNS = {
    "cluster_id",
    "cluster_name",
    "dominant_need",
    "description",
    "cluster_size",
    "recommendations",
}

CLUSTER_MEDOID_COLUMNS = {
    "cluster_id",
    "cluster_name",
    "medoid_student_code",
    "cluster_size",
    "mean_medoid_distance",
}

STUDENT_RECOMMENDATION_COLUMNS = {
    "student_code",
    "cluster_id",
    "cluster_name",
    "dominant_need_1",
    "dominant_need_2",
    "dominant_need_3",
    "maximum_need_score",
    "average_need_score",
    "critical_domain_count",
    "high_domain_count",
    "priority_level",
    "priority_action",
    "critical_access_flag",
    "critical_access_domains",
    "cluster_recommendations",
    "individual_recommendations",
    "material_preference",
    "assistive_tool",
    "individual_silhouette",
    "mean_distance_to_cluster",
    "dbscan_unique_case",
    "needs_human_review",
    "human_review_reason",
}


# HELPER FUNCTIONS

def clean_optional_text(
    value: Any,
) -> str | None:
    if pd.isna(value):
        return None

    cleaned_value = str(value).strip()

    if not cleaned_value:
        return None

    return cleaned_value


def split_pipe_values(
    value: Any,
) -> list[str]:
    cleaned_value = clean_optional_text(
        value
    )

    if cleaned_value is None:
        return []

    return [
        item.strip()
        for item in cleaned_value.split("|")
        if item.strip()
    ]


def parse_boolean(
    value: Any,
    field_name: str,
) -> bool:
    if isinstance(value, bool):
        return value

    normalized_value = str(
        value
    ).strip().lower()

    true_values = {
        "true",
        "1",
        "yes",
        "y",
    }

    false_values = {
        "false",
        "0",
        "no",
        "n",
    }

    if normalized_value in true_values:
        return True

    if normalized_value in false_values:
        return False

    raise ValueError(
        f"Nilai boolean pada '{field_name}' "
        f"tidak dikenal: {value}"
    )


def parse_integer(
    value: Any,
    field_name: str,
) -> int:
    try:
        numeric_value = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"Nilai '{field_name}' harus berupa integer."
        ) from error

    if (
        not math.isfinite(numeric_value)
        or not numeric_value.is_integer()
    ):
        raise ValueError(
            f"Nilai '{field_name}' harus berupa integer."
        )

    return int(numeric_value)


def parse_float(
    value: Any,
    field_name: str,
) -> float:
    try:
        numeric_value = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"Nilai '{field_name}' harus berupa angka."
        ) from error

    if not math.isfinite(numeric_value):
        raise ValueError(
            f"Nilai '{field_name}' harus finite."
        )

    return numeric_value


def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: set[str],
    file_name: str,
) -> None:
    missing_columns = sorted(
        required_columns
        - set(dataframe.columns)
    )

    if missing_columns:
        raise ValueError(
            f"Kolom pada {file_name} tidak lengkap: "
            + ", ".join(missing_columns)
        )


def read_json_file(
    file_path: Path,
) -> dict[str, Any]:
    with file_path.open(
        "r",
        encoding="utf-8",
    ) as json_file:
        return json.load(
            json_file
        )


# LOAD AND VALIDATE FILES

def validate_source_files() -> None:
    required_files = [
        CLUSTER_CATALOG_PATH,
        CLUSTER_MEDOIDS_PATH,
        STUDENT_RECOMMENDATIONS_PATH,
        CLUSTERING_SUMMARY_PATH,
        RECOMMENDATION_SUMMARY_PATH,
    ]

    missing_files = [
        file_path
        for file_path in required_files
        if not file_path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "File analytics berikut tidak ditemukan: "
            + ", ".join(
                str(file_path)
                for file_path in missing_files
            )
        )


def load_analytics_data() -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    dict[str, Any],
    dict[str, Any],
]:
    validate_source_files()

    cluster_catalog = pd.read_csv(
        CLUSTER_CATALOG_PATH,
        encoding="utf-8-sig",
    )

    cluster_medoids = pd.read_csv(
        CLUSTER_MEDOIDS_PATH,
        encoding="utf-8-sig",
    )

    student_recommendations = pd.read_csv(
        STUDENT_RECOMMENDATIONS_PATH,
        encoding="utf-8-sig",
        dtype={
            "student_code": "string",
        },
    )

    clustering_summary = read_json_file(
        CLUSTERING_SUMMARY_PATH
    )

    recommendation_summary = read_json_file(
        RECOMMENDATION_SUMMARY_PATH
    )

    validate_required_columns(
        cluster_catalog,
        CLUSTER_CATALOG_COLUMNS,
        CLUSTER_CATALOG_PATH.name,
    )

    validate_required_columns(
        cluster_medoids,
        CLUSTER_MEDOID_COLUMNS,
        CLUSTER_MEDOIDS_PATH.name,
    )

    validate_required_columns(
        student_recommendations,
        STUDENT_RECOMMENDATION_COLUMNS,
        STUDENT_RECOMMENDATIONS_PATH.name,
    )

    return (
        cluster_catalog,
        cluster_medoids,
        student_recommendations,
        clustering_summary,
        recommendation_summary,
    )


def normalize_analytics_data(
    cluster_catalog: pd.DataFrame,
    cluster_medoids: pd.DataFrame,
    student_recommendations: pd.DataFrame,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    for dataframe in (
        cluster_catalog,
        cluster_medoids,
        student_recommendations,
    ):
        dataframe["cluster_id"] = (
            dataframe["cluster_id"]
            .apply(
                lambda value: parse_integer(
                    value,
                    "cluster_id",
                )
            )
        )

    cluster_catalog["cluster_size"] = (
        cluster_catalog["cluster_size"]
        .apply(
            lambda value: parse_integer(
                value,
                "cluster_size",
            )
        )
    )

    cluster_medoids["cluster_size"] = (
        cluster_medoids["cluster_size"]
        .apply(
            lambda value: parse_integer(
                value,
                "cluster_size",
            )
        )
    )

    student_recommendations[
        "student_code"
    ] = (
        student_recommendations[
            "student_code"
        ]
        .astype("string")
        .str.strip()
    )

    return (
        cluster_catalog,
        cluster_medoids,
        student_recommendations,
    )


def validate_analytics_consistency(
    cluster_catalog: pd.DataFrame,
    cluster_medoids: pd.DataFrame,
    student_recommendations: pd.DataFrame,
    clustering_summary: dict[str, Any],
    recommendation_summary: dict[str, Any],
) -> float:
    expected_cluster_ids = set(
        range(
            1,
            EXPECTED_CLUSTER_COUNT + 1,
        )
    )

    catalog_cluster_ids = set(
        cluster_catalog[
            "cluster_id"
        ].tolist()
    )

    medoid_cluster_ids = set(
        cluster_medoids[
            "cluster_id"
        ].tolist()
    )

    recommendation_cluster_ids = set(
        student_recommendations[
            "cluster_id"
        ].tolist()
    )

    if len(cluster_catalog) != EXPECTED_CLUSTER_COUNT:
        raise ValueError(
            "Jumlah cluster pada katalog harus "
            f"{EXPECTED_CLUSTER_COUNT}."
        )

    if len(cluster_medoids) != EXPECTED_CLUSTER_COUNT:
        raise ValueError(
            "Jumlah medoid harus "
            f"{EXPECTED_CLUSTER_COUNT}."
        )

    if (
        catalog_cluster_ids
        != expected_cluster_ids
        or medoid_cluster_ids
        != expected_cluster_ids
        or recommendation_cluster_ids
        != expected_cluster_ids
    ):
        raise ValueError(
            "Cluster ID pada file analytics "
            "tidak konsisten."
        )

    if (
        len(student_recommendations)
        != EXPECTED_STUDENT_COUNT
    ):
        raise ValueError(
            "Jumlah rekomendasi siswa harus "
            f"{EXPECTED_STUDENT_COUNT}."
        )

    duplicate_student_codes = (
        student_recommendations[
            "student_code"
        ].duplicated()
    )

    if duplicate_student_codes.any():
        duplicate_codes = (
            student_recommendations.loc[
                duplicate_student_codes,
                "student_code",
            ]
            .astype(str)
            .tolist()
        )

        raise ValueError(
            "Kode siswa duplikat pada hasil analytics: "
            + ", ".join(duplicate_codes)
        )

    if student_recommendations[
        "student_code"
    ].isna().any():
        raise ValueError(
            "Kode siswa pada hasil analytics "
            "tidak boleh kosong."
        )

    actual_cluster_sizes = (
        student_recommendations[
            "cluster_id"
        ]
        .value_counts()
        .sort_index()
        .to_dict()
    )

    catalog_size_mapping = dict(
        zip(
            cluster_catalog[
                "cluster_id"
            ],
            cluster_catalog[
                "cluster_size"
            ],
            strict=True,
        )
    )

    medoid_size_mapping = dict(
        zip(
            cluster_medoids[
                "cluster_id"
            ],
            cluster_medoids[
                "cluster_size"
            ],
            strict=True,
        )
    )

    summary_cluster_sizes = {
        int(cluster_id): int(count)
        for cluster_id, count
        in recommendation_summary[
            "cluster_sizes"
        ].items()
    }

    for cluster_id in sorted(
        expected_cluster_ids
    ):
        actual_size = int(
            actual_cluster_sizes.get(
                cluster_id,
                0,
            )
        )

        if (
            actual_size
            != int(
                catalog_size_mapping[
                    cluster_id
                ]
            )
            or actual_size
            != int(
                medoid_size_mapping[
                    cluster_id
                ]
            )
            or actual_size
            != int(
                summary_cluster_sizes[
                    cluster_id
                ]
            )
        ):
            raise ValueError(
                "Ukuran cluster tidak konsisten "
                f"untuk cluster {cluster_id}."
            )

    catalog_name_mapping = dict(
        zip(
            cluster_catalog[
                "cluster_id"
            ],
            cluster_catalog[
                "cluster_name"
            ],
            strict=True,
        )
    )

    for row in (
        student_recommendations
        .itertuples(
            index=False
        )
    ):
        cluster_id = int(
            row.cluster_id
        )

        expected_name = str(
            catalog_name_mapping[
                cluster_id
            ]
        ).strip()

        actual_name = str(
            row.cluster_name
        ).strip()

        if actual_name != expected_name:
            raise ValueError(
                "Nama cluster siswa tidak sesuai "
                f"untuk {row.student_code}."
            )

    recommendation_by_student = (
        student_recommendations
        .set_index(
            "student_code"
        )
    )

    for medoid_row in (
        cluster_medoids.itertuples(
            index=False
        )
    ):
        medoid_code = str(
            medoid_row.medoid_student_code
        ).strip()

        if medoid_code not in (
            recommendation_by_student.index
        ):
            raise ValueError(
                "Kode siswa medoid tidak ditemukan: "
                f"{medoid_code}"
            )

        medoid_cluster_id = int(
            recommendation_by_student.loc[
                medoid_code,
                "cluster_id",
            ]
        )

        if (
            medoid_cluster_id
            != int(
                medoid_row.cluster_id
            )
        ):
            raise ValueError(
                "Medoid tidak berada pada cluster "
                f"yang sesuai: {medoid_code}"
            )

    best_hierarchical = (
        clustering_summary.get(
            "best_hierarchical_gower",
            {},
        )
    )

    silhouette_score = parse_float(
        best_hierarchical.get(
            "silhouette_score"
        ),
        "silhouette_score",
    )

    if not -1 <= silhouette_score <= 1:
        raise ValueError(
            "Silhouette model harus berada "
            "antara -1 dan 1."
        )

    if (
        recommendation_summary.get(
            "total_students"
        )
        != EXPECTED_STUDENT_COUNT
    ):
        raise ValueError(
            "Jumlah siswa pada recommendation "
            "summary tidak sesuai."
        )

    selected_rule = (
        recommendation_summary
        .get(
            "priority_rule",
            {},
        )
        .get(
            "selected_rule"
        )
    )

    if selected_rule != "balanced":
        raise ValueError(
            "Aturan prioritas final harus balanced."
        )

    valid_priorities = {
        "high",
        "medium",
        "low",
    }

    actual_priorities = set(
        student_recommendations[
            "priority_level"
        ]
        .astype(str)
        .str.strip()
        .str.lower()
        .unique()
    )

    if not actual_priorities.issubset(
        valid_priorities
    ):
        raise ValueError(
            "Terdapat priority_level "
            "yang tidak dikenal."
        )

    return silhouette_score


# DATABASE LOOKUPS

def get_student_mapping(
    database: Session,
    student_codes: list[str],
) -> dict[str, Student]:
    students = database.scalars(
        select(Student).where(
            Student.student_code.in_(
                student_codes
            )
        )
    ).all()

    student_mapping = {
        student.student_code: student
        for student in students
    }

    missing_student_codes = sorted(
        set(student_codes)
        - set(student_mapping)
    )

    if missing_student_codes:
        raise ValueError(
            "Siswa berikut tidak ditemukan "
            "di database: "
            + ", ".join(missing_student_codes)
        )

    incomplete_student_codes = sorted(
        student_code
        for student_code, student
        in student_mapping.items()
        if student.assessment_status
        != "complete"
    )

    if incomplete_student_codes:
        raise ValueError(
            "Hasil analytics hanya boleh diimpor "
            "untuk siswa berstatus complete: "
            + ", ".join(
                incomplete_student_codes
            )
        )

    return student_mapping


def get_latest_assessment_mapping(
    database: Session,
    student_codes: list[str],
) -> dict[str, Assessment]:
    rows = database.execute(
        select(
            Student.student_code,
            Assessment,
        )
        .join(
            Assessment,
            Assessment.student_id
            == Student.id,
        )
        .where(
            Student.student_code.in_(
                student_codes
            ),
            Assessment.status.in_(
                [
                    "submitted",
                    "validated",
                ]
            ),
        )
        .order_by(
            Student.student_code,
            Assessment.assessment_date.desc(),
            Assessment.id.desc(),
        )
    ).all()

    assessment_mapping: dict[
        str,
        Assessment,
    ] = {}

    for student_code, assessment in rows:
        if (
            student_code
            not in assessment_mapping
        ):
            assessment_mapping[
                student_code
            ] = assessment

    missing_assessments = sorted(
        set(student_codes)
        - set(assessment_mapping)
    )

    if missing_assessments:
        raise ValueError(
            "Assessment submitted/validated "
            "tidak ditemukan untuk siswa: "
            + ", ".join(missing_assessments)
        )

    return assessment_mapping


# UPSERT FUNCTIONS

def upsert_cluster_profiles(
    database: Session,
    cluster_catalog: pd.DataFrame,
    cluster_medoids: pd.DataFrame,
    student_mapping: dict[str, Student],
    model_version: str,
    silhouette_score: float,
) -> tuple[
    dict[int, ClusterProfile],
    int,
    int,
]:
    medoid_mapping = (
        cluster_medoids.set_index(
            "cluster_id"
        )
    )

    profile_mapping: dict[
        int,
        ClusterProfile,
    ] = {}

    inserted_count = 0
    updated_count = 0

    for catalog_row in (
        cluster_catalog.itertuples(
            index=False
        )
    ):
        cluster_id = int(
            catalog_row.cluster_id
        )

        medoid_row = medoid_mapping.loc[
            cluster_id
        ]

        medoid_student_code = str(
            medoid_row[
                "medoid_student_code"
            ]
        ).strip()

        profile = database.scalar(
            select(
                ClusterProfile
            ).where(
                ClusterProfile.model_version
                == model_version,
                ClusterProfile.cluster_number
                == cluster_id,
            )
        )

        if profile is None:
            profile = ClusterProfile(
                model_version=model_version,
                cluster_number=cluster_id,
            )

            database.add(
                profile
            )

            inserted_count += 1
        else:
            updated_count += 1

        profile.model_name = MODEL_NAME
        profile.distance_metric = (
            DISTANCE_METRIC
        )
        profile.linkage = LINKAGE_METHOD
        profile.cluster_name = str(
            catalog_row.cluster_name
        ).strip()
        profile.dominant_need = str(
            catalog_row.dominant_need
        ).strip()
        profile.description = str(
            catalog_row.description
        ).strip()
        profile.recommendations = (
            split_pipe_values(
                catalog_row.recommendations
            )
        )
        profile.medoid_student_id = (
            student_mapping[
                medoid_student_code
            ].id
        )
        profile.cluster_size = int(
            catalog_row.cluster_size
        )
        profile.mean_medoid_distance = (
            parse_float(
                medoid_row[
                    "mean_medoid_distance"
                ],
                "mean_medoid_distance",
            )
        )
        profile.model_silhouette_score = (
            silhouette_score
        )

        database.flush()

        profile_mapping[
            cluster_id
        ] = profile

    return (
        profile_mapping,
        inserted_count,
        updated_count,
    )


def get_dominant_needs(
    row: Any,
) -> list[str]:
    values = [
        row.dominant_need_1,
        row.dominant_need_2,
        row.dominant_need_3,
    ]

    dominant_needs = []

    for value in values:
        cleaned_value = clean_optional_text(
            value
        )

        if (
            cleaned_value is not None
            and cleaned_value
            not in dominant_needs
        ):
            dominant_needs.append(
                cleaned_value
            )

    return dominant_needs


def upsert_student_results(
    database: Session,
    recommendations: pd.DataFrame,
    assessment_mapping: dict[
        str,
        Assessment,
    ],
    profile_mapping: dict[
        int,
        ClusterProfile,
    ],
    model_version: str,
) -> tuple[int, int, int, int]:
    inserted_results = 0
    updated_results = 0
    inserted_recommendations = 0
    updated_recommendations = 0

    for row in recommendations.itertuples(
        index=False
    ):
        student_code = str(
            row.student_code
        ).strip()

        assessment = assessment_mapping[
            student_code
        ]

        cluster_id = int(
            row.cluster_id
        )

        cluster_profile = (
            profile_mapping[
                cluster_id
            ]
        )

        cluster_result = database.scalar(
            select(
                StudentClusterResult
            ).where(
                StudentClusterResult.assessment_id
                == assessment.id,
                StudentClusterResult.model_version
                == model_version,
            )
        )

        if cluster_result is None:
            cluster_result = (
                StudentClusterResult(
                    assessment_id=assessment.id,
                    model_version=model_version,
                )
            )

            database.add(
                cluster_result
            )

            inserted_results += 1
        else:
            updated_results += 1

        cluster_result.cluster_profile_id = (
            cluster_profile.id
        )
        cluster_result.dominant_needs = (
            get_dominant_needs(
                row
            )
        )
        cluster_result.maximum_need_score = (
            parse_integer(
                row.maximum_need_score,
                "maximum_need_score",
            )
        )
        cluster_result.average_need_score = (
            parse_float(
                row.average_need_score,
                "average_need_score",
            )
        )
        cluster_result.critical_domain_count = (
            parse_integer(
                row.critical_domain_count,
                "critical_domain_count",
            )
        )
        cluster_result.high_domain_count = (
            parse_integer(
                row.high_domain_count,
                "high_domain_count",
            )
        )
        cluster_result.priority_level = str(
            row.priority_level
        ).strip().lower()
        cluster_result.individual_silhouette = (
            parse_float(
                row.individual_silhouette,
                "individual_silhouette",
            )
        )
        cluster_result.mean_distance_to_cluster = (
            parse_float(
                row.mean_distance_to_cluster,
                "mean_distance_to_cluster",
            )
        )
        cluster_result.critical_access_flag = (
            parse_boolean(
                row.critical_access_flag,
                "critical_access_flag",
            )
        )
        cluster_result.critical_access_domains = (
            split_pipe_values(
                row.critical_access_domains
            )
        )
        cluster_result.dbscan_unique_case = (
            parse_boolean(
                row.dbscan_unique_case,
                "dbscan_unique_case",
            )
        )
        cluster_result.needs_human_review = (
            parse_boolean(
                row.needs_human_review,
                "needs_human_review",
            )
        )
        cluster_result.human_review_reason = (
            clean_optional_text(
                row.human_review_reason
            )
        )

        database.flush()

        recommendation = database.scalar(
            select(
                StudentRecommendation
            ).where(
                StudentRecommendation.cluster_result_id
                == cluster_result.id
            )
        )

        if recommendation is None:
            recommendation = (
                StudentRecommendation(
                    cluster_result_id=(
                        cluster_result.id
                    ),
                    recommendation_status=(
                        "generated"
                    ),
                )
            )

            database.add(
                recommendation
            )

            inserted_recommendations += 1
        else:
            updated_recommendations += 1

        recommendation.priority_action = str(
            row.priority_action
        ).strip()
        recommendation.cluster_recommendations = (
            split_pipe_values(
                row.cluster_recommendations
            )
        )
        recommendation.individual_recommendations = (
            split_pipe_values(
                row.individual_recommendations
            )
        )
        recommendation.material_preference = (
            clean_optional_text(
                row.material_preference
            )
        )
        recommendation.assistive_tool = (
            clean_optional_text(
                row.assistive_tool
            )
        )

    return (
        inserted_results,
        updated_results,
        inserted_recommendations,
        updated_recommendations,
    )


# DATABASE VALIDATION

def validate_database_counts(
    database: Session,
    model_version: str,
) -> tuple[int, int, int]:
    profile_count = (
        database.scalar(
            select(
                func.count(
                    ClusterProfile.id
                )
            ).where(
                ClusterProfile.model_version
                == model_version
            )
        )
        or 0
    )

    result_count = (
        database.scalar(
            select(
                func.count(
                    StudentClusterResult.id
                )
            ).where(
                StudentClusterResult.model_version
                == model_version
            )
        )
        or 0
    )

    recommendation_count = (
        database.scalar(
            select(
                func.count(
                    StudentRecommendation.id
                )
            )
            .join(
                StudentClusterResult,
                StudentRecommendation.cluster_result_id
                == StudentClusterResult.id,
            )
            .where(
                StudentClusterResult.model_version
                == model_version
            )
        )
        or 0
    )

    if profile_count != EXPECTED_CLUSTER_COUNT:
        raise RuntimeError(
            "Jumlah cluster_profiles untuk model "
            f"{model_version} harus "
            f"{EXPECTED_CLUSTER_COUNT}, ditemukan "
            f"{profile_count}."
        )

    if result_count != EXPECTED_STUDENT_COUNT:
        raise RuntimeError(
            "Jumlah student_cluster_results untuk "
            f"model {model_version} harus "
            f"{EXPECTED_STUDENT_COUNT}, ditemukan "
            f"{result_count}."
        )

    if (
        recommendation_count
        != EXPECTED_STUDENT_COUNT
    ):
        raise RuntimeError(
            "Jumlah student_recommendations untuk "
            f"model {model_version} harus "
            f"{EXPECTED_STUDENT_COUNT}, ditemukan "
            f"{recommendation_count}."
        )

    return (
        int(profile_count),
        int(result_count),
        int(recommendation_count),
    )


# IMPORT PROCESS

def import_analytics_results(
    model_version: str,
    dry_run: bool,
) -> None:
    (
        cluster_catalog,
        cluster_medoids,
        student_recommendations,
        clustering_summary,
        recommendation_summary,
    ) = load_analytics_data()

    (
        cluster_catalog,
        cluster_medoids,
        student_recommendations,
    ) = normalize_analytics_data(
        cluster_catalog,
        cluster_medoids,
        student_recommendations,
    )

    silhouette_score = (
        validate_analytics_consistency(
            cluster_catalog,
            cluster_medoids,
            student_recommendations,
            clustering_summary,
            recommendation_summary,
        )
    )

    student_codes = (
        student_recommendations[
            "student_code"
        ]
        .astype(str)
        .tolist()
    )

    database = SessionLocal()

    try:
        student_mapping = (
            get_student_mapping(
                database,
                student_codes,
            )
        )

        assessment_mapping = (
            get_latest_assessment_mapping(
                database,
                student_codes,
            )
        )

        (
            profile_mapping,
            inserted_profiles,
            updated_profiles,
        ) = upsert_cluster_profiles(
            database=database,
            cluster_catalog=cluster_catalog,
            cluster_medoids=cluster_medoids,
            student_mapping=student_mapping,
            model_version=model_version,
            silhouette_score=silhouette_score,
        )

        (
            inserted_results,
            updated_results,
            inserted_recommendations,
            updated_recommendations,
        ) = upsert_student_results(
            database=database,
            recommendations=student_recommendations,
            assessment_mapping=assessment_mapping,
            profile_mapping=profile_mapping,
            model_version=model_version,
        )

        database.flush()

        (
            profile_count,
            result_count,
            recommendation_count,
        ) = validate_database_counts(
            database,
            model_version,
        )

        if dry_run:
            database.rollback()
        else:
            database.commit()

        print()
        print(
            "IMPORT ANALYTICS BERHASIL"
            if not dry_run
            else "DRY RUN ANALYTICS BERHASIL"
        )
        print("-" * 60)
        print(
            f"Model version               : "
            f"{model_version}"
        )
        print(
            f"Cluster profile baru        : "
            f"{inserted_profiles}"
        )
        print(
            f"Cluster profile diperbarui  : "
            f"{updated_profiles}"
        )
        print(
            f"Cluster result baru         : "
            f"{inserted_results}"
        )
        print(
            f"Cluster result diperbarui   : "
            f"{updated_results}"
        )
        print(
            f"Rekomendasi baru            : "
            f"{inserted_recommendations}"
        )
        print(
            f"Rekomendasi diperbarui      : "
            f"{updated_recommendations}"
        )
        print(
            f"Total cluster profile       : "
            f"{profile_count}"
        )
        print(
            f"Total cluster result        : "
            f"{result_count}"
        )
        print(
            f"Total rekomendasi           : "
            f"{recommendation_count}"
        )
        print(
            f"Silhouette model            : "
            f"{silhouette_score:.4f}"
        )
        print(
            "Perubahan database          : "
            + (
                "dibatalkan karena dry run"
                if dry_run
                else "disimpan"
            )
        )
        print("-" * 60)

    except Exception:
        database.rollback()
        raise

    finally:
        database.close()


# MAIN PROGRAM

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Mengimpor hasil clustering dan "
            "rekomendasi InkluMap ke PostgreSQL "
            "secara idempotent."
        )
    )

    parser.add_argument(
        "--model-version",
        default=DEFAULT_MODEL_VERSION,
        help=(
            "Versi model analytics. Default: "
            f"{DEFAULT_MODEL_VERSION}"
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Menjalankan validasi dan simulasi "
            "import tanpa menyimpan perubahan."
        ),
    )

    arguments = parser.parse_args()

    model_version = (
        arguments.model_version.strip()
    )

    if not model_version:
        raise ValueError(
            "Model version tidak boleh kosong."
        )

    import_analytics_results(
        model_version=model_version,
        dry_run=arguments.dry_run,
    )


if __name__ == "__main__":
    main()
