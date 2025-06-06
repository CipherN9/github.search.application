from api.repositories.SearchRepositories import AbstractRepository, UsersRepository, RepositoriesRepository
from api.services.github_services import GraphQLGithubService
from api.utils.enums import SearchType


def repository_factory(search_type: SearchType, implementation="graphQL") -> AbstractRepository:
    if implementation == "graphQL":
        service = GraphQLGithubService()
    else:
        raise ValueError(f"Invalid implementation: {implementation}")

    if search_type == SearchType.USERS:
        return UsersRepository(service=service)
    elif search_type == SearchType.REPOSITORIES:
        return RepositoriesRepository(service=service)
    else:
        raise ValueError(f"Invalid search type: {search_type}")
