import hashlib
from typing import Type

from rest_framework import serializers

from api.serializers import (
    RepositorySerializer,
    SearchBodySerializer,
    SearchParametersSerializer,
    UserSerializer,
)
from api.utils.constants import SEARCH_CACHE_KEY
from api.utils.enums import SearchType
from api.utils.logger import logger


class SearchPOSTMixin:
    @staticmethod
    def _get_post_query_params(request):
        logger.debug(f"Query parameters: {request.query_params}")
        serializer = SearchParametersSerializer(data={**request.query_params.dict()})
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    @staticmethod
    def _get_post_request_body(request):
        logger.debug(f"Request body parameters: {request.data}")
        serializer = SearchBodySerializer(data={**request.data})
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    @staticmethod
    def _make_cache_key(search_type: SearchType, search_text: str) -> str:
        normalized_search_text = search_text.strip().lower()
        raw = f"{search_type.value}:{normalized_search_text}"
        short_representation = normalized_search_text[:8].replace(" ", "_")
        hashed = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        cache_key = f"{SEARCH_CACHE_KEY['PREFIX']}:{short_representation}:{hashed}"
        logger.debug(f"Calculated cache key: {cache_key}")
        return cache_key

    @staticmethod
    def _get_response_serializer(
        search_type: SearchType,
    ) -> Type[serializers.Serializer]:
        if search_type == SearchType.USERS:
            serializer = UserSerializer
        elif search_type == SearchType.REPOSITORIES:
            serializer = RepositorySerializer
        else:
            raise ValueError("Invalid search type")

        logger.debug(
            f"Response serializer for given search_type:{search_type} is {serializer}"
        )
        return serializer
