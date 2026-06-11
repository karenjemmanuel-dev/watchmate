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