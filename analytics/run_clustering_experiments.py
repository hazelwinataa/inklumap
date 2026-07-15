# STANDARD LIBRARY

import json
from pathlib import Path
from typing import Any


# THIRD-PARTY LIBRARIES

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import (
    AgglomerativeClustering,
    DBSCAN,
    KMeans,
)
from sklearn.manifold import MDS
from sklearn.metrics import (
    davies_bouldin_score,
    silhouette_score,
)
from sklearn.preprocessing import StandardScaler


# CONFIGURATION

RANDOM_STATE = 42

K_VALUES = range(2, 7)

HIERARCHICAL_LINKAGES = [
    "average",
    "complete",
]

DBSCAN_MIN_SAMPLES = [
    3,
    4,
    5,
    6,
    8,
]


# FILE PATHS

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SOURCE_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "modeling_complete_students.csv"
)

ENCODED_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "modeling_features_encoded.csv"
)

RESULTS_DIRECTORY = (
    PROJECT_ROOT
    / "analytics"
    / "results"
)

MODELS_DIRECTORY = (
    PROJECT_ROOT
    / "analytics"
    / "models"
)

REPORTS_DIRECTORY = (
    PROJECT_ROOT
    / "reports"
    / "analytics"
)


# FEATURE CONFIGURATION

ORDINAL_FEATURES = [
    "visual_score",
    "hearing_score",
    "communication_score",
    "instruction_score",
    "attention_score",
    "mobility_score",
    "assistance_score",
    "evaluation_adjustment_score",
]

CATEGORICAL_FEATURES = [
    "material_preference",
    "assistive_tool",
]

FEATURE_LABELS = {
    "visual_score": "Akses Visual",
    "hearing_score": "Pendengaran",
    "communication_score": "Komunikasi",
    "instruction_score": (
        "Pemahaman Instruksi"
    ),
    "attention_score": (
        "Perhatian & Konsentrasi"
    ),
    "mobility_score": "Mobilitas",
    "assistance_score": "Pendampingan",
    "evaluation_adjustment_score": (
        "Penyesuaian Evaluasi"
    ),
}


# DIRECTORY PREPARATION

def ensure_directories() -> None:
    directories = [
        RESULTS_DIRECTORY,
        MODELS_DIRECTORY,
        REPORTS_DIRECTORY,
    ]

    for directory in directories:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )


# DATA LOADING

