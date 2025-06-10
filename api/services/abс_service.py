from abc import ABC, abstractmethod
from typing import Dict, List


class UsersAbstractService(ABC):
    @abstractmethod
    def get_users(self, search_text: str, **kwargs) -> List[Dict[str, str]]:
        raise NotImplementedError


class RepositoriesAbstractService(ABC):
    @abstractmethod
    def get_repositories(self, search_text: str, **kwargs) -> List[Dict[str, str]]:
        raise NotImplementedError
