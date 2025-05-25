import os
from concurrent.futures import ThreadPoolExecutor

import requests
from rest_framework import status
from rest_framework.response import Response


def perform_search(search_type, text):
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    resp = requests.get(
        f"https://api.github.com/search/{search_type}",
        params={"q": text},
        headers=headers,
        timeout=10
    )
    if resp.status_code != 200:
        return Response(
            {"detail": "GitHub Search failed", "github_status": resp.status_code},
            status=status.HTTP_502_BAD_GATEWAY
        )
    items = resp.json().get("items", [])

    # 3. для users — паралельні запити у потоках
    def fetch_profile(user):
        r = requests.get(f"https://api.github.com/users/{user['login']}",
                         headers=headers, timeout=10)
        data = r.json() if r.status_code == 200 else {}
        return {
            "id": user.get("id"),
            "title": user.get("login"),
            "location": data.get("location"),
            "avatar_url": data.get("avatar_url")
        }

    with ThreadPoolExecutor(max_workers=30) as executor:
        profiles = list(executor.map(fetch_profile, items[:30]))

    return profiles