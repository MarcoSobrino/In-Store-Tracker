import pandas as pd
import sqlite3
import os

def convert_heatmap_data(date):
    # Connect to the local SQLite database
    conn = sqlite3.connect('LiveTracking.db')

    if not conn:
        print("Error connecting to the database.")
        return

    # Specify the date you want to retrieve
    # date = '12/01/23'  # Replace with the actual date you want to retrieve

    # Query the database to retrieve the data for the specified date
    query = f"SELECT * FROM HeatMap WHERE Date = '{date}'"
    df = pd.read_sql_query(query, conn)

    # Close the database connection when done
    conn.close()

    # Create a 4x4 DataFrame from the retrieved data
    if not df.empty:
        # Extract the data values from the row
        data_values = df.iloc[0, 1:].values

        # Reshape the data into a 4x4 grid
        data_grid = [data_values[i:i+4] for i in range(0, len(data_values), 4)]

        # Create a DataFrame with the 4x4 grid
        grid_df = pd.DataFrame(data_grid)

    # Create a DataFrame with the desired row and column labels
    row_labels = ['d', 'c', 'b', 'a']
    col_labels = ['A', 'B', 'C', 'D']

    grid_df = pd.DataFrame(data_grid, columns=col_labels, index=row_labels)

    # Write the DataFrame to a CSV file with the first row as column names then save to same directory as this file
    grid_df.to_csv('test.csv')

    #move the csv file to the HeatMap directory and replace if already exits
    os.replace('test.csv', os.path.join(os.path.dirname(__file__), 'test.csv'))

    print("Success")

convert_heatmap_data('12/01/23')