import json
from pathlib import Path

import pytest
from requests import Response

from api.services.github_services import GraphQLGithubService
from api.services.github_services.graphql_service.exceptions import (
    GithubServiceException,
)
from api.utils.constants import (
    TEST_SEARCH_REPOSITORIES_RESPONSE,
    TEST_SEARCH_USERS_RESPONSE,
)


@pytest.fixture(autouse=True)
def patch_github_token(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "TEST_GITHUB_TOKEN")


def get_fake_response(return_value: bytes) -> Response:
    fake_response = Response()
    fake_response.status_code = 200
    fake_response._content = return_value

    return fake_response


def test_github_token_provided():
    service = GraphQLGithubService()
    assert isinstance(service, GraphQLGithubService)


def test_github_token_is_absent(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    with pytest.raises(GithubServiceException):
        GraphQLGithubService()


def test_execute_request_success(mocker):
    fake_response = get_fake_response(
        json.dumps({"data": {"search": {"nodes": "result"}}}).encode()
    )

    mocker.patch("requests.post", return_value=fake_response)
    service = GraphQLGithubService()
    result = service.execute_request({})

    assert result == "result"


def test_execute_request_http_error(mocker):
    fake_response = Response()
    fake_response.status_code = 404

    mocker.patch("requests.post", return_value=fake_response)
    service = GraphQLGithubService()
    with pytest.raises(GithubServiceException):
        service.execute_request({})


#
def test_execute_request_graphql_error(mocker):
    fake_response = get_fake_response(
        json.dumps({"errors": ["Some problem with GraphQL"]}).encode()
    )

    mocker.patch("requests.post", return_value=fake_response)
    service = GraphQLGithubService()
    with pytest.raises(GithubServiceException):
        service.execute_request({})


def test_execute_request_json_error(mocker):
    fake_response = get_fake_response(b"invalid json")

    mocker.patch("requests.post", return_value=fake_response)
    service = GraphQLGithubService()
    with pytest.raises(GithubServiceException):
        service.execute_request({})


def test_execute_request_bad_json_structure(mocker):
    fake_response = get_fake_response(json.dumps({"data": ["data"]}).encode())

    mocker.patch("requests.post", return_value=fake_response)
    service = GraphQLGithubService()
    with pytest.raises(GithubServiceException):
        service.execute_request({})


def test_service_end_to_end(tmp_path, mocker):
    search_text = "string"
    service = GraphQLGithubService()
    (tmp_path / Path(service.SEARCH_USERS_QUERY_FILE)).write_text("some query")

    service.GRAPHQL_QUERIES_PATH = tmp_path

    fake_response = get_fake_response(
        json.dumps({"data": {"search": {"nodes": TEST_SEARCH_USERS_RESPONSE}}}).encode()
    )
    mocker.patch("requests.post", return_value=fake_response)

    result = service.get_users(search_text)
    assert result == TEST_SEARCH_USERS_RESPONSE

    (tmp_path / Path(service.SEARCH_REPOSITORIES_QUERY_FILE)).write_text("some query")

    repositories_response = [
        {
            "id": 1,
            "title": "title",
            "owner": {"login": "owner"},
            "stars": 12,
            "description": None,
            "url": "http://github.com/repository_url",
        }
    ]
    fake_response = get_fake_response(
        json.dumps({"data": {"search": {"nodes": repositories_response}}}).encode()
    )
    mocker.patch("requests.post", return_value=fake_response)

    result = service.get_repositories(search_text)
    assert result == TEST_SEARCH_REPOSITORIES_RESPONSE