def load_datasets(
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not SOURCE_DATA_PATH.exists():
        raise FileNotFoundError(
            "Dataset sumber tidak ditemukan: "
            f"{SOURCE_DATA_PATH}"
        )

    if not ENCODED_DATA_PATH.exists():
        raise FileNotFoundError(
            "Dataset encoded tidak ditemukan: "
            f"{ENCODED_DATA_PATH}"
        )

    source_dataframe = pd.read_csv(
        SOURCE_DATA_PATH,
        encoding="utf-8-sig",
    )

    encoded_dataframe = pd.read_csv(
        ENCODED_DATA_PATH,
        encoding="utf-8-sig",
    )

    required_source_columns = {
        "student_code",
        *ORDINAL_FEATURES,
        *CATEGORICAL_FEATURES,
    }

    missing_source_columns = (
        required_source_columns
        - set(source_dataframe.columns)
    )

    if missing_source_columns:
        raise ValueError(
            "Kolom dataset sumber tidak lengkap: "
            + ", ".join(
                sorted(
                    missing_source_columns
                )
            )
        )

    if (
        "student_code"
        not in encoded_dataframe.columns
    ):
        raise ValueError(
            "Kolom student_code tidak ditemukan "
            "pada dataset encoded."
        )

    source_dataframe["student_code"] = (
        source_dataframe["student_code"]
        .astype(str)
        .str.strip()
    )

    encoded_dataframe["student_code"] = (
        encoded_dataframe["student_code"]
        .astype(str)
        .str.strip()
    )

    if source_dataframe[
        "student_code"
    ].duplicated().any():
        raise ValueError(
            "Dataset sumber memiliki "
            "student_code duplikat."
        )

    if encoded_dataframe[
        "student_code"
    ].duplicated().any():
        raise ValueError(
            "Dataset encoded memiliki "
            "student_code duplikat."
        )

    source_codes = set(
        source_dataframe["student_code"]
    )

    encoded_codes = set(
        encoded_dataframe["student_code"]
    )

    if source_codes != encoded_codes:
        raise ValueError(
            "Daftar student_code pada kedua "
            "dataset tidak sama."
        )

    source_dataframe = (
        source_dataframe
        .sort_values("student_code")
        .reset_index(drop=True)
    )

    encoded_dataframe = (
        encoded_dataframe
        .sort_values("student_code")
        .reset_index(drop=True)
    )

    if not source_dataframe[
        "student_code"
    ].equals(
        encoded_dataframe["student_code"]
    ):
        raise ValueError(
            "Urutan student_code pada kedua "
            "dataset tidak sama."
        )

    encoded_feature_columns = [
        column
        for column in encoded_dataframe.columns
        if column != "student_code"
    ]

    if encoded_dataframe[
        encoded_feature_columns
    ].isna().any().any():
        raise ValueError(
            "Dataset encoded masih memiliki "
            "missing value."
        )

    source_feature_columns = [
        *ORDINAL_FEATURES,
        *CATEGORICAL_FEATURES,
    ]

    if source_dataframe[
        source_feature_columns
    ].isna().any().any():
        raise ValueError(
            "Dataset sumber modeling masih "
            "memiliki missing value."
        )

    return (
        source_dataframe,
        encoded_dataframe,
    )


# HELPER FUNCTIONS

def get_cluster_size_statistics(
    labels: np.ndarray,
    ignore_noise: bool = False,
) -> tuple[int, int]:
    label_series = pd.Series(
        labels
    )

    if ignore_noise:
        label_series = label_series[
            label_series != -1
        ]

    cluster_counts = (
        label_series.value_counts()
    )

    if cluster_counts.empty:
        return 0, 0

    return (
        int(cluster_counts.min()),
        int(cluster_counts.max()),
    )


def convert_float(
    value: Any,
) -> float | None:
    if value is None:
        return None

    if pd.isna(value):
        return None

    return float(value)


# GOWER DISTANCE

def calculate_gower_distance(
    dataframe: pd.DataFrame,
) -> np.ndarray:
    row_count = len(dataframe)

    distance_matrix = np.zeros(
        shape=(
            row_count,
            row_count,
        ),
        dtype=float,
    )

    feature_count = (
        len(ORDINAL_FEATURES)
        + len(CATEGORICAL_FEATURES)
    )

    for column in ORDINAL_FEATURES:
        values = pd.to_numeric(
            dataframe[column],
            errors="raise",
        ).to_numpy(
            dtype=float
        )

        value_range = (
            values.max()
            - values.min()
        )

        if value_range == 0:
            feature_distance = np.zeros(
                shape=(
                    row_count,
                    row_count,
                ),
                dtype=float,
            )

        else:
            feature_distance = (
                np.abs(
                    values[:, None]
                    - values[None, :]
                )
                / value_range
            )

        distance_matrix += (
            feature_distance
        )

    for column in CATEGORICAL_FEATURES:
        values = (
            dataframe[column]
            .astype(str)
            .str.strip()
            .to_numpy()
        )

        feature_distance = (
            values[:, None]
            != values[None, :]
        ).astype(float)

        distance_matrix += (
            feature_distance
        )

    distance_matrix = (
        distance_matrix
        / feature_count
    )

    np.fill_diagonal(
        distance_matrix,
        0.0,
    )

    if not np.allclose(
        distance_matrix,
        distance_matrix.T,
    ):
        raise ValueError(
            "Matriks jarak Gower tidak simetris."
        )

    if (
        distance_matrix.min() < 0
        or distance_matrix.max() > 1
    ):
        raise ValueError(
            "Nilai jarak Gower harus berada "
            "antara 0 dan 1."
        )

    return distance_matrix


# K-MEANS BASELINE

def run_kmeans_experiments(
    encoded_dataframe: pd.DataFrame,
) -> tuple[
    pd.DataFrame,
    KMeans,
    StandardScaler,
]:
    feature_columns = [
        column
        for column
        in encoded_dataframe.columns
        if column != "student_code"
    ]

    feature_matrix = (
        encoded_dataframe[
            feature_columns
        ].to_numpy(
            dtype=float
        )
    )

    scaler = StandardScaler()

    scaled_features = (
        scaler.fit_transform(
            feature_matrix
        )
    )

    experiment_rows = []
    trained_models = {}

    for cluster_count in K_VALUES:
        model = KMeans(
            n_clusters=cluster_count,
            random_state=RANDOM_STATE,
            n_init=20,
        )

        labels = model.fit_predict(
            scaled_features
        )

        (
            minimum_cluster_size,
            maximum_cluster_size,
        ) = get_cluster_size_statistics(
            labels
        )

        experiment_rows.append(
            {
                "method": "kmeans",
                "configuration": (
                    f"k={cluster_count}"
                ),
                "n_clusters": (
                    cluster_count
                ),
                "silhouette_score": (
                    silhouette_score(
                        scaled_features,
                        labels,
                        metric="euclidean",
                    )
                ),
                "davies_bouldin_index": (
                    davies_bouldin_score(
                        scaled_features,
                        labels,
                    )
                ),
                "inertia": model.inertia_,
                "noise_count": 0,
                "noise_ratio": 0.0,
                "minimum_cluster_size": (
                    minimum_cluster_size
                ),
                "maximum_cluster_size": (
                    maximum_cluster_size
                ),
            }
        )

        trained_models[
            cluster_count
        ] = model

    results = pd.DataFrame(
        experiment_rows
    )

    results = results.sort_values(
        by=[
            "silhouette_score",
            "davies_bouldin_index",
        ],
        ascending=[
            False,
            True,
        ],
    ).reset_index(
        drop=True
    )

    best_cluster_count = int(
        results.iloc[0][
            "n_clusters"
        ]
    )

    best_model = trained_models[
        best_cluster_count
    ]

    return (
        results,
        best_model,
        scaler,
    )


# HIERARCHICAL CLUSTERING

def run_hierarchical_experiments(
    distance_matrix: np.ndarray,
) -> tuple[
    pd.DataFrame,
    AgglomerativeClustering,
    np.ndarray,
]:
    experiment_rows = []

    trained_models = {}

    labels_by_configuration = {}

    for linkage in HIERARCHICAL_LINKAGES:
        for cluster_count in K_VALUES:
            model = (
                AgglomerativeClustering(
                    n_clusters=(
                        cluster_count
                    ),
                    metric="precomputed",
                    linkage=linkage,
                )
            )

            labels = model.fit_predict(
                distance_matrix
            )

            (
                minimum_cluster_size,
                maximum_cluster_size,
            ) = (
                get_cluster_size_statistics(
                    labels
                )
            )

            silhouette_value = (
                silhouette_score(
                    distance_matrix,
                    labels,
                    metric="precomputed",
                )
            )

            configuration_key = (
                linkage,
                cluster_count,
            )

            experiment_rows.append(
                {
                    "method": (
                        "hierarchical_gower"
                    ),
                    "configuration": (
                        f"linkage={linkage};"
                        f"k={cluster_count}"
                    ),
                    "linkage": linkage,
                    "n_clusters": (
                        cluster_count
                    ),
                    "silhouette_score": (
                        silhouette_value
                    ),
                    "davies_bouldin_index": (
                        np.nan
                    ),
                    "inertia": np.nan,
                    "noise_count": 0,
                    "noise_ratio": 0.0,
                    "minimum_cluster_size": (
                        minimum_cluster_size
                    ),
                    "maximum_cluster_size": (
                        maximum_cluster_size
                    ),
                }
            )

            trained_models[
                configuration_key
            ] = model

            labels_by_configuration[
                configuration_key
            ] = labels

    results = pd.DataFrame(
        experiment_rows
    )

    results = results.sort_values(
        by=[
            "silhouette_score",
            "minimum_cluster_size",
        ],
        ascending=[
            False,
            False,
        ],
    ).reset_index(
        drop=True
    )

    best_linkage = str(
        results.iloc[0]["linkage"]
    )

    best_cluster_count = int(
        results.iloc[0][
            "n_clusters"
        ]
    )

    best_key = (
        best_linkage,
        best_cluster_count,
    )

    return (
        results,
        trained_models[best_key],
        labels_by_configuration[
            best_key
        ],
    )


# DBSCAN

def create_dbscan_eps_values(
    distance_matrix: np.ndarray,
) -> np.ndarray:
    upper_triangle = (
        distance_matrix[
            np.triu_indices_from(
                distance_matrix,
                k=1,
            )
        ]
    )

    positive_distances = (
        upper_triangle[
            upper_triangle > 0
        ]
    )

    if positive_distances.size == 0:
        raise ValueError(
            "Seluruh jarak Gower bernilai nol."
        )

    quantiles = np.arange(
        0.05,
        0.51,
        0.05,
    )

    eps_values = np.quantile(
        positive_distances,
        quantiles,
    )

    return np.unique(
        np.round(
            eps_values,
            4,
        )
    )


def run_dbscan_experiments(
    distance_matrix: np.ndarray,
) -> pd.DataFrame:
    experiment_rows = []

    eps_values = (
        create_dbscan_eps_values(
            distance_matrix
        )
    )

    total_rows = len(
        distance_matrix
    )

    for eps_value in eps_values:
        for min_samples in (
            DBSCAN_MIN_SAMPLES
        ):
            model = DBSCAN(
                eps=float(eps_value),
                min_samples=min_samples,
                metric="precomputed",
            )

            labels = model.fit_predict(
                distance_matrix
            )

            non_noise_mask = (
                labels != -1
            )

            cluster_labels = set(
                labels[
                    non_noise_mask
                ]
            )

            cluster_count = len(
                cluster_labels
            )

            noise_count = int(
                np.sum(
                    ~non_noise_mask
                )
            )

            silhouette_value = (
                np.nan
            )

            if (
                cluster_count >= 2
                and non_noise_mask.sum()
                > cluster_count
            ):
                filtered_distances = (
                    distance_matrix[
                        np.ix_(
                            non_noise_mask,
                            non_noise_mask,
                        )
                    ]
                )

                filtered_labels = (
                    labels[
                        non_noise_mask
                    ]
                )

                silhouette_value = (
                    silhouette_score(
                        filtered_distances,
                        filtered_labels,
                        metric="precomputed",
                    )
                )

            (
                minimum_cluster_size,
                maximum_cluster_size,
            ) = (
                get_cluster_size_statistics(
                    labels,
                    ignore_noise=True,
                )
            )

            experiment_rows.append(
                {
                    "method": (
                        "dbscan_gower"
                    ),
                    "configuration": (
                        f"eps={eps_value:.4f};"
                        f"min_samples="
                        f"{min_samples}"
                    ),
                    "eps": float(
                        eps_value
                    ),
                    "min_samples": (
                        min_samples
                    ),
                    "n_clusters": (
                        cluster_count
                    ),
                    "silhouette_score": (
                        silhouette_value
                    ),
                    "davies_bouldin_index": (
                        np.nan
                    ),
                    "inertia": np.nan,
                    "noise_count": (
                        noise_count
                    ),
                    "noise_ratio": (
                        noise_count
                        / total_rows
                    ),
                    "minimum_cluster_size": (
                        minimum_cluster_size
                    ),
                    "maximum_cluster_size": (
                        maximum_cluster_size
                    ),
                }
            )

    results = pd.DataFrame(
        experiment_rows
    )

    results = results.sort_values(
        by=[
            "silhouette_score",
            "noise_ratio",
        ],
        ascending=[
            False,
            True,
        ],
        na_position="last",
    ).reset_index(
        drop=True
    )

    return results


# CLUSTER ASSIGNMENT

def create_cluster_assignments(
    source_dataframe: pd.DataFrame,
    labels: np.ndarray,
    linkage: str,
) -> pd.DataFrame:
    assignments = (
        source_dataframe.copy()
    )

    assignments.insert(
        1,
        "cluster_id",
        labels.astype(int) + 1,
    )

    assignments.insert(
        2,
        "model_name",
        "hierarchical_gower",
    )

    assignments.insert(
        3,
        "linkage",
        linkage,
    )

    return assignments


# CLUSTER PROFILE

def create_cluster_profiles(
    assignments: pd.DataFrame,
) -> pd.DataFrame:
    profile_rows = []

    grouped_clusters = (
        assignments.groupby(
            "cluster_id"
        )
    )

    for (
        cluster_id,
        cluster_dataframe,
    ) in grouped_clusters:
        score_means = (
            cluster_dataframe[
                ORDINAL_FEATURES
            ].mean()
        )

        dominant_feature = str(
            score_means.idxmax()
        )

        material_mode = (
            cluster_dataframe[
                "material_preference"
            ]
            .mode()
            .iloc[0]
        )

        tool_mode = (
            cluster_dataframe[
                "assistive_tool"
            ]
            .mode()
            .iloc[0]
        )

        profile_row = {
            "cluster_id": int(
                cluster_id
            ),
            "cluster_size": len(
                cluster_dataframe
            ),
            "dominant_need_feature": (
                dominant_feature
            ),
            "dominant_need_label": (
                FEATURE_LABELS[
                    dominant_feature
                ]
            ),
            "dominant_need_mean": (
                score_means[
                    dominant_feature
                ]
            ),
            "most_common_material_preference": (
                material_mode
            ),
            "most_common_assistive_tool": (
                tool_mode
            ),
        }

        for feature in ORDINAL_FEATURES:
            profile_row[
                f"mean_{feature}"
            ] = score_means[
                feature
            ]

        profile_rows.append(
            profile_row
        )

    return (
        pd.DataFrame(
            profile_rows
        )
        .sort_values(
            "cluster_id"
        )
        .reset_index(
            drop=True
        )
    )


# MDS VISUALIZATION

def create_mds_embedding(
    distance_matrix: np.ndarray,
) -> np.ndarray:
    mds_model = MDS(
        n_components=2,
        metric_mds=True,
        metric="precomputed",
        init="classical_mds",
        n_init=1,
        max_iter=500,
        normalized_stress="auto",
        random_state=RANDOM_STATE,
    )

    embedding = (
        mds_model.fit_transform(
            distance_matrix
        )
    )

    return embedding


# PLOTS

def save_plots(
    kmeans_results: pd.DataFrame,
    hierarchical_results: pd.DataFrame,
    assignments: pd.DataFrame,
    embedding: np.ndarray,
) -> None:
    kmeans_sorted = (
        kmeans_results
        .sort_values(
            "n_clusters"
        )
    )

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        kmeans_sorted[
            "n_clusters"
        ],
        kmeans_sorted[
            "silhouette_score"
        ],
        marker="o",
    )

    plt.xlabel(
        "Jumlah Cluster"
    )

    plt.ylabel(
        "Silhouette Score"
    )

    plt.title(
        "K-Means: Silhouette Score"
    )

    plt.tight_layout()

    plt.savefig(
        REPORTS_DIRECTORY
        / "kmeans_silhouette.png",
        dpi=200,
    )

    plt.close()

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        kmeans_sorted[
            "n_clusters"
        ],
        kmeans_sorted[
            "davies_bouldin_index"
        ],
        marker="o",
    )

    plt.xlabel(
        "Jumlah Cluster"
    )

    plt.ylabel(
        "Davies-Bouldin Index"
    )

    plt.title(
        "K-Means: Davies-Bouldin Index"
    )

    plt.tight_layout()

    plt.savefig(
        REPORTS_DIRECTORY
        / "kmeans_davies_bouldin.png",
        dpi=200,
    )

    plt.close()

    plt.figure(
        figsize=(8, 5)
    )

    for (
        linkage,
        linkage_results,
    ) in hierarchical_results.groupby(
        "linkage"
    ):
        linkage_results = (
            linkage_results.sort_values(
                "n_clusters"
            )
        )

        plt.plot(
            linkage_results[
                "n_clusters"
            ],
            linkage_results[
                "silhouette_score"
            ],
            marker="o",
            label=str(linkage),
        )

    plt.xlabel(
        "Jumlah Cluster"
    )

    plt.ylabel(
        "Silhouette Score"
    )

    plt.title(
        "Hierarchical Gower: "
        "Silhouette Score"
    )

    plt.legend(
        title="Linkage"
    )

    plt.tight_layout()

    plt.savefig(
        REPORTS_DIRECTORY
        / "hierarchical_gower_silhouette.png",
        dpi=200,
    )

    plt.close()

    plt.figure(
        figsize=(8, 6)
    )

    cluster_ids = sorted(
        assignments[
            "cluster_id"
        ].unique()
    )

    for cluster_id in cluster_ids:
        cluster_mask = (
            assignments[
                "cluster_id"
            ]
            == cluster_id
        ).to_numpy()

        plt.scatter(
            embedding[
                cluster_mask,
                0,
            ],
            embedding[
                cluster_mask,
                1,
            ],
            label=(
                f"Cluster "
                f"{cluster_id}"
            ),
            alpha=0.8,
        )

    plt.xlabel(
        "MDS Dimension 1"
    )

    plt.ylabel(
        "MDS Dimension 2"
    )

    plt.title(
        "Visualisasi Cluster Utama "
        "dengan MDS"
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        REPORTS_DIRECTORY
        / "hierarchical_gower_mds.png",
        dpi=200,
    )

    plt.close()

    cluster_sizes = (
        assignments[
            "cluster_id"
        ]
        .value_counts()
        .sort_index()
    )

    plt.figure(
        figsize=(8, 5)
    )

    plt.bar(
        cluster_sizes.index.astype(
            str
        ),
        cluster_sizes.values,
    )

    plt.xlabel(
        "Cluster"
    )

    plt.ylabel(
        "Jumlah Siswa"
    )

    plt.title(
        "Distribusi Anggota Cluster"
    )

    plt.tight_layout()

    plt.savefig(
        REPORTS_DIRECTORY
        / "hierarchical_gower_cluster_sizes.png",
        dpi=200,
    )

    plt.close()


