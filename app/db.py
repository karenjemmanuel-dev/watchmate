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
