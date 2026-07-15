# STANDARD LIBRARY

import json
from pathlib import Path
from typing import Any


# THIRD-PARTY LIBRARIES

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_samples


# FILE PATHS

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ASSIGNMENTS_PATH = (
    PROJECT_ROOT
    / "analytics"
    / "results"
    / "hierarchical_gower_assignments.csv"
)

SOURCE_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "modeling_complete_students.csv"
)

DISTANCE_MATRIX_PATH = (
    PROJECT_ROOT
    / "analytics"
    / "models"
    / "gower_distance_matrix.npy"
)

RESULTS_DIRECTORY = (
    PROJECT_ROOT
    / "analytics"
    / "results"
)

STUDENT_RECOMMENDATIONS_PATH = (
    RESULTS_DIRECTORY
    / "student_recommendations.csv"
)

CLUSTER_CATALOG_CSV_PATH = (
    RESULTS_DIRECTORY
    / "cluster_catalog.csv"
)

CLUSTER_CATALOG_JSON_PATH = (
    RESULTS_DIRECTORY
    / "cluster_catalog.json"
)

CLUSTER_MEDOIDS_PATH = (
    RESULTS_DIRECTORY
    / "cluster_medoids.csv"
)

RECOMMENDATION_SUMMARY_PATH = (
    RESULTS_DIRECTORY
    / "recommendation_summary.json"
)


# FEATURE CONFIGURATION

SCORE_COLUMNS = [
    "visual_score",
    "hearing_score",
    "communication_score",
    "instruction_score",
    "attention_score",
    "mobility_score",
    "assistance_score",
    "evaluation_adjustment_score",
]

CRITICAL_ACCESS_FEATURES = [
    "visual_score",
    "hearing_score",
    "mobility_score",
]

FEATURE_LABELS = {
    "visual_score": "Akses Visual",
    "hearing_score": "Pendengaran",
    "communication_score": "Komunikasi",
    "instruction_score": "Pemahaman Instruksi",
    "attention_score": "Perhatian dan Konsentrasi",
    "mobility_score": "Mobilitas",
    "assistance_score": "Pendampingan",
    "evaluation_adjustment_score": (
        "Penyesuaian Evaluasi"
    ),
}

FEATURE_RECOMMENDATIONS = {
    "visual_score": (
        "Sediakan materi audio, deskripsi verbal, "
        "teks berkontras baik, dan dokumen yang "
        "kompatibel dengan pembaca layar."
    ),
    "hearing_score": (
        "Sediakan caption, transkrip, instruksi "
        "tertulis, dan posisi belajar yang "
        "memudahkan siswa melihat guru."
    ),
    "communication_score": (
        "Gunakan dukungan komunikasi visual, "
        "pilihan respons tertulis, dan waktu "
        "tambahan untuk menyampaikan jawaban."
    ),
    "instruction_score": (
        "Pecah instruksi menjadi langkah pendek, "
        "gunakan contoh konkret, dan lakukan "
        "pemeriksaan pemahaman."
    ),
    "attention_score": (
        "Kurangi distraksi, gunakan jadwal "
        "terstruktur, berikan jeda, dan pecah "
        "aktivitas menjadi bagian yang singkat."
    ),
    "mobility_score": (
        "Pastikan jalur, meja, ruang belajar, "
        "dan fasilitas sekolah mudah diakses."
    ),
    "assistance_score": (
        "Sediakan pendampingan bertahap dan "
        "monitor kebutuhan bantuan individual."
    ),
    "evaluation_adjustment_score": (
        "Berikan waktu tambahan, jeda, pilihan "
        "bentuk evaluasi, dan ruang dengan "
        "distraksi rendah."
    ),
}


# CLUSTER CATALOG

