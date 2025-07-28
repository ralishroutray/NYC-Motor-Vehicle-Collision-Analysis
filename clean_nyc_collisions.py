# Loading pandas library and nicknaming it 'pd'
import pandas as pd

# Loading the original dataset
df = pd.read_csv(r"C:\Users\ralis\OneDrive\Desktop\NYC Open Data Project\nyc_motor_collisions.csv")

# Removing any spaces at the beginning or end of each column name in the DataFrame.
df.columns = df.columns.str.strip()

# Viewing the first 5 rows (for debugging)
print(df.head())

# Creating a list called "columns_to_keep" that stores the specific column names I want to keep from your dataset.
columns_to_keep = [
    'COLLISION_ID', 'CRASH DATE', 'CRASH TIME', 'BOROUGH', 'ZIP CODE',
    'LATITUDE', 'LONGITUDE', 'ON STREET NAME', 'CROSS STREET NAME', 'OFF STREET NAME',
    'NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED',
    'NUMBER OF PEDESTRIANS INJURED', 'NUMBER OF PEDESTRIANS KILLED',
    'NUMBER OF CYCLIST INJURED', 'NUMBER OF CYCLIST KILLED',
    'NUMBER OF MOTORIST INJURED', 'NUMBER OF MOTORIST KILLED'
]

# Filtering dataframe: Keeping only the columns listed above.
df = df[columns_to_keep]

# Removing any rows where either LATITUDE or LONGITUDE is missing (i.e. empty or NaN).
df = df.dropna(subset=['LATITUDE', 'LONGITUDE'])

# Replace nulls with "Unknown" in text-based columns
text_columns = ['BOROUGH', 'ZIP CODE', 'ON STREET NAME', 'CROSS STREET NAME', 'OFF STREET NAME']
df[text_columns] = df[text_columns].fillna("Unknown")


#--------------------CONVERSIONS--------------------------------------------------------------------

# Converting the 'CRASH DATE' column from string to real date format.
# If a value can't be converted (like a typo), it becomes NaT (Not a Time).
df['CRASH DATE'] = pd.to_datetime(df['CRASH DATE'], errors='coerce')

# Converting 'CRASH TIME' (like '13:45') into a datetime object and extracting just the hour part (13 in this case).
# It's useful for checking when most accidents happen during the day.
df['HOUR'] = pd.to_datetime(df['CRASH TIME'], format='%H:%M', errors='coerce').dt.hour

# Pulling out the year from the crash date (e.g., 2023, 2024) into a new column.
# It helps in yearly trend analysis.
df['YEAR'] = df['CRASH DATE'].dt.year

# Extracting the full month name (like 'January', 'February') from the date.
# It makes charts and visuals easier to read than using just numbers (1, 2, 3).
df['MONTH'] = df['CRASH DATE'].dt.month_name()

#-----------------------DONE-----------------------------------------------------------------------

# Filtering to last 5 years because the data is huge.
df = df[df['YEAR'] >= 2021]

# Drop any remaining rows with null value(s)
df = df.dropna()

# Saving the cleaned dataset to a new csv file named "cleaned_nyc_collisions.csv"
df.to_csv("cleaned_nyc_collisions.csv", index=False)
print("Cleaned data saved to cleaned_collisions.csv")    #prints a confirmation message to let us know if the file was saved.
print("Shape:", df.shape)   #Prints the shape of the final DataFrame: [Shape: (Rows, Columns)]

# Printing an overview of the cleaned dataset.
print(df.head())