import hashlib
from typing import Type

from rest_framework import serializers

from api.serializers import SearchParametersSerializer, UserSerializer, RepositorySerializer, SearchBodySerializer
from api.utils.constants import SEARCH_CACHE_KEY
from api.utils.enums import SearchType


class SearchPOSTMixin:
    @staticmethod
    def _get_post_query_params(request):
        serializer = SearchParametersSerializer(data={**request.query_params.dict()})
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    @staticmethod
    def _get_post_request_body(request):
        serializer = SearchBodySerializer(data={**request.data})
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    @staticmethod
    def _make_cache_key(search_type: SearchType, search_text: str) -> str:
        normalized_search_text = search_text.strip().lower()
        raw = f"{search_type.value}:{normalized_search_text}"
        short_representation = normalized_search_text[:8].replace(" ", "_")
        hashed = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return f"{SEARCH_CACHE_KEY['PREFIX']}:{short_representation}:{hashed}"

    @staticmethod
    def _get_response_serializer(search_type: SearchType) -> Type[serializers.Serializer]:
        if search_type == SearchType.USERS:
            return UserSerializer
        elif search_type == SearchType.REPOSITORIES:
            return RepositorySerializer
        else:
            raise ValueError('Invalid search type')