CLUSTER_CATALOG = {
    1: {
        "cluster_name": (
            "Dukungan Instruksi Terstruktur"
        ),
        "dominant_need": (
            "Pemahaman Instruksi"
        ),
        "description": (
            "Kelompok dengan kebutuhan utama "
            "pada pemahaman instruksi, perhatian, "
            "pendampingan, dan penyesuaian evaluasi."
        ),
        "recommendations": [
            (
                "Pecah instruksi menjadi "
                "langkah-langkah pendek."
            ),
            (
                "Gunakan materi visual sederhana "
                "dan contoh konkret."
            ),
            (
                "Lakukan pemeriksaan pemahaman "
                "setelah setiap tahap."
            ),
            (
                "Sediakan lingkungan belajar "
                "dengan distraksi minimal."
            ),
            (
                "Berikan waktu tambahan dan "
                "pendampingan pada tugas kompleks."
            ),
        ],
    },
    2: {
        "cluster_name": (
            "Akses Visual dan Materi Auditori"
        ),
        "dominant_need": "Akses Visual",
        "description": (
            "Kelompok dengan kebutuhan akses "
            "visual yang dominan serta preferensi "
            "terhadap materi audio dan "
            "Text-to-Speech."
        ),
        "recommendations": [
            "Sediakan materi pembelajaran audio.",
            (
                "Gunakan Text-to-Speech dan "
                "dokumen digital yang aksesibel."
            ),
            (
                "Berikan deskripsi verbal untuk "
                "gambar, grafik, dan diagram."
            ),
            (
                "Pastikan ukuran teks dan kontras "
                "dapat disesuaikan."
            ),
            (
                "Jangan menyampaikan informasi "
                "hanya melalui media visual."
            ),
        ],
    },
    3: {
        "cluster_name": (
            "Akses Pendengaran dan "
            "Komunikasi Tertulis"
        ),
        "dominant_need": "Pendengaran",
        "description": (
            "Kelompok dengan kebutuhan utama "
            "pada akses pendengaran dan komunikasi, "
            "serta memerlukan caption dan teks."
        ),
        "recommendations": [
            "Sediakan caption dan subtitle.",
            (
                "Sediakan transkrip untuk materi "
                "audio dan video."
            ),
            "Berikan instruksi dalam bentuk tertulis.",
            (
                "Kurangi kebisingan latar belakang "
                "di ruang belajar."
            ),
            (
                "Gunakan dukungan komunikasi visual "
                "dan konfirmasi tertulis."
            ),
        ],
    },
    4: {
        "cluster_name": (
            "Akses Mobilitas dan "
            "Lingkungan Belajar"
        ),
        "dominant_need": "Mobilitas",
        "description": (
            "Kelompok dengan kebutuhan utama pada "
            "mobilitas, akses ruang, tata letak, "
            "dan penggunaan perangkat mobilitas."
        ),
        "recommendations": [
            (
                "Pastikan jalur dan ruang kelas "
                "dapat diakses."
            ),
            (
                "Gunakan meja dan tata letak "
                "belajar yang adaptif."
            ),
            (
                "Sediakan waktu tambahan untuk "
                "perpindahan antarruang."
            ),
            (
                "Sediakan pilihan pengumpulan "
                "tugas secara digital."
            ),
            (
                "Siapkan prosedur evakuasi yang "
                "aksesibel."
            ),
        ],
    },
    5: {
        "cluster_name": (
            "Evaluasi Adaptif dan "
            "Pendampingan Intensif"
        ),
        "dominant_need": (
            "Penyesuaian Evaluasi"
        ),
        "description": (
            "Kelompok dengan kebutuhan "
            "multidimensi pada penyesuaian evaluasi, "
            "pendampingan, instruksi, dan perhatian."
        ),
        "recommendations": [
            "Berikan waktu evaluasi tambahan.",
            (
                "Pecah evaluasi menjadi beberapa "
                "sesi dengan jeda terstruktur."
            ),
            (
                "Sediakan ruang evaluasi dengan "
                "distraksi rendah."
            ),
            (
                "Sediakan pilihan evaluasi lisan, "
                "praktik, proyek, atau tertulis."
            ),
            (
                "Gunakan instruksi tertulis dan "
                "verbal secara bersamaan."
            ),
            (
                "Sediakan alat tulis adaptif dan "
                "pendampingan individual."
            ),
        ],
    },
}


# VALIDATION

def validate_files() -> None:
    required_files = [
        ASSIGNMENTS_PATH,
        SOURCE_DATA_PATH,
        DISTANCE_MATRIX_PATH,
    ]

    missing_files = [
        file_path
        for file_path in required_files
        if not file_path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "File berikut tidak ditemukan: "
            + ", ".join(
                str(file_path)
                for file_path in missing_files
            )
        )


