import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERP_API = os.getenv("SERPAPI_KEY")
YT_API = os.getenv("YOUTUBE_API_KEY")


def search_trends(query):
    url = "https://serpapi.com/search"
    params = {"q": query, "api_key": SERP_API}
    res = requests.get(url, params=params)
    return res.json()


def search_youtube(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": os.getenv("YOUTUBE_API_KEY"),
        "maxResults": 3,
        "type": "video"
    }

    res = requests.get(url, params=params).json()

    videos = []
    for item in res.get("items", []):
        video_id = item["id"]["videoId"]
        videos.append({
            "title": item["snippet"]["title"],
            "link": f"https://www.youtube.com/watch?v={video_id}",
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
        })

    return videos