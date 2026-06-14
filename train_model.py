import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle
import os

# ============================================================================
# STEP 1: Load Data
# ============================================================================
print("Loading data...")
ratings = pd.read_csv('data/u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])
movies = pd.read_csv('data/u.item', sep='|', encoding='latin-1',
                     names=['movie_id', 'title', 'release_date', 'video_release', 'imdb_url',
                            'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy',
                            'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                            'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])

print(f"✓ Loaded {len(ratings)} ratings and {len(movies)} movies")

# ============================================================================
# STEP 2: Prepare Data for Modeling
# ============================================================================
print("\nPreparing data for modeling...")

# Create feature matrix: just user_id and movie_id
# The model will learn: given these two IDs, predict the rating
X = ratings[['user_id', 'movie_id']].values
y = ratings['rating'].values

print(f"✓ Features shape: {X.shape}")
print(f"✓ Target shape: {y.shape}")

# ============================================================================
# STEP 3: Train/Test Split
# ============================================================================
print("\nSplitting data into train (80%) and test (20%)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"✓ Training set: {X_train.shape[0]} samples")
print(f"✓ Test set: {X_test.shape[0]} samples")

# ============================================================================
# STEP 4: Train Model 1 - Random Forest
# ============================================================================
print("\n" + "="*60)
print("TRAINING MODEL 1: RANDOM FOREST")
print("="*60)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
rf_mae = mean_absolute_error(y_test, rf_pred)
rf_r2 = r2_score(y_test, rf_pred)

print(f"\nRandom Forest Results:")
print(f"  RMSE: {rf_rmse:.4f}")
print(f"  MAE:  {rf_mae:.4f}")
print(f"  R²:   {rf_r2:.4f}")

# ============================================================================
# STEP 5: Train Model 2 - Gradient Boosting
# ============================================================================
print("\n" + "="*60)
print("TRAINING MODEL 2: GRADIENT BOOSTING")
print("="*60)

gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb_model.fit(X_train, y_train)

gb_pred = gb_model.predict(X_test)
gb_rmse = np.sqrt(mean_squared_error(y_test, gb_pred))
gb_mae = mean_absolute_error(y_test, gb_pred)
gb_r2 = r2_score(y_test, gb_pred)

print(f"\nGradient Boosting Results:")
print(f"  RMSE: {gb_rmse:.4f}")
print(f"  MAE:  {gb_mae:.4f}")
print(f"  R²:   {gb_r2:.4f}")

# ============================================================================
# STEP 6: Compare Models
# ============================================================================
print("\n" + "="*60)
print("MODEL COMPARISON")
print("="*60)

print(f"\n{'Metric':<15} {'Random Forest':<20} {'Gradient Boosting':<20}")
print("-" * 55)
print(f"{'RMSE':<15} {rf_rmse:<20.4f} {gb_rmse:<20.4f}")
print(f"{'MAE':<15} {rf_mae:<20.4f} {gb_mae:<20.4f}")
print(f"{'R²':<15} {rf_r2:<20.4f} {gb_r2:<20.4f}")

# Select the better model (lower RMSE)
if rf_rmse < gb_rmse:
    winner = "Random Forest"
    best_model = rf_model
    best_rmse = rf_rmse
else:
    winner = "Gradient Boosting"
    best_model = gb_model
    best_rmse = gb_rmse

print(f"\n🏆 Winner: {winner} (RMSE: {best_rmse:.4f})")

# ============================================================================
# STEP 7: Save the Model
# ============================================================================
print("\nSaving model...")
with open('model.pkl', 'wb') as f:
    pickle.dump(best_model, f)
print(f"✓ Model saved to model.pkl")

# ============================================================================
# STEP 8: Test with Sample Predictions
# ============================================================================
print("\n" + "="*60)
print("SAMPLE PREDICTIONS")
print("="*60)

# Get a few examples from test set
sample_indices = [0, 100, 500, 1000, 5000]
print(f"\n{'User':<10} {'Movie':<10} {'Actual':<10} {'Predicted':<10} {'Error':<10}")
print("-" * 50)

for idx in sample_indices:
    user_id, movie_id = X_test[idx]
    actual = y_test[idx]
    predicted = best_model.predict([[user_id, movie_id]])[0]
    error = abs(actual - predicted)
    print(f"{user_id:<10} {movie_id:<10} {actual:<10.2f} {predicted:<10.2f} {error:<10.2f}")

print("\n✓ Training complete!")