def load_data(
) -> tuple[
    pd.DataFrame,
    np.ndarray,
]:
    assignments = pd.read_csv(
        ASSIGNMENTS_PATH,
        encoding="utf-8-sig",
    )

    source_dataframe = pd.read_csv(
        SOURCE_DATA_PATH,
        encoding="utf-8-sig",
    )

    distance_matrix = np.load(
        DISTANCE_MATRIX_PATH
    )

    assignments = assignments.sort_values(
        "student_code"
    ).reset_index(drop=True)

    source_dataframe = source_dataframe.sort_values(
        "student_code"
    ).reset_index(drop=True)

    if not assignments[
        "student_code"
    ].equals(
        source_dataframe["student_code"]
    ):
        raise ValueError(
            "Urutan student_code pada assignments "
            "dan source dataset tidak sama."
        )

    expected_shape = (
        len(assignments),
        len(assignments),
    )

    if distance_matrix.shape != expected_shape:
        raise ValueError(
            "Ukuran matriks Gower tidak sesuai. "
            f"Ditemukan {distance_matrix.shape}, "
            f"seharusnya {expected_shape}."
        )

    missing_score_columns = [
        column
        for column in SCORE_COLUMNS
        if column not in assignments.columns
    ]

    if missing_score_columns:
        raise ValueError(
            "Kolom skor tidak ditemukan: "
            + ", ".join(missing_score_columns)
        )

    available_clusters = set(
        assignments["cluster_id"]
        .astype(int)
        .unique()
    )

    expected_clusters = set(
        CLUSTER_CATALOG.keys()
    )

    if available_clusters != expected_clusters:
        raise ValueError(
            "Cluster pada data tidak sesuai "
            "dengan katalog cluster."
        )

    return assignments, distance_matrix


# PRIORITY

def determine_priority(
    scores: np.ndarray,
) -> tuple[str, int, int, float]:
    critical_domain_count = int(
        np.sum(scores == 3)
    )

    high_domain_count = int(
        np.sum(scores >= 2)
    )

    average_need_score = float(
        np.mean(scores)
    )

    # Aturan balanced dipilih berdasarkan
    # sensitivity analysis.
    if (
        critical_domain_count >= 3
        or high_domain_count >= 5
        or average_need_score >= 2.00
    ):
        priority_level = "high"

    elif (
        critical_domain_count >= 1
        or high_domain_count >= 3
        or average_need_score >= 1.25
    ):
        priority_level = "medium"

    else:
        priority_level = "low"

    return (
        priority_level,
        critical_domain_count,
        high_domain_count,
        average_need_score,
    )


def get_priority_action(
    priority_level: str,
) -> str:
    priority_actions = {
        "high": (
            "Lakukan validasi manusia dan susun "
            "rencana akomodasi individual sesegera "
            "mungkin."
        ),
        "medium": (
            "Lakukan verifikasi guru dan siapkan "
            "akomodasi pada domain kebutuhan utama."
        ),
        "low": (
            "Lanjutkan pemantauan berkala dan "
            "sediakan dukungan ketika dibutuhkan."
        ),
    }

    return priority_actions[
        priority_level
    ]


# INDIVIDUAL PROFILE

def get_dominant_domains(
    row: pd.Series,
    maximum_domains: int = 3,
) -> list[str]:
    score_pairs = [
        (
            feature,
            int(row[feature]),
        )
        for feature in SCORE_COLUMNS
    ]

    sorted_scores = sorted(
        score_pairs,
        key=lambda item: (
            -item[1],
            SCORE_COLUMNS.index(
                item[0]
            ),
        ),
    )

    selected_features = [
        feature
        for feature, score
        in sorted_scores
        if score >= 1
    ][:maximum_domains]

    if not selected_features:
        selected_features = [
            sorted_scores[0][0]
        ]

    return selected_features


def get_critical_access_domains(
    row: pd.Series,
) -> list[str]:
    critical_domains = [
        FEATURE_LABELS[feature]
        for feature in CRITICAL_ACCESS_FEATURES
        if int(row[feature]) == 3
    ]

    return critical_domains


def calculate_mean_cluster_distance(
    row_index: int,
    labels: np.ndarray,
    distance_matrix: np.ndarray,
) -> float:
    own_cluster = labels[
        row_index
    ]

    cluster_member_indexes = np.where(
        labels == own_cluster
    )[0]

    other_member_indexes = (
        cluster_member_indexes[
            cluster_member_indexes
            != row_index
        ]
    )

    if len(other_member_indexes) == 0:
        return 0.0

    return float(
        np.mean(
            distance_matrix[
                row_index,
                other_member_indexes,
            ]
        )
    )


