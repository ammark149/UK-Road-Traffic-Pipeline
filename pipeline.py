import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

# 1. EXTRACT & TRANSFORM
raw_df = pd.read_csv("local_authority_traffic.csv", low_memory=False)

columns_to_keep = [
    "local_authority_id",
    "local_authority_name",
    "year",
    "cars_and_taxis",
    "all_motor_vehicles",
]
clean_df = raw_df[columns_to_keep].dropna(subset=["all_motor_vehicles"]).copy()

clean_df["cars_and_taxis"] = pd.to_numeric(clean_df["cars_and_taxis"], errors="coerce")
clean_df["all_motor_vehicles"] = pd.to_numeric(clean_df["all_motor_vehicles"], errors="coerce")

# 2. LOAD TO A SINGLE SQLITE DB
conn = sqlite3.connect("uk_traffic.db")
clean_df.to_sql("la_traffic", conn, if_exists="replace", index=False)


# --- QUERY 1: Birmingham 10-Year Trend (Used for Chart) ---
query_1 = """
SELECT year, cars_and_taxis AS car_miles, all_motor_vehicles AS total_vehicle_miles
FROM la_traffic
WHERE local_authority_name = 'Birmingham' 
  AND year >= 2015 AND year <= 2024
ORDER BY year ASC;
"""
df_bham = pd.read_sql_query(query_1, conn)
print("--- QUERY 1: Birmingham 10-Year Trend ---")
print(df_bham)


# --- QUERY 2: Top 5 Highest Traffic Local Authorities in 2024 ---
query_2 = """
SELECT local_authority_name, all_motor_vehicles AS total_traffic
FROM la_traffic
WHERE year = 2024
ORDER BY all_motor_vehicles DESC
LIMIT 5;
"""
df_top5 = pd.read_sql_query(query_2, conn)
print("\n--- QUERY 2: Top 5 Highest Traffic Regions (2024) ---")
print(df_top5)


# --- QUERY 3: Nationwide Pre vs Post Pandemic Traffic Drop (2019 vs 2020) ---
query_3 = """
SELECT 
    year, 
    SUM(all_motor_vehicles) AS total_uk_traffic
FROM la_traffic
WHERE year IN (2019, 2020, 2024)
GROUP BY year
ORDER BY year ASC;
"""
df_pandemic = pd.read_sql_query(query_3, conn)
print("\n--- QUERY 3: UK Total Pandemic Traffic Shift ---")
print(df_pandemic)


# 3. VISUALIZATION (Chart generated from Query 1)
plt.figure(figsize=(10, 5))
plt.plot(df_bham["year"], df_bham["total_vehicle_miles"] / 1e9, marker="o", linewidth=2.5, color="#005A9C", label="Total Motor Vehicles")
plt.plot(df_bham["year"], df_bham["car_miles"] / 1e9, marker="s", linewidth=2, color="#E05A47", linestyle="--", label="Cars & Taxis")

plt.title("Birmingham Annual Traffic Volume (2015–2024)", fontsize=13, pad=12)
plt.xlabel("Year", fontsize=10)
plt.ylabel("Vehicle Miles (Billions)", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()

plt.savefig("birmingham_traffic_trend.png")
conn.close()