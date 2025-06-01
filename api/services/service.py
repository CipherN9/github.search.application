from api.enums import SearchType
from api.services.github_service import AbstractService


class ServiceLayer:
    def __init__(self, service: AbstractService):
        self.service = service

    def search_by_query(self, query, search_type):
        if search_type == SearchType.USERS:
            result = self.service.get_users(query)
        elif search_type == SearchType.REPOSITORIES:
            result = self.service.get_repositories(query)
        else:
            raise ValueError(f"Invalid search type: {search_type}")

        return result