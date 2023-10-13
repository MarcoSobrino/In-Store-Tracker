import csv
import pandas as pd
import io
from databaseInsert import insert_register_data
from datetime import datetime
import decimal

def registerData(file_path):
    csv_data  = []
    with open(file_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
    
        for row in csv_reader:
            cleaned_row = [field.strip() for field in row]
            csv_data.append(cleaned_row)

    cleaned_data = [[field.strip() for field in row] for row in csv_data]

    # Create a Pandas DataFrame from the cleaned data
    df = pd.DataFrame(cleaned_data)

    # Extract and print the desired columns
    columns_to_extract = [0, 1, 2, 3, 4, 6, 8, 9, 10]  # RegID, Date/Time, Tender, User, Customer, SubTotal, Tax, Total
    df = df[columns_to_extract]

    # You can replace 'Attribute' with the actual name of the first column
    df[0] = df[0].str.strip()  # Remove leading/trailing whitespace

    # Filter the DataFrame based on the length of the first column
    df = df[df[0].str.len() > 0]

    df = df.iloc[5:]  # This selects all rows starting from the 6th row (index 5)

    # Set the first row as column names
    df.columns = df.iloc[0]

    # Skip the first row, as it is now the header
    df = df.iloc[1:]

    # Reset the index after skipping the first row
    df.reset_index(drop=True, inplace=True)

    df.columns.values[1] = 'Date'
    df.columns.values[2] = 'Time'

    df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y').strftime('%Y-%m-%d'))
    df['Time'] = df['Time'].apply(lambda x: datetime.strptime(x, '%I:%M%p').strftime('%H:%M:%S'))
    # df['SubTotal'] = df['SubTotal'].apply(convert_to_decimal)

    print(df)

    insert_register_data(df)

def registerDF(file):
    df = pd.read_csv(file)
    print(df)

# Function to convert the string to DECIMAL
def convert_to_decimal(money_string):
    return decimal.Decimal(money_string.replace('$', ''))

    

if __name__ == '__main__':
    # registerDF('/Users/marcosobr/Desktop/Science of Computers/SeniorProject/In-Store-Tracker/LiveTracking/Register_Transaction_Activity_0316231925.csv')
    registerData('/Users/marcosobr/Desktop/Science of Computers/SeniorProject/In-Store-Tracker/LiveTracking/Register_Transaction_Activity_0316231925.csv')

