import pandas as pd

# Load data
ratings = pd.read_csv('data/u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])
movies = pd.read_csv('data/u.item', sep='|', encoding='latin-1',
                     names=['movie_id', 'title', 'release_date', 'video_release', 'imdb_url',
                            'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy',
                            'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                            'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])

# Merge
data = pd.merge(ratings, movies[['movie_id', 'title']], on='movie_id')

# Save clean data
data.to_csv('outputs/clean_data.csv', index=False)
print("✓ Clean data saved to outputs/clean_data.csv")
print(f"  Shape: {data.shape}")