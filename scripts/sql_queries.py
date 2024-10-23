from sqlalchemy import create_engine, text
import pandas as pd
import tkinter as tk
from tkinter import messagebox

def execute_and_display_query(query, sqlite_db_path):
    # Connect to the SQLite database
    connection_string = f'sqlite:///{sqlite_db_path}'
    engine = create_engine(connection_string)

    # Execute the query and fetch results
    with engine.connect() as connection:
        # Use text() to explicitly define the query
        result = connection.execute(text(query.strip()))  # Strip any whitespace/newline characters
        df = pd.DataFrame(result.fetchall(), columns=result.keys())  # Convert to DataFrame

    # Display results in a pop-up window
    display_results_in_popup(df)

def display_results_in_popup(df):
    # Create a new Tkinter window
    root = tk.Tk()
    root.title("SQL Query Results")
    
    # Create a message to display results
    message = df.to_string(index=False)
    
    # Create a scrollable text widget
    text = tk.Text(root, wrap=tk.WORD)
    text.insert(tk.END, message)
    text.config(state=tk.DISABLED)  # Make the text read-only
    text.pack(expand=True, fill=tk.BOTH)

    # Create an OK button to close the window
    ok_button = tk.Button(root, text="OK", command=root.destroy)
    ok_button.pack(pady=10)

    root.mainloop()

def execute_queries():
    # Path to the SQLite database
    sqlite_db_path = './data/GrooverDB.db'

    # Define your SQL queries
    queries = {
    'most_popular_genres': '''
        SELECT genre, COUNT(DISTINCT user_id) AS artist_count
        FROM GrooverDB
        GROUP BY genre
        ORDER BY artist_count DESC
        LIMIT 2;
    ''',

    'artists_with_multiple_genres': '''
        SELECT user_id, artist_name, COUNT(DISTINCT genre) AS genre_count
        FROM GrooverDB
        GROUP BY user_id, artist_name
        HAVING genre_count > 1;
    ''',

    'aggregate_artists_genres_info': '''
        WITH genre_counts AS (
            SELECT 
                genre,
                COUNT(DISTINCT user_id) AS total_artists
            FROM 
                GrooverDB
            GROUP BY 
                genre
        ),
        total_artists_count AS (
            SELECT COUNT(DISTINCT user_id) AS total_artists_count
            FROM GrooverDB
        )
        SELECT 
            g.spotify_id,
            g.user_id,
            g.artist_name,
            GROUP_CONCAT(DISTINCT g.genre) AS genres,
            COUNT(DISTINCT g.genre) AS total_genres,
            gc.total_artists,
            (gc.total_artists * 100.0 / tac.total_artists_count) AS genre_popularity
        FROM 
            GrooverDB g
        JOIN genre_counts gc ON g.genre = gc.genre
        CROSS JOIN total_artists_count tac
        GROUP BY 
            g.spotify_id, g.user_id, g.artist_name
        ORDER BY 
            g.spotify_id;
    ''',
    'order_artists_by_genre': '''
        SELECT DISTINCT genre, artist_name
        FROM GrooverDB
        ORDER BY genre, artist_name;
    ''',

    'genres_spending_most': '''
        SELECT genre, AVG(spendings) AS average_spending
        FROM GrooverDB
        GROUP BY genre
        ORDER BY average_spending DESC;
    '''
}
    # Execute the most popular genres query
    execute_and_display_query(queries['most_popular_genres'], sqlite_db_path)

    # Execute the artists with multiple genres query
    execute_and_display_query(queries['artists_with_multiple_genres'], sqlite_db_path)

    # Execute the aggregate artists genres information query
    execute_and_display_query(queries['aggregate_artists_genres_info'], sqlite_db_path)
    execute_and_display_query(queries['order_artists_by_genre'], sqlite_db_path)
    execute_and_display_query(queries['genres_spending_most'], sqlite_db_path)

if __name__ == "__main__":
    execute_queries()
