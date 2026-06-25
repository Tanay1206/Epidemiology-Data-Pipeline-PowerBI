import os
import sqlite3
import pandas as pd
import requests

# --- THE GPS SYSTEM ---
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "epidemiology_tracker.db")
csv_location_path = os.path.join(script_dir, "Dim_Location.csv")
csv_outbreak_path = os.path.join(script_dir, "Fact_Outbreak.csv")
raw_data_path = os.path.join(script_dir, "raw_covid_data.csv")

# --- 1. DOWNLOAD THE DATA ---
print("Step 1: Fetching data from the web...")
url = "https://api.covidtracking.com/v1/states/daily.csv"
response = requests.get(url)
with open(raw_data_path, "wb") as f:
    f.write(response.content)
df = pd.read_csv(raw_data_path)

# --- 2. CLEAN THE DATA ---
print("Step 2: Cleaning the data...")
columns_to_keep = ["date", "state", "positive", "positiveIncrease", "death", "deathIncrease", "hospitalizedCurrently"]
df_filtered = df[columns_to_keep].copy()
df_filtered["date"] = pd.to_datetime(df_filtered["date"], format="%Y%m%d").dt.strftime("%Y-%m-%d")

numerical_cols = ["positive", "positiveIncrease", "death", "deathIncrease", "hospitalizedCurrently"]
df_filtered[numerical_cols] = df_filtered[numerical_cols].fillna(0).astype(int)

# --- 3. BUILD THE DATABASE ---
print("Step 3: Building the SQL Database...")
if os.path.exists(db_path):
    os.remove(db_path) # Deletes the old broken database so we start fresh

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create Dimension Table
cursor.execute("""
CREATE TABLE Dim_Location (
    Location_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    State_Code TEXT UNIQUE
)
""")
unique_states = df_filtered["state"].unique()
for state in unique_states:
    cursor.execute("INSERT OR IGNORE INTO Dim_Location (State_Code) VALUES (?)", (state,))

# Create Fact Table
cursor.execute("""
CREATE TABLE Fact_Outbreak (
    Fact_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Date TEXT,
    Location_ID INTEGER,
    Cumulative_Cases INTEGER,
    Daily_New_Cases INTEGER,
    Cumulative_Deaths INTEGER,
    Daily_New_Deaths INTEGER,
    Current_Hospitalizations INTEGER,
    FOREIGN KEY (Location_ID) REFERENCES Dim_Location (Location_ID)
)
""")
conn.commit()

# Link the tables and format the data
location_mapping = pd.read_sql_query("SELECT * FROM Dim_Location", conn)
df_final = df_filtered.merge(location_mapping, left_on="state", right_on="State_Code")

# FIXING THE TYPO: Renaming lowercase "date" to capital "Date"
df_final = df_final.rename(columns={
    "date": "Date", 
    "positive": "Cumulative_Cases",
    "positiveIncrease": "Daily_New_Cases",
    "death": "Cumulative_Deaths",
    "deathIncrease": "Daily_New_Deaths",
    "hospitalizedCurrently": "Current_Hospitalizations"
})

fact_table_data = df_final[[
    "Date", "Location_ID", "Cumulative_Cases", "Daily_New_Cases", 
    "Cumulative_Deaths", "Daily_New_Deaths", "Current_Hospitalizations"
]]

# Push the numbers into the database
fact_table_data.to_sql("Fact_Outbreak", conn, if_exists="append", index=False)

# --- 4. EXPORT THE CSVS ---
print("Step 4: Exporting the final CSVs...")
df_loc_export = pd.read_sql_query("SELECT * FROM Dim_Location", conn)
df_out_export = pd.read_sql_query("SELECT * FROM Fact_Outbreak", conn)

df_loc_export.to_csv(csv_location_path, index=False)
df_out_export.to_csv(csv_outbreak_path, index=False)

conn.close()
print("SUCCESS! Your database is built and your CSVs are fully populated.")