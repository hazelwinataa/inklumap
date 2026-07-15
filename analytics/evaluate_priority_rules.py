# STANDARD LIBRARY

from pathlib import Path


# THIRD-PARTY LIBRARIES

import numpy as np
import pandas as pd


# FILE PATHS

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    PROJECT_ROOT
    / "analytics"
    / "results"
    / "student_recommendations.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "analytics"
    / "results"
    / "priority_rule_sensitivity.csv"
)

DETAIL_OUTPUT_PATH = (
    PROJECT_ROOT
    / "analytics"
    / "results"
    / "priority_rule_assignments.csv"
)


# PRIORITY RULES

PRIORITY_RULES = {
    "current": {
        "high_critical_domains": 2,
        "high_scored_domains": 4,
        "high_average_score": 1.75,
        "medium_critical_domains": 1,
        "medium_scored_domains": 2,
        "medium_average_score": 1.00,
    },
    "balanced": {
        "high_critical_domains": 3,
        "high_scored_domains": 5,
        "high_average_score": 2.00,
        "medium_critical_domains": 1,
        "medium_scored_domains": 3,
        "medium_average_score": 1.25,
    },
    "selective": {
        "high_critical_domains": 3,
        "high_scored_domains": 6,
        "high_average_score": 2.25,
        "medium_critical_domains": 1,
        "medium_scored_domains": 3,
        "medium_average_score": 1.25,
    },
}


def assign_priority(
    dataframe: pd.DataFrame,
    rule: dict[str, float],
) -> pd.Series:
    high_mask = (
        (
            dataframe["critical_domain_count"]
            >= rule["high_critical_domains"]
        )
        | (
            dataframe["high_domain_count"]
            >= rule["high_scored_domains"]
        )
        | (
            dataframe["average_need_score"]
            >= rule["high_average_score"]
        )
    )

    medium_mask = (
        (
            dataframe["critical_domain_count"]
            >= rule["medium_critical_domains"]
        )
        | (
            dataframe["high_domain_count"]
            >= rule["medium_scored_domains"]
        )
        | (
            dataframe["average_need_score"]
            >= rule["medium_average_score"]
        )
    )

    priorities = np.select(
        condlist=[
            high_mask,
            medium_mask,
        ],
        choicelist=[
            "high",
            "medium",
        ],
        default="low",
    )

    return pd.Series(
        priorities,
        index=dataframe.index,
        dtype="string",
    )


