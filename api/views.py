from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from api.enums import SearchType
from api.services.github_service import perform_search
from api.serializers import SearchSerializer, SearchParametersSerializer, SearchRequestSerializer, SearchResponseSerializer


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

        profiles = perform_search(search_type, search_text)

        out = SearchResponseSerializer(data=profiles, many=True)
        out.is_valid(raise_exception=True)
        return Response(out.data)