# MEDOIDS

def create_cluster_medoids(
    assignments: pd.DataFrame,
    distance_matrix: np.ndarray,
) -> pd.DataFrame:
    medoid_rows = []

    labels = assignments[
        "cluster_id"
    ].to_numpy(dtype=int)

    for cluster_id in sorted(
        assignments["cluster_id"].unique()
    ):
        cluster_indexes = np.where(
            labels == cluster_id
        )[0]

        cluster_distances = (
            distance_matrix[
                np.ix_(
                    cluster_indexes,
                    cluster_indexes,
                )
            ]
        )

        mean_distances = (
            cluster_distances.mean(axis=1)
        )

        local_medoid_position = int(
            np.argmin(mean_distances)
        )

        medoid_index = int(
            cluster_indexes[
                local_medoid_position
            ]
        )

        medoid_rows.append(
            {
                "cluster_id": int(
                    cluster_id
                ),
                "cluster_name": (
                    CLUSTER_CATALOG[
                        int(cluster_id)
                    ]["cluster_name"]
                ),
                "medoid_student_code": (
                    assignments.iloc[
                        medoid_index
                    ]["student_code"]
                ),
                "cluster_size": int(
                    len(cluster_indexes)
                ),
                "mean_medoid_distance": float(
                    mean_distances[
                        local_medoid_position
                    ]
                ),
            }
        )

    return pd.DataFrame(
        medoid_rows
    )


# RECOMMENDATION DATASET

def create_student_recommendations(
    assignments: pd.DataFrame,
    distance_matrix: np.ndarray,
) -> pd.DataFrame:
    labels = assignments[
        "cluster_id"
    ].to_numpy(dtype=int)

    individual_silhouettes = (
        silhouette_samples(
            distance_matrix,
            labels,
            metric="precomputed",
        )
    )

    dbscan_labels = DBSCAN(
        eps=0.1,
        min_samples=3,
        metric="precomputed",
    ).fit_predict(
        distance_matrix
    )

    output_rows = []

    for row_index, row in assignments.iterrows():
        cluster_id = int(
            row["cluster_id"]
        )

        cluster_information = (
            CLUSTER_CATALOG[
                cluster_id
            ]
        )

        scores = row[
            SCORE_COLUMNS
        ].to_numpy(dtype=float)

        (
            priority_level,
            critical_domain_count,
            high_domain_count,
            average_need_score,
        ) = determine_priority(
            scores
        )

        dominant_features = (
            get_dominant_domains(
                row
            )
        )

        dominant_labels = [
            FEATURE_LABELS[feature]
            for feature in dominant_features
        ]

        critical_access_domains = (
            get_critical_access_domains(
                row
            )
        )

        critical_access_flag = bool(
            critical_access_domains
        )

        individual_recommendations = [
            FEATURE_RECOMMENDATIONS[
                feature
            ]
            for feature in dominant_features
        ]

        is_dbscan_unique_case = bool(
            dbscan_labels[
                row_index
            ]
            == -1
        )

        silhouette_value = float(
            individual_silhouettes[
                row_index
            ]
        )

        review_reasons = []

        if priority_level == "high":
            review_reasons.append(
                "prioritas kebutuhan tinggi"
            )

        if critical_access_flag:
            review_reasons.append(
                "terdapat skor kritis pada domain "
                "akses utama: "
                + ", ".join(
                    critical_access_domains
                )
            )

        if is_dbscan_unique_case:
            review_reasons.append(
                "terdeteksi sebagai kasus unik "
                "oleh DBSCAN"
            )

        if silhouette_value < 0.25:
            review_reasons.append(
                "kesesuaian cluster relatif rendah"
            )

        needs_human_review = bool(
            review_reasons
        )

        output_row: dict[str, Any] = {
            "student_code": (
                row["student_code"]
            ),
            "initials": row["initials"],
            "grade_level": (
                row["grade_level"]
            ),
            "class_name": (
                row["class_name"]
            ),
            "cluster_id": cluster_id,
            "cluster_name": (
                cluster_information[
                    "cluster_name"
                ]
            ),
            "cluster_description": (
                cluster_information[
                    "description"
                ]
            ),
            "dominant_need_1": (
                dominant_labels[0]
                if len(dominant_labels) >= 1
                else None
            ),
            "dominant_need_2": (
                dominant_labels[1]
                if len(dominant_labels) >= 2
                else None
            ),
            "dominant_need_3": (
                dominant_labels[2]
                if len(dominant_labels) >= 3
                else None
            ),
            "maximum_need_score": int(
                np.max(scores)
            ),
            "average_need_score": (
                average_need_score
            ),
            "critical_domain_count": (
                critical_domain_count
            ),
            "high_domain_count": (
                high_domain_count
            ),
            "priority_level": (
                priority_level
            ),
            "priority_action": (
                get_priority_action(
                    priority_level
                )
            ),
            "critical_access_flag": (
                critical_access_flag
            ),
            "critical_access_domains": (
                " | ".join(
                    critical_access_domains
                )
                if critical_access_domains
                else None
            ),
            "cluster_recommendations": (
                " | ".join(
                    cluster_information[
                        "recommendations"
                    ]
                )
            ),
            "individual_recommendations": (
                " | ".join(
                    individual_recommendations
                )
            ),
            "material_preference": (
                row["material_preference"]
            ),
            "assistive_tool": (
                row["assistive_tool"]
            ),
            "individual_silhouette": (
                silhouette_value
            ),
            "mean_distance_to_cluster": (
                calculate_mean_cluster_distance(
                    row_index=row_index,
                    labels=labels,
                    distance_matrix=(
                        distance_matrix
                    ),
                )
            ),
            "dbscan_unique_case": (
                is_dbscan_unique_case
            ),
            "needs_human_review": (
                needs_human_review
            ),
            "human_review_reason": (
                "; ".join(review_reasons)
                if review_reasons
                else None
            ),
        }

        for score_column in SCORE_COLUMNS:
            output_row[
                score_column
            ] = int(
                row[score_column]
            )

        output_rows.append(
            output_row
        )

    return pd.DataFrame(
        output_rows
    )


