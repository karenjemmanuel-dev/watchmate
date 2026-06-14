from app.mood_filter import combine_mood_genres
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

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-fallback-secret")

print("Loading movie data...")
MOVIES_DF = pd.read_csv('data/u.item', sep='|', encoding='latin-1', header=None)
print(f"Loaded {len(MOVIES_DF)} movies")


def get_movie_title(movie_id):
    row = MOVIES_DF[MOVIES_DF[0] == movie_id]
    if len(row) > 0:
        return row.iloc[0][1]
    return f"Movie {movie_id}"


@app.route("/")
def index():
    session_id = create_session()
    session["session_id"] = session_id
    return redirect(url_for("partner_a"))


@app.route("/partner/a", methods=["GET", "POST"])
def partner_a():
    if request.method == "POST":
        prefs = {
            "genres": request.form.getlist("genres"),
            "mood": request.form.get("mood", ""),
            "year_from": int(request.form.get("year_from", 1900)),
            "year_to": int(request.form.get("year_to", 2026)),
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
            "year_from": int(request.form.get("year_from", 1900)),
            "year_to": int(request.form.get("year_to", 2026)),
        }
        save_preferences(session["session_id"], "b", prefs)

        all_prefs = get_preferences(session["session_id"])
        prefs_a = next(p for p in all_prefs if p["partner"] == "a")
        prefs_b = next(p for p in all_prefs if p["partner"] == "b")

        recommender = MovieRecommender('model.pkl')
        all_movie_ids = list(range(1, 1683))

        recommendations = recommender.find_compatible_movies(
            user_a_id=1,
            user_b_id=2,
            all_movie_ids=all_movie_ids,
            threshold=3.5
        )

        mood_genres = combine_mood_genres(prefs_a["mood"], prefs_b["mood"])
        mood_a = prefs_a["mood"]
        mood_b = prefs_b["mood"]
        combined_mood_description = f"{mood_a} + {mood_b}"

        recommendations_list = []
        for rank, (movie_id, score) in enumerate(recommendations[:10], 1):
            title = get_movie_title(movie_id)
            normalized_score = (score - 1.0) / 4.0
            normalized_score = max(0, min(1, normalized_score))
            
            recommendations_list.append({
                "rank": rank,
                "movie_id": movie_id,
                "title": title,
                "score": normalized_score,
                "explanation": f"Based on both your moods: {combined_mood_description}"
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