# SUMMARY

def create_experiment_summary(
    row_count: int,
    encoded_feature_count: int,
    kmeans_results: pd.DataFrame,
    hierarchical_results: pd.DataFrame,
    dbscan_results: pd.DataFrame,
) -> dict[str, Any]:
    best_kmeans = (
        kmeans_results.iloc[0]
    )

    best_hierarchical = (
        hierarchical_results.iloc[0]
    )

    valid_dbscan_results = (
        dbscan_results.dropna(
            subset=[
                "silhouette_score"
            ]
        )
    )

    best_dbscan = None

    if not valid_dbscan_results.empty:
        best_dbscan_row = (
            valid_dbscan_results.iloc[0]
        )

        best_dbscan = {
            "configuration": str(
                best_dbscan_row[
                    "configuration"
                ]
            ),
            "n_clusters": int(
                best_dbscan_row[
                    "n_clusters"
                ]
            ),
            "silhouette_score": (
                convert_float(
                    best_dbscan_row[
                        "silhouette_score"
                    ]
                )
            ),
            "noise_count": int(
                best_dbscan_row[
                    "noise_count"
                ]
            ),
            "noise_ratio": (
                convert_float(
                    best_dbscan_row[
                        "noise_ratio"
                    ]
                )
            ),
        }

    return {
        "dataset": {
            "row_count": row_count,
            "kmeans_encoded_feature_count": (
                encoded_feature_count
            ),
            "gower_variable_count": (
                len(ORDINAL_FEATURES)
                + len(
                    CATEGORICAL_FEATURES
                )
            ),
        },
        "best_kmeans_baseline": {
            "configuration": str(
                best_kmeans[
                    "configuration"
                ]
            ),
            "n_clusters": int(
                best_kmeans[
                    "n_clusters"
                ]
            ),
            "silhouette_score": (
                convert_float(
                    best_kmeans[
                        "silhouette_score"
                    ]
                )
            ),
            "davies_bouldin_index": (
                convert_float(
                    best_kmeans[
                        "davies_bouldin_index"
                    ]
                )
            ),
            "inertia": (
                convert_float(
                    best_kmeans[
                        "inertia"
                    ]
                )
            ),
        },
        "best_hierarchical_gower": {
            "configuration": str(
                best_hierarchical[
                    "configuration"
                ]
            ),
            "linkage": str(
                best_hierarchical[
                    "linkage"
                ]
            ),
            "n_clusters": int(
                best_hierarchical[
                    "n_clusters"
                ]
            ),
            "silhouette_score": (
                convert_float(
                    best_hierarchical[
                        "silhouette_score"
                    ]
                )
            ),
            "minimum_cluster_size": int(
                best_hierarchical[
                    "minimum_cluster_size"
                ]
            ),
            "maximum_cluster_size": int(
                best_hierarchical[
                    "maximum_cluster_size"
                ]
            ),
        },
        "best_dbscan_gower": (
            best_dbscan
        ),
        "primary_model": {
            "method": (
                "hierarchical_gower"
            ),
            "selection_basis": (
                "Hierarchical Gower dipakai "
                "sebagai model utama karena "
                "data terdiri dari fitur ordinal "
                "dan kategorikal. Jumlah cluster "
                "dan linkage terbaik dipilih "
                "berdasarkan silhouette tertinggi "
                "di dalam eksperimen hierarchical."
            ),
        },
        "comparison_note": (
            "Silhouette K-Means dan "
            "Hierarchical Gower tidak digunakan "
            "sebagai satu-satunya dasar pemilihan "
            "lintas metode karena menggunakan "
            "ruang jarak yang berbeda."
        ),
    }


