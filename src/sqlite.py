import sqlite3
import os

# Path to your database folder
db_folder = "data/test/"

# Loop through all .sqlite files in the folder
for db_file in os.listdir(db_folder):
    if db_file.endswith(".sqlite"):
        db_path = os.path.join(db_folder, db_file)
        print(f"\n--- Database: {db_file} ---")

        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables:", [t[0] for t in tables])

        # Show first 5 rows of each table
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
            rows = cursor.fetchall()
            print(f"\nTable: {table_name}")
            for row in rows:
                print(row)


        conn.close()
