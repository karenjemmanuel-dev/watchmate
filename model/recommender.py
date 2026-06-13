def recommend(partner_a: dict, partner_b: dict) -> list[dict]:
    """
    Stub — returns dummy results until Karen's model.pkl is ready.
    Real implementation will replace this body; the signature must not change.
    """
    dummy = [
        {
            "movie_id": 1,
            "title": "The Shawshank Redemption",
            "score": 0.95,
            "explanation": "Highly rated drama both partners will enjoy.",
            "rank": 1,
        },
        {
            "movie_id": 2,
            "title": "Forrest Gump",
            "score": 0.91,
            "explanation": "Feel-good classic matching both moods.",
            "rank": 2,
        },
        {
            "movie_id": 3,
            "title": "The Dark Knight",
            "score": 0.88,
            "explanation": "High-rated thriller with broad appeal.",
            "rank": 3,
        },
    ]
    return dummy
