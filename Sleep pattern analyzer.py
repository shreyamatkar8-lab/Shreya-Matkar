import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ----------------------------------
# SLEEP PATTERN ANALYZER
# ----------------------------------

print("=" * 45)
print("       SLEEP PATTERN ANALYZER")
print("=" * 45)

# Sample sleep data
sample_data = {
    "Date": [
        "2026-10-01", "2026-10-02", "2026-10-03",
        "2026-10-04", "2026-10-05", "2026-10-06",
        "2026-10-07"
    ],
    "Bedtime": [
        "22:00", "23:00", "22:30", "00:00",
        "23:30", "22:15", "23:00"
    ],
    "Wakeup": [
        "06:00", "06:30", "06:30", "07:00",
        "06:30", "06:15", "07:00"
    ],
    "Sleep_Quality": [8, 7, 9, 6, 7, 9, 8],
    "Stress_Level": [3, 5, 2, 7, 5, 2, 3]
}

# Create a sample CSV if one does not exist
if not os.path.exists("sleep_data.csv"):
    pd.DataFrame(sample_data).to_csv(
        "sleep_data.csv", index=False
    )
    print("\nSample dataset created: sleep_data.csv")

# Load dataset
df = pd.read_csv("sleep_data.csv")

# Check required columns
required_columns = [
    "Date", "Bedtime", "Wakeup",
    "Sleep_Quality", "Stress_Level"
]

if not all(col in df.columns for col in required_columns):
    raise ValueError(
        "Dataset must contain: " + ", ".join(required_columns)
    )

# Convert dates
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Calculate sleep duration
def calculate_sleep_duration(row):
    try:
        bedtime = pd.to_datetime(
            str(row["Bedtime"]), format="%H:%M"
        )
        wakeup = pd.to_datetime(
            str(row["Wakeup"]), format="%H:%M"
        )

        duration = (
            wakeup.hour * 60 + wakeup.minute
        ) - (
            bedtime.hour * 60 + bedtime.minute
        )

        # Handle sleep continuing past midnight
        if duration < 0:
            duration += 24 * 60

        return duration / 60

    except (ValueError, TypeError):
        return float("nan")


df["Sleep_Duration"] = df.apply(
    calculate_sleep_duration, axis=1
)

# Remove invalid records
df = df.dropna(
    subset=[
        "Date", "Sleep_Duration",
        "Sleep_Quality", "Stress_Level"
    ]
)

df = df[
    (df["Sleep_Duration"] > 0)
    & (df["Sleep_Duration"] <= 24)
    & df["Sleep_Quality"].between(1, 10)
    & df["Stress_Level"].between(1, 10)
]

if df.empty:
    raise ValueError("No valid sleep records found.")

# ----------------------------------
# ANALYSIS
# ----------------------------------

average_sleep = df["Sleep_Duration"].mean()
average_quality = df["Sleep_Quality"].mean()
average_stress = df["Stress_Level"].mean()

print("\n========== SLEEP ANALYSIS ==========")

print(f"Average Sleep Duration: {average_sleep:.2f} hours")
print(f"Average Sleep Quality: {average_quality:.2f}/10")
print(f"Average Stress Level: {average_stress:.2f}/10")

print("\n========== DAILY RECORDS ==========")

print(
    df[
        ["Date", "Bedtime", "Wakeup",
         "Sleep_Duration", "Sleep_Quality", "Stress_Level"]
    ].to_string(index=False)
)

# ----------------------------------
# SLEEP OBSERVATIONS
# ----------------------------------

print("\n========== SLEEP OBSERVATIONS ==========")

if average_sleep < 7:
    print("Your average sleep duration is below 7 hours.")
elif average_sleep <= 9:
    print("Your average sleep duration is within 7-9 hours.")
else:
    print("Your average sleep duration exceeds 9 hours.")

if average_quality < 5:
    print("Your recorded sleep quality is relatively low.")
elif average_quality < 8:
    print("Your recorded sleep quality is moderate.")
else:
    print("Your recorded sleep quality ratings are high.")

if average_stress >= 7:
    print("Your recorded stress levels are relatively high.")
else:
    print("Your recorded stress levels are below 7/10 on average.")

print("\nNote: These observations are informational,")
print("not a medical diagnosis.")

# ----------------------------------
# DATA VISUALIZATION
# ----------------------------------

sns.set_theme(style="whitegrid")

fig, axes = plt.subplots(2, 2, figsize=(13, 9))

# Graph 1: Sleep duration by date
sns.lineplot(
    data=df,
    x="Date",
    y="Sleep_Duration",
    marker="o",
    ax=axes[0, 0]
)
axes[0, 0].axhline(
    8, linestyle="--", label="8-hour reference"
)
axes[0, 0].set_title("Daily Sleep Duration")
axes[0, 0].set_ylabel("Hours")
axes[0, 0].legend()

# Graph 2: Sleep quality
sns.barplot(
    data=df,
    x="Date",
    y="Sleep_Quality",
    ax=axes[0, 1]
)
axes[0, 1].set_title("Daily Sleep Quality")
axes[0, 1].set_ylabel("Quality (1-10)")
axes[0, 1].tick_params(axis="x", rotation=45)

# Graph 3: Stress level
sns.lineplot(
    data=df,
    x="Date",
    y="Stress_Level",
    marker="o",
    ax=axes[1, 0]
)
axes[1, 0].set_title("Daily Stress Levels")
axes[1, 0].set_ylabel("Stress (1-10)")

# Graph 4: Sleep duration distribution
sns.histplot(
    data=df,
    x="Sleep_Duration",
    bins=7,
    kde=True,
    ax=axes[1, 1]
)
axes[1, 1].set_title("Sleep Duration Distribution")
axes[1, 1].set_xlabel("Sleep Duration (hours)")

plt.tight_layout()

# Save graphs
plt.savefig("sleep_analysis.png", dpi=300)

print("\nGraph saved as sleep_analysis.png")

# Display graphs
plt.show()

# Save analyzed data
df.to_csv("analyzed_sleep_data.csv", index=False)

print("Analyzed data saved as analyzed_sleep_data.csv")
print("\nSleep Pattern Analysis Completed!")
