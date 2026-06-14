from model.recommender import MovieRecommender

print("Testing model integration...")

# Load model
recommender = MovieRecommender('model.pkl')

# Test 1: Predict for one user across 5 movies
print("\nTest 1: Predict ratings for user 1 on movies 1-5")
ratings = recommender.predict_ratings(1, [1, 2, 3, 4, 5])
for movie_id, rating in zip([1, 2, 3, 4, 5], ratings):
    print(f"  Movie {movie_id}: {rating:.2f}")

# Test 2: Find compatible movies for two users
print("\nTest 2: Find compatible movies for users 1 and 2")
all_movies = list(range(1, 101))  # Check first 100 movies
compatible = recommender.find_compatible_movies(1, 2, all_movies, threshold=3.5)
print(f"  Found {len(compatible)} compatible movies (threshold 3.5+)")
for movie_id, score in compatible[:5]:
    print(f"    Movie {movie_id}: {score:.2f}")

print("\n✓ Integration test passed!")