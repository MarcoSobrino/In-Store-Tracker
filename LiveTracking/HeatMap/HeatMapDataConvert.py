import pandas as pd
from sqalchemy import create_engine

def convert_heatmap_data():
    # Replace 'your_file.db' with the path to your local SQLite database file
    database_url = 'sqlite:///LiveTracking.db'

    # Create a database connection using SQLAlchemy
    engine = create_engine(database_url)

    # Assuming 'your_table' is the name of the destination table in your database
    table_name = 'HeatMap'

    # Read the data from the SQL table into a Pandas DataFrame
    sql_query = f"SELECT * FROM {table_name}"
    df_sql = pd.read_sql_query(sql_query, engine)

    # Read the data from the CSV file into another Pandas DataFrame
    df_csv = pd.read_csv('test.csv')

    # Merge the data from the SQL table into the CSV DataFrame based on a common column
    common_column = 'A'  # Replace with the actual common column name
    df_merged = pd.merge(df_csv, df_sql, on=common_column, how='left', suffixes=('_csv', '_sql'))

    # Update the CSV DataFrame with the data from the SQL DataFrame
    # Fill missing values in the CSV DataFrame with data from the SQL DataFrame
    for col in df_csv.columns:
        if f"{col}_sql" in df_merged.columns:
            df_csv[col] = df_merged[f"{col}_sql"].combine_first(df_merged[f"{col}_csv"])

    # Save the updated CSV DataFrame back to the CSV file
    df_csv.to_csv('test.csv', index=False)


    # Close the database connection
    engine.dispose()

convert_heatmap_data()