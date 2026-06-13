from unittest.mock import patch, MagicMock
from app.db import (
    create_session,
    save_preferences,
    get_preferences,
    save_results,
    get_results,
    session_exists,
)


def _mock_client():
    return MagicMock()


def test_create_session_returns_uuid():
    mock_client = _mock_client()
    mock_client.table.return_value.insert.return_value.execute.return_value.data = [
        {"id": "abc-123"}
    ]
    with patch("app.db.get_client", return_value=mock_client):
        result = create_session()
    assert result == "abc-123"


def test_save_preferences_inserts_row():
    mock_client = _mock_client()
    with patch("app.db.get_client", return_value=mock_client):
        save_preferences("session-1", "a", {
            "genres": ["Action"],
            "mood": "fun",
            "min_rating": 3.0,
            "year_from": 2000,
            "year_to": 2023,
            "content_type": "movies",
        })
    mock_client.table.assert_called_with("preferences")
    mock_client.table.return_value.insert.assert_called_once()
    inserted = mock_client.table.return_value.insert.call_args[0][0]
    assert inserted["partner"] == "a"
    assert inserted["session_id"] == "session-1"


def test_get_preferences_returns_list():
    mock_client = _mock_client()
    mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {"partner": "a", "genres": ["Action"]},
        {"partner": "b", "genres": ["Comedy"]},
    ]
    with patch("app.db.get_client", return_value=mock_client):
        result = get_preferences("session-1")
    assert len(result) == 2
    assert result[0]["partner"] == "a"


def test_save_results_inserts_and_updates_status():
    mock_client = _mock_client()
    recs = [
        {"movie_id": 1, "title": "Movie A", "score": 0.9, "explanation": "Great", "rank": 1}
    ]
    with patch("app.db.get_client", return_value=mock_client):
        save_results("session-1", recs)
    calls = [str(c) for c in mock_client.table.call_args_list]
    assert any("results" in c for c in calls)
    assert any("sessions" in c for c in calls)


def test_get_results_returns_ordered_list():
    mock_client = _mock_client()
    mock_client.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = [
        {"rank": 1, "title": "Movie A"},
        {"rank": 2, "title": "Movie B"},
    ]
    with patch("app.db.get_client", return_value=mock_client):
        result = get_results("session-1")
    assert result[0]["rank"] == 1


def test_session_exists_true():
    mock_client = _mock_client()
    mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [
        {"id": "abc-123"}
    ]
    with patch("app.db.get_client", return_value=mock_client):
        assert session_exists("abc-123") is True


def test_session_exists_false():
    mock_client = _mock_client()
    mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    with patch("app.db.get_client", return_value=mock_client):
        assert session_exists("no-such-id") is False
