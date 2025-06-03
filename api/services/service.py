from api.services.exceptions import ExternalServiceError
from api.services.github_services.graphql_service.exceptions import GraphQLGithubServiceException
from api.utils.enums import SearchType
from api.services.abс_service import AbstractService

class ServiceLayer:
    def __init__(self, service: AbstractService):
        self._service = service

    def search_by_type_and_text(self, search_type: SearchType, search_text: str,):
        try:
            if search_type == SearchType.USERS:
                result = self._service.get_users(search_text)
            elif search_type == SearchType.REPOSITORIES:
                result = self._service.get_repositories(search_text)
            else:
                raise ValueError(f"Invalid search type: {search_type}")
        except GraphQLGithubServiceException as e:
            exc = ExternalServiceError(e, detail='GraphQL Github server does not respond.')
            raise exc
        except Exception as e:
            exc = ExternalServiceError(e, detail='Unexpected error.')
            raise exc

        return result