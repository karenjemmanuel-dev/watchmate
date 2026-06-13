from model.recommender import recommend


def test_recommend_returns_list_of_dicts():
    partner_a = {
        "genres": ["Action"], "mood": "fun",
        "min_rating": 3.0, "year_from": 2000, "year_to": 2023,
        "content_type": "movies"
    }
    partner_b = {
        "genres": ["Comedy"], "mood": "relaxed",
        "min_rating": 3.5, "year_from": 1995, "year_to": 2023,
        "content_type": "both"
    }
    results = recommend(partner_a, partner_b)
    assert isinstance(results, list)
    assert 3 <= len(results) <= 5


def test_recommend_result_has_required_keys():
    partner_a = {
        "genres": ["Drama"], "mood": "thoughtful",
        "min_rating": 4.0, "year_from": 1990, "year_to": 2020,
        "content_type": "both"
    }
    partner_b = {
        "genres": ["Drama"], "mood": "emotional",
        "min_rating": 3.0, "year_from": 1985, "year_to": 2020,
        "content_type": "movies"
    }
    results = recommend(partner_a, partner_b)
    required_keys = {"movie_id", "title", "score", "explanation", "rank"}
    for item in results:
        assert required_keys.issubset(item.keys())


def test_recommend_ranks_are_sequential():
    partner_a = {
        "genres": ["Thriller"], "mood": "tense",
        "min_rating": 3.0, "year_from": 2000, "year_to": 2023,
        "content_type": "movies"
    }
    partner_b = {
        "genres": ["Thriller"], "mood": "excited",
        "min_rating": 3.0, "year_from": 2000, "year_to": 2023,
        "content_type": "movies"
    }
    results = recommend(partner_a, partner_b)
    ranks = [r["rank"] for r in results]
    assert ranks == list(range(1, len(results) + 1))