def create_summary(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary_rows = []

    detailed_dataframe = dataframe[
        [
            "student_code",
            "cluster_id",
            "cluster_name",
            "critical_domain_count",
            "high_domain_count",
            "average_need_score",
            "dbscan_unique_case",
            "individual_silhouette",
        ]
    ].copy()

    total_students = len(
        dataframe
    )

    for rule_name, rule in PRIORITY_RULES.items():
        priority_column = (
            f"priority_{rule_name}"
        )

        detailed_dataframe[
            priority_column
        ] = assign_priority(
            dataframe,
            rule,
        )

        priority_counts = (
            detailed_dataframe[
                priority_column
            ]
            .value_counts()
        )

        high_count = int(
            priority_counts.get(
                "high",
                0,
            )
        )

        medium_count = int(
            priority_counts.get(
                "medium",
                0,
            )
        )

        low_count = int(
            priority_counts.get(
                "low",
                0,
            )
        )

        summary_rows.append(
            {
                "rule_name": rule_name,
                "high_count": high_count,
                "high_percentage": (
                    high_count
                    / total_students
                    * 100
                ),
                "medium_count": medium_count,
                "medium_percentage": (
                    medium_count
                    / total_students
                    * 100
                ),
                "low_count": low_count,
                "low_percentage": (
                    low_count
                    / total_students
                    * 100
                ),
                "high_critical_domains": (
                    rule[
                        "high_critical_domains"
                    ]
                ),
                "high_scored_domains": (
                    rule[
                        "high_scored_domains"
                    ]
                ),
                "high_average_score": (
                    rule[
                        "high_average_score"
                    ]
                ),
                "medium_critical_domains": (
                    rule[
                        "medium_critical_domains"
                    ]
                ),
                "medium_scored_domains": (
                    rule[
                        "medium_scored_domains"
                    ]
                ),
                "medium_average_score": (
                    rule[
                        "medium_average_score"
                    ]
                ),
            }
        )

    summary_dataframe = pd.DataFrame(
        summary_rows
    )

    return (
        summary_dataframe,
        detailed_dataframe,
    )


def print_score_distribution(
    dataframe: pd.DataFrame,
) -> None:
    print()
    print("DISTRIBUSI INDIKATOR KEBUTUHAN")
    print("-" * 60)

    print(
        dataframe[
            [
                "critical_domain_count",
                "high_domain_count",
                "average_need_score",
            ]
        ]
        .describe()
        .round(3)
        .to_string()
    )

    print()
    print(
        "Jumlah domain berskor 3:"
    )

    print(
        dataframe[
            "critical_domain_count"
        ]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print()
    print(
        "Jumlah domain berskor 2-3:"
    )

    print(
        dataframe[
            "high_domain_count"
        ]
        .value_counts()
        .sort_index()
        .to_string()
    )


def print_rule_summary(
    summary_dataframe: pd.DataFrame,
) -> None:
    display_columns = [
        "rule_name",
        "high_count",
        "high_percentage",
        "medium_count",
        "medium_percentage",
        "low_count",
        "low_percentage",
    ]

    display_dataframe = (
        summary_dataframe[
            display_columns
        ].copy()
    )

    percentage_columns = [
        "high_percentage",
        "medium_percentage",
        "low_percentage",
    ]

    display_dataframe[
        percentage_columns
    ] = display_dataframe[
        percentage_columns
    ].round(2)

    print()
    print("PERBANDINGAN ATURAN PRIORITAS")
    print("-" * 60)

    print(
        display_dataframe.to_string(
            index=False
        )
    )


def print_cluster_distribution(
    detailed_dataframe: pd.DataFrame,
) -> None:
    for rule_name in PRIORITY_RULES:
        priority_column = (
            f"priority_{rule_name}"
        )

        cluster_summary = pd.crosstab(
            detailed_dataframe[
                "cluster_id"
            ],
            detailed_dataframe[
                priority_column
            ],
        )

        cluster_summary = (
            cluster_summary.reindex(
                columns=[
                    "high",
                    "medium",
                    "low",
                ],
                fill_value=0,
            )
        )

        print()
        print(
            "DISTRIBUSI CLUSTER - "
            f"ATURAN {rule_name.upper()}"
        )

        print("-" * 60)

        print(
            cluster_summary.to_string()
        )


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            "File rekomendasi tidak ditemukan: "
            f"{INPUT_PATH}"
        )

    dataframe = pd.read_csv(
        INPUT_PATH,
        encoding="utf-8-sig",
    )

    required_columns = [
        "student_code",
        "cluster_id",
        "cluster_name",
        "critical_domain_count",
        "high_domain_count",
        "average_need_score",
        "dbscan_unique_case",
        "individual_silhouette",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Kolom berikut tidak ditemukan: "
            + ", ".join(missing_columns)
        )

    (
        summary_dataframe,
        detailed_dataframe,
    ) = create_summary(
        dataframe
    )

    print_score_distribution(
        dataframe
    )

    print_rule_summary(
        summary_dataframe
    )

    print_cluster_distribution(
        detailed_dataframe
    )

    summary_dataframe.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    detailed_dataframe.to_csv(
        DETAIL_OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print()
    print("-" * 60)

    print(
        f"Ringkasan aturan : {OUTPUT_PATH}"
    )

    print(
        f"Detail siswa     : {DETAIL_OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()