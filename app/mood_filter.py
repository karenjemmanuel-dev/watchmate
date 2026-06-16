from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

def get_genres_from_mood(mood_text):
    """Use LLM to translate mood/emotion into movie genres"""
    
    if not mood_text or mood_text.strip() == "":
        return ["Drama", "Comedy"]
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"""
    User's mood or feeling: "{mood_text}"
    
    Based on this emotional state, what 2-4 movie genres would best help them find the right movie?
    
    Think about:
    - Do they need something uplifting and fun?
    - Do they need something relaxing and chill?
    - Do they need something exciting and intense?
    - Do they need something thoughtful and deep?
    
    Available genres: Action, Adventure, Animation, Comedy, Drama, Documentary, Fantasy, Horror, Romance, Sci-Fi, Thriller
    
    Return ONLY the genre names as a comma-separated list. Nothing else.
    
    Example: If mood is "exhausted and bummed", return: Comedy, Animation
    Example: If mood is "stressed but want adventure", return: Action, Adventure
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=50
        )
        
        genres_text = response.choices[0].message.content.strip()
        genres = [g.strip() for g in genres_text.split(",")]
        return genres
    
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return ["Drama", "Comedy"]


def get_movie_synopses(titles: list[str]) -> dict[str, str]:
    """Fetch a one-sentence synopsis for each movie title in a single API call."""
    if not titles:
        return {}

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    titles_block = "\n".join(f"- {t}" for t in titles)

    prompt = f"""For each movie below, write exactly one sentence describing what it's about.
Reply as a numbered list matching the order. Only the sentence, nothing else.

Movies:
{titles_block}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400,
        )
        lines = response.choices[0].message.content.strip().splitlines()
        result = {}
        for i, title in enumerate(titles):
            if i < len(lines):
                line = lines[i].strip()
                # strip leading "1. " / "- " etc.
                line = line.lstrip("0123456789.-) ").strip()
                result[title] = line
            else:
                result[title] = ""
        return result
    except Exception as e:
        print(f"Error fetching synopses: {e}")
        return {t: "" for t in titles}


def combine_mood_genres(mood_a, mood_b):
    """Get genres from both moods and find overlap"""
    
    genres_a = get_genres_from_mood(mood_a)
    genres_b = get_genres_from_mood(mood_b)
    
    print(f"Partner A mood genres: {genres_a}")
    print(f"Partner B mood genres: {genres_b}")
    
    # Find intersection (genres both moods suggest)
    shared_genres = set(genres_a) & set(genres_b)
    
    if shared_genres:
        return list(shared_genres)
    else:
        # If no overlap, use union (any genre either person likes)
        return list(set(genres_a) | set(genres_b))