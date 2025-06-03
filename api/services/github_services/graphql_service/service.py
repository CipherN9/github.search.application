from pathlib import Path

from api.services.github_services.abс_service import GithubService
import requests
from typing import Dict, Any, List

from api.services.github_services.graphql_service.exceptions import GraphQLGithubServiceException

BASE_PATH = Path(__file__).resolve().parent
GRAPHQL_QUERIES_PATH = BASE_PATH / "graphql_queries"

class GraphQLGithubService(GithubService):
    GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

    @staticmethod
    def get_graphql_query(query_path: Path):
        with query_path.open(encoding="utf-8") as f:
            query: str = f.read()

        return query

    def execute_request(self, payload: Dict[str, Any]) -> List[Dict[str, str]]:
        headers = {
            "Authorization": f"Bearer {self.GITHUB_TOKEN}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(self.GITHUB_GRAPHQL_URL, json=payload, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            raise GraphQLGithubServiceException(f"HTTP error: {e}")

        try:
            result = response.json()
        except ValueError as e:
            raise GraphQLGithubServiceException(f"Invalid JSON response: {e}")

        if "errors" in result:
            raise GraphQLGithubServiceException(result["errors"])

        try:
            return result["data"]["search"]["nodes"]
        except:
            raise GraphQLGithubServiceException("Unexpected GraphQL structure: missing data.search.nodes")

    def get_search_payload(self, search_text: str, graphql_query_name: str) -> Dict[str, Any]:
        payload = {
            "query": self.get_graphql_query(GRAPHQL_QUERIES_PATH / Path(graphql_query_name)),
            "variables": {"text": search_text, "first": 30},
        }

        return payload

    def get_users(self, search_text: str, first: int = 30) -> List[Dict[str, str]]:
        payload = self.get_search_payload(search_text, "search_users.graphql")
        items: List[Dict[str, str]] = self.execute_request(payload)

        return [item for item in items if item]

    def get_repositories(self, search_text: str, first: int = 30) -> List[Dict[str, str]]:
        payload = self.get_search_payload(search_text, "search_repositories.graphql")
        items: List[Dict[str, Any]] = self.execute_request(payload)

        return [{**item, "owner": item["owner"]["login"]} for item in items if item]
