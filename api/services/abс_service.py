from abc import ABC, abstractmethod
from typing import List, Dict

class AbstractService(ABC):
    @abstractmethod
    def get_users(self, search_text: str, first: int = 30) -> List[Dict[str, str]]:
        raise NotImplementedError()

    @abstractmethod
    def get_repositories(self, search_text: str, first: int = 30) -> List[Dict[str, str]]:
        raise NotImplementedError()