import os
from pathlib import Path
from typing import Any, Dict, List

import requests

from api.services.abс_service import RepositoriesAbstractService, UsersAbstractService
from api.services.github_services.graphql_service.exceptions import (
    GithubServiceException,
    GraphQLGithubServiceException,
)
from api.utils.logger import logger

BASE_PATH = Path(__file__).resolve().parent


class GraphQLGithubService(UsersAbstractService, RepositoriesAbstractService):
    GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
    GRAPHQL_QUERIES_PATH = BASE_PATH / "graphql_queries"
    SEARCH_USERS_QUERY_FILE = "search_users.graphql"
    SEARCH_REPOSITORIES_QUERY_FILE = "search_repositories.graphql"

    def __init__(self, github_token: str = None):
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")

        if not self.github_token:
            logger.error("GITHUB_TOKEN environment variable is not set")
            raise GithubServiceException("GITHUB_TOKEN must be set")

    @staticmethod
    def get_graphql_query(query_path: Path) -> str:
        with query_path.open(encoding="utf-8") as f:
            query: str = f.read()

        return query

    def execute_request(self, payload: Dict[str, Any]) -> Any:
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Content-Type": "application/json",
        }

        try:
            logger.debug(
                f"Executing GraphQL request to {self.GITHUB_GRAPHQL_URL} "
                f"with payload: {payload}, headers: {headers}"
            )
            response = requests.post(
                self.GITHUB_GRAPHQL_URL, json=payload, headers=headers
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise GraphQLGithubServiceException(f"GraphQL HTTP error: {e}.")

        try:
            result = response.json()
        except ValueError as e:
            raise GraphQLGithubServiceException(f"Invalid JSON response: {e}")

        if "errors" in result:
            raise GraphQLGithubServiceException(result["errors"])

        try:
            return result["data"]["search"]["nodes"]
        except Exception:
            raise GraphQLGithubServiceException(
                "Unexpected GraphQL structure: missing data.search.nodes"
            )

    def get_search_payload(
        self, search_text: str, graphql_query_name: str, **kwargs
    ) -> Dict[str, Any]:
        payload = {
            "query": self.get_graphql_query(
                self.GRAPHQL_QUERIES_PATH / Path(graphql_query_name)
            ),
            "variables": {"text": search_text, **kwargs},
        }

        return payload

    def get_users(self, search_text: str, **kwargs) -> List[Dict[str, str]]:
        payload = self.get_search_payload(
            search_text, self.SEARCH_USERS_QUERY_FILE, **kwargs
        )
        items: List[Dict[str, str]] = self.execute_request(payload)
        logger.debug(f"Users result from GitHub: {items}")

        return [item for item in items if item]

    def get_repositories(self, search_text: str, **kwargs) -> List[Dict[str, str]]:
        payload = self.get_search_payload(
            search_text, self.SEARCH_REPOSITORIES_QUERY_FILE, **kwargs
        )
        items: List[Dict[str, Any]] = self.execute_request(payload)
        logger.debug(f"Repositories result from GitHub: {items}")

        return [{**item, "owner": item["owner"]["login"]} for item in items if item]
