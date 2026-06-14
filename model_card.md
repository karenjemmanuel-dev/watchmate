# WatchMate Model Card

## Model Details

**Model Name:** WatchMate Movie Recommendation Model
**Model Type:** Gradient Boosting Regressor
**Framework:** scikit-learn
**Created:** June 14, 2026

## Intended Use

Predict movie ratings for two users to find movies they both might enjoy watching together.

## Model Performance

- **RMSE (Test Set):** 1.0472
- **MAE (Test Set):** 0.8516
- **R² Score (Test Set):** 0.1317

### Performance Interpretation
- Average prediction error: ±1.05 stars (on 1-5 scale)
- Model explains ~13% of rating variance
- Reasonable baseline for collaborative filtering without user/movie features

## Training Data

- **Dataset:** MovieLens 100K
- **Size:** 100,000 ratings
- **Users:** 943
- **Movies:** 1,682
- **Train/Test Split:** 80% / 20%

## Input Features

- `user_id` (integer 1-943)
- `movie_id` (integer 1-1682)

## Output

- `prediction` (float 1.0-5.0) — predicted rating

## Limitations

1. **Simple features:** Only uses user and movie IDs, not content or user profiles
2. **Cold start problem:** Cannot predict for new users or movies
3. **Temporal bias:** Data from 1997 — preferences may have changed
4. **No implicit feedback:** Only explicit ratings, not viewing behavior

## Ethical Considerations

- **Potential bias:** May reflect biases in 1997 user demographics
- **Recommendation diversity:** Could recommend mainstream movies only
- **Privacy:** Individual user ratings aggregated into model

## Future Improvements

1. Add movie genres and user demographics as features
2. Implement matrix factorization for better accuracy
3. Add content-based filtering for new movies
4. Regular retraining with current data

## Model Card Version

Version 1.0 — Initial model card for course project