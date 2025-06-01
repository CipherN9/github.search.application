from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from api.enums import SearchType
from api.serializers import SearchSerializer, SearchParametersSerializer, SearchRequestSerializer, SearchResponseSerializer

from api.services.github_service import GraphQLGithubService
from api.services.service import ServiceLayer

class SearchAPIView(APIView):
    @extend_schema(
        tags=['Search'],
        parameters=[SearchParametersSerializer],
        request=SearchRequestSerializer,
        responses=SearchResponseSerializer(many=True),
    )
    def post(self, request, *args, **kwargs):
        serializer = SearchSerializer(data={**request.query_params.dict(), **request.data})
        serializer.is_valid(raise_exception=True)

        search_type: SearchType = serializer.validated_data['search_type']
        search_text: str = serializer.validated_data['search_text']

        service = ServiceLayer(GraphQLGithubService())
        response = service.search_by_query(query=search_text, search_type=search_type)

        out = SearchResponseSerializer(data=response, many=True)
        out.is_valid(raise_exception=True)
        return Response(out.data)
