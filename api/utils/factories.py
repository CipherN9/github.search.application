from api.repositories.SearchRepositories import (
    AbstractRepository,
    RepositoriesRepository,
    UsersRepository,
)
from api.services.github_services import GraphQLGithubService
from api.utils.enums import SearchType
from api.utils.logger import logger


def repository_factory(
    search_type: SearchType, implementation="graphQL"
) -> AbstractRepository:
    logger.info(
        f"Using {implementation} GitHub implementation for getting search results"
    )
    if implementation == "graphQL":
        service = GraphQLGithubService()
    else:
        raise ValueError(f"Invalid implementation: {implementation}")

    if search_type == SearchType.USERS:
        repository = UsersRepository(service=service)
    elif search_type == SearchType.REPOSITORIES:
        repository = RepositoriesRepository(service=service)
    else:
        raise ValueError(f"Invalid search type: {search_type}")

    logger.debug(f"Using repository type: {type(repository)}")

    return repository
