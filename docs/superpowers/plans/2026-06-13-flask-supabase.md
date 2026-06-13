# Flask + Supabase Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Flask backend and Supabase database for WatchMate so the full partner-preference → recommendation → results flow works end-to-end, ready to integrate Karen's `model.pkl` when it's done.

**Architecture:** Partner A and Partner B fill in forms sequentially on the same device. Flask stores preferences in Supabase, calls `model/recommender.py` (stub for now), saves results to Supabase, and renders result cards. All DB access goes through `app/db.py`; routes live in `app/app.py` and touch nothing but `db.py` and `recommender.py`.

**Tech Stack:** Flask 3.x, supabase-py 2.x, python-dotenv, pytest, pytest-flask

---

## File Map

| File | Responsibility |
|---|---|
| `app/__init__.py` | Empty — makes `app` a Python package |
| `app/app.py` | Flask routes only — no DB or ML logic |
| `app/db.py` | All Supabase reads/writes |
| `app/templates/index.html` | Landing page |
| `app/templates/partner_a.html` | Partner A preference form |
| `app/templates/partner_b.html` | Partner B preference form |
| `app/templates/results.html` | Result cards |
| `app/templates/error.html` | Error page |
| `model/__init__.py` | Empty — makes `model` a Python package |
| `model/recommender.py` | Stub returning dummy results |
| `tests/conftest.py` | pytest fixtures (Flask test client, db mock) |
| `tests/test_recommender.py` | Tests for recommender stub contract |
| `tests/test_db.py` | Tests for db.py functions (mocked Supabase) |
| `tests/test_routes.py` | Tests for all Flask routes |
| `.env.example` | Template for environment variables |
| `requirements.txt` | Pinned dependencies |

---

## Task 1: Project Structure & Dependencies

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `app/__init__.py`
- Create: `model/__init__.py`
- Create: `tests/__init__.py`
- Modify: `.gitignore`

- [ ] **Step 1: Create requirements.txt**

```
flask>=3.0.0
supabase>=2.0.0
python-dotenv>=1.0.0
pytest>=8.0.0
pytest-flask>=1.3.0
```

- [ ] **Step 2: Create .env.example**

```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key
FLASK_SECRET_KEY=any-long-random-string
```

- [ ] **Step 3: Create empty package init files**

Create `app/__init__.py`, `model/__init__.py`, `tests/__init__.py` — all empty files.

- [ ] **Step 4: Update .gitignore to exclude .env**

Add these lines to `.gitignore`:
```
.env
__pycache__/
*.pyc
*.pkl
```

- [ ] **Step 5: Install dependencies**

```bash
pip install -r requirements.txt
```

Expected: all packages install without error.

- [ ] **Step 6: Create .env from example**

```bash
cp .env.example .env
```

Leave it empty for now — you'll fill in real values after Supabase setup in Task 3.

- [ ] **Step 7: Commit**

```bash
git add requirements.txt .env.example app/__init__.py model/__init__.py tests/__init__.py .gitignore
git commit -m "chore: project structure and dependencies"
```

---

## Task 2: Recommender Stub (TDD)

**Files:**
- Create: `model/recommender.py`
- Create: `tests/test_recommender.py`

The stub lets the full Flask flow be tested before Karen's model is ready. It must satisfy the same interface the real model will use.

- [ ] **Step 1: Write the failing test**

Create `tests/test_recommender.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_recommender.py -v
```

Expected: `ImportError: cannot import name 'recommend' from 'model.recommender'`

- [ ] **Step 3: Write the stub implementation**

Create `model/recommender.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_recommender.py -v
```

Expected: all 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add model/recommender.py tests/test_recommender.py
git commit -m "feat: recommender stub with interface contract tests"
```

---

## Task 3: Supabase Project Setup (Manual)

**This task has no code — it's manual setup in the Supabase dashboard.**

- [ ] **Step 1: Create Supabase project**

1. Go to [supabase.com](https://supabase.com) and sign in
2. Click **New project**
3. Name it `watchmate`, choose a region close to you, set a database password
4. Wait ~2 minutes for the project to provision

- [ ] **Step 2: Run the schema SQL**

In the Supabase dashboard, go to **SQL Editor** and run:

```sql
create table sessions (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  status text not null default 'waiting_b'
);

create table preferences (
  id uuid primary key default gen_random_uuid(),
  session_id uuid references sessions(id),
  partner text not null check (partner in ('a', 'b')),
  genres text[] default '{}',
  mood text,
  min_rating float default 1.0,
  year_from int default 1900,
  year_to int default 2026,
  content_type text default 'both' check (content_type in ('movies', 'shows', 'both'))
);

create table results (
  id uuid primary key default gen_random_uuid(),
  session_id uuid references sessions(id),
  movie_id int not null,
  title text not null,
  score float not null,
  explanation text,
  rank int not null
);
```

Expected: green "Success" banner for each statement.

- [ ] **Step 3: Get your API credentials**

In the Supabase dashboard go to **Project Settings → API**. Copy:
- **Project URL** (looks like `https://abcdef.supabase.co`)
- **anon public** key (long JWT string)

