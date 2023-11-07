import sqlite3

# Connect to the database
conn = sqlite3.connect('LiveTracking.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Retrieve all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# cursor.execute("""
#         CREATE TABLE IF NOT EXISTS persons (
#         frame_count INTEGER NOT NULL,
#         start_time INTEGER NOT NULL,
#         certainty REAL NOT NULL,
#         x INTEGER NOT NULL,
#         y INTEGER NOT NULL,
#         w INTEGER NOT NULL,
#         h INTEGER NOT NULL)
#     """)

# cursor.execute("""
#                 DROP TABLE IF EXISTS persons
#                 """)

tables = cursor.fetchall()

# Print all tables and their contents
for table in tables:
    print(f"Contents of table {table[0]}:")
    cursor.execute(f"SELECT * FROM {table[0]};")
    for row in cursor.fetchall():
        print(row)

print("Thats it!")
# Close the connection
conn.close()