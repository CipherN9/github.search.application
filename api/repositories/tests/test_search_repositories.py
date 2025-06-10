from api.repositories.SearchRepositories import RepositoriesRepository, UsersRepository
from api.services.abс_service import RepositoriesAbstractService, UsersAbstractService
from api.utils.constants import (
    TEST_SEARCH_REPOSITORIES_RESPONSE,
    TEST_SEARCH_USERS_RESPONSE,
)


def test_users_repository(mocker):
    service = mocker.MagicMock(UsersAbstractService, autospec=True)
    service.get_users.return_value = TEST_SEARCH_USERS_RESPONSE
    user_repository = UsersRepository(service)

    result = user_repository.get("some_text")
    assert result == TEST_SEARCH_USERS_RESPONSE


def test_repositories_repository(mocker):
    service = mocker.MagicMock(RepositoriesAbstractService, autospec=True)
    service.get_repositories.return_value = TEST_SEARCH_REPOSITORIES_RESPONSE
    repositories_repository = RepositoriesRepository(service)

    result = repositories_repository.get("some_text")
    assert result == TEST_SEARCH_REPOSITORIES_RESPONSE
