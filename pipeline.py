import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

# 1. EXTRACT
raw_df = pd.read_csv("local_authority_traffic.csv", low_memory=False)

# 2. TRANSFORM & CLEAN
bham_df = raw_df[raw_df["local_authority_name"] == "Birmingham"].copy()

columns_to_keep = [
    "local_authority_id",
    "local_authority_name",
    "year",
    "cars_and_taxis",
    "all_motor_vehicles",
]
bham_clean = bham_df[columns_to_keep].dropna(subset=["all_motor_vehicles"]).copy()

bham_clean["cars_and_taxis"] = pd.to_numeric(bham_clean["cars_and_taxis"], errors="coerce")
bham_clean["all_motor_vehicles"] = pd.to_numeric(bham_clean["all_motor_vehicles"], errors="coerce")

# 3. LOAD TO SQLITE
conn = sqlite3.connect("birmingham_traffic.db")
bham_clean.to_sql("la_traffic", conn, if_exists="replace", index=False)

# 4. SQL QUERY EXECUTION
query = """
SELECT 
    year, 
    cars_and_taxis AS car_miles,
    all_motor_vehicles AS total_vehicle_miles
FROM la_traffic
WHERE year >= 2015 AND year <= 2024
ORDER BY year ASC;
"""
df_yearly = pd.read_sql_query(query, conn)

print(df_yearly)

# 5. VISUALIZATION
plt.figure(figsize=(10, 5))

plt.plot(
    df_yearly["year"],
    df_yearly["total_vehicle_miles"] / 1e9,
    marker="o",
    linewidth=2.5,
    color="#005A9C",
    label="Total Motor Vehicles",
)
plt.plot(
    df_yearly["year"],
    df_yearly["car_miles"] / 1e9,
    marker="s",
    linewidth=2,
    color="#E05A47",
    linestyle="--",
    label="Cars & Taxis",
)

plt.title("Birmingham Annual Traffic Volume (2015–2024)", fontsize=13, pad=12)
plt.xlabel("Year", fontsize=10)
plt.ylabel("Vehicle Miles (Billions)", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()

plt.savefig("birmingham_traffic_trend.png")
conn.close()