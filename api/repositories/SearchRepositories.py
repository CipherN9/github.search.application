from abc import ABC, abstractmethod
from typing import List, Dict

from api.services.abс_service import UsersAbstractService, RepositoriesAbstractService


class AbstractRepository(ABC):
    @abstractmethod
    def get(self, search_text: str) -> List[Dict[str, str]]:
        raise NotImplementedError


class UsersRepository(AbstractRepository):
    def __init__(self, service: UsersAbstractService):
        self._service = service

    def get(self, search_text: str) -> List[Dict[str, str]]:
        items: List[Dict[str, str]] = self._service.get_users(search_text)

        return items


class RepositoriesRepository(AbstractRepository):
    def __init__(self, service: RepositoriesAbstractService):
        self._service = service

    def get(self, search_text: str) -> List[Dict[str, str]]:
        items: List[Dict[str, str]] = self._service.get_repositories(search_text)

        return items