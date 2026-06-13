# WatchMate — Design Spec
_Date: 2026-06-13_

## Overview

WatchMate is a two-person movie recommendation web app. Two partners sequentially enter their preferences on the same device, and the system uses a trained ML model (MovieLens 100K, collaborative filtering) to recommend 3–5 movies/shows they'll both enjoy.

**Team split:**
- Karen: ML recommendation model (`model.pkl`)
- Shai: Flask backend + Supabase database

---

## Architecture

### Data Flow

```
GET /                   → create session in Supabase → redirect to /partner/a
GET  /partner/a         → render Partner A form
POST /partner/a         → save prefs to Supabase → redirect to /partner/b
GET  /partner/b         → render Partner B form
POST /partner/b         → save prefs to Supabase → call recommend() → save results → redirect to /results/<session_id>
GET  /results/<id>      → fetch results from Supabase → render result cards
```

### Integration Contract with Karen's Model

Flask calls a single function:

```python
# model/recommender.py
def recommend(partner_a: dict, partner_b: dict) -> list[dict]:
    # returns list of dicts: {movie_id, title, score, explanation, rank}
    ...
```

Shai writes a stub now returning dummy data. Karen fills it in when `model.pkl` is ready.

### File Structure

```
watchmate/
├── app/
│   ├── app.py           # Flask routes only
│   ├── db.py            # All Supabase reads/writes
│   └── templates/
│       ├── index.html
│       ├── partner_a.html
│       ├── partner_b.html
│       ├── results.html
│       └── error.html
├── model/
│   └── recommender.py   # stub → Karen fills in
├── docs/
│   └── superpowers/specs/
└── requirements.txt
```

---

## Supabase Schema

### `sessions`
| column | type | notes |
|---|---|---|
| id | uuid PK | auto-generated |
| created_at | timestamp | auto |
| status | text | `waiting_b`, `processing`, `done` |

### `preferences`
| column | type | notes |
|---|---|---|
| id | uuid PK | |
| session_id | uuid FK → sessions | |
| partner | text | `a` or `b` |
| genres | text[] | e.g. `["Action", "Comedy"]` |
| mood | text | free text, interpreted by model |
| min_rating | float | 1.0–5.0 |
| year_from | int | |
| year_to | int | |
| content_type | text | `movies`, `shows`, or `both` |

### `results`
| column | type | notes |
|---|---|---|
| id | uuid PK | |
| session_id | uuid FK → sessions | |
| movie_id | int | MovieLens movie ID |
| title | text | |
| score | float | match score 0–1 |
| explanation | text | one-line why it works for both |
| rank | int | 1–5 |

---

## Flask Routes

| Method | Route | Action |
|---|---|---|
| GET | `/` | Create session, redirect to `/partner/a` |
| GET | `/partner/a` | Render Partner A form |
| POST | `/partner/a` | Save Partner A prefs, redirect to `/partner/b` |
| GET | `/partner/b` | Render Partner B form |
| POST | `/partner/b` | Save Partner B prefs, call `recommend()`, save results, redirect to `/results/<id>` |
| GET | `/results/<session_id>` | Fetch results from Supabase, render cards |

---

## Error Handling

1. **Invalid session ID** on `/results/<id>` → render `error.html` with link back to start
2. **Model not ready** → `recommender.py` stub returns dummy results so full flow is testable
3. **Supabase failure** → 500 error page, no silent failures

---

## Decisions & Rationale

- **Synchronous flow** (no background workers): dataset is static and small enough; a short wait is acceptable for a class project
- **Sequential partner input** (A then B on same device): simpler than simultaneous forms
- **Mood as free text**: interpreted by the ML model, not a fixed enum
- **Content type preference**: partners specify movies, shows, or both — model filters accordingly
- **Model stub pattern**: allows Flask + Supabase to be built and tested independently of Karen's model

---

## Final Deliverables (Due Next Week)

- `clean_data.csv`, `eda_report.html`, `dataset_contract.json` (Karen)
- `model.pkl`, `model_card.md` (Karen)
- Flask app + Supabase integration (Shai)
- Frontend UI (Both)
- CrewAI agents (Both, after model + backend ready)
- Railway deployment (Both, final step)
- 10–12 slide deck + ≤5 min demo video
