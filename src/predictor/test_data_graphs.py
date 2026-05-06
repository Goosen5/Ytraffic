import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

BASE = "graphs/test_png"
os.makedirs(BASE, exist_ok=True)

df = pd.read_csv("assets/test/traffic_per_stop.csv", low_memory=False)

df.columns = [
    "datetime", "date", "hour",
    "station_code", "station_name",
    "line", "value"
]

df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
df = df.dropna(subset=["datetime"])

df["hour"] = df["datetime"].dt.hour
df["month"] = df["datetime"].dt.month

station = "A06"

# =========================
# HOURLY GRAPHS
# =========================

plt.figure()
plt.scatter(df["value"][:500], df["value"][:500], alpha=0.4)
plt.title("Real vs Real (Baseline)")
plt.xlabel("Real")
plt.ylabel("Real")
plt.savefig(f"{BASE}/real_vs_self.png")
plt.close()

hourly = df.groupby("hour")["value"].mean()

plt.figure()
plt.plot(hourly.index, hourly.values)
plt.title("Hourly Traffic Pattern (Real)")
plt.xlabel("Hour")
plt.ylabel("Traffic")
plt.grid()
plt.savefig(f"{BASE}/hourly_pattern.png")
plt.close()

errors = np.zeros(len(df))

plt.figure()
plt.hist(errors, bins=20)
plt.title("Error Distribution (Perfect Model Baseline)")
plt.savefig(f"{BASE}/error_distribution.png")
plt.close()

bias = pd.Series(0, index=hourly.index)

plt.figure()
plt.plot(bias.index, bias.values)
plt.axhline(0, linestyle="--")
plt.title("Hourly Bias (Perfect Model Baseline)")
plt.xlabel("Hour")
plt.savefig(f"{BASE}/hourly_bias.png")
plt.close()

pivot = df.pivot_table(
    index="hour",
    columns="station_name",
    values="value",
    aggfunc="mean"
)

plt.figure(figsize=(14, 6))
sns.heatmap(pivot, cmap="viridis")
plt.title("Real Traffic Heatmap (Station × Hour)")
plt.savefig(f"{BASE}/heatmap.png")
plt.close()

station_df = df[df["station_code"] == station]
real_s = station_df.groupby("hour")["value"].mean()

plt.figure()
plt.plot(real_s.index, real_s.values)
plt.title(f"Station {station} Pattern (Real)")
plt.xlabel("Hour")
plt.ylabel("Traffic")
plt.grid()
plt.savefig(f"{BASE}/station_pattern.png")
plt.close()

# =========================
# MONTHLY GRAPHS
# =========================

month_order = [
    pd.Timestamp(2000, m, 1).strftime("%b")
    for m in range(1, 13)
]

df["month_name"] = pd.Categorical(
    df["datetime"].dt.strftime("%b"),
    categories=month_order,
    ordered=True
)

# Monthly average traffic (bar)
monthly = df.groupby("month_name", observed=True)["value"].mean()

plt.figure(figsize=(10, 5))
plt.bar(monthly.index, monthly.values, color="steelblue")
plt.title("Monthly Average Traffic")
plt.xlabel("Month")
plt.ylabel("Average Traffic")
plt.grid(axis="y")
plt.savefig(f"{BASE}/monthly_avg.png")
plt.close()

# Monthly distribution (boxplot)
plt.figure(figsize=(12, 5))
df.boxplot(column="value", by="month_name", grid=True)
plt.title("Monthly Traffic Distribution")
plt.suptitle("")
plt.xlabel("Month")
plt.ylabel("Traffic")
plt.savefig(f"{BASE}/monthly_boxplot.png")
plt.close()

# Monthly heatmap (station x month)
pivot_month = df.pivot_table(
    index="month",
    columns="station_name",
    values="value",
    aggfunc="mean"
)

plt.figure(figsize=(14, 6))
sns.heatmap(pivot_month, cmap="viridis")
plt.title("Monthly Traffic Heatmap (Station × Month)")
plt.xlabel("Station")
plt.ylabel("Month")
plt.savefig(f"{BASE}/monthly_heatmap.png")
plt.close()

# Monthly pattern for station A06
station_monthly = df[df["station_code"] == station].groupby("month")["value"].mean()

plt.figure()
plt.plot(station_monthly.index, station_monthly.values, marker="o")
plt.title(f"Station {station} — Monthly Pattern")
plt.xlabel("Month")
plt.ylabel("Traffic")
plt.xticks(station_monthly.index)
plt.grid()
plt.savefig(f"{BASE}/monthly_station_pattern.png")
plt.close()

# Hour x Month heatmap
pivot_month_hour = df.pivot_table(
    index="hour",
    columns="month",
    values="value",
    aggfunc="mean"
)

plt.figure(figsize=(12, 6))
sns.heatmap(pivot_month_hour, cmap="viridis")
plt.title("Traffic Heatmap (Hour × Month)")
plt.xlabel("Month")
plt.ylabel("Hour")
plt.savefig(f"{BASE}/monthly_hour_heatmap.png")
plt.close()

print("Test data PNG graphs saved in graphs/test_png/")