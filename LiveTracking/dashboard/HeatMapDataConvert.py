import pandas as pd
import sqlite3
import os

def convert_heatmap_data(date):
    # Connect to the local SQLite database
    conn = sqlite3.connect('LiveTracking.db')

    if not conn:
        print("Error connecting to the database.")
        return

    # Query the database to retrieve the data for the specified date
    query = f"SELECT Date, A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P FROM HeatMap WHERE Date = '{date}'"
    df = pd.read_sql_query(query, conn)

    # Close the database connection when done
    conn.close()

    if not df.empty:
        # Extract the data values from the row
        data_values = df.iloc[0, 1:].values

        # Reshape the data into a 4x4 grid
        data_grid = [data_values[i:i+4] for i in range(0, len(data_values), 4)]

        # Create a DataFrame with the 4x4 grid
        grid_df = pd.DataFrame(data_grid, columns=['A', 'B', 'C', 'D'], index=['d', 'c', 'b', 'a'])

        # Write the DataFrame to a CSV file
        grid_df.to_csv('test.csv')

        # Move the CSV file to the HeatMap directory and replace if it already exists
        os.replace('test.csv', os.path.join(os.path.dirname(__file__), 'test.csv'))

        print("Success")

convert_heatmap_data('12/01/23')
