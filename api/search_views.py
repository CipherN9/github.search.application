from typing import Dict, List

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import status

from api.mixins.SearchMixin import SearchPOSTMixin
from api.services.exceptions import ExternalServiceError
from api.utils.enums import SearchType
from api.utils.schemas import search_extend_schema

from api.services.github_services import GraphQLGithubService
from api.services.service import ServiceLayer
from django.core.cache import cache
from django_redis.cache import RedisCache
from api.utils.cache_conf import SEARCH_CACHE_KEY

cache: RedisCache

class SearchAPIView(APIView, SearchPOSTMixin):
    parser_classes = [JSONParser]

    @search_extend_schema
    def post(self, request, *args, **kwargs):
        query_params = self._get_post_query_params(request)
        request_body = self._get_post_request_body(request)

        search_type: SearchType = query_params['search_type']
        search_text: str = request_body['search_text']

        try:
            result = self.get_from_cache_or_execute_search(search_type, search_text)
        except ExternalServiceError as e:
            return Response(
                {"detail": f"{e.detail} " + str(e.error)},
                status=status.HTTP_502_BAD_GATEWAY
            )

        return Response(result, status=status.HTTP_200_OK)

    def get_from_cache_or_execute_search(self, search_type: SearchType, search_text):
        cache_key = self._make_cache_key(search_type, search_text)
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        result = self.execute_search(search_type, search_text)

        cache.set(cache_key, result, timeout=SEARCH_CACHE_KEY['EXPIRATION'])

        return result

    def execute_search(self, search_type: SearchType, search_text: str):
        service = ServiceLayer(GraphQLGithubService())
        data: List[Dict[str]] = service.search_by_type_and_text(search_type=search_type, search_text=search_text)

        response_serializer = self._get_response_serializer(search_type=search_type)(data=data, many=True)
        response_serializer.is_valid(raise_exception=True)

        return response_serializer.data



@extend_schema(tags=['Search'])
@permission_classes([IsAdminUser])
@api_view(["POST"])
def clear_search_endpoint_cache(request):
    cache.delete_pattern(f"{SEARCH_CACHE_KEY['PREFIX']}*")
    return Response({"detail": "All keys for this cache were cleared."},
                    status=status.HTTP_200_OK)