# CLUSTER CATALOG OUTPUT

def create_cluster_catalog_dataframe(
    recommendations: pd.DataFrame,
) -> pd.DataFrame:
    catalog_rows = []

    for cluster_id, information in (
        CLUSTER_CATALOG.items()
    ):
        cluster_students = (
            recommendations.loc[
                recommendations[
                    "cluster_id"
                ]
                == cluster_id
            ]
        )

        catalog_rows.append(
            {
                "cluster_id": cluster_id,
                "cluster_name": (
                    information[
                        "cluster_name"
                    ]
                ),
                "dominant_need": (
                    information[
                        "dominant_need"
                    ]
                ),
                "description": (
                    information[
                        "description"
                    ]
                ),
                "cluster_size": int(
                    len(cluster_students)
                ),
                "high_priority_count": int(
                    (
                        cluster_students[
                            "priority_level"
                        ]
                        == "high"
                    ).sum()
                ),
                "medium_priority_count": int(
                    (
                        cluster_students[
                            "priority_level"
                        ]
                        == "medium"
                    ).sum()
                ),
                "low_priority_count": int(
                    (
                        cluster_students[
                            "priority_level"
                        ]
                        == "low"
                    ).sum()
                ),
                "recommendations": (
                    " | ".join(
                        information[
                            "recommendations"
                        ]
                    )
                ),
            }
        )

    return pd.DataFrame(
        catalog_rows
    )


# SAVE OUTPUTS

