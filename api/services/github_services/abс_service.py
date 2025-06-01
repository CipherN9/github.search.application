import os
from abc import  abstractmethod
from typing import Any, Dict

from api.services.abс_service import AbstractService


class GithubService(AbstractService):
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    @abstractmethod
    def execute_request(self, payload: Dict[str, Any]):
        raise NotImplementedError()
