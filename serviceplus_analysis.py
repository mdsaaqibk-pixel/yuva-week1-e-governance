"""
Reproducible exploratory analysis of a small ServicePlus public dashboard sample.
Run: python serviceplus_analysis.py
Install dependencies: pip install pandas matplotlib
Data source: ServicePlus official portal; state figures shown in the report were
reported on 19 October 2026. This is a small illustrative sample, not all India.
"""
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "serviceplus_state_data.csv"
df = pd.read_csv(DATA_FILE)

# Basic validation
numeric = ["Applications_Total", "Delivered", "Rejected", "Underprocess", "Services_Launched"]
for col in numeric:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["Status_Sum_Check"] = df["Delivered"] + df["Rejected"] + df["Underprocess"] - df["Applications_Total"]
df["Delivered_Pct_of_Total"] = (df["Delivered"] / df["Applications_Total"] * 100).round(2)
df["Rejected_Pct_of_Total"] = (df["Rejected"] / df["Applications_Total"] * 100).round(2)
df["Pending_Pct_of_Total"] = (df["Underprocess"] / df["Applications_Total"] * 100).round(2)

print("Rows, columns:", df.shape)
print("\\nMissing values:\\n", df.isna().sum())
print("\\nStatus reconciliation (ideally zero):\\n",
      df[["State", "Status_Sum_Check"]].to_string(index=False))
print("\\nSummary indicators:\\n",
      df[["State", "Applications_Total", "Delivered_Pct_of_Total",
          "Rejected_Pct_of_Total", "Pending_Pct_of_Total"]].to_string(index=False))

df.to_csv("serviceplus_analysis_output.csv", index=False)

plt.figure(figsize=(10, 6))
plt.bar(df["State"], df["Underprocess"])
plt.xticks(rotation=20, ha="right")
plt.ylabel("Applications under process")
plt.title("ServicePlus: Applications Under Process by State")
plt.tight_layout()
plt.savefig("pending_applications_by_state.png", dpi=180)
plt.close()

plt.figure(figsize=(9, 6))
plt.bar(df["State"], df["Pending_Pct_of_Total"])
plt.xticks(rotation=20, ha="right")
plt.ylabel("Under-process applications (% of total)")
plt.title("ServicePlus: Pending Share by State")
plt.tight_layout()
plt.savefig("pending_share_by_state.png", dpi=180)
plt.close()

print("\\nSaved serviceplus_analysis_output.csv and two charts.")
