import pytest
from unittest.mock import patch


@pytest.fixture
def mock_db(monkeypatch):
    """Patches all db functions so routes don't hit Supabase."""
    with patch("app.app.create_session", return_value="test-session-id"), \
         patch("app.app.save_preferences"), \
         patch("app.app.get_preferences", return_value=[
             {"partner": "a", "genres": ["Action"], "mood": "fun",
              "min_rating": 3.0, "year_from": 2000, "year_to": 2023,
              "content_type": "movies"},
             {"partner": "b", "genres": ["Comedy"], "mood": "relaxed",
              "min_rating": 3.5, "year_from": 1995, "year_to": 2023,
              "content_type": "both"},
         ]), \
         patch("app.app.save_results"), \
         patch("app.app.get_results", return_value=[
             {"movie_id": 1, "title": "Movie A", "score": 0.9,
              "explanation": "Great pick", "rank": 1},
         ]), \
         patch("app.app.session_exists", return_value=True), \
         patch("app.app.recommend", return_value=[
             {"movie_id": 1, "title": "Movie A", "score": 0.9,
              "explanation": "Great pick", "rank": 1},
         ]):
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
