import pickle
import random
import numpy as np

class MovieRecommender:
    def __init__(self, model_path='model.pkl'):
        """Load the trained model."""
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        print("Model loaded successfully")
    
    def predict_ratings(self, user_id, movie_ids):
        """
        Predict ratings for a user across multiple movies.
        
        Args:
            user_id: Integer user ID (1-943)
            movie_ids: List of movie IDs (1-1682)
        
        Returns:
            List of predicted ratings (1.0-5.0)
        """
        predictions = []
        for movie_id in movie_ids:
            pred = self.model.predict([[user_id, movie_id]])[0]
            # Clamp to 1-5 range
            pred = max(1.0, min(5.0, pred))
            predictions.append(pred)
        return predictions
    
    def find_compatible_movies(self, user_a_id, user_b_id, all_movie_ids, threshold=3.5):
        """
        Find movies both users would likely enjoy.
        
        Args:
            user_a_id: First user's ID
            user_b_id: Second user's ID
            all_movie_ids: List of all movie IDs to check
            threshold: Minimum average rating threshold (default 3.5)
        
        Returns:
            List of (movie_id, avg_score) tuples, sorted by score
        """
        compatible = []
        
        for movie_id in all_movie_ids:
            # Get predictions for both users
            pred_a = self.model.predict([[user_a_id, movie_id]])[0]
            pred_b = self.model.predict([[user_b_id, movie_id]])[0]
            
            # Clamp to 1-5
            pred_a = max(1.0, min(5.0, pred_a))
            pred_b = max(1.0, min(5.0, pred_b))
            
            # Average their scores
            avg_score = (pred_a + pred_b) / 2
            
            # Only include if both would likely enjoy
            if avg_score >= threshold:
                compatible.append((movie_id, avg_score))
        
        # Shuffle first so movies tied on score (common with this model)
        # aren't always broken in the same movie_id order, then sort by
        # score descending.
        random.shuffle(compatible)
        compatible.sort(key=lambda x: x[1], reverse=True)
        return compatible