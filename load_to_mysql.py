# Creating a python script to load the cleaned dataset 'CSV' into MySQL
# importing pandas and mysql connector
import pandas as pd
import mysql.connector

# Loading cleaned CSV file
df = pd.read_csv("C:/Users/ralis/OneDrive/Desktop/NYC Open Data Project/cleaned_nyc_collisions.csv")

# Connecting to MySQL database and creating a curson to run SQL commands
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2025SQL",
    database="nyc_crashes"
)
cursor = conn.cursor()

# Replacing all the column names in the DataFrame (df.columns) with a cleaner, MySQL-safe format
# So a column like "CRASH DATE" becomes "CRASH_DATE" and "zip code" becomes "ZIP_CODE"
df.columns = [col.strip().upper().replace(" ", "_") for col in df.columns]

# Generate the dynamic insert statement
columns = list(df.columns)
columns_str = ", ".join(columns)
placeholders = ", ".join(["%s"] * len(columns))
insert_query = f"INSERT IGNORE INTO collisions ({columns_str}) VALUES ({placeholders})"

# Insert row by row
for index, row in df.iterrows():
    cursor.execute(insert_query, tuple(row))
    if index % 5000 == 0:
        print(f"Inserted {index} rows...")
        conn.commit()

# Final commit and close
conn.commit()
cursor.close()
conn.close()

print("All data successfully loaded into MySQL!")
