def test_index_redirects_to_partner_a(client, mock_db):
    response = client.get("/")
    assert response.status_code == 302
    assert "/partner/a" in response.location


def test_partner_a_get_renders_form(client, mock_db):
    with client.session_transaction() as sess:
        sess["session_id"] = "test-session-id"
    response = client.get("/partner/a")
    assert response.status_code == 200
    assert b"Partner A" in response.data or b"partner" in response.data.lower()


def test_partner_a_post_saves_and_redirects(client, mock_db):
    with client.session_transaction() as sess:
        sess["session_id"] = "test-session-id"
    response = client.post("/partner/a", data={
        "genres": ["Action", "Drama"],
        "mood": "excited",
        "year_from": "2000",
        "year_to": "2023",
    })
    assert response.status_code == 302
    assert "/partner/b" in response.location


def test_partner_b_get_renders_form(client, mock_db):
    with client.session_transaction() as sess:
        sess["session_id"] = "test-session-id"
    response = client.get("/partner/b")
    assert response.status_code == 200
    assert b"Partner B" in response.data or b"partner" in response.data.lower()


def test_partner_b_post_triggers_recommend_and_redirects(client, mock_db):
    with client.session_transaction() as sess:
        sess["session_id"] = "test-session-id"
    response = client.post("/partner/b", data={
        "genres": ["Comedy"],
        "mood": "relaxed",
        "year_from": "1995",
        "year_to": "2023",
    })
    assert response.status_code == 302
    assert "/results/test-session-id" in response.location


def test_results_page_renders_cards(client, mock_db):
    response = client.get("/results/test-session-id")
    assert response.status_code == 200
    assert b"Movie A" in response.data


def test_results_invalid_session_returns_404(client):
    from unittest.mock import patch
    with patch("app.app.session_exists", return_value=False):
        response = client.get("/results/bad-session-id")
    assert response.status_code == 404
