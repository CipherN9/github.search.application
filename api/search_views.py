from typing import Dict, List

from django.core.cache import cache
from django_redis.cache import RedisCache
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins.SearchMixin import SearchPOSTMixin
from api.services.exceptions import ExternalServiceError
from api.services.service import ServiceLayer
from api.utils.constants import SEARCH_CACHE_KEY
from api.utils.enums import SearchType
from api.utils.exceptions import generate_exception
from api.utils.logger import logger
from api.utils.schemas import search_extend_schema

cache: RedisCache


class SearchAPIView(APIView, SearchPOSTMixin):
    parser_classes = [JSONParser]

    @search_extend_schema
    def post(self, request, *args, **kwargs):
        logger.info("Received POST search request")

        query_params = self._get_post_query_params(request)
        request_body = self._get_post_request_body(request)

        search_type: SearchType = query_params["search_type"]
        search_text: str = request_body["search_text"]

        logger.info(
            f"Input parameters: search_type: {search_type}; search_text: {search_text}"
        )

        try:
            data = self.get_from_cache_or_execute_search(search_type, search_text)
        except ExternalServiceError as e:
            logger.exception(e)
            return Response(generate_exception(e), status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            logger.exception(e)
            payload = generate_exception(e)
            payload["detail"] = f"Unexpected error: {payload['detail']}"
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_serializer = self._get_response_serializer(search_type=search_type)(
            data=data, many=True
        )
        response_serializer.is_valid(raise_exception=True)

        logger.info("Returning response")
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def get_from_cache_or_execute_search(self, search_type: SearchType, search_text):
        cache_key = self._make_cache_key(search_type, search_text)
        cached = cache.get(cache_key)
        if cached is not None:
            logger.info("Returning cached value")
            return cached

        logger.info("No cached value. Calculating result")
        result = self.execute_search(search_type, search_text)
        logger.debug(f"Search result: {result}")

        cache_timeout = SEARCH_CACHE_KEY["EXPIRATION"]
        cache.set(cache_key, result, timeout=cache_timeout)
        logger.debug(f"Cache:'{cache_key}' is saved with TTL:{cache_timeout}")

        return result

    @staticmethod
    def execute_search(search_type: SearchType, search_text: str):
        service = ServiceLayer(search_type)
        data: List[Dict[str]] = service.search_by_text(text=search_text)

        return data


@extend_schema(tags=["Search"])
@api_view(["POST"])
@permission_classes([IsAdminUser])
def clear_search_endpoint_cache(request):
    prefix = SEARCH_CACHE_KEY["PREFIX"]
    logger.debug(f"Deleting cache wih starting prefix:'{prefix}'")
    cache.delete_pattern(f"{prefix}*")
    return Response(
        {"detail": "All keys for this cache were cleared."}, status=status.HTTP_200_OK
    )
