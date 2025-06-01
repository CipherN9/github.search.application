from api.utils.enums import SearchType
from api.services.abс_service import AbstractService


class ServiceLayer:
    def __init__(self, service: AbstractService):
        self.service = service

    def search_by_text(self, search_text: str, search_type: SearchType):
        if search_type == SearchType.USERS:
            result = self.service.get_users(search_text)
        elif search_type == SearchType.REPOSITORIES:
            result = self.service.get_repositories(search_text)
        else:
            raise ValueError(f"Invalid search type: {search_type}")

        return result