import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any
import requests


BASE_PATH = Path(__file__).resolve().parent


class AbstractService(ABC):
    @abstractmethod
    def get_users(self, query: str, first: int = 30) -> List[Dict[str, str]]:
        raise NotImplementedError()

    @abstractmethod
    def get_repositories(self, query: str, first: int = 30) -> List[Dict[str, str]]:
        raise NotImplementedError()

class GithubService(AbstractService):
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    @abstractmethod
    def execute_request(self, payload: Dict[str, Any]):
        raise NotImplementedError()

    def get_users(self, query: str, first: int = 30) -> List[Dict[str, str]]:
        pass

    def get_repositories(self, query: str, first: int = 30) -> List[Dict[str, str]]:
        pass

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

    def get_users(self, query: str, first: int = 30) -> List[Dict[str, str]]:
        search_users_query_path = BASE_PATH / "graphql_queries" / "search_users.graphql"
        payload = {
            "query": self.get_graphql_query(search_users_query_path),
            "variables": {"text": query, "first": 30},
        }

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

    def get_repositories(self, text: str, first: int = 30) -> List[Dict[str, str]]:
        pass





