"""
airtable_upload.py

Uploads cleaned enrollment data and city-level metrics to Airtable.
"""

import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}


def upload_records(table_name: str, records: list):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_name}"
    payload = {"records": records}
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code != 200:
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
    
    response.raise_for_status()


def upload_enrollments():
    df = pd.read_csv("data/clean_enrollment.csv")
    records = [
    {
        "fields": {
            "Enrollment ID": int(row["enrollment_id"]),
            "City": row["city"],
            "Participant ID": row["participant_id"],
            "Enrollment Date": str(row["enrollment_date"]),
            "Program Center": row["program_center"],
            "Completion Status": row["completion_status"]
        }
    }
    for _, row in df.iterrows()

   
]


    for i in range(0, len(records), 10):
        upload_records("Enrollments", records[i:i+10])


def upload_city_metrics():
    df = pd.read_csv("data/clean_enrollment.csv")

    metrics = (
        df.groupby("city")
        .agg(
            total_enrollments=("enrollment_id", "count"),
            first_enrollment=("enrollment_date", "min"),
            last_enrollment=("enrollment_date", "max")
        )
        .reset_index()
    )

    records = [
        {
            "fields": {
                "City": row["city"],
                "Total Enrollments": int(row["total_enrollments"]),
                "First Enrollment": row["first_enrollment"],
                "Last Enrollment": row["last_enrollment"]
            }
        }
        for _, row in metrics.iterrows()
    ]

    for i in range(0, len(records), 10):
        upload_records("Cities", records[i:i+10])


def main():
    upload_enrollments()
    upload_city_metrics()
    print("Airtable upload complete.")


if __name__ == "__main__":
    main()
