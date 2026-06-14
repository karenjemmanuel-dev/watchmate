import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session

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
            "min_rating": float(request.form.get("min_rating", 1.0)),
            "year_from": int(request.form.get("year_from", 1900)),
            "year_to": int(request.form.get("year_to", 2026)),
            "content_type": request.form.get("content_type", "both"),
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
            "min_rating": float(request.form.get("min_rating", 1.0)),
            "year_from": int(request.form.get("year_from", 1900)),
            "year_to": int(request.form.get("year_to", 2026)),
            "content_type": request.form.get("content_type", "both"),
        }
        save_preferences(session["session_id"], "b", prefs)

        all_prefs = get_preferences(session["session_id"])
        prefs_a = next(p for p in all_prefs if p["partner"] == "a")
        prefs_b = next(p for p in all_prefs if p["partner"] == "b")

        recommendations = recommend(prefs_a, prefs_b)
        save_results(session["session_id"], recommendations)

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
