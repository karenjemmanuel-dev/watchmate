import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def get_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)


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


def save_results(session_id: str, recommendations: list) -> None:
    client = get_client()
    client.table("results").insert({
        "session_id": session_id,
        "recommendations": recommendations,
    }).execute()


def get_results(session_id: str) -> list[dict]:
    client = get_client()
    result = (
        client.table("results")
        .select("*")
        .eq("session_id", session_id)
        .execute()
    )
    if result.data:
        return result.data[0].get("recommendations", [])
    return []


def session_exists(session_id: str) -> bool:
    client = get_client()
    result = (
        client.table("sessions")
        .select("id")
        .eq("id", session_id)
        .execute()
    )
    return len(result.data) > 0