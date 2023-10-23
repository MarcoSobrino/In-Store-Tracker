import pandas as pd
from sqlalchemy import create_engine

def insert_register_data(df):

    # Replace 'your_file.db' with the path to your local SQLite database file
    database_url = 'sqlite:///LiveTracking.db'

    # Create a database connection using SQLAlchemy
    engine = create_engine(database_url)

    # Assuming 'your_table' is the name of the destination table in your database
    table_name = 'Register'

    # Assuming you have a DataFrame named 'df'
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

    # Close the database connection
    engine.dispose()