# SAVE OUTPUTS

def save_outputs(
    source_dataframe: pd.DataFrame,
    encoded_dataframe: pd.DataFrame,
    distance_matrix: np.ndarray,
    kmeans_results: pd.DataFrame,
    hierarchical_results: pd.DataFrame,
    dbscan_results: pd.DataFrame,
    best_kmeans_model: KMeans,
    scaler: StandardScaler,
    best_hierarchical_model: (
        AgglomerativeClustering
    ),
    hierarchical_labels: np.ndarray,
) -> None:
    best_hierarchical_row = (
        hierarchical_results.iloc[0]
    )

    best_linkage = str(
        best_hierarchical_row[
            "linkage"
        ]
    )

    assignments = (
        create_cluster_assignments(
            source_dataframe,
            hierarchical_labels,
            best_linkage,
        )
    )

    profiles = (
        create_cluster_profiles(
            assignments
        )
    )

    embedding = (
        create_mds_embedding(
            distance_matrix
        )
    )

    embedding_dataframe = pd.DataFrame(
        {
            "student_code": (
                source_dataframe[
                    "student_code"
                ]
            ),
            "mds_dimension_1": (
                embedding[:, 0]
            ),
            "mds_dimension_2": (
                embedding[:, 1]
            ),
            "cluster_id": (
                assignments[
                    "cluster_id"
                ]
            ),
        }
    )

    all_metrics = pd.concat(
        [
            kmeans_results,
            hierarchical_results,
            dbscan_results,
        ],
        ignore_index=True,
        sort=False,
    )

    kmeans_results.to_csv(
        RESULTS_DIRECTORY
        / "kmeans_candidates.csv",
        index=False,
        encoding="utf-8-sig",
    )

    hierarchical_results.to_csv(
        RESULTS_DIRECTORY
        / "hierarchical_gower_candidates.csv",
        index=False,
        encoding="utf-8-sig",
    )

    dbscan_results.to_csv(
        RESULTS_DIRECTORY
        / "dbscan_gower_candidates.csv",
        index=False,
        encoding="utf-8-sig",
    )

    all_metrics.to_csv(
        RESULTS_DIRECTORY
        / "all_clustering_metrics.csv",
        index=False,
        encoding="utf-8-sig",
    )

    assignments.to_csv(
        RESULTS_DIRECTORY
        / "hierarchical_gower_assignments.csv",
        index=False,
        encoding="utf-8-sig",
    )

    profiles.to_csv(
        RESULTS_DIRECTORY
        / "hierarchical_gower_profiles.csv",
        index=False,
        encoding="utf-8-sig",
    )

    embedding_dataframe.to_csv(
        RESULTS_DIRECTORY
        / "hierarchical_gower_mds.csv",
        index=False,
        encoding="utf-8-sig",
    )

    np.save(
        MODELS_DIRECTORY
        / "gower_distance_matrix.npy",
        distance_matrix,
    )

    joblib.dump(
        scaler,
        MODELS_DIRECTORY
        / "kmeans_standard_scaler.joblib",
    )

    joblib.dump(
        best_kmeans_model,
        MODELS_DIRECTORY
        / "best_kmeans_model.joblib",
    )

    joblib.dump(
        best_hierarchical_model,
        MODELS_DIRECTORY
        / "best_hierarchical_gower_model.joblib",
    )

    summary = (
        create_experiment_summary(
            row_count=len(
                source_dataframe
            ),
            encoded_feature_count=(
                len(
                    encoded_dataframe.columns
                )
                - 1
            ),
            kmeans_results=(
                kmeans_results
            ),
            hierarchical_results=(
                hierarchical_results
            ),
            dbscan_results=(
                dbscan_results
            ),
        )
    )

    summary_path = (
        RESULTS_DIRECTORY
        / "clustering_experiment_summary.json"
    )

    with summary_path.open(
        "w",
        encoding="utf-8",
    ) as summary_file:
        json.dump(
            summary,
            summary_file,
            ensure_ascii=False,
            indent=2,
        )

    save_plots(
        kmeans_results=(
            kmeans_results
        ),
        hierarchical_results=(
            hierarchical_results
        ),
        assignments=assignments,
        embedding=embedding,
    )


