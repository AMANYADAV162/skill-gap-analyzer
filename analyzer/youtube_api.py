import requests
from django.conf import settings

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def fetch_free_courses(skill_name, max_results=5):
    """
    Calls the YouTube Data API to find free tutorial/course videos
    for a given skill. Returns a list of dicts (empty list on any error).
    """
    api_key = getattr(settings, "YOUTUBE_API_KEY", None)
    if not api_key:
        return []

    params = {
        "part": "snippet",
        "q": f"{skill_name} free tutorial course",
        "type": "video",
        "maxResults": max_results,
        "key": api_key,
        "relevanceLanguage": "en",
        "safeSearch": "strict",
    }

    try:
        response = requests.get(YOUTUBE_SEARCH_URL, params=params, timeout=6)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return []

    results = []
    for item in data.get("items", []):
        video_id = item.get("id", {}).get("videoId")
        snippet = item.get("snippet", {})
        if not video_id:
            continue
        results.append({
            "title": snippet.get("title"),
            "channel": snippet.get("channelTitle"),
            "thumbnail": snippet.get("thumbnails", {}).get("medium", {}).get("url"),
            "url": f"https://www.youtube.com/watch?v={video_id}",
        })
    return results