"""
visualize_metrics.py

Generates visual summaries of enrollment impact and engagement.
"""

import pandas as pd
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv("data/clean_enrollment.csv", parse_dates=["enrollment_date"])

    # Impact: total enrollments by city
    city_counts = (
        df["city"]
        .value_counts()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 6))
    city_counts.plot(kind="bar")
    plt.title("Total Enrollments by City")
    plt.xlabel("City")
    plt.ylabel("Number of Enrollments")
    plt.tight_layout()
    plt.savefig("visuals/enrollments_by_city.png")
    plt.close()

    # Engagement over time
    time_series = (
        df
        .set_index("enrollment_date")
        .resample("ME")
        .size()
    )

    plt.figure(figsize=(10, 6))
    time_series.plot()
    plt.title("Enrollment Trends Over Time")
    plt.xlabel("Date")
    plt.ylabel("Enrollments")
    plt.tight_layout()
    plt.savefig("visuals/enrollment_trends.png")
    plt.close()

    print("Visualizations generated in /visuals directory.")


if __name__ == "__main__":
    main()
