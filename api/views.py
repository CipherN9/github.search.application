from typing import Type, Dict, List

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import serializers, status
from api.utils.enums import SearchType
from api.utils.schemas import search_extend_schema
from api.serializers import SearchSerializer, UserSerializer, RepositorySerializer

from api.services.github_services import GraphQLGithubService
from api.services.service import ServiceLayer

class SearchAPIView(APIView):
    parser_classes = [JSONParser]

    @search_extend_schema
    def post(self, request, *args, **kwargs):
        serializer = SearchSerializer(data={**request.query_params.dict(), **request.data})
        serializer.is_valid(raise_exception=True)

        search_type: SearchType = serializer.validated_data['search_type']
        search_text: str = serializer.validated_data['search_text']

        service = ServiceLayer(GraphQLGithubService())
        data: List[Dict[str]] = service.search_by_text(search_text=search_text, search_type=search_type)

        response_serializer = self.get_response_serializer(search_type=search_type)(data=data, many=True)
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def get_response_serializer(search_type: SearchType) -> Type[serializers.Serializer]:
        if search_type == SearchType.USERS:
            return UserSerializer
        elif search_type == SearchType.REPOSITORIES:
            return RepositorySerializer
        else:
            raise ValueError('Invalid search type')
