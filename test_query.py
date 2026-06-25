import sqlite3
import pandas as pd

# Connect to our newly created database
conn = sqlite3.connect("epidemiology_tracker.db")

# A relational SQL query joining our Dimension table and Fact table
query = """
SELECT 
    f.Date,
    l.State_Code,
    f.Daily_New_Cases,
    f.Current_Hospitalizations
FROM Fact_Outbreak f
JOIN Dim_Location l ON f.Location_ID = l.Location_ID
WHERE l.State_Code = 'NY'
ORDER BY f.Date DESC
LIMIT 5;
"""

# Read the query output using pandas to display it neatly
df_result = pd.read_sql_query(query, conn)
print(df_result)

conn.close()