- [ ] **Step 4: Fill in .env**

Edit your `.env` file:
```
SUPABASE_URL=https://your-actual-project-id.supabase.co
SUPABASE_KEY=your-actual-anon-key
FLASK_SECRET_KEY=watchmate-dev-secret-key-change-in-prod
```

- [ ] **Step 5: Verify connection (quick manual check)**

Run this one-liner in a Python shell from the project root:

```python
import os; from dotenv import load_dotenv; load_dotenv()
from supabase import create_client
c = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
print(c.table("sessions").select("*").execute())
```

Expected: `data=[]` (empty table, no error).

---

## Task 4: db.py (TDD)

**Files:**
- Create: `app/db.py`
- Create: `tests/test_db.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_db.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_db.py -v
```

Expected: `ImportError: cannot import name 'create_session' from 'app.db'`

- [ ] **Step 3: Implement db.py**

Create `app/db.py`:

```python
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


def get_client() -> Client:
    return create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])


def create_session() -> str:
    client = get_client()
    result = client.table("sessions").insert({"status": "waiting_b"}).execute()
    return result.data[0]["id"]


def save_preferences(session_id: str, partner: str, prefs: dict) -> None:
    client = get_client()
    client.table("preferences").insert({
        "session_id": session_id,
        "partner": partner,
        **prefs,
    }).execute()


def get_preferences(session_id: str) -> list[dict]:
    client = get_client()
    result = (
        client.table("preferences")
        .select("*")
        .eq("session_id", session_id)
        .execute()
    )
    return result.data


def save_results(session_id: str, recommendations: list[dict]) -> None:
    client = get_client()
    rows = [{"session_id": session_id, **r} for r in recommendations]
    client.table("results").insert(rows).execute()
    client.table("sessions").update({"status": "done"}).eq("id", session_id).execute()


def get_results(session_id: str) -> list[dict]:
    client = get_client()
    result = (
        client.table("results")
        .select("*")
        .eq("session_id", session_id)
        .order("rank")
        .execute()
    )
    return result.data


def session_exists(session_id: str) -> bool:
    client = get_client()
    result = (
        client.table("sessions")
        .select("id")
        .eq("id", session_id)
        .execute()
    )
    return len(result.data) > 0
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_db.py -v
```

Expected: all 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add app/db.py tests/test_db.py
git commit -m "feat: supabase db layer with full CRUD"
```

---

## Task 5: Flask Routes (TDD)

**Files:**
- Create: `app/app.py`
- Create: `tests/conftest.py`
- Create: `tests/test_routes.py`

- [ ] **Step 1: Create conftest.py**

Create `tests/conftest.py`:

```python
import pytest
from unittest.mock import patch, MagicMock


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
```

- [ ] **Step 2: Write failing route tests**

Create `tests/test_routes.py`:

```python
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
        "min_rating": "3.5",
        "year_from": "2000",
        "year_to": "2023",
        "content_type": "movies",
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
        "min_rating": "3.0",
        "year_from": "1995",
        "year_to": "2023",
        "content_type": "both",
    })
    assert response.status_code == 302
    assert "/results/test-session-id" in response.location


def test_results_page_renders_cards(client, mock_db):
    response = client.get("/results/test-session-id")
    assert response.status_code == 200
    assert b"Movie A" in response.data


def test_results_invalid_session_returns_404(client):
    with client.application.test_request_context():
        import app.app
    from unittest.mock import patch
    with patch("app.app.session_exists", return_value=False):
        response = client.get("/results/bad-session-id")
    assert response.status_code == 404
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
pytest tests/test_routes.py -v
```

Expected: `ImportError: cannot import name 'app' from 'app.app'`

- [ ] **Step 4: Implement app.py**

Create `app/app.py`:

```python
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
from model.recommender import recommend

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
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
pytest tests/test_routes.py -v
```

Expected: all 7 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add app/app.py tests/conftest.py tests/test_routes.py
git commit -m "feat: flask routes with full partner flow"
```

---

## Task 6: HTML Templates

**Files:**
- Create: `app/templates/index.html`
- Create: `app/templates/partner_a.html`
- Create: `app/templates/partner_b.html`
- Create: `app/templates/results.html`
- Create: `app/templates/error.html`

These are functional placeholders. Shai will replace them with the Stitch UI design.

- [ ] **Step 1: Create base layout (index.html)**

Create `app/templates/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>WatchMate</title>
</head>
<body>
  <h1>WatchMate</h1>
  <p>Find movies you'll both love.</p>
  <a href="/">Start</a>
</body>
</html>
```

- [ ] **Step 2: Create partner_a.html**

