from pathlib import Path

from api.services.github_services.abс_service import GithubService
import requests
from typing import Dict, Any, List

BASE_PATH = Path(__file__).resolve().parent
GRAPHQL_QUERIES_PATH = BASE_PATH / "graphql_queries"

class GraphQLGithubService(GithubService):
    GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

    @staticmethod
    def get_graphql_query(query_path: Path):
        with query_path.open(encoding="utf-8") as f:
            query: str = f.read()

        return query

    def execute_request(self, payload: Dict[str, Any]) -> requests.Response:
        headers = {
            "Authorization": f"Bearer {self.GITHUB_TOKEN}",
            "Content-Type": "application/json",
        }

        resp = requests.post(self.GITHUB_GRAPHQL_URL, json=payload, headers=headers)
        resp.raise_for_status()

        return resp

    def get_search_payload(self, search_text: str, graphql_query_name: str) -> Dict[str, Any]:
        payload = {
            "query": self.get_graphql_query(GRAPHQL_QUERIES_PATH / Path(graphql_query_name)),
            "variables": {"text": search_text, "first": 30},
        }

        return payload

    def get_users(self, search_text: str, first: int = 30) -> List[Dict[str, str]]:
        payload = self.get_search_payload(search_text, "search_users.graphql")
        data  = self.execute_request(payload).json()

        if "errors" in data:
            raise Exception(data["errors"])

        result = data["data"]["search"]["nodes"]
        res = []
        for item in result:
            if item:
                res.append({'id': item["databaseId"],
                            'title': item["login"],
                            'location': item["location"],
                            'avatar_url': item["avatarUrl"]}
                           )
        return res

    def get_repositories(self, search_text: str, first: int = 30) -> List[Dict[str, str]]:
        payload = self.get_search_payload(search_text, "search_repositories.graphql")
        data  = self.execute_request(payload).json()

        if "errors" in data:
            raise Exception(data["errors"])

        result = data["data"]["search"]["nodes"]
        res = []
        print(result)
        for item in result:
            if item:
                res.append({'id': item["databaseId"],
                            'title': item['name'],
                            'owner': item['owner']['login'],
                            'stars': item['stargazerCount'],
                            'description': item['description'],
                            'url': item['url']}
                           )
        return res
