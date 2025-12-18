"""
analyze_engagement.py

Computes city-level impact and engagement metrics
from cleaned enrollment data.
"""

import pandas as pd


def load_clean_data() -> pd.DataFrame:
    return pd.read_csv(
        "data/clean_enrollment.csv",
        parse_dates=["enrollment_date"]
    )


def analyze_city_metrics(df: pd.DataFrame) -> pd.DataFrame:
    city_metrics = (
        df.groupby("city")
        .agg(
            total_enrollments=("enrollment_id", "count"),
            repeat_enrollments=("participant_id", lambda x: x.duplicated().sum()),
            first_enrollment=("enrollment_date", "min"),
            last_enrollment=("enrollment_date", "max"),
        )
        .reset_index()
        .sort_values("total_enrollments", ascending=False)
    )

    return city_metrics


def main():
    df = load_clean_data()
    metrics = analyze_city_metrics(df)

    print("\nCity-level Impact & Engagement Metrics:")
    print(metrics)


if __name__ == "__main__":
    main()
