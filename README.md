# Birmingham Road Traffic ETL Pipeline

This project is a Python data pipeline. It reads raw UK traffic data, cleans and filters the data for Birmingham, stores it in a SQLite database, and runs SQL queries to analyze traffic trends from 2015 to 2024.

## Pipeline Breakdown (ETL)

* **Extract:** Ingests raw traffic data from a CSV file (`local_authority_traffic.csv`).
* **Transform:** Filters the dataset for Birmingham records, cleans missing values, fixes column data types, and formats numbers for readability.
* **Load:** Stores the cleaned data into a table named `la_traffic` inside a local SQLite database (`birmingham_traffic.db`).

## SQL Queries

The pipeline runs 3 SQL queries on the database:

1. **10-Year Trend (2015–2024):** Pulls yearly traffic totals to generate the trend line chart.
2. **Peak Traffic Year:** Finds the single year with the highest traffic volume in Birmingham.
3. **Pandemic Impact:** Compares 2019 and 2020 traffic to calculate the exact drop during covid lockdowns.

## Technologies Used

* **Python 3**
* **Pandas** (Data cleaning & transformation)
* **SQLite / SQL** (Database storage & analysis)
* **Matplotlib** (Chart generation)
* **Git & GitHub** (Version control)

## Output

The script automatically exports a line chart named `birmingham_traffic_trend.png`.
