from app.mood_filter import combine_mood_genres, get_movie_synopses
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

from app.db import (
    create_session,
    save_preferences,
    get_preferences,
    save_results,
    get_results,
    session_exists,
)
from model.recommender import MovieRecommender

load_dotenv(override=True)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-fallback-secret")

print("Loading movie data...")
MOVIES_DF = pd.read_csv('data/u.item', sep='|', encoding='latin-1', header=None)
RATINGS_DF = pd.read_csv('data/u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])
print(f"Loaded {len(MOVIES_DF)} movies and {len(RATINGS_DF)} ratings")

GENRE_COLS = {
    "Action": 6, "Adventure": 7, "Animation": 8, "Comedy": 10,
    "Documentary": 12, "Drama": 13, "Fantasy": 14, "Horror": 16,
    "Romance": 19, "Sci-Fi": 20, "Thriller": 21,
}

GENRE_NAMES = {v: k for k, v in GENRE_COLS.items()}


def get_movie_title(movie_id):
    row = MOVIES_DF[MOVIES_DF[0] == movie_id]
    if len(row) > 0:
        return row.iloc[0][1]
    return f"Movie {movie_id}"


def get_movie_meta(movie_id):
    """Return (title, year, genres_list) for a movie."""
    row = MOVIES_DF[MOVIES_DF[0] == movie_id]
    if len(row) == 0:
        return f"Movie {movie_id}", None, []
    r = row.iloc[0]
    title = r[1]
    year = pd.to_datetime(r[2], errors='coerce')
    year = int(year.year) if pd.notna(year) else None
    genres = [name for col, name in GENRE_NAMES.items() if r[col] == 1]
    return title, year, genres


def find_user_for_genres(genres):
    """Find the dataset user who gave the highest avg rating to movies in these genres."""
    known = [g for g in genres if g in GENRE_COLS]
    if not known:
        return None
    mask = pd.Series(False, index=MOVIES_DF.index)
    for g in known:
        mask |= (MOVIES_DF[GENRE_COLS[g]] == 1)
    genre_movie_ids = set(MOVIES_DF[mask][0].tolist())
    if not genre_movie_ids:
        return None
    genre_ratings = RATINGS_DF[RATINGS_DF['movie_id'].isin(genre_movie_ids)]
    user_avg = genre_ratings.groupby('user_id').agg(
        avg=('rating', 'mean'), count=('rating', 'count')
    )
    user_avg = user_avg[user_avg['count'] >= 10]
    if user_avg.empty:
        return None
    return int(user_avg['avg'].idxmax())


def filter_movie_ids(genres_a, genres_b, year_from_a, year_to_a, year_from_b, year_to_b, mood_genres):
    year_from = min(year_from_a, year_from_b)
    year_to = max(year_to_a, year_to_b)
    all_genres = set(genres_a) | set(genres_b) | set(mood_genres)

    df = MOVIES_DF.copy()
    df['_year'] = pd.to_datetime(df[2], errors='coerce').dt.year
    if year_from > 1922 or year_to < 1998:
        df = df[(df['_year'] >= year_from) & (df['_year'] <= year_to)]

    known_genres = [g for g in all_genres if g in GENRE_COLS]
    if known_genres:
        mask = pd.Series(False, index=df.index)
        for g in known_genres:
            mask |= (df[GENRE_COLS[g]] == 1)
        df = df[mask]

    movie_ids = df[0].tolist()
    if len(movie_ids) < 20:
        movie_ids = list(range(1, 1683))
    return movie_ids


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start")
def start():
    session_id = create_session()
    session["session_id"] = session_id
    return redirect(url_for("partner_a"))


@app.route("/partner/a", methods=["GET", "POST"])
def partner_a():
    if request.method == "POST":
        prefs = {
            "genres": request.form.getlist("genres"),
            "mood": request.form.get("mood", ""),
            "year_from": int(request.form.get("year_from") or 1922),
            "year_to": int(request.form.get("year_to") or 1998),
        }
        save_preferences(session["session_id"], "a", prefs)
        return redirect(url_for("partner_b"))
    return render_template("partner_a.html")


@app.route("/partner/b", methods=["GET", "POST"])
def partner_b():
    if request.method == "POST":
        prefs = {
            "genres": request.form.getlist("genres"),
            "mood": request.form.get("mood", ""),
            "year_from": int(request.form.get("year_from") or 1922),
            "year_to": int(request.form.get("year_to") or 1998),
        }
        save_preferences(session["session_id"], "b", prefs)

        all_prefs = get_preferences(session["session_id"])
        prefs_a = next(p for p in all_prefs if p["partner"] == "a")
        prefs_b = next(p for p in all_prefs if p["partner"] == "b")

        mood_genres = combine_mood_genres(prefs_a["mood"], prefs_b["mood"])

        candidate_ids = filter_movie_ids(
            genres_a=prefs_a.get("genres", []),
            genres_b=prefs_b.get("genres", []),
            year_from_a=prefs_a.get("year_from", 1922),
            year_to_a=prefs_a.get("year_to", 1998),
            year_from_b=prefs_b.get("year_from", 1922),
            year_to_b=prefs_b.get("year_to", 1998),
            mood_genres=mood_genres,
        )

        # Pick user IDs that best match each partner's genre taste
        user_a_id = find_user_for_genres(prefs_a.get("genres", []) or mood_genres) or 1
        user_b_id = find_user_for_genres(prefs_b.get("genres", []) or mood_genres) or 2
        if user_a_id == user_b_id:
            user_b_id = (user_b_id % 943) + 1

        recommender = MovieRecommender('model.pkl')
        recommendations = recommender.find_compatible_movies(
            user_a_id=user_a_id,
            user_b_id=user_b_id,
            all_movie_ids=candidate_ids,
            threshold=3.0,
        )

        top_recs = recommendations[:10]
        titles = [get_movie_title(movie_id) for movie_id, _ in top_recs]
        synopses = get_movie_synopses(titles)

        recommendations_list = []
        for rank, (movie_id, score) in enumerate(top_recs, 1):
            title, year, genres = get_movie_meta(movie_id)
            normalized_score = (score - 1.0) / 4.0
            normalized_score = max(0, min(1, normalized_score))
            recommendations_list.append({
                "rank": rank,
                "movie_id": movie_id,
                "title": title,
                "year": year,
                "genres": genres,
                "score": normalized_score,
                "explanation": synopses.get(title, ""),
            })

        save_results(session["session_id"], recommendations_list)
        return redirect(url_for("results", session_id=session["session_id"]))

    return render_template("partner_b.html")


@app.route("/results/<session_id>")
def results(session_id):
    if not session_exists(session_id):
        return render_template("error.html", message="Session not found."), 404
    recommendations = get_results(session_id)
    return render_template("results.html", recommendations=recommendations)


if __name__ == "__main__":
    app.run(debug=True)