def save_outputs(
    recommendations: pd.DataFrame,
    catalog_dataframe: pd.DataFrame,
    medoids: pd.DataFrame,
) -> None:
    RESULTS_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    recommendations.to_csv(
        STUDENT_RECOMMENDATIONS_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    catalog_dataframe.to_csv(
        CLUSTER_CATALOG_CSV_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    medoids.to_csv(
        CLUSTER_MEDOIDS_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    catalog_json = {
        str(cluster_id): information
        for cluster_id, information
        in CLUSTER_CATALOG.items()
    }

    with CLUSTER_CATALOG_JSON_PATH.open(
        "w",
        encoding="utf-8",
    ) as catalog_file:
        json.dump(
            catalog_json,
            catalog_file,
            ensure_ascii=False,
            indent=2,
        )

    priority_counts = (
        recommendations[
            "priority_level"
        ]
        .value_counts()
        .to_dict()
    )

    cluster_counts = (
        recommendations[
            "cluster_id"
        ]
        .value_counts()
        .sort_index()
        .to_dict()
    )

    summary = {
        "total_students": int(
            len(recommendations)
        ),
        "cluster_count": int(
            recommendations[
                "cluster_id"
            ].nunique()
        ),
        "cluster_sizes": {
            str(cluster_id): int(count)
            for cluster_id, count
            in cluster_counts.items()
        },
        "priority_counts": {
            "high": int(
                priority_counts.get(
                    "high",
                    0,
                )
            ),
            "medium": int(
                priority_counts.get(
                    "medium",
                    0,
                )
            ),
            "low": int(
                priority_counts.get(
                    "low",
                    0,
                )
            ),
        },
        "critical_access_review_count": int(
            recommendations[
                "critical_access_flag"
            ].sum()
        ),
        "dbscan_unique_case_count": int(
            recommendations[
                "dbscan_unique_case"
            ].sum()
        ),
        "human_review_count": int(
            recommendations[
                "needs_human_review"
            ].sum()
        ),
        "priority_rule": {
            "selected_rule": "balanced",
            "high": (
                "Minimal tiga domain berskor 3, "
                "atau minimal lima domain berskor "
                "2-3, atau rata-rata skor minimal "
                "2.00."
            ),
            "medium": (
                "Minimal satu domain berskor 3, "
                "atau minimal tiga domain berskor "
                "2-3, atau rata-rata skor minimal "
                "1.25."
            ),
            "low": (
                "Tidak memenuhi kriteria "
                "prioritas tinggi atau sedang."
            ),
        },
        "disclaimer": (
            "Hasil cluster dan prioritas merupakan "
            "dukungan pengambilan keputusan, bukan "
            "diagnosis. Seluruh rekomendasi perlu "
            "divalidasi oleh guru atau tenaga "
            "pendukung yang berwenang."
        ),
    }

    with RECOMMENDATION_SUMMARY_PATH.open(
        "w",
        encoding="utf-8",
    ) as summary_file:
        json.dump(
            summary,
            summary_file,
            ensure_ascii=False,
            indent=2,
        )


# MAIN PROGRAM

def main() -> None:
    validate_files()

    (
        assignments,
        distance_matrix,
    ) = load_data()

    recommendations = (
        create_student_recommendations(
            assignments=assignments,
            distance_matrix=distance_matrix,
        )
    )

    catalog_dataframe = (
        create_cluster_catalog_dataframe(
            recommendations
        )
    )

    medoids = create_cluster_medoids(
        assignments=assignments,
        distance_matrix=distance_matrix,
    )

    save_outputs(
        recommendations=recommendations,
        catalog_dataframe=(
            catalog_dataframe
        ),
        medoids=medoids,
    )

    priority_counts = (
        recommendations[
            "priority_level"
        ].value_counts()
    )

    print()
    print(
        "PROFIL DAN REKOMENDASI BERHASIL DIBUAT"
    )
    print("-" * 60)
    print(
        f"Jumlah siswa             : "
        f"{len(recommendations)}"
    )
    print(
        f"Jumlah cluster           : "
        f"{recommendations['cluster_id'].nunique()}"
    )
    print(
        f"Prioritas tinggi         : "
        f"{priority_counts.get('high', 0)}"
    )
    print(
        f"Prioritas sedang         : "
        f"{priority_counts.get('medium', 0)}"
    )
    print(
        f"Prioritas rendah         : "
        f"{priority_counts.get('low', 0)}"
    )
    print(
        f"Akses kritis             : "
        f"{recommendations['critical_access_flag'].sum()}"
    )
    print(
        f"Kasus unik DBSCAN        : "
        f"{recommendations['dbscan_unique_case'].sum()}"
    )
    print(
        f"Perlu validasi manusia   : "
        f"{recommendations['needs_human_review'].sum()}"
    )
    print(
        f"Rekomendasi siswa        : "
        f"{STUDENT_RECOMMENDATIONS_PATH}"
    )
    print(
        f"Katalog cluster          : "
        f"{CLUSTER_CATALOG_CSV_PATH}"
    )
    print(
        f"Medoid cluster           : "
        f"{CLUSTER_MEDOIDS_PATH}"
    )
    print("-" * 60)


if __name__ == "__main__":
    main()