Create `app/templates/partner_a.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Partner A – WatchMate</title>
</head>
<body>
  <h1>Partner A Preferences</h1>
  <form method="POST" action="/partner/a">
    <label>Genres (hold Ctrl/Cmd to pick multiple)
      <select name="genres" multiple>
        <option value="Action">Action</option>
        <option value="Comedy">Comedy</option>
        <option value="Drama">Drama</option>
        <option value="Horror">Horror</option>
        <option value="Romance">Romance</option>
        <option value="Sci-Fi">Sci-Fi</option>
        <option value="Thriller">Thriller</option>
        <option value="Animation">Animation</option>
        <option value="Documentary">Documentary</option>
      </select>
    </label>
    <br>
    <label>Mood (describe how you're feeling tonight)
      <input type="text" name="mood" placeholder="e.g. tired and want something light" required>
    </label>
    <br>
    <label>Minimum rating (1–5)
      <input type="number" name="min_rating" min="1" max="5" step="0.5" value="3.0">
    </label>
    <br>
    <label>Year from
      <input type="number" name="year_from" min="1900" max="2026" value="2000">
    </label>
    <label>to
      <input type="number" name="year_to" min="1900" max="2026" value="2026">
    </label>
    <br>
    <label>Content type
      <select name="content_type">
        <option value="both">Movies &amp; Shows</option>
        <option value="movies">Movies only</option>
        <option value="shows">Shows only</option>
      </select>
    </label>
    <br>
    <button type="submit">Next → Partner B</button>
  </form>
</body>
</html>
```

- [ ] **Step 3: Create partner_b.html**

Create `app/templates/partner_b.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Partner B – WatchMate</title>
</head>
<body>
  <h1>Partner B Preferences</h1>
  <form method="POST" action="/partner/b">
    <label>Genres (hold Ctrl/Cmd to pick multiple)
      <select name="genres" multiple>
        <option value="Action">Action</option>
        <option value="Comedy">Comedy</option>
        <option value="Drama">Drama</option>
        <option value="Horror">Horror</option>
        <option value="Romance">Romance</option>
        <option value="Sci-Fi">Sci-Fi</option>
        <option value="Thriller">Thriller</option>
        <option value="Animation">Animation</option>
        <option value="Documentary">Documentary</option>
      </select>
    </label>
    <br>
    <label>Mood (describe how you're feeling tonight)
      <input type="text" name="mood" placeholder="e.g. want something exciting" required>
    </label>
    <br>
    <label>Minimum rating (1–5)
      <input type="number" name="min_rating" min="1" max="5" step="0.5" value="3.0">
    </label>
    <br>
    <label>Year from
      <input type="number" name="year_from" min="1900" max="2026" value="2000">
    </label>
    <label>to
      <input type="number" name="year_to" min="1900" max="2026" value="2026">
    </label>
    <br>
    <label>Content type
      <select name="content_type">
        <option value="both">Movies &amp; Shows</option>
        <option value="movies">Movies only</option>
        <option value="shows">Shows only</option>
      </select>
    </label>
    <br>
    <button type="submit">Get Recommendations</button>
  </form>
</body>
</html>
```

- [ ] **Step 4: Create results.html**

Create `app/templates/results.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Your Watchlist – WatchMate</title>
</head>
<body>
  <h1>Your WatchMate Picks</h1>
  {% for rec in recommendations %}
  <div>
    <h2>{{ rec.rank }}. {{ rec.title }}</h2>
    <p>Match score: {{ "%.0f"|format(rec.score * 100) }}%</p>
    <p>{{ rec.explanation }}</p>
  </div>
  {% endfor %}
  <a href="/">Start over</a>
</body>
</html>
```

- [ ] **Step 5: Create error.html**

Create `app/templates/error.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Error – WatchMate</title>
</head>
<body>
  <h1>Something went wrong</h1>
  <p>{{ message }}</p>
  <a href="/">Start over</a>
</body>
</html>
```

- [ ] **Step 6: Run all tests to confirm templates don't break anything**

```bash
pytest -v
```

Expected: all tests PASS.

- [ ] **Step 7: Commit**

```bash
git add app/templates/
git commit -m "feat: functional html templates (placeholder for stitch ui)"
```

---

## Task 7: Smoke Test — Full Flow Locally

- [ ] **Step 1: Run all tests one final time**

```bash
pytest -v
```

Expected: all tests PASS, 0 failures.

- [ ] **Step 2: Start Flask**

```bash
python app/app.py
```

Expected output:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

- [ ] **Step 3: Walk through the full flow in browser**

1. Open `http://127.0.0.1:5000`
2. Confirm you're redirected to `/partner/a`
3. Fill in Partner A's form and submit
4. Confirm you're redirected to `/partner/b`
5. Fill in Partner B's form and submit
6. Confirm you're redirected to `/results/<session-id>`
7. Confirm 3 result cards appear (dummy data from stub)
8. Open Supabase dashboard → Table Editor → check `sessions`, `preferences`, `results` tables have rows

- [ ] **Step 4: Push to GitHub**

```bash
git push origin main
```

---

## Integration Checklist (when Karen's model is ready)

When Karen finishes `model.pkl`, she replaces the body of `model/recommender.py::recommend()`. The function signature must stay the same:

```python
def recommend(partner_a: dict, partner_b: dict) -> list[dict]:
    # returns: list of {movie_id, title, score, explanation, rank}
```

Run `pytest tests/test_recommender.py -v` after she integrates — all existing tests must still pass.
