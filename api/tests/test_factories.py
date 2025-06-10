import pytest

from api.utils.enums import SearchType
from api.repositories.SearchRepositories import UsersRepository, RepositoriesRepository
from api.utils.factories import repository_factory

@pytest.mark.parametrize(
    "search_type, repository_class", [
    (SearchType.USERS, UsersRepository),
    (SearchType.REPOSITORIES, RepositoriesRepository)]
)
def test_users_repository_created(search_type: SearchType, repository_class, mocker):
    mocker.patch('api.utils.factories.GraphQLGithubService')
    repo = repository_factory(search_type, implementation="graphQL")
    assert isinstance(repo, repository_class)

def test_factory_invalid_implementation():
    with pytest.raises(ValueError):
        repository_factory(search_type=SearchType.USERS, implementation="invalidImplementation")
