import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_db(monkeypatch):
    """Patches all db and ML calls so routes don't hit Supabase or load model.pkl."""
    mock_recommender = MagicMock()
    mock_recommender.find_compatible_movies.return_value = [(1, 3.9), (2, 3.7)]

    with patch("app.app.create_session", return_value="test-session-id"), \
         patch("app.app.save_preferences"), \
         patch("app.app.get_preferences", return_value=[
             {"partner": "a", "genres": ["Action"], "mood": "fun",
              "year_from": 2000, "year_to": 2023},
             {"partner": "b", "genres": ["Comedy"], "mood": "relaxed",
              "year_from": 1995, "year_to": 2023},
         ]), \
         patch("app.app.save_results"), \
         patch("app.app.get_results", return_value=[
             {"movie_id": 1, "title": "Movie A", "score": 0.9,
              "explanation": "Great pick", "rank": 1},
         ]), \
         patch("app.app.session_exists", return_value=True), \
         patch("app.app.MovieRecommender", return_value=mock_recommender), \
         patch("app.app.combine_mood_genres", return_value=["Action", "Comedy"]):
        yield


@pytest.fixture
def app():
    from app.app import app as flask_app
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "test-secret-key"
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()
