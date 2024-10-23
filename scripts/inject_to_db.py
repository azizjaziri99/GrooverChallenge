import pandas as pd
from sqlalchemy import create_engine


def inject_data_to_db():

    # File path to the cleaned data
    cleaned_file_path = './output/cleaned_artist_data.csv'

    # Load the cleaned DataFrame
    cleaned_df = pd.read_csv(cleaned_file_path)

    # SQLite database connection details
    sqlite_db_path = './data/GrooverDB.db'  # Path to your SQLite database file
    table_name = 'GrooverDB'  # Name of the table to insert data into

    # Create a database connection string
    connection_string = f'sqlite:///{sqlite_db_path}'
    engine = create_engine(connection_string)

    # Insert data into the database table
    try:
        cleaned_df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Data successfully inserted into {table_name} table.")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")
        
        
if __name__ == "__main__":
    inject_data_to_db()