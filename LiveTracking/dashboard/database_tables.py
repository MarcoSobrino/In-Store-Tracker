import sqlite3

# Connect to the database
conn = sqlite3.connect('LiveTracking.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Retrieve all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")
    
    # Retrieve the table structure
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    # Print the details of each column in the table
    for column in columns:
        print(f"  Column: {column[1]}, Type: {column[2]}")
    print()

cursor.execute("SELECT * FROM running")
print(cursor.fetchall())



# Close the connection
conn.close()