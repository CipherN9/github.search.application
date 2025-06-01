import hashlib
from typing import Type, Dict, List

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import serializers, status
from api.utils.enums import SearchType
from api.utils.schemas import search_extend_schema
from api.serializers import SearchSerializer, UserSerializer, RepositorySerializer

from api.services.github_services import GraphQLGithubService
from api.services.service import ServiceLayer
from django.core.cache import cache
from django_redis.cache import RedisCache

CACHE_KEY_PREFIX = 'search_endpoint'
CACHE_EXPIRATION = 60 * 5
cache: RedisCache


def make_cache_key(search_type: str, search_text: str) -> str:
    raw = f"{search_type}:{search_text}"
    hashed = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return f"{CACHE_KEY_PREFIX}{hashed}"

class SearchAPIView(APIView):
    parser_classes = [JSONParser]

    @search_extend_schema
    def post(self, request, *args, **kwargs):
        serializer = SearchSerializer(data={**request.query_params.dict(), **request.data})
        serializer.is_valid(raise_exception=True)

        search_type: SearchType = serializer.validated_data['search_type']
        search_text: str = serializer.validated_data['search_text']

        cache_key = make_cache_key(search_type, search_text)

        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached, status=status.HTTP_200_OK)

        service = ServiceLayer(GraphQLGithubService())
        data: List[Dict[str]] = service.search_by_text(search_text=search_text, search_type=search_type)

        response_serializer = self.get_response_serializer(search_type=search_type)(data=data, many=True)
        response_serializer.is_valid(raise_exception=True)

        cache.set(cache_key, response_serializer.data, timeout=CACHE_EXPIRATION)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def get_response_serializer(search_type: SearchType) -> Type[serializers.Serializer]:
        if search_type == SearchType.USERS:
            return UserSerializer
        elif search_type == SearchType.REPOSITORIES:
            return RepositorySerializer
        else:
            raise ValueError('Invalid search type')


@extend_schema(tags=['Search'])
@api_view(["POST"])
def clear_search_endpoint_cache(request):
    cache.delete_pattern(f"{CACHE_KEY_PREFIX}*")
    return Response({"detail": "All keys for this cache were cleared."},
                    status=status.HTTP_200_OK)
