import pytest
from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.services.exceptions import ExternalServiceError
from api.utils.constants import (
    SEARCH_CACHE_KEY,
    TEST_SEARCH_REPOSITORIES_RESPONSE,
    TEST_SEARCH_USERS_RESPONSE,
)
from api.utils.enums import SearchType


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def service_layer_class(mocker):
    service_class = mocker.patch("api.search_views.ServiceLayer", autospec=True)

    return service_class


@pytest.mark.parametrize(
    "search_type, service_response",
    [
        (SearchType.USERS.value, TEST_SEARCH_USERS_RESPONSE),
        (SearchType.REPOSITORIES.value, TEST_SEARCH_REPOSITORIES_RESPONSE),
    ],
)
def test_search_success_and_cache(
    search_type, service_response, api_client, service_layer_class
):
    url = reverse("search-endpoint") + f"?search_type={search_type}"
    payload = {"search_text": "string"}
    service_layer = service_layer_class.return_value
    service_layer.search_by_text.return_value = service_response
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 200
    assert response.json() == service_response

    service_layer.search_by_text.reset_mock()
    cached_response = api_client.post(url, data=payload, format="json")
    assert cached_response.status_code == 200
    assert service_layer.search_by_text.call_count == 0
    assert cached_response.json() == service_response


def test_external_service_returns_502(api_client, service_layer_class):
    url = reverse("search-endpoint") + f"?search_type={SearchType.USERS.value}"
    payload = {"search_text": "string"}
    service_layer = service_layer_class.return_value
    exception_detail = "GitHub is down"
    service_layer.search_by_text.side_effect = ExternalServiceError(exception_detail)

    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == status.HTTP_502_BAD_GATEWAY
    result = response.json()
    assert exception_detail in result["detail"]
    assert "ExternalServiceError" in result["exception"]


def test_external_service_returns_500(api_client, service_layer_class):
    url = reverse("search-endpoint") + f"?search_type={SearchType.USERS.value}"
    payload = {"search_text": "string"}
    service_layer = service_layer_class.return_value
    exception_detail = "Python Exception"
    service_layer.search_by_text.side_effect = ValueError(exception_detail)

    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    result = response.json()
    assert exception_detail in result["detail"]
    assert "ValueError" in result["exception"]


def test_clear_endpoint_cache(api_client, django_user_model):
    cache_key = f"{SEARCH_CACHE_KEY['PREFIX']}_hashed_data"
    result = "result"
    cache.set(key=cache_key, value=result)
    assert cache.get(key=cache_key) == result

    url = reverse("clear-search-cache")
    response = api_client.post(url, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    user: User = django_user_model.objects.create_user(
        username="user", password="user", is_staff=False
    )

    api_client.force_authenticate(user)
    response = api_client.post(url, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    admin: User = django_user_model.objects.create_user(
        username="admin", password="admin", is_staff=True
    )

    api_client.force_authenticate(admin)
    response = api_client.post(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert cache.get(key=cache_key) is None