# MAIN PROGRAM

def main() -> None:
    ensure_directories()

    (
        source_dataframe,
        encoded_dataframe,
    ) = load_datasets()

    print()
    print(
        "MENJALANKAN EKSPERIMEN CLUSTERING"
    )
    print("-" * 58)

    print(
        f"Jumlah siswa       : "
        f"{len(source_dataframe)}"
    )

    print(
        f"Fitur K-Means      : "
        f"{len(encoded_dataframe.columns) - 1}"
    )

    print(
        f"Variabel Gower     : "
        f"{len(ORDINAL_FEATURES) + len(CATEGORICAL_FEATURES)}"
    )

    distance_matrix = (
        calculate_gower_distance(
            source_dataframe
        )
    )

    (
        kmeans_results,
        best_kmeans_model,
        scaler,
    ) = run_kmeans_experiments(
        encoded_dataframe
    )

    (
        hierarchical_results,
        best_hierarchical_model,
        hierarchical_labels,
    ) = run_hierarchical_experiments(
        distance_matrix
    )

    dbscan_results = (
        run_dbscan_experiments(
            distance_matrix
        )
    )

    save_outputs(
        source_dataframe=(
            source_dataframe
        ),
        encoded_dataframe=(
            encoded_dataframe
        ),
        distance_matrix=(
            distance_matrix
        ),
        kmeans_results=(
            kmeans_results
        ),
        hierarchical_results=(
            hierarchical_results
        ),
        dbscan_results=(
            dbscan_results
        ),
        best_kmeans_model=(
            best_kmeans_model
        ),
        scaler=scaler,
        best_hierarchical_model=(
            best_hierarchical_model
        ),
        hierarchical_labels=(
            hierarchical_labels
        ),
    )

    best_kmeans = (
        kmeans_results.iloc[0]
    )

    best_hierarchical = (
        hierarchical_results.iloc[0]
    )

    print("-" * 58)
    print("EKSPERIMEN BERHASIL")
    print()

    print(
        "K-Means baseline terbaik"
    )

    print(
        f"  Jumlah cluster    : "
        f"{int(best_kmeans['n_clusters'])}"
    )

    print(
        f"  Silhouette        : "
        f"{best_kmeans['silhouette_score']:.4f}"
    )

    print(
        f"  Davies-Bouldin    : "
        f"{best_kmeans['davies_bouldin_index']:.4f}"
    )

    print()
    print(
        "Hierarchical Gower terbaik"
    )

    print(
        f"  Linkage           : "
        f"{best_hierarchical['linkage']}"
    )

    print(
        f"  Jumlah cluster    : "
        f"{int(best_hierarchical['n_clusters'])}"
    )

    print(
        f"  Silhouette        : "
        f"{best_hierarchical['silhouette_score']:.4f}"
    )

    valid_dbscan_results = (
        dbscan_results.dropna(
            subset=[
                "silhouette_score"
            ]
        )
    )

    print()
    print("DBSCAN Gower")

    if valid_dbscan_results.empty:
        print(
            "  Tidak ditemukan konfigurasi "
            "dengan minimal dua cluster valid."
        )

    else:
        best_dbscan = (
            valid_dbscan_results.iloc[0]
        )

        print(
            f"  Konfigurasi       : "
            f"{best_dbscan['configuration']}"
        )

        print(
            f"  Jumlah cluster    : "
            f"{int(best_dbscan['n_clusters'])}"
        )

        print(
            f"  Noise             : "
            f"{int(best_dbscan['noise_count'])}"
        )

        print(
            f"  Silhouette        : "
            f"{best_dbscan['silhouette_score']:.4f}"
        )

    print()
    print(
        f"Hasil numerik       : "
        f"{RESULTS_DIRECTORY}"
    )

    print(
        f"Model tersimpan     : "
        f"{MODELS_DIRECTORY}"
    )

    print(
        f"Grafik              : "
        f"{REPORTS_DIRECTORY}"
    )

    print("-" * 58)


if __name__ == "__main__":
    main()