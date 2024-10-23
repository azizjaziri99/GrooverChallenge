from scripts.merge_clean import merge_and_clean  # Import the merge_and_clean function
from scripts.inject_to_db import inject_data_to_db  # Import the inject_data_to_db function
from scripts.sql_queries import execute_queries  # Import the execute_queries function

def main():
    # Step 1: Merge and Clean Data
    print("Starting the merge and cleaning process...")
    merge_and_clean()  # Call the function to merge and clean data

    # Step 2: Inject Data into Database
    print("Injecting data into the database...")
    inject_data_to_db()  # Call the function to inject data into the database

    # Step 3: Execute SQL Queries
    print("Executing SQL queries...")
    execute_queries()  # Call the function to execute and display SQL queries

if __name__ == "__main__":
    main()
