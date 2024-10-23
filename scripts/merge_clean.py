
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def merge_and_clean():


    # File paths
    artist_data_file = './data/artist_data.csv'
    spotify_data_file = './data/spotify_data.csv'
    tag_artist_data_file = './data/tag_artist_data.csv'
    tag_genre_data_file = './data/tag_genre_data.csv'

    # Load CSV files into dataframes
    artist_data = pd.read_csv(artist_data_file)
    spotify_data = pd.read_csv(spotify_data_file)
    tag_artist_data = pd.read_csv(tag_artist_data_file)
    tag_genre_data = pd.read_csv(tag_genre_data_file)

    # Inspect the data
    print("Artist Data:")
    print(artist_data.head(), '\n')

    print("Spotify Data:")
    print(spotify_data.head(), '\n')

    print("Tag Artist Data:")
    print(tag_artist_data.head(), '\n')

    print("Tag Genre Data:")
    print(tag_genre_data.head(), '\n')


    # Merge artist_data and spotify_data on 'user_id'
    merged_df = artist_data.merge(spotify_data, on='user_id', how='left')
    # Merge the result with tag_artist_data on 'user_id'
    merged_df = merged_df.merge(tag_artist_data, on='user_id', how='left')
    # Merge the result with tag_genre_data on 'tag_id'
    merged_df = merged_df.merge(tag_genre_data, on='tag_id', how='left')


    # Preview the first few rows of the merged data
    print(merged_df.head())


    # Load the merged dataframe (assume df is already available)
    # df = pd.read_csv('merged_data.csv')  # Example if loading from a file

    # 1. Column Data Types
    print("\nColumn Data Types:")
    print(merged_df.dtypes)

    # Ensure all values are compatible with their data type
    merged_df['spendings'] = pd.to_numeric(merged_df['spendings'], errors='coerce')  
    merged_df['user_id'] = merged_df['user_id'].astype('int64')  
    merged_df['tag_id'] = merged_df['tag_id'].astype('int64') 

    # 2. Missing Values
    print("\nMissing Values:")
    print(merged_df.isnull().sum())


    # 3. Duplicate Rows
    duplicate_rows = merged_df[merged_df.duplicated()]
    print(f"\nDuplicate Rows: {len(duplicate_rows)}")

    # 4. Duplicate Artist Entries (by 'user_id' or 'artist_name')
    duplicate_artists = merged_df[merged_df.duplicated(subset=['user_id', 'artist_name'])]
    print(f"\nDuplicate Artist Entries: {len(duplicate_artists)}")

    # 5. Unique Artists
    unique_artists = merged_df['user_id'].nunique()
    print(f"\nUnique Artists: {unique_artists}")

    # 6. Unique Genres
    unique_genres = merged_df['genre'].nunique()
    print(f"\nUnique Genres: {unique_genres}")

    # 7. Tag-Genre Association (Check consistency)
    tag_genre_association = merged_df[['tag_id', 'genre']].drop_duplicates()
    inconsistent_tag_genre = tag_genre_association[tag_genre_association.duplicated(subset='tag_id')]
    print(f"\nInconsistent Tag-Genre Mappings: {len(inconsistent_tag_genre)}")

    # 8. Spendings Summary
    print("\nSpendings Summary:")
    print(merged_df['spendings'].describe())

    # 9. Outliers in Spendings (using Z-scores)
    merged_df['spendings_zscore'] = np.abs(stats.zscore(merged_df['spendings'].dropna()))  # Calculate Z-score for non-null values
    outliers = merged_df[merged_df['spendings_zscore'] > 3]  # Outliers where Z-score > 3
    print(f"\nOutliers in Spendings: {len(outliers)}")

    # 10. User-Artist Relationship (Check unique relationship)
    user_artist_relationship = merged_df[['user_id', 'artist_name']].drop_duplicates()
    multiple_artists_per_user = user_artist_relationship[user_artist_relationship.duplicated('user_id')]
    print(f"\nUsers with Multiple Artists: {len(multiple_artists_per_user)}")

    # 11. User-Spotify Relationship (Validate uniqueness of spotify_id)
    unique_user_spotify = merged_df[['user_id', 'spotify_id']].drop_duplicates()
    duplicate_spotify_ids = unique_user_spotify[unique_user_spotify.duplicated('user_id')]
    print(f"\nUsers with Duplicate Spotify IDs: {len(duplicate_spotify_ids)}")

    # 12. Artist-Genre Relationship (Check valid tag_id and genre)
    artist_genre_relationship = merged_df[['user_id', 'tag_id', 'genre']].drop_duplicates()
    invalid_tag_genre = artist_genre_relationship[artist_genre_relationship['tag_id'].isnull()]
    print(f"\nInvalid Tag-Genre Entries: {len(invalid_tag_genre)}")

    # 13. Popular Genres (Frequency distribution)
    print("\nPopular Genres (Top 5):")
    print(merged_df['genre'].value_counts().head(5))

    # 14. Genre Coverage (Percentage of artists associated with each genre)
    artist_per_genre = merged_df.groupby('genre')['user_id'].nunique()
    genre_coverage = (artist_per_genre / merged_df['user_id'].nunique()) * 100
    print("\nGenre Coverage (% of artists per genre):")
    print(genre_coverage)


    # 16. Spending by Genre (Average spendings per genre)
    avg_spendings_per_genre = merged_df.groupby('genre')['spendings'].mean().sort_values(ascending=False)
    print("\nAverage Spendings by Genre:")
    print(avg_spendings_per_genre)

    # 17. Artists with Multiple Genres (Count of unique genres per artist)
    artist_multiple_genres = merged_df.groupby('user_id')['genre'].nunique()
    artists_with_multiple_genres = artist_multiple_genres[artist_multiple_genres > 1]
    print(f"\nArtists with Multiple Genres: {len(artists_with_multiple_genres)}")

    # 19. Inconsistent Tag-Genre Mappings (Check tag_id-genre consistency)
    inconsistent_mappings = merged_df.groupby('tag_id')['genre'].nunique()
    inconsistent_tags = inconsistent_mappings[inconsistent_mappings > 1]
    print(f"\nInconsistent Tag-Genre Mappings: {len(inconsistent_tags)}")

    # 20. ID Integrity (Check orphan records for user_id, spotify_id, tag_id)
    orphan_user_id = merged_df[merged_df['user_id'].isnull()]
    orphan_spotify_id = merged_df[merged_df['spotify_id'].isnull()]
    orphan_tag_id = merged_df[merged_df['tag_id'].isnull()]
    print(f"\nOrphan Records (User ID): {len(orphan_user_id)}")
    print(f"Orphan Records (Spotify ID): {len(orphan_spotify_id)}")
    print(f"Orphan Records (Tag ID): {len(orphan_tag_id)}")



    # 22. Spending by Genre Comparison (Total/average spendings per genre)
    total_spendings_per_genre = merged_df.groupby('genre')['spendings'].sum()
    print("\nTotal Spendings by Genre:")
    print(total_spendings_per_genre)


    # Fill missing artist_name values with "Unknown Artist"
    merged_df['artist_name'].fillna("Unknown Artist", inplace=True)

    # Verify if the missing artist_name values have been filled
    remaining_missing_artist = merged_df['artist_name'].isna().sum()
    print(f"\nRemaining missing artist_name values after filling: {remaining_missing_artist}")

    # Optionally, display the rows where artist_name was previously missing
    filled_rows = merged_df[merged_df['artist_name'] == "Unknown Artist"]
    print("\nRows where artist_name was filled with 'Unknown Artist':")
    print(filled_rows)


    # 2. Missing Values
    print("\nMissing Values:")
    print(merged_df.isnull().sum())

    # Remove the spendings_zscore column
    if 'spendings_zscore' in merged_df.columns:
        merged_df.drop(columns=['spendings_zscore'], inplace=True)
        print("\n'spendings_zscore' column removed from the DataFrame.")
    # Step 23: Save the cleaned DataFrame for database injection
    cleaned_file_path = './output/cleaned_artist_data.csv'
    merged_df.to_csv(cleaned_file_path, index=False)

    print(f"\nCleaned DataFrame saved to {cleaned_file_path} for database injection.")
if __name__ == "__main__":
    merge_and_clean()