import pandas as pd

# Load ratings
ratings = pd.read_csv('data/u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])

# Load movies
movies = pd.read_csv('data/u.item', sep='|', encoding='latin-1',
                     names=['movie_id', 'title', 'release_date', 'video_release', 'imdb_url',
                            'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy',
                            'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                            'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])

print(movies[['movie_id', 'title']].head(10))
print(movies.shape)
# Merge ratings with movie titles
data = pd.merge(ratings, movies[['movie_id', 'title']], on='movie_id')
print(data.head(10))
print(data.shape)
# Check for missing values
print("Missing values in ratings:")
print(ratings.isnull().sum())

print("\nMissing values in movies:")
print(movies[['movie_id', 'title']].isnull().sum())

# Check rating range (should be 1-5 only)
print("\nRating range:")
print(ratings['rating'].min(), "to", ratings['rating'].max())

# Check for duplicate ratings (same user rating same movie twice)
duplicates = ratings.duplicated(subset=['user_id', 'movie_id']).sum()
print("\nDuplicate ratings:", duplicates)