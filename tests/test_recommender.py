from unittest.mock import patch, MagicMock, mock_open
import pickle
import numpy as np
from model.recommender import MovieRecommender


def _make_recommender():
    mock_model = MagicMock()
    mock_model.predict.side_effect = lambda x: np.array([4.0])
    with patch("builtins.open", mock_open(read_data=b"")), \
         patch("pickle.load", return_value=mock_model):
        rec = MovieRecommender("model.pkl")
    return rec, mock_model


def test_movie_recommender_loads_model():
    rec, _ = _make_recommender()
    assert rec.model is not None


def test_predict_ratings_returns_floats_clamped():
    rec, mock_model = _make_recommender()
    mock_model.predict.side_effect = lambda x: np.array([6.0])  # above max
    ratings = rec.predict_ratings(user_id=1, movie_ids=[1, 2, 3])
    assert len(ratings) == 3
    assert all(r <= 5.0 for r in ratings)


def test_predict_ratings_low_clamped():
    rec, mock_model = _make_recommender()
    mock_model.predict.side_effect = lambda x: np.array([0.0])  # below min
    ratings = rec.predict_ratings(user_id=1, movie_ids=[1])
    assert ratings[0] >= 1.0


def test_find_compatible_movies_returns_sorted_tuples():
    rec, mock_model = _make_recommender()
    call_count = [0]

    def alternating_predict(x):
        call_count[0] += 1
        return np.array([4.0 if call_count[0] % 2 == 0 else 3.0])

    mock_model.predict.side_effect = alternating_predict
    results = rec.find_compatible_movies(
        user_a_id=1, user_b_id=2, all_movie_ids=[1, 2, 3], threshold=3.0
    )
    assert isinstance(results, list)
    assert all(isinstance(r, tuple) and len(r) == 2 for r in results)
    scores = [s for _, s in results]
    assert scores == sorted(scores, reverse=True)


def test_find_compatible_movies_filters_by_threshold():
    rec, mock_model = _make_recommender()
    mock_model.predict.side_effect = lambda x: np.array([2.0])  # below threshold
    results = rec.find_compatible_movies(
        user_a_id=1, user_b_id=2, all_movie_ids=[1, 2, 3], threshold=3.5
    )
    assert results == []


def test_find_compatible_movies_randomizes_tied_scores():
    rec, mock_model = _make_recommender()
    mock_model.predict.side_effect = lambda x: np.array([4.0])  # all movies tie
    movie_ids = list(range(1, 11))

    orderings = set()
    for _ in range(20):
        results = rec.find_compatible_movies(
            user_a_id=1, user_b_id=2, all_movie_ids=movie_ids, threshold=3.0
        )
        orderings.add(tuple(movie_id for movie_id, _ in results))

    assert len(orderings) > 1
