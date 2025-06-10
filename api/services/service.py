from api.repositories.SearchRepositories import  AbstractRepository

from api.utils.enums import SearchType
from api.utils.factories import repository_factory
from api.utils.logger import logger


class ServiceLayer:
    def __init__(self, search_type: SearchType):
        self._repository: AbstractRepository = repository_factory(search_type)

    def search_by_text(self, text: str):
        result = self._repository.get(text)

        logger.info(f"<{self._repository}> returns {len(result)} elements")

        return result
