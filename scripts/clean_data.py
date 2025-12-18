"""
clean_data.py

Loads raw enrollment data from CSV, performs basic cleaning and normalization,
and outputs a cleaned DataFrame for downstream analysis and Airtable upload.
"""

import pandas as pd
from pathlib import Path


def load_raw_data(file_path: str) -> pd.DataFrame:
    """
    Load raw enrollment data from a CSV file.

    Args:
        file_path (str): Path to the raw CSV file

    Returns:
        pd.DataFrame: Raw enrollment data
    """
    return pd.read_csv(file_path)


def clean_enrollment_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and normalize enrollment data based on the raw schema.

    Mappings:
    - record_id          -> enrollment_id
    - leader_info        -> participant_id
    - city_data          -> city
    - course_enrollment  -> enrollment_date
    """

    df = df.copy()

    # Rename columns to normalized internal names
    df = df.rename(columns={
        "record_id": "enrollment_id",
        "leader_info": "participant_id",
        "city_data": "city",
        "course_enrollment": "enrollment_date"
    })

    # # Normalize city names
    # df["city"] = (
    #     df["city"]
    #     .astype(str)
    #     .str.strip()
    #     .str.title()
    # )

    # Extract city name from compound city_data field
    df["city"] = (
        df["city"]
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # Parse enrollment dates (best-effort)
    # df["enrollment_date"] = pd.to_datetime(
    #     df["enrollment_date"],
    #     errors="coerce"
    # )
# Extract enrollment start date from compound course_enrollment field
    df["enrollment_date"] = (
        df["enrollment_date"]
        .astype(str)
        .str.split("~")
        .str[2]
)

    df["enrollment_date"] = pd.to_datetime(
        df["enrollment_date"],
        errors="coerce"
)
    # Drop rows missing required fields
    df = df.dropna(
        subset=["enrollment_id", "participant_id", "city"]
    )

    return df


def main():
    data_dir = Path("data")
    input_file = data_dir / "raw_enrollment.csv"
    output_file = data_dir / "clean_enrollment.csv"

    if not input_file.exists():
        raise FileNotFoundError(
            f"CSV file not found at {input_file}"
        )

    df_raw = load_raw_data(input_file)
    df_clean = clean_enrollment_data(df_raw)

    # ✅ SAVE cleaned data
    df_clean.to_csv(output_file, index=False)

    print("Raw rows:", len(df_raw))
    print("Clean rows:", len(df_clean))
    print(f"Cleaned data written to {output_file}")
    print("\nSample cleaned data:")
    print(df_clean.head())

# def main():
#     data_dir = Path("data")
#     input_file = data_dir / "raw_enrollment.csv"

#     if not input_file.exists():
#         raise FileNotFoundError(
#             f"CSV file not found at {input_file}"
#         )

#     df_raw = load_raw_data(input_file)
#     df_clean = clean_enrollment_data(df_raw)

#     output_file = data_dir / "clean_enrollment.csv"
#     df_clean.to_csv(output_file, index=False)

#     print(f"Cleaned data written to {output_file}")

#     print("Raw rows:", len(df_raw))
#     print("Clean rows:", len(df_clean))
#     print("\nSample cleaned data:")
#     print(df_clean.head())


if __name__ == "__main__":
    